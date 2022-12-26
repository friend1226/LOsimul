from ..lo_char import *


class UnderWatcherArm1(Character):
    
    name = "언더왓쳐 암"
    code = "UnderWatcherArm_B05"
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
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.type_[0] == CharType.FLY:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.HIT:
            if self.find_buff(type_=BT.ACC, efft=BET.BUFF):
                self.give_buff(BT.ACC, 0, bv[0], round_=1, efft=BET.BUFF, desc="재 조준")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_B05] >= 5:
                self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], efft=BET.BUFF, round_=1)
                self.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, round_=1)
