from ..lo_char import *

id_ = "UnderWatcher_B05"
name = "언더왓쳐"
code = "UnderWatcher_B05"
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
        if targets[t] > 0:
            if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="포착")
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _active2(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        if targets[t] > 0:
            if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="포착")
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    desc = "특수 합금"
    if tt == TR.ROUND_START:
        if self.find_buff(tag=G.UNDER_WATCHER_GENERATOR_B05):
            self.give_buff(BT.DEF, 1, bv[0], round_=1, tag="UWB05_P1_DEF", desc=desc)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[1], round_=1, tag="UWB05_P1_ACTIVE_RES", desc=desc)
    elif tt == TR.ATTACK:
        self.remove_buff(tag="UWB05_P1")

def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.ROUND_START:
        if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_B05] >= 4:
            self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, efft=BET.BUFF)

def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.DEAD:
        for t in self.get_passive_targets(targets):
            t.give_buff(BT.INSTANT_DMG, 1, bv[0], desc="시스템 정지", data=D.FDmgInfo(self))

def extra_passive(self, tt, args=None):
    if tt == TR.WAVE_START:
        desc = "해킹 (스카디)"
        self.give_buff(BT.ATK, 1, d('.-5'), round_=3, desc=desc)
        self.give_buff(BT.SPD, 1, d('.-25'), round_=3, desc=desc)
