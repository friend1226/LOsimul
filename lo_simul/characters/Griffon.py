from ..lo_char import *


class Griffon(Character):
    _id = 92
    name = "그리폰"
    code = "BR_PA00EL"
    group = Group.SKY_NIGHTS
    isenemy = False
    is21squad = True
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_={BT.ROOTED, BT.MARKED}, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="정밀 사격")
                for p in self.game.get_chars(field=self.isenemy):
                    if p.code == "BR_Sleipnir":
                        self.give_buff(BT.COOP_ATTACK, 0, 1, data=D.CoopAttack(p, 2), round_=1, efft=BET.BUFF,
                                       desc="정밀 사격 - P-49 슬레이프니르")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.TAKEDMGDEC, 1, bv[0], data=D.DmgInfo(element=E.FIRE), overlap_type=BOT.INSTANCE, 
                            desc="화염 폭격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "정찰 비행"
        if tt == TR.ROUND_START:
            self.give_buff(BT.ACC, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc)
            self.give_buff(BT.EVA, 0, bv[1], efft=BET.BUFF, round_=1, desc=desc)
            self.give_buff(BT.DEFPEN, 1, bv[2], efft=BET.BUFF, round_=1, desc=desc)
        elif tt == TR.WAVE_START:
            if self.find_buff(BT.RACON):
                self.give_buff(BT.AP, 0, bv[4], efft=BET.BUFF, desc="선제 폭격")
        elif tt == TR.WAVE_END:
            self.give_buff(BT.RACON, 0, 1, efft=BET.BUFF, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "연계 폭격"
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.CRIT, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            for t in self.get_passive_targets(targets):
                if t != self and (t.type_[0] == CT.FLY or t.is21squad):
                    t.give_buff(BT.FOLLOW_ATTACK, 0, 1, data=D.FollowAttack(self), 
                                round_=1, efft=BET.BUFF, desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass
