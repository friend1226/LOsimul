from ..lo_char import *


class EliteCenturion1(Character):
    id_ = "CenturionEX_TU"
    name = "엘리트 센츄리온"
    code = "CenturionEX_TU"
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
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="직격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            desc = "일제 공격 표식"
            t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=2, efft=BET.DEBUFF, desc=desc)
            t.give_buff(BT.MARKED, 0, 1, round_=2, efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ALLY_DEAD:
            desc = "역습 태세"
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=2, desc=desc, tag="CenturionEX_TU_P1_ATK")
            self.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=2, desc=desc, tag="CenturionEX_TU_P1_CRIT")
            self.give_buff(BT.COUNTER_ATTACK, 1, bv[2], efft=BET.BUFF, round_=2, desc=desc, tag="CenturionEX_TU_P1_CNT")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(tag="CenturionEX_TU_P1"):
            desc = "부대 재 정비"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.SPD, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACC, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
