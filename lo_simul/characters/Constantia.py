from ..lo_char import *


class Constantia(Character):
    id_ = 3
    name = "콘스탄챠S2"
    code = "3P_ConstantiaS2"
    group = Group.BATTLE_MAID
    isenemy = False
    is21squad = True
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="정밀 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.SPD, 1, bv[0], efft=BET.DEBUFF, round_=1)
                t.give_buff(BT.ROOTED, 0, 1, efft=BET.DEBUFF, round_=2)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, round_=2)
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, round_=2)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc="준비 만전")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ATTACK:
            for t in self.get_passive_targets(targets):
                desc = "사냥감 몰이"
                t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=3, max_stack=1,
                            tag='Constantia_P2_ATK', desc=desc)
                t.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, round_=3, max_stack=1,
                            tag='Constantia_P2_ACC', desc=desc)
                t.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, round_=3, max_stack=1,
                            tag='Constantia_P2_CRIT', desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass
