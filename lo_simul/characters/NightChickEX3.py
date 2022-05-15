from ..lo_char import *


class NightChickEX3(Character):
    id_ = "NightChickEX_TU3"
    name = "강화형 나이트 칙"
    code = "NightChickEX_TU3"
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
                t.give_buff(BT.EVA, 0, bv[0], round_=2, efft=BET.DEBUFF)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.EVA, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="집중사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.IDLE:
            self.give_buff(BT.ACC, 0, bv[0], efft=BET.BUFF, round_=3)
            self.give_buff(BT.RANGE, 0, 1, efft=BET.BUFF, round_=3)
            self.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=3)
