from ..lo_char import *


class NightChickModifiedEX3(Character):
    id_ = "NightChickMEX_TU3"
    name = "강화형 칙 런처"
    code = "NightChickMEX_TU3"
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
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="직격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="직격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.MOVE:
            desc = "기동 사격"
            self.give_buff(BT.RANGE, 0, 1, efft=BET.BUFF, round_=4, desc=desc)
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=4, desc=desc)
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, round_=4, desc=desc)
