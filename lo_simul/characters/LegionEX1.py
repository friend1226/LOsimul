from ..lo_char import *


class LegionEX1(Character):
    name = "정예 레기온"
    code = "LegionEX_TU"
    group = Group.PARASITE
    isenemy = True
    isags = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.type_[0] == CT.FLY:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "강화 점착탄"
                t.give_buff(BT.ROOTED, 0, 1, round_=3, efft=BET.DEBUFF, desc=desc, overlap_type=BOT.RENEW)
                t.give_buff(BT.EVA, 0, bv[0], round_=3, efft=BET.DEBUFF, desc=desc, chance=75)
                t.give_buff(BT.SPD, 1, bv[1], round_=3, efft=BET.DEBUFF, desc=desc, chance=75)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, round_=3, efft=BET.DEBUFF, desc=desc,
                            data=D.BuffCond(type_=BT.EVA, efft=BET.BUFF), chance=50)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, round_=3, efft=BET.DEBUFF, desc=desc,
                            data=D.BuffCond(type_=BT.SPD, efft=BET.BUFF), chance=50)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ALLY_DEAD:
            desc = "경계 태세"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.SPD, 1, bv[0], round_=3, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.FOLLOW_ATTACK, 0, 1, round_=3, efft=BET.BUFF, desc=desc, data=D.FollowAttack(self))
