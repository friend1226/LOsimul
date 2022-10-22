from ..lo_char import *


class Glacias(Character):
    id_ = 232
    name = "글라시아스"
    code = "PECS_Glacias"
    group = Group.BISMARK
    isenemy = False
    is21squad = False
    isags = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "고룡의 숨결"
                self.give_buff(BT.GIVEDMGINC, 1, bv[0], data=D.DmgInfo(hp_type=4), overlap_type=BOT.INSTANCE, efft=BET.BUFF, desc=desc)
                if t.hp_rate <= d('.5'):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC), desc=desc)
                if t.find_buff(tag=G.FLOOD):
                    t.give_buff(BT.INABILLITY_ACT, 0, 1, round_=2, efft=BET.DEBUFF, desc=desc)
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "니플헤임의 폭풍"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.ICE_RES, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], data=D.DmgInfo(element=E.ICE), overlap_type=BOT.INSTANCE, desc=desc)
                if t.find_buff(tag=G.FLOOD):
                    t.give_buff(BT.ROOTED, 0, 1, round_=2, efft=BET.DEBUFF, desc=desc)
                    t.give_buff(BT.SPD, 1, bv[1], round_=2, efft=BET.DEBUFF, desc=desc)
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF))
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "차가운 분노"
        if tt == TR.WAVE_START:
            self.give_buff(BT.ATK, 1, bv[0], desc=desc)
            self.give_buff(BT.CRIT, 0, bv[1], desc=desc)
        elif tt == TR.ROUND_START:
            if self.game.round >= 1:
                self.give_buff(BT.ATK, 1, bv[2], round_=7, desc=desc + " (라운드/중첩)")
        elif tt == TR.KILL:
            self.give_buff(BT.ATK, 1, bv[3], desc=desc + " (적 처치)")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "한기의 포옹"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.CRIT, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ACC, 0, bv[2], round_=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.FIRE_RES, 0, bv[3], round_=1, efft=BET.BUFF, desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "몰아치는 냉기"
        if tt == TR.WAVE_START:
            for t in self.get_passive_targets(targets, True):
                t.give_buff(BT.SPD, 1, bv[0], round_=5, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.EVA, 0, bv[1], round_=5, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ICE_RES, 0, bv[2], round_=5, efft=BET.DEBUFF, desc=desc)
