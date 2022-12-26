from ..lo_char import *


class Ignis(Character):
    _id = 134
    name = "이그니스"
    code = "PECS_Ignis"
    group = Group.PUBLIC_SERVANT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "화염 분사"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.DEF, 1, bv[0], efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.FIRE_RES, 0, bv[0]*100, efft=BET.DEBUFF, round_=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.CRIT, 0, -bv[0]*40, efft=BET.DEBUFF, round_=2, desc="인화물 부착")
                t.give_buff(BT.FIRE_DOT_DMG, 0, bv[0]*400, efft=BET.DEBUFF, round_=2, desc="점화")
                if t.find_buff(type_=BT.FIRE_RES, efft=BET.DEBUFF):
                    t.give_buff(BT.INSTANT_DMG, 1, bv[0], data=D.DmgInfo(subject=self, element=E.FIRE), 
                                efft=BET.DEBUFF, desc="잔불")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "적응형 방호복"
            self.give_buff(BT.DEF, 1, bv[0]/100, efft=BET.BUFF, round_=1, desc=desc)
            self.give_buff(BT.FIRE_RES, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
        if tt == TR.GET_HIT:
            desc = "환경 적응"
            if args["element"]:
                self.give_buff(BT_ELEMENT_RES[args["element"]], 0, bv[0], 
                               efft=BET.BUFF, round_=2, max_stack=1, tag=f"Ignis_P1_{args['element']}RES", desc=desc)
            else:
                self.give_buff(BT.DEF, 1, bv[0]/100, efft=BET.BUFF, round_=2,
                               max_stack=1, tag="Ignis_P1_DEF", desc=desc)

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "요원 엄폐"
        if tt == TR.ROUND_START:
            takedmgdef_trg = False
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, round_=1, data=D.TargetProtect(self), desc=desc)
                takedmgdef_trg = True
            self.give_buff(BT.COLUMN_PROTECT, 0, 1, efft=BET.BUFF, round_=1, overlap_type=BOT.RENEW, desc=desc)
            if takedmgdef_trg:
                self.give_buff(BT.TAKEDMGDEC, 1, bv[0], efft=BET.BUFF, round_=1, 
                               max_stack=1, tag="Ignis_P2_TDD", desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        is_front = (self.isenemy and self.getposy() == 0) or (not self.isenemy and self.getposy() == 2)
        if tt == TR.WAVE_START:
            if is_front:
                self.give_buff(BT.RANGE, 0, 1, desc="Model_Livens")
                self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], efft=BET.BUFF, desc="분멸", tag="Ignis_P3_CA")
        elif tt == TR.IDLE:
            if is_front:
                if self.find_buff(tag="Ignis_P3_CA"):
                    self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag="Ignis_P3_CA"), desc="진정")
                else:
                    self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], efft=BET.BUFF, desc="분멸", tag="Ignis_P3_CA")
        elif tt == TR.ROUND_START:
            for element in Element:
                if self.find_buff(type_=BT_ELEMENT_RES[element]):
                    self.give_buff(BT_ELEMENT_MIN[element], 0, bv[1], efft=BET.BUFF, round_=1, 
                                   desc=f"{element.desc} 차폐")
