from ..lo_char import *


class KunoichiEnrai(Character):
    id_ = 99
    name = "쿠노이치 엔라이"
    code = "DS_KunoichiEnrai"
    group = Group.D_ENTERTAINMENT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "호무라"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.FIRE_RES, 0, bv[0], round_=3, efft=BET.DEBUFF, overlap_type=BOT.RENEW, desc=desc)
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE), desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "이카즈치"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.ELEC_RES, 0, bv[0], round_=3, efft=BET.DEBUFF, overlap_type=BOT.RENEW, desc=desc)
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE), desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "은형술"
        if tt == TR.ROUND_START:
            targets = self.get_passive_targets(targets)
            if {CP.get("DS_KunoichiKaen").id_, CP.get("DS_KunoichiZero").id_} & set(map(lambda c_: c_.id_, targets)):
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, efft=BET.BUFF, desc=desc)
            else:
                for p in targets:
                    if p.type_[1] == CR.ATTACKER:
                        p.give_buff(BT.FOLLOW_ATTACK, 0, 1, round_=1, efft=BET.BUFF,
                                    data=D.FollowAttack(self), desc=desc)
        elif tt == TR.HIT:
            targets = args["targets"]
            element = E.FIRE if args["skill_no"] == 1 else E.ELEC

            def tempf(b_: 'Buff'):
                try:
                    return b_.data.element == E.FIRE
                except AttributeError:
                    return b_.type == BT.EVA
            for t in targets:
                if targets[t] > 0 and t.find_buff(type_={BT.DOT_DMG, BT.EVA}, func=tempf, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, data=D.DmgInfo(element=element), desc=desc)

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "연화보"
        if tt == TR.HIT:
            self.give_buff(BT.GIMMICK, 0, 1, round_=2, max_stack=1, tag="Enrai_P2_AFTERSKILL", desc=desc)
        elif tt == TR.ROUND_START and self.game.round > 0:
            if not self.find_buff(tag="Enrai_P2_AFTERSKILL"):
                self.give_buff(BT.CHANGE_AP, 0, 7, efft=BET.BUFF, desc=desc)
        elif tt == TR.WAVE_START:
            if not self.find_buff(tag="Enrai_P2_AFTERSKILL"):
                self.give_buff(BT.AP, 0, 3, efft=BET.BUFF, desc=desc)
        elif tt == TR.AFTER_COOP or tt == TR.AFTER_FOLLOW:
            self.give_buff(BT.SKILL_RATE, 0, bv[0], count=1, count_trig={TR.AFTER_HIT, },
                           max_stack=1, tag="Enrai_P2_SR", desc="히나후부키")

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, tag=G.AUSGJROWJS, desc=G.AUSGJROWJS + " <무라사키 류>", removable=False)
        elif tt == TR.ROUND_START:
            self.give_buff(BT.CRIT, 0, bv[0], round_=1, efft=BET.BUFF, desc=G.AUSGJROWJS)
            for p in self.get_passive_targets(targets):
                if p.name.startswith("쿠노이치") and p.find_buff(G.AUSGJROWJS):
                    p.give_buff(BT.RANGE, 0, 2, round_=1, efft=BET.BUFF, desc=G.AUSGJROWJS)
        elif tt == TR.WAVE_END:
            self.remove_buff(type_=BT.GIMMICK, tag=G.AUSGJROWJS, force=True, log=False)
