from ..lo_char import *


class Titania(Character):
    _id = 10
    name = "티타니아"
    code = "3P_Titania"
    group = Group.FAIRY
    isenemy = False
    is21squad = False
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "차가운 고통"
                t.give_buff(BT.ICE_DOT_DMG, 0, bv[0], round_=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ROOTED, 0, 1, round_=2, efft=BET.DEBUFF, desc=desc, overlap_type=BOT.RENEW)
                t.give_buff(BT.ICE_RES, 0, bv[1], round_=2, efft=BET.DEBUFF,
                            max_stack=2, tag="Titania_A1_RES", desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "서리 폭풍"
        for t in targets:
            if targets[t] > 0 and t.find_buff(type_=BT.ICE_RES, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.ICE), desc=desc)
        self.give_buff(BT.SPD, 1, d('-.55'), round_=2, desc=desc, tag="Titania_A2_SPD_DEC")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "피해의식"
            self.give_buff(BT_ANTI_OS[CharType.HEAVY], 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "천년서리"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.FIRE_RES, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT_ANTI_OS[CT.HEAVY], 1, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                if p.type_[1] == CR.DEFENDER:
                    p.give_buff(BT.IMMUNE_BUFF, 0, 1, round_=1, efft=BET.BUFF, desc=desc,
                                data=D.BuffCond(type_=BT.FIRE_RES, efft=BET.DEBUFF))
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(tag="Titania_A2_SPD_DEC"):
            desc = "끝없는 증오"
            self.give_buff(BT.RANGE, 0, 2, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.EVA, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[2], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.COUNTER_ATTACK, 1, d('.8'), round_=1, efft=BET.BUFF, desc=desc)
