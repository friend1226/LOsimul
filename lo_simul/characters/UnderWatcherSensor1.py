from ..lo_char import *


class UnderWatcherSensor1(Character):
    id_ = "UnderWatcherSensor_B05"
    name = "언더왓쳐 센서"
    code = "UnderWatcherSensor_B05"
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
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, round_=3)
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, round_=3)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, round_=3, max_stack=1,
                            tag="UWS1_A1", desc="록 온")
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, round_=3)
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, round_=3)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, round_=3)
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            hprate = self.hp / self.maxhp
            ts = self.get_passive_targets(targets)
            if hprate >= d('.75'):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[0], efft=BET.BUFF, round_=1)
            if hprate >= d('.5'):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, round_=1, chance=50)
            if hprate >= d('.25'):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[2], efft=BET.BUFF, round_=1, chance=20)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_B05] >= 3:
                self.give_buff(BT.ACTIVE_RATE, 0, bv[0], efft=BET.BUFF, round_=1)
