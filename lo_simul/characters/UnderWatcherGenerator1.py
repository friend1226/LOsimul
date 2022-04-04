from ..lo_char import *

id_ = "UnderWatcherGenerator_B05"
name = "언더왓쳐 제네레이터"
code = "UnderWatcherGenerator_B05"
group = None
isenemy = True
isboss = True

def _active1(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        t.give_buff(BT.ATK, 1, bv[0], round_=15, max_stack=5, efft=BET.BUFF,
                    tag=G.UNDER_WATCHER_GENERATOR_B05, desc="충전")

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

def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.ROUND_START and self.hp / self.maxhp <= d('.5'):
        desc = "재충전 개시"
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)
        self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=1, desc=desc)
        self.give_buff(BT.ACTIVE_RESIST, 1, bv[0], round_=1, desc=desc)

def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.GET_HIT:
        chance = 10
        if self.find_buff(type_=BT.DEF, efft=BET.DEBUFF):
            chance = 50
        self.give_buff(BT.INABILLITY_ACT, 0, 1, round_=2, efft=BET.DEBUFF,
                       chance=chance, desc="제네레이터 쇼트")

def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.DEAD:
        desc = "제네레이터 파괴"
        for t in self.get_passive_targets(targets):
            t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
            t.give_buff(BT.INABILLITY_ACT, 0, 1, round_=1, desc=desc)
