from ..lo_char import *


class Aqua(Character):
    _id = 9
    name = "아쿠아"
    code = "3P_Aqua"
    group = Group.FAIRY
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "내부 파괴"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(tag=G.CORROSION):
                    t.give_buff(BT.INSTANT_DMG, 1, bv[1], efft=BET.DEBUFF, data=D.DmgInfo(self), desc=desc)
                    t.give_buff(BT.TAKEDMGINC, 1, -bv[0]*4, round_=3, efft=BET.DEBUFF,
                                max_stack=1, tag="Aqua_A1_TDI", desc=desc)
                t.give_buff(BT.SPD, 1, bv[0], round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_SPD)
                t.give_buff(BT.DEF, 1, bv[0]*4, round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_DEF)
                t.give_buff(BT.PHYSICAL_DOT_DMG, 0, bv[2], round_=3, efft=BET.DEBUFF, max_stack=3, tag=G.CORROSION_DOT)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            t.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.BUFF)
            t.give_buff(BT.ACTIVE_RESIST, 1, bv[0], efft=BET.BUFF, round_=2, tag="Aqua_A2_AR")
            t.give_buff(BT.FIRE_RES, 0, bv[1], round_=2, efft=BET.DEBUFF, max_stack=1, tag=G.FLOOD_FIRE)
            t.give_buff(BT.ICE_RES, 0, -bv[1], round_=2, efft=BET.DEBUFF, max_stack=1, tag=G.FLOOD_ICE)
            t.give_buff(BT.ELEC_RES, 0, -bv[1], round_=2, efft=BET.DEBUFF, max_stack=1, tag=G.FLOOD_ELEC)
        return {}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "상쾌함!"
            for t in self.get_passive_targets(targets):
                if t.find_buff(tag="Aqua_A2_AR"):
                    t.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.ACC, 0, bv[0] * 500 / 3, round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.EVA, 0, bv[0] * 100, round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.AP, 0, bv[1], efft=BET.BUFF, desc=desc)

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass
