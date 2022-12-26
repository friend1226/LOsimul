from ..lo_char import *


class Empress(Character):
    _id = 161
    name = "엠프리스"
    code = "PECS_Empress"
    group = Group.PUBLIC_SERVANT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "아이스 에이지"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.ICE_RES, 0, bv[0]*300, efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.SPD, 1, bv[0], efft=BET.DEBUFF, round_=2, desc=desc)
                if t.find_buff(tag=G.FLOOD):
                    t.give_buff(BT.ROOTED, 0, 1, efft=BET.DEBUFF, round_=2, 
                                tag=G.FREEZE, desc=G.FREEZE, overlap_type=BOT.RENEW)
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, round_=2, 
                                tag=G.FREEZE, desc=G.FREEZE, max_stack=1)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.ICE), desc="서프라이즈!")
                if t.find_buff(tag=G.FLOOD):
                    t.give_buff(BT.ROOTED, 0, 1, efft=BET.DEBUFF, round_=2, 
                                tag=G.FREEZE, desc=G.FREEZE, overlap_type=BOT.RENEW)
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, round_=2, 
                                tag=G.FREEZE, desc=G.FREEZE, max_stack=1)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "의태"
        if tt == TR.WAVE_START:
            self.give_buff(BT.MINIMIZE_DMG, 0, 9999999, efft=BET.BUFF, count=2, desc=desc, tag="Empress_P1_MD")
        elif tt == TR.ROUND_START:
            if self.find_buff(tag="Empress_P1_MD"):
                self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=3, desc=desc)
                self.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=3, desc=desc)
        elif tt == TR.IDLE:
            if not self.find_buff(tag="Empress_P1_MD"):
                self.give_buff(BT.MINIMIZE_DMG, 0, 9999999, efft=BET.BUFF, count=2, desc=desc, tag="Empress_P1_MD")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "극지 대비책"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ICE_RES, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                if t.find_buff(type_=BT.TARGET_PROTECT):
                    t.give_buff(BT.AP, 0, bv[1], efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ICE_RES, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc + " (펭귄)")

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            self.give_buff(BT.SPD, 1, bv[0], efft=BET.BUFF, round_=1, desc="남극 대모험")
            if self.find_buff(tag="Empress_P1_MD"):
                self.give_buff(BT.IGNORE_PROTECT, 0, 1, efft=BET.BUFF, round_=1, desc="의태")
            for t in self.get_passive_targets(targets, True):
                if t.find_buff(tag=G.FREEZE):
                    t.give_buff(BT.ICE_RES, 0, bv[1], efft=BET.DEBUFF, round_=1, desc="얼음땡")
        elif tt == TR.HIT:
            for t in (targets := args["targets"]):
                if targets[t] > 0 and t.find_buff(tag=G.FLOOD):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc="점프스케어")
