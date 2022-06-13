from ..lo_char import *


class Silky(Character):
    id_ = 26
    name = "실키"
    code = "BR_PXSilky"
    group = Group.STEEL_LINE
    isenemy = False
    is21squad = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "점착탄"
        for t in targets:
            if targets[t] > 0:
                extrav = 1 if t.type_ == CT.FLY else d('1.5')
                t.give_buff(BT.EVA, 0, bv[0] * extrav, efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.ROOTED, 0, 1, efft=BET.DEBUFF, round_=2, desc=desc)
                if extrav > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[2], efft=BET.DEBUFF, round_=2, desc=desc)
                    t.give_buff(BT.SPD, 1, d('.-1'), efft=BET.DEBUFF, round_=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "현장 보급"
        for t in targets:
            t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)
            t.give_buff(BT.AP, 0, bv[2] * 2, efft=BET.BUFF, desc=desc)
            if t.type_[1] == CR.ATTACKER:
                t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=2, desc=desc, max_stack=1, tag="Silky_A2_ATK")
            if t.type_[1] == CR.DEFENDER:
                t.give_buff(BT.DEF, 1, bv[1], efft=BET.BUFF, round_=2, desc=desc, max_stack=1, tag="Silky_A2_DEF")
            if t.type_[1] == CR.SUPPORTER:
                t.give_buff(BT.AP, 0, bv[2], efft=BET.BUFF, desc=desc)
        return {}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.GET_ATTACKED:
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], efft=BET.BUFF, count=1, count_trig={TR.GET_HIT},
                           max_stack=2, tag="Silky_P1_TAKEDMGDEC")
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[0], efft=BET.BUFF, count=1, count_trig={TR.GET_HIT},
                           max_stack=2, tag="Silky_P1_ACTIVE_RESIST")
        elif tt == TR.EXPECT_GET_HIT:
            self.give_buff(BT.MINIMIZE_DMG, 0, 9999999, count=1, count_trig={TR.GET_HIT},
                           max_stack=2, tag="Silky_P1_MINIMIZE_DMG")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "거대 배낭"
        if tt == TR.ROUND_START:
            myspd = self.get_stats(BT.SPD)
            for t in self.get_passive_targets(targets):
                if t.type_[0] != CT.FLY:
                    t.give_buff(BT.EVA, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.TAKEDMGDEC, 1, bv[0]/200, efft=BET.BUFF, round_=1, desc=desc)
                    if t.get_stats(BT.SPD) < myspd:
                        t.give_buff(BT.ACC, 0, -bv[0], efft=BET.DEBUFF, round_=1, desc=desc)
        elif tt == TR.GET_HIT or (tt == TR.AFTER_SKILL and args["skill_no"] == 1):
            for t in self.get_passive_targets(targets):
                if t.type_[0] != CT.FLY:
                    t.give_buff(BT.AP, 0, 1, efft=BET.BUFF, desc="뭔가 떨어졌는데?")

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "안돼요!"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                t.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=1, desc=desc)
                if t.group == Group.STEEL_LINE:
                    t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.SPD, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                if t.find_buff(type_=BT.SPD, efft=BET.BUFF):
                    t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.DEFPEN, 0, bv[2], efft=BET.BUFF, round_=1, desc=desc)
