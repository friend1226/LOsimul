from ..lo_char import *


class NightChickSniper1(Character):
    id_ = "NightChickSP_N"
    name = "칙 스나이퍼"
    code = "NightChickSP_N"
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
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="정밀 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        self.give_buff(BT.EVA, 0, bv[0], round_=3, efft=BET.BUFF, tag="NightChickSP_N_A2_EVA")
        self.give_buff(BT.CRIT, 0, bv[1], round_=3, efft=BET.BUFF, tag="NightChickSP_N_A2_CRIT")
        self.give_buff(BT.TAKEDMGINC, 1, bv[2], round_=3, efft=BET.BUFF, tag="NightChickSP_N_A2_TAKEDMGINC")
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(tag="NightChickSP_N_A2"):
            self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], round_=1, efft=BET.BUFF, desc="대응 저격")
