from ..lo_char import *


class UnderWatcher2(Character):
    id_ = "UnderWatcher_TU2"
    name = "언더왓쳐"
    code = "UnderWatcher_TU2"
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
        desc = "포착"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc=desc)
                    t.give_buff(BT.DEF, 1, bv[1], round_=5, desc=desc)
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
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="포착", overlap_type=BOT.RENEW)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "특수 합금"
        if tt == TR.GET_ATTACKED:
            if self.find_buff(tag=G.UNDER_WATCHER_GENERATOR_TU2):
                self.give_buff(BT.MINIMIZE_DMG, 0, bv[0], count=1, max_stack=1, tag="UWTU2_P1", desc=desc,
                               efft=BET.BUFF, count_trig={TR.GET_HIT}, chance=90, overlap_type=BOT.RENEW)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_TU2] >= 4:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, efft=BET.BUFF)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.DEAD:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], desc="시스템 정지", data=D.DmgInfo(self))
