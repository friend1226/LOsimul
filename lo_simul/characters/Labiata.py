from ..lo_char import *


class Labiata(Character):
    id_ = 2
    name = "라비아타"
    code = "3P_Labiata"
    group = Group.BATTLE_MAID
    isenemy = False
    is21squad = True
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        if any(targets.values()):
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, max_stack=3, tag=G.LABIATA)
        for t in targets:
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], round_=0, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        if self.stack_limited_buff_tags[G.LABIATA] == 3:
            for t in targets:
                if targets[t] > 0:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="최대 출력 강타")
            self.remove_buff(tag=G.LABIATA, limit=1)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "강화 근력"
            self.give_buff(BT.SPD, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            if self.stack_limited_buff_tags[G.LABIATA] == 3:
                desc = "초" + desc
                self.give_buff(BT.SPD, 1, bv[0] * d(.5), round_=1, efft=BET.BUFF, desc=desc)
                self.give_buff(BT.TAKEDMGDEC, 1, bv[1] * d(.5), round_=1, efft=BET.BUFF, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            self.give_buff(BT.DEFPEN, 1, bv[0], round_=1, efft=BET.BUFF, desc="P.G 활성화")
            if self.stack_limited_buff_tags[G.LABIATA] == 2:
                self.give_buff(BT.DEFPEN, 1, bv[0], round_=1, efft=BET.BUFF, desc="P.G 출력 강화")
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, efft=BET.BUFF, desc="P.G 출력 강화")
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                desc = "든든한 큰언니"
                t.give_buff(BT.CRIT, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ATK, 1, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ACC, 0, bv[2], round_=1, efft=BET.BUFF, desc=desc)
