from ..lo_char import *


class KunoichiKaen(Character):
    _id = 180
    name = "쿠노이치 카엔"
    code = "DS_KunoichiKaen"
    group = Group.D_ENTERTAINMENT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "시라누이"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.ACTIVE_RESIST, 0, bv[0], round_=2, max_stack=1, tag="Kaen_A1_AR", desc=desc)
                if targets[t] > 1:
                    t.give_buff(BT.FIRE_DOT_DMG, 0, bv[1], round_=2, efft=BET.DEBUFF, overlap_type=BOT.SINGLE, desc=desc)
                if self.find_buff(type_=BT.GIMMICK, tag="Kaen_P2_일격필살"):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[2], overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.FIRE), desc="일격필살")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "오의 [화신강림]"
        gflag = bool(self.find_buff(type_=BT.GIMMICK, tag="Kaen_P2_일격필살"))
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.FIRE_RES, 0, bv[0], round_=2, efft=BET.DEBUFF, max_stack=1, tag="Kaen_A2_FR", desc=desc)
                if t.find_buff(type_={BT.ICE_RES, BT.ELEC_RES}, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.FIRE), desc=desc)
                if gflag:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[2], overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.FIRE), desc="일격필살")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "불꽃의 춤"
        if tt == TR.ROUND_START:
            if self.find_buff(type_=BT.GIMMICK, tag=G.AUSGJROWJS):
                self.give_buff(BT.ATK, 1, bv[0] + bv[1] * 4, round_=1, efft=BET.BUFF, desc="하이카구라")
            else:
                self.give_buff(BT.ATK, 1, bv[0] + max(bv[1] * (4 - self.game.round), 0),
                               round_=1, efft=BET.BUFF, desc=desc)
        elif tt == TR.DEAD:
            for p in self.get_passive_targets(targets):
                if p.code == "DS_KuoichiZero":
                    p.give_buff(BT.ATK, 1, bv[2], round_=2, efft=BET.BUFF, desc="사그라든 불꽃")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "일격필살"
        if tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, count=1, count_trig={TR.AFTER_HIT, }, desc=desc, tag="Kaen_P2_일격필살")
        elif tt == TR.ROUND_START:
            self.give_buff(BT.SPD, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        targets = self.get_passive_targets(targets)
        if tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, tag=G.AUSGJROWJS, desc=G.AUSGJROWJS + " <무라사키 류>", removable=False)
            self.give_buff(BT.ANTI_LIGHT, 1, bv[0], desc=G.AUSGJROWJS)
        elif tt == TR.IDLE:
            if "DS_KunoichiEnrai" in set(map(lambda c_: c_.code, targets)) \
                    and not self.find_buff(type_=BT.GIMMICK, tag="Kaen_P2_일격필살"):
                self.give_buff(BT.GIMMICK, 0, 1, count=1, count_trig={TR.AFTER_HIT, },
                               desc="일격필살", tag="Kaen_P2_일격필살")
        elif tt == TR.DEAD:
            if "DS_KunoichiEnrai" in set(map(lambda c_: c_.code, targets)):
                for p in targets:
                    p.give_buff(BT.ATK, 1, bv[1], round_=2, efft=BET.BUFF,
                                max_stack=1, tag="Kunoichi_P3_ATK", desc="진에")
        elif tt == TR.HIT:
            if args["skill_no"] == 1:
                self.give_buff(BT.COOP_ATTACK, 0, 1, round_=1, efft=BET.BUFF, data=D.CoopAttack(self, 1),
                               max_stack=1, tag="Zero_P3_CA", desc="무라사키 류 - 쿠노이치 엔라이 [호무라]")
        elif tt == TR.WAVE_END:
            self.remove_buff(type_=BT.GIMMICK, tag=G.AUSGJROWJS, force=True, log=False)
