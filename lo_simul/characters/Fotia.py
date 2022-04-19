from ..lo_char import *


class Fotia(Character):
    id_ = 15
    name = "포티아"
    code = "3P_Fotia"
    group = Group.ANYWHERE
    isenemy = False
    is21squad = False
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "점화"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.DOT_DMG, 0, bv[0], round_=3, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ELEMENT_RES[E.FIRE], 0, bv[1], round_=2, efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "점화"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.DOT_DMG, 0, bv[0], round_=3, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ELEMENT_RES[E.FIRE], 0, bv[1], round_=2, efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            tag = "Fotia_P1_ATK"
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, max_stack=3, tag=tag)
            if self.stack_limited_buff_tags[tag] == 3:
                desc = "과출력 버너"
                self.give_buff(BT.ATK, 1, bv[0]*2, efft=BET.BUFF, count=1, count_trig={TR.AFTER_SKILL, }, max_stack=1,
                               tag="Fotia_P1_MAXATK_ATK", desc=desc)
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, efft=BET.BUFF, count=1, count_trig={TR.AFTER_SKILL, },
                               max_stack=1, tag="Fotia_P1_MAXATK_IGN", desc=desc)
