from ..lo_char import *


class Daphne(Character):
    _id = 8
    name = "다프네"
    code = "3P_Daphne"
    group = Group.FAIRY
    isenemy = False
    is21squad = False
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "내부 파괴"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.INSTANT_DMG, 1, bv[1], efft=BET.DEBUFF, data=D.DmgInfo(self), desc=desc)
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*4, round_=3, efft=BET.DEBUFF,
                                max_stack=1, tag="Daphne_A_TDI", desc=desc)
                t.give_buff(BT.SPD, 1, bv[0], round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_SPD)
                t.give_buff(BT.DEF, 1, bv[0]*4, round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_DEF)
                t.give_buff(BT.PHYSICAL_DOT_DMG, 0, bv[2], round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_DOT)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "내부 파괴"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.INSTANT_DMG, 1, bv[1], efft=BET.DEBUFF, data=D.DmgInfo(self), desc=desc)
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*4, round_=3, efft=BET.DEBUFF,
                                max_stack=1, tag="Daphne_A_TDI", desc=desc)
                t.give_buff(BT.SPD, 1, bv[0], round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_SPD)
                t.give_buff(BT.DEF, 1, bv[0]*4, round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_DEF)
                t.give_buff(BT.PHYSICAL_DOT_DMG, 0, bv[2], round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_DOT)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "민감한 눈"
            self.give_buff(BT.RANGE, 0, 1, efft=BET.BUFF, round_=1, max_stack=1, tag="Daphne_P1_RANGE", desc=desc)
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.CRIT, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                t.give_buff(BT.ACC, 0, bv[0]*2, efft=BET.BUFF, round_=1, desc=desc)
                t.give_buff(BT.DEFPEN, 1, bv[0]/75, efft=BET.BUFF, round_=1, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "대사 촉진"
            for t in self.get_passive_targets(targets):
                if not t.isenemy and t.isags:
                    continue
                t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0]*200, efft=BET.BUFF, round_=1, desc=desc)
                t.give_buff(BT.SPD, 1, bv[0]/2, efft=BET.BUFF, round_=1, desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass
