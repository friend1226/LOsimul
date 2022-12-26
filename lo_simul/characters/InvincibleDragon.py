from ..lo_char import *


class InvincibleDragon(Character):
    _id = 85
    name = "무적의 용"
    code = "BR_InvDragon"
    group = Group.HORIZEN
    isenemy = False
    is21squad = True
    
    def isformchanged(self):
        return bool(self.find_buff(type_=BT.GIMMICK, tag=G.DRAGON_BOMBARDMENT))

    def skill_idx_convert(self, skill_idx):
        if skill_idx < 2 and self.isformchanged():
            return skill_idx + 5
        return skill_idx
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = ("예리한 참격", "회심의 일격")
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.MARKED, 0, 1, round_=2, efft=BET.DEBUFF, overlap_type=BOT.RENEW, desc=desc[0])
                t.give_buff(BT.TAKEDMGINC, 0, bv[0], round_=1, efft=BET.DEBUFF, 
                            max_stack=1, tag="InvDragon_A1_TDI", desc=desc[0])
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 0, bv[0], overlap_type=BOT.INSTANCE, desc=desc[1])
                    t.give_buff(BT.ACTIVE_RESIST, 0, -bv[0]*100, round_=2, desc=desc[1])
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = ("호령", "익숙한 편제")
        for t in targets:
            t.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc=desc[0])
            t.give_buff(BT.ATK, 1, bv[1], round_=2, efft=BET.BUFF, desc=desc[0])
            if t.group == Group.HORIZEN or t.is21squad:
                t.give_buff(BT.AP, 0, bv[0]/2, efft=BET.BUFF, desc=desc[1])
                t.give_buff(BT.ATK, 1, bv[1]/2, round_=2, efft=BET.BUFF, desc=desc[1])
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "불굴"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.EVA, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.TAKEDMGDEC, 1, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ACTIVE_RESIST, 1, bv[1] * 200, round_=1, efft=BET.BUFF, desc=desc)
        elif tt == TR.DEAD:
            desc = "사기 진작"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.EVA, 0, bv[0], round_=2, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.TAKEDMGDEC, 1, bv[1], round_=2, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ACTIVE_RESIST, 1, bv[1] * 200, round_=2, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.COUNTER_ATTACK, 1, bv[2], round_=2, efft=BET.BUFF, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = ("군사 전략 통달", "일제 공격", "통솔 대응")
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc[0])
                t.give_buff(BT.ACC, 0, bv[0] * 160, round_=1, efft=BET.BUFF, desc=desc[0])
                t.give_buff(BT.CRIT, 0, bv[0] * 80, round_=1, efft=BET.BUFF, desc=desc[0])
                t.give_buff(BT.SPD, 1, bv[0] * d('.4'), round_=1, efft=BET.BUFF, desc=desc[0])
                if t.find_buff(BT.FOLLOW_ATTACK, efft=BET.BUFF):
                    t.give_buff(BT.ATK, 1, bv[0] / 2, round_=1, efft=BET.BUFF, desc=desc[1])
                    t.give_buff(BT.ACC, 0, bv[0] * 80, round_=1, efft=BET.BUFF, desc=desc[1])
                    t.give_buff(BT.CRIT, 0, bv[0] * 0, round_=1, efft=BET.BUFF, desc=desc[1])
                    t.give_buff(BT.SPD, 1, bv[0] * d('.2'), round_=1, efft=BET.BUFF, desc=desc[1])
                if t.find_buff(BT.RACON):
                    t.give_buff(BT.ATK, 1, bv[0] / 2, round_=1, efft=BET.BUFF, desc=desc[2])
                    t.give_buff(BT.ACC, 0, bv[0] * 80, round_=1, efft=BET.BUFF, desc=desc[2])
                    t.give_buff(BT.CRIT, 0, bv[0] * 0, round_=1, efft=BET.BUFF, desc=desc[2])
                    t.give_buff(BT.SPD, 1, bv[0] * d('.2'), round_=1, efft=BET.BUFF, desc=desc[2])
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "포격 좌표 송신"
        if tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, tag=G.DRAGON_STANDBY)
            for t in self.get_passive_targets(targets):
                if t.has_impact_skill:
                    t.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc=desc)
        elif tt == TR.WAVE_END:
            self.give_buff(BT.RACON, 0, 1, efft=BET.BUFF, max_stack=1, tag="InvDragon_P3_RACON", desc="포격 좌표 검색")
        elif tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.has_impact_skill or (t == self and t.find_buff(BT.RACON)):
                    t.give_buff(BT.CRIT, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.ATK, 0, bv[1] * d('.015'), round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.ACC, 0, bv[1] * 3, round_=1, efft=BET.BUFF, desc=desc)
        elif tt == TR.IDLE:
            if self.find_buff(tag=G.DRAGON_STANDBY):
                self.give_buff(BT.GIMMICK, 0, 1, tag=G.DRAGON_BOMBARDMENT)
        elif tt == TR.AFTER_COUNTER:
            if self.isformchanged():
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag=G.DRAGON_BOMBARDMENT), 
                            desc="함대 포격 모드 해제")
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag=G.DRAGON_STANDBY), 
                            desc="함대 은밀 기동 개시")
    
    def _factive1(self, 
                  targets: Dict['Character', NUM_T], 
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                  bv: Sequence[NUM_T], 
                  wr: NUM_T, 
                  element: int):
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag=G.DRAGON_BOMBARDMENT), 
                       desc="함대 포격 모드 해제")
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag=G.DRAGON_STANDBY), 
                       desc="함대 은밀 기동 개시")
        if any(targets.values()):
            self.give_buff(BT.DEFPEN, 1, bv[0], overlap_type=BOT.INSTANCE, efft=BET.BUFF, desc="철갑탄 포격")
        racon = self.find_buff(BT.RACON)
        for t in targets:
            if targets[t] > 0:
                if racon:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], overlap_type=BOT.INSTANCE, desc="정밀 조준 포격")
                if targets[t] > 1:
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(BT.BARRIER, efft=BET.BUFF), desc="회심의 포격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}


    def _factive2(self, 
                  targets: Dict['Character', NUM_T], 
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                  bv: Sequence[NUM_T], 
                  wr: NUM_T, 
                  element: int):
        desc = "함대 대기 명령"
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag=G.DRAGON_BOMBARDMENT), desc=desc)
        self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)
        return {}  
        
