from ..lo_char import *


class UnderWatcherGenerator2(Character):
    id_ = "UnderWatcherGenerator_TU2"
    name = "언더왓쳐 제네레이터"
    code = "UnderWatcherGenerator_TU2"
    group = Group.PARASITE
    isenemy = True
    isags = True
    isboss = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "충전"
        for t in targets:
            t.give_buff(BT.ATK, 1, bv[0], round_=99, max_stack=5, efft=BET.BUFF,
                        tag=G.UNDER_WATCHER_GENERATOR_TU2, desc=desc)
            t.give_buff(BT.IMMUNE_DMG, 0, bv[1], round_=9, efft=BET.BUFF, desc=desc)
            t.give_buff(BT.ACTIVE_RESIST, 1, bv[2], round_=1, efft=BET.BUFF, desc=desc)
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "에너지 실드"
        for t in targets:
            t.give_buff(BT.BARRIER, 0, bv[0], round_=9, efft=BET.BUFF, desc=desc)
            t.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.BUFF, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.HIT:
            desc = "에너지 코팅"
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=3, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[1], round_=3, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.IMMUNE_DMG, 0, bv[2], round_=3, efft=BET.BUFF, max_stack=1, tag="UWG2_P1", desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.GET_HIT:
            desc = "제네레이터 쇼트"
            self.give_buff(BT.AP, 0, bv[0], desc=desc, chance=75)
            self.give_buff(BT.INABILLITY_ACT, 0, 1, round_=2, desc=desc, chance=4)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.DEAD:
            desc = "제네레이터 파괴"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
                t.give_buff(BT.INABILLITY_ACT, 0, 1, round_=2, desc=desc)
