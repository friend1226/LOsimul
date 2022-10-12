from ..lo_char import *


class Cerestia(Character):
    id_ = 176
    name = "세레스티아"
    code = "PECS_HighElven"
    group = Group.PUBLIC_SERVANT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "급속 성장"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(tag=G.FLOOD):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
                t.give_buff(BT.ROOTED, 0, 1, round_=3, efft=BET.DEBUFF, desc=desc, overlap_type=BOT.RENEW)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "숲의 노래"
        elvenid = CP.get("PECS_ElvenForestmaker").id_
        darkid = CP.get("PECS_DarkElf").id_
        for t in targets:
            if t.id_ == elvenid or t.id_ == darkid or t.type_[0] == CT.LIGHT:
                t.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc=desc)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), efft=BET.BUFF, desc=desc)
                t.give_buff(BT.ATK, 1, bv[1], efft=BET.BUFF, round_=3, desc=desc)
                t.give_buff(BT.CRIT, 0, bv[1]*100, efft=BET.BUFF, round_=3, desc=desc)
                t.give_buff(BT.DEFPEN, 0, bv[2], efft=BET.BUFF, round_=3, desc=desc)
                t.give_buff(BT.INSTANT_DMG, 0, self.get_orig_atk() * d('.02'), efft=BET.BUFF)
        return {}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "정화"
        if tt == TR.WAVE_START:
            self.give_buff(BT.BARRIER, 0, bv[0], efft=BET.BUFF, round_=3, desc=desc)
        elif tt == TR.ROUND_START:
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, round_=1, desc=desc)
            allys = set(map(lambda ch: ch.id_, self.game.get_chars(field=self.isenemy).values()))
            if CP.get("PECS_ElvenForestmaker").id_ in allys:
                self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, round_=1, desc=desc + "(엘븐)")
            if CP.get("PECS_DarkElf").id_ in allys:
                self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, round_=1, desc=desc + "(다크 엘븐)")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "세계수의 은총"
        if tt == TR.ROUND_START:
            allys = set(map(lambda ch: ch.id_, self.game.get_chars(field=self.isenemy).values()))
            elvenid = CP.get("PECS_ElvenForestmaker").id_
            darkid = CP.get("PECS_DarkElf").id_
            elven = elvenid in allys
            darkelven = darkid in allys
            for t in self.get_passive_targets(targets):
                if t.id_ == elvenid or t.id_ == darkid or t.type_[0] == CT.LIGHT:
                    t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.SPD, 1, bv[0]/2, efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.DEFPEN, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                    if elven:
                        t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                        t.give_buff(BT.SPD, 1, bv[0]/2, efft=BET.BUFF, round_=1, desc=desc)
                        t.give_buff(BT.DEFPEN, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                    if darkelven:
                        t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                        t.give_buff(BT.SPD, 1, bv[0]/2, efft=BET.BUFF, round_=1, desc=desc)
                        t.give_buff(BT.DEFPEN, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "모성"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.find_buff(type_=BT.COLUMN_PROTECT, efft=BET.BUFF):
                    t.give_buff(BT.TAKEDMGDEC, 1, bv[0], efft=BET.BUFF, round_=1, max_stack=1,
                                tag="Cerestia_P3_TAKEDMGDEC", desc=desc)
