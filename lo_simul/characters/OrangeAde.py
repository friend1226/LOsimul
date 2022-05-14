from ..lo_char import *


class OrangeAde(Character):
    id_ = 211
    name = "오렌지에이드"
    code = "PECS_Orangeade"
    group = Group.PUBLIC_SERVANT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "회로 간섭"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], efft=BET.DEBUFF, data=D.FDmgInfo(subject=self), desc=desc)
                t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), efft=BET.DEBUFF, round_=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "정보 공유"
        for t in targets:
            t.give_buff(BT.ATK, 0, bv[0], proportion=(self, BT.ATK), efft=BET.BUFF, round_=2, desc=desc)
        return {}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "화력 지원 OS"
        if tt == TR.WAVE_START:
            allys = self.get_passive_targets(targets)
            if len([c for c in allys if c.type_[0] == CT.FLY]) <= 2:
                for t in allys:
                    t.give_buff(BT.SKILL_RATE, 0, bv[0], round_=99, desc=desc)
                    t.give_buff(BT.CRIT, 0, bv[0]*100, round_=99, desc=desc)

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "능력 강화 OS"
        if tt == TR.WAVE_START:
            allys = self.get_passive_targets(targets)
            if len([c for c in allys if c.type_[0] == CT.HEAVY]) <= 2:
                for t in allys:
                    t.give_buff(BT.ATK, 0, bv[0], round_=99, desc=desc)
                    t.give_buff(BT.DEF, 0, bv[0], round_=99, desc=desc)
