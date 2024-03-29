from ..lo_char import *


class Rhea(Character):
    _id = 6
    name = "레아"
    code = "3P_Rhea"
    group = Group.FAIRY
    isenemy = False
    is21squad = False
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "기능 오류"
        bv1 = bv[0]*3/5
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.FIRE_RES, 0, bv[0], round_=2, efft=BET.DEBUFF, max_stack=1,
                            tag=G.FLOOD_FIRE)
                t.give_buff(BT.ICE_RES, 0, -bv[0], round_=2, efft=BET.DEBUFF, max_stack=1,
                            tag=G.FLOOD_ICE)
                t.give_buff(BT.ELEC_RES, 0, -bv[0], round_=2, efft=BET.DEBUFF, max_stack=1,
                            tag=G.FLOOD_ELEC)
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.TAKEDMGINC, 1, bv1 / 100, overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.ELEC), desc="급속 부식")
                if targets[t] > 1:
                    t.give_buff(BT.ACC, 0, -bv1, round_=2, efft=BET.DEBUFF, max_stack=1, tag="Rhea_A1_ACC", desc=desc)
                    t.give_buff(BT.EVA, 0, -bv1, round_=2, efft=BET.DEBUFF, max_stack=1, tag="Rhea_A1_EVA", desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "금속 열피로"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.DEF, 1, bv[0], round_=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], round_=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, 1, overlap_type=BOT.INSTANCE, efft=BET.DEBUFF, data=D.DmgInfo(element=E.FIRE), desc=desc)
                if targets[t] > 1:
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF))
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.INSTANT_DMG, 1, bv[1] * 2, efft=BET.DEBUFF,
                                data=D.DmgInfo(subject=self), desc="내부 파괴")
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(type_=BT.SPD, efft=BET.BUFF):
            desc = "느긋함"
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.CRIT, 0, bv[0] * 200 / 3, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ACC, 0, bv[0] * 200, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.BUFF, desc=desc, data=D.BuffCond(type_=BT.SPD, efft=BET.BUFF))
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            desc = "기상 최적화"
            bv2 = bv[0]*500
            for p in self.get_passive_targets(targets):
                if p.type_[0] != CT.FLY:
                    continue
                p.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc=desc)
                p.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, desc=desc)
                for i in range(1, 4):
                    p.give_buff(BT_ELEMENT_RES[i], 0, bv2, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACTIVE_RESIST, 1, bv2, efft=BET.BUFF, desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "강운"
        if tt == TR.ATTACK:
            self.give_buff(BT.ATK, 0, 1, efft=BET.BUFF, count=1, count_trig={TR.AFTER_SKILL, },
                           max_stack=1, tag="Rhea_P3_ATK", desc=desc)
        elif tt == TR.GET_ATTACKED:
            self.give_buff(BT.MINIMIZE_DMG, 0, 999999, efft=BET.BUFF, count=1, 
                           max_stack=1, tag="Rhea_P3_MINIMIZEDMG", desc=desc)
    
    def get_active_chance(self, skill_idx: int):
        if skill_idx == 4:
            return self.skillvl[4] + 1
        return 100
