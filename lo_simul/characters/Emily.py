from ..lo_char import *


class Emily(Character):
    id_ = 68
    name = "에밀리"
    code = "BR_Emily"
    group = Group.AA_CANNONIERS
    isenemy = False
    is21squad = False
    
    def isformchanged(self):
        return bool(self.find_buff(type_=BT.GIMMICK, tag=Gimmick.EMILY))
    
    def skill_no_convert(self, skill_no):
        if skill_no == 1 and self.isformchanged():
            return 6
        else:
            return skill_no
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], efft=BET.BUFF, round_=0, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        if self.find_buff(tag="Emily_P1"):
            pbuffs = True
        else:
            pbuffs = False
        for t in targets:
            if targets[t] > 0:
                if pbuffs:
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BARRIER, efft=BET.BUFF))
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF))
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.IDLE:
            desc = "출력 강화"
            self.give_buff(BT.CRIT, 0, bv[0], round_=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_CRIT")
            self.give_buff(BT.DEFPEN, 1, bv[1], round_=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_DEFPEN")
            self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_IGN")
            self.give_buff(BT.ATK, 1, bv[2], round_=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_ATK")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ATTACK:
            if self.find_buff(type_=BT.FOLLOW_ATTACK, efft=BET.BUFF):
                self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc="급속 충전")
            if self.find_buff(type_=BT.TARGET_PROTECT):
                self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc="급속 충전")
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt in {TR.ROUND_START, TR.ATTACK, TR.GET_ATTACKED} and self.hp / self.maxhp <= d('.33'):
            self.give_buff(BT.GIMMICK, 0, 1, max_stack=1, tag=Gimmick.EMILY)
            self.give_buff(BT.ATK, 1, bv[1], max_stack=1, efft=BET.BUFF, desc=Gimmick.EMILY, tag="Emily_P3_ATK")
            self.give_buff(BT.SPD, 1, bv[1], max_stack=1, efft=BET.BUFF, desc=Gimmick.EMILY, tag="Emily_P3_SPD")
            self.give_buff(BT.EVA, 0, bv[2], max_stack=1, efft=BET.BUFF, desc=Gimmick.EMILY, tag="Emily_P3_EVA")
        if tt == TR.ATTACK:
            self.give_buff(BT.DOT_DMG, 0, bv[0], round_=1, desc="과부하")
    
    def _factive2(self, 
                  targets: Dict['Character', NUM_T],
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                  bv: Sequence[NUM_T],
                  wr: NUM_T,
                  element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BARRIER, efft=BET.BUFF))
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF))
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
