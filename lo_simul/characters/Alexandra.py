from ..lo_char import *


class Alexandra(Character):
    _id = 11
    name = "알렉산드라"
    code = "3P_Alexandra"
    group = Group.ANYWHERE
    isenemy = False
    
    def isformchanged(self):
        return self.find_buff(tag="Alexandra_FormChange")
    
    def skill_idx_convert(self, skill_idx):
        if skill_idx != 4 and self.isformchanged():
            skill_idx += 5
        return skill_idx
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "감전"
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0]*100, round_=3, efft=BET.DEBUFF, desc=desc)
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*2/3, data=D.DmgInfo(element=E.ELEC), 
                                overlap_type=BOT.INSTANCE, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "감전"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0]*100, round_=3, efft=BET.DEBUFF, desc=desc)
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*5/6, data=D.DmgInfo(element=E.ELEC), 
                                overlap_type=BOT.INSTANCE, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.KILL:
            desc = "전하 집속"
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, tag="Alexandra_P1_ATK", desc=desc)
            self.give_buff(BT.CRIT, 0, bv[0]*100, efft=BET.BUFF, tag="Alexandra_P1_CRIT", desc=desc)
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, tag="Alexandra_P1_SPD", desc=desc)
            if self.find_buff(tag="Alexandra_P1").count >= 6:
                self.give_buff(BT.GIMMICK, 0, 1, efft=BET.BUFF, 
                               max_stack=1, tag="Alexandra_FormChange", desc="전하 방출")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "전기장 자극"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ELEC_RES, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0]*2/3, round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.SPD, 1, bv[0]/750, round_=1, efft=BET.BUFF, desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.EXP, 1, bv[0], round_=1, efft=BET.BUFF, 
                            max_stack=1, tag="Alexandra_P3_EXP", desc="모범 교사")
        elif tt == TR.ATTACK:
            desc = "잘 보고 배우세요"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ATK, 1, bv[1], round_=2, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ACC, 0, bv[1]*200, round_=2, efft=BET.BUFF, desc=desc)
    
    def _factive1(self, 
                  targets: Dict['Character', NUM_T], 
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                  bv: Sequence[NUM_T], 
                  wr: NUM_T,
                  element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "감전"
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0]*1000/6, round_=3, efft=BET.DEBUFF, desc=desc)
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*2/3, data=D.DmgInfo(element=E.ELEC), 
                                overlap_type=BOT.INSTANCE, desc=desc)
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF), desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _factive2(self, 
                  targets: Dict['Character', NUM_T], 
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                  bv: Sequence[NUM_T], 
                  wr: NUM_T,
                  element: int):
        desc = "감전"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0]*100, round_=3, efft=BET.DEBUFF, desc=desc)
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*5/6, data=D.DmgInfo(element=E.ELEC), 
                                overlap_type=BOT.INSTANCE, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _fpassive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.KILL:
            desc = "전하 집속"
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, tag="Alexandra_P1_ATK", desc=desc)
            self.give_buff(BT.CRIT, 0, bv[0]*100, efft=BET.BUFF, tag="Alexandra_P1_CRIT", desc=desc)
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, tag="Alexandra_P1_SPD", desc=desc)
        elif tt == TR.ROUND_START:
            desc = "전하 방출"
            self.give_buff(BT.ATK, 1, bv[0]*2, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.CRIT, 0, bv[0]*200, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.SPD, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
    
    def _fpassive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "전기장 자극"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ELEC_RES, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.SPD, 1, bv[1]/500, round_=1, efft=BET.BUFF, desc=desc)
