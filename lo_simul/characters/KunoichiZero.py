from ..lo_char import *


class KunoichiZero(Character):
    id_ = 174
    name = "쿠노이치 제로"
    code = "DS_KunoichiZero"
    group = Group.D_ENTERTAINMENT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "은밀"
        for t in targets:
            if targets[t] > 0:
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0]*3, round_=1, data=D.DmgInfo(element=E.ELEC), desc=desc)
                self.give_buff(BT.ANTI_HEAVY, 1, bv[0], round_=1, efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "뇌신 일섬"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.SPD, 1, bv[0], round_=1, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[1], round_=1, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ELEC_RES, 0, bv[2]*400/3, round_=1, efft=BET.DEBUFF, desc=desc)
                if t.find_buff(type_={BT.FIRE_RES, BT.ICE_RES}, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[2], overlap_type=BOT.INSTANCE, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "허공 둔"
        if tt == TR.ROUND_START:
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.EVA, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACC, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.CRIT, 0, bv[2]*200, round_=1, efft=BET.BUFF, max_stack=1, tag="Zero_P1_CRIT", desc=desc)
                p.give_buff(BT.SPD, 1, bv[2], round_=4, efft=BET.BUFF, max_stack=3, tag="Zero_P1_SPD", desc=desc)

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "가속"
        if tt == TR.ROUND_START:
            self.give_buff(BT.ELEC_RES, 0, bv[0]*200, round_=1, efft=BET.BUFF, desc=desc)
        elif tt == TR.KILL:
            self.give_buff(BT.ATK, 1, bv[0], round_=3, efft=BET.BUFF, max_stack=3, tag="Zero_P2_ATK", desc=desc)
            self.give_buff(BT.AP, 0, bv[1], efft=BET.BUFF, desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        targets = self.get_passive_targets(targets)
        if tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, tag=G.AUSGJROWJS, desc=G.AUSGJROWJS + " <무라사키 류>", removable=False)
            self.give_buff(BT.ANTI_LIGHT, 1, bv[0], desc=G.AUSGJROWJS)
        elif tt == TR.ROUND_START:
            desc = "허공 기문둔갑"
            for p in targets:
                if p.name.startswith("쿠노이치"):
                    p.give_buff(BT.EVA, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                    p.give_buff(BT.ACC, 0, bv[2], round_=1, efft=BET.BUFF, desc=desc)
                    p.give_buff(BT.CRIT, 0, bv[3]*200, round_=1, efft=BET.BUFF, desc=desc)
                    p.give_buff(BT.SPD, 1, bv[3], round_=4, efft=BET.BUFF, max_stack=3, tag="Zero_P1_SPD", desc=desc)
        elif tt == TR.DEAD:
            if CP.get("DS_KunoichiEnrai").id_ in set(map(lambda c_: c_.id_, targets)):
                for p in targets:
                    p.give_buff(BT.ATK, 1, bv[4], round_=2, efft=BET.BUFF,
                                max_stack=1, tag="Kunoichi_P3_ATK", desc="진에")
        elif tt == TR.KILL:
            if CP.get("DS_KunoichiEnrai").id_ in set(map(lambda c_: c_.id_, targets)):
                desc = "가속"
                for p in targets:
                    if p.name.startswith("쿠노이치") and p != self:
                        p.give_buff(BT.ATK, 1, bv[5], round_=3, efft=BET.BUFF,
                                    max_stack=3, tag="Zero_P2_ATK", desc=desc)
                        # TODO : 패시브2스킬과 중첩되는가?
                        p.give_buff(BT.AP, 0, bv[3], efft=BET.BUFF, desc=desc)
        elif tt == TR.HIT:
            if args["skill_no"] == 1:
                self.give_buff(BT.COOP_ATTACK, 0, 1, round_=1, efft=BET.BUFF, data=D.CoopAttack(self, 2),
                               max_stack=1, tag="Zero_P3_CA", desc="무라사키 류 - 쿠노이치 엔라이 [이카즈치]")
        elif tt == TR.WAVE_END:
            self.remove_buff(type_=BT.GIMMICK, tag=G.AUSGJROWJS, force=True, log=False)
