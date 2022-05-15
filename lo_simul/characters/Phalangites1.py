from ..lo_char import *


class Phalangites1(Character):
    id_ = "Phalangites_TU"
    name = "팔랑스"
    code = "Phalangites_TU"
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
            if targets[t] > 0 and t.type_[0] == CT.FLY:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=3, efft=BET.BUFF)
        self.give_buff(BT.COLUMN_PROTECT, 0, 1, round_=3, efft=BET.BUFF)
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=1, efft=BET.BUFF,
                            desc="밀집 대형", tag="Phalagites1_P1", max_stack=1)
