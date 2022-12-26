from ..lo_char import *


class LemonadeAlpha(Character):
    _id = 187
    name = "레모네이드 알파"
    code = "PECS_LemonadeAlpha"
    group = Group.PUBLIC_SERVANT
    isenemy = False
    is21squad = True
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "회로 침식"
        for t in targets:
            if t.hp_rate >= 1:
                t.give_buff(BT.ACTIVE_RESIST, 0, -bv[0] * 100, round_=5, desc=desc)
            if targets[t] > 0:
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], efft=BET.DEBUFF, data=D.DmgInfo(self), desc=desc)
                t.give_buff(BT.INSTANT_DMG, 1, bv[1], efft=BET.DEBUFF, data=D.DmgInfo(self), desc=desc, chance=50)
                t.give_buff(BT.TAKEDMGINC, 1, bv[2], efft=BET.DEBUFF, round_=2, desc=desc, chance=40)
                t.give_buff(BT.INABILLITY_SKILL, 0, 1, efft=BET.DEBUFF, round_=1, 
                            overlap_type=BOT.RENEW, desc=desc, chance=30)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "출력전개"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], efft=BET.DEBUFF, data=D.DmgInfo(self), desc=desc)
                t.give_buff(BT.FORCE_MOVE, 0, -1, efft=BET.DEBUFF, overlap_type=BOT.INSTANCE, desc=desc)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, 
                            data=D.BuffCond(type_={BT.ROW_PROTECT, BT.COLUMN_PROTECT, BT.TARGET_PROTECT}, 
                                            efft=BET.BUFF), 
                            desc=desc)
                t.give_buff(BT.EVA, 0, bv[1], efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.RANGE, 0, -1, efft=BET.DEBUFF, round_=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            desc = "경장갑 OS"
            lights = [_c for _c in self.get_passive_targets(targets) if _c.type_[0] == CT.LIGHT]
            if len(lights) >= 2:
                for _c in lights:
                    _c.give_buff(BT.DEFPEN, 1, bv[0], desc=desc)
                for _c in self.get_passive_targets(targets, enemy=True):
                    if _c.type_[0] != CT.LIGHT:
                        _c.give_buff(BT.TAKEDMGINC, 1, -bv[0], desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            desc = "사거리 OS"
            flys = [_c for _c in self.get_passive_targets(targets) if _c.type_[0] == CT.FLY]
            if len(flys) >= 2:
                for _c in flys:
                    _c.give_buff(BT.RANGE, 0, 1, desc=desc)
                    _c.give_buff(BT.ACC, 0, bv[0], desc=desc)
                for _c in self.get_passive_targets(targets, enemy=True):
                    if _c.type_[0] != CT.FLY:
                        _c.give_buff(BT.RANGE, 0, -1, desc=desc)
                        _c.give_buff(BT.ACC, 0, -bv[0], desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            desc = "중장갑 OS"
            heavys = [_c for _c in self.get_passive_targets(targets) if _c.type_[0] == CT.HEAVY]
            if len(heavys) >= 2:
                for _c in heavys:
                    _c.give_buff(BT.AP, 0, bv[0], desc=desc)
                    _c.give_buff(BT.SPD, 1, bv[1], desc=desc)
                for _c in self.get_passive_targets(targets, enemy=True):
                    if _c.type_[0] != CT.HEAVY:
                        _c.give_buff(BT.FIRE_RES, 0, bv[2], desc=desc)
                        _c.give_buff(BT.ICE_RES, 0, bv[2], desc=desc)
                        _c.give_buff(BT.ELEC_RES, 0, bv[2], desc=desc)
                        _c.give_buff(BT.SPD, 1, -bv[1], desc=desc)
