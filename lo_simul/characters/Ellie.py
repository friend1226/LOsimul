from ..lo_char import *


class Ellie(Character):
    id_ = 230
    name = "엘리"
    code = "BR_Ellie"
    group = Group.AGENCY_080
    isenemy = False
    is21squad = False
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "테이저 니들"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                if t.get_spd() > self.get_spd():
                    t.give_buff(BT.AP, 0, bv[1], efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "방호 모드"
        self.give_buff(BT.IMMUNE_DMG, 0, 1, round_=2, efft=BET.BUFF, desc=desc)
        self.give_buff(BT.ROW_PROTECT, 0, 1, round_=2, efft=BET.BUFF, desc=desc)
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.WIDE_TAKEDMG, 1, bv[0], round_=2, efft=BET.BUFF, desc=desc)
    
    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "노블레스 오블리주"
            self.give_buff(BT.COLUMN_PROTECT, 0, 1, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
    
    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "편안한 티타임"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.WIDE_TAKEDMG, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.BARRIER, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
