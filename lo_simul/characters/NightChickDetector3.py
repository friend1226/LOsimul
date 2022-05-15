from ..lo_char import *


class NightChickDetector3(Character):
    id_ = "NightChickDE_TU3"
    name = "나이트 칙 디텍터"
    code = "NightChickDE_TU3"
    group = G.PARASITE
    isenemy = True
    isags = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=2, efft=BET.DEBUFF)
                t.give_buff(BT.EVA, 0, bv[1], round_=2, efft=BET.DEBUFF)
                t.give_buff(BT.MARKED, 0, 1, round_=2, efft=BET.DEBUFF)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.ACC, 0, bv[0], round_=2, efft=BET.DEBUFF)
                t.give_buff(BT.AP, 0, bv[1], round_=2, efft=BET.DEBUFF)
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.GET_HIT:
            desc = "레이더 공유"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.AP, 0, 1, round_=2, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACC, 0, bv[0], round_=2, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.RANGE, 0, 1, round_=2, efft=BET.BUFF, desc=desc)
    
    def extra_passive(self, tt, args=None):
        if tt == TR.DEAD:
            desc = "레이더 재밍"
            buff_values = self.get_skill_buff_value(3)
            aoe = self.get_aoe(self.pos, 3)
            for p in self.get_passive_targets(aoe):
                p.give_buff(BT.REMOVE_BUFF, 0, 1, desc=desc,
                            data=D.BuffCond(type_=BT.ACC, efft=BET.BUFF))
                p.give_buff(BT.ACC, 0, -buff_values[0], round_=1, desc=desc)
    
    def get_passive_active_chance(self, skill_no: int):
        if skill_no == 2:
            return 40
        else:
            return 100
