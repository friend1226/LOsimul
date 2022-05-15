from ..lo_char import *


class NightChickShielder3(Character):
    id_ = "NightChickSI_TU3"
    name = "나이트 칙 실더 개"
    code = "NightChickSI_TU3"
    group = Group.PARASITE
    isenemy = True
    isags = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.EVA, efft=BET.DEBUFF):
                t.give_buff(BT.INABILLITY_ACT, 0, 1, round_=1, efft=BET.DEBUFF, chance=50)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        self.give_buff(BT.ROW_PROTECT, 0, 1, round_=3, efft=BET.BUFF)
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=1, efft=BET.BUFF, max_stack=1, tag="NightChickSI_TU3_P1",
                           desc="강화 방패")
