from ..lo_char import *


class CyclopsePrincess(Character):
    id_ = 240
    name = "사이클롭스 프린세스"
    code = "PECS_CyclopsePrincess"
    group = Group.BISMARK
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "<마검 : 어둠의 서약>"
        stack = ["base"]
        for pbt in ("CRIT", "IP", "BC"):
            if self.find_buff(tag="CyclopsePrincess_P1_"+pbt):
                stack.append(pbt)
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0]*5, round_=0, desc=desc)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, 
                            data=D.BuffCond(type_={BT.COUNTER_ATTACK, BT.MINIMIZE_DMG}, efft=BET.BUFF), desc=desc)
                for tagad in stack:
                    t.give_buff(BT.DEF, 1, -bv[0], round_=2, max_stack=1,
                                tag=f"CyclopsePrincess_A1_DEF_{tagad}", desc=desc)
                    t.give_buff(BT.ACTIVE_RESIST, 0, -bv[0], round_=2, max_stack=1, 
                                tag=f"CyclopsePrincess_A1_AR_{tagad}", desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "영원한 진조의 섬광"
        stack = ["base"]
        for pbt in ("CRIT", "IP", "BC"):
            if self.find_buff(tag="CyclopsePrincess_P1_"+pbt):
                stack.append(pbt)
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.COUNTER_ATTACK, efft=BET.BUFF), desc=desc)
                for tagad in stack:
                    t.give_buff(BT.TAKEDMGDEC, 1, bv[0], efft=BET.DEBUFF, round_=2, max_stack=1, 
                                tag=f"CyclopsePrincess_A2_TDD_{tagad}", desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "진조의 권능"
        if tt == TR.ROUND_START:
            if not self.find_buff(type_=BT.FOLLOW_ATTACK):
                self.give_buff(BT.CRIT, 0, bv[0], efft=BET.BUFF, round_=1, max_stack=1, 
                               tag="CyclopsePrincess_P1_CRIT", desc=f"<{desc} : 사안>")
                if not self.find_buff(type_=BT.TARGET_PROTECT):
                    self.give_buff(BT.IGNORE_PROTECT, 0, 1, efft=BET.BUFF, round_=1, max_stack=1, 
                               tag="CyclopsePrincess_P1_IP", desc=f"<{desc} : 운명조작>")
        elif tt == TR.KILL:
            self.give_buff(BT.BATTLE_CONTINUATION, 0, bv[1], max_stack=3, 
                           tag="CyclopsePrincess_P1_BC", desc=f"<{desc} : 불사>")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "힘이 넘쳐 흐르는구나!"
        if tt == TR.BATTLE_CONTINUED:
            self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc=desc)
        elif tt == TR.ROUND_START:
            stack = 0
            for pbt in ("CRIT", "IP", "BC"):
                if self.find_buff(tag="CyclopsePrincess_P1_"+pbt):
                    stack += 1
            for t in self.get_passive_targets(targets):
                for _ in range(stack):
                    t.give_buff(BT.ATK, 1, bv[0]/20, efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, round_=1, desc=desc)
                if t.find_buff(tag="LRL_P2"):
                    t.give_buff(BT.ATK, 1, bv[0]/20, efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, round_=1, desc=desc)
                    t.give_buff(BT.DEFPEN, 0, bv[1]*5, efft=BET.BUFF, round_=1, desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "피의 저주"
        if tt == TR.HIT:
            stack = 0
            for pbt in ("CRIT", "IP", "BC"):
                if self.find_buff(tag="CyclopsePrincess_P1_"+pbt):
                    stack += 1
            if stack >= 2:
                for t, v in args["targets"].items():
                    if v > 0:
                        t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_={BT.FOLLOW_ATTACK, BT.TARGET_PROTECT}), 
                                    desc=desc)
                        t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=1, max_stack=1, tag="CyclopsePrincess_P3_TDI", 
                                    desc=desc)
        elif tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.find_buff(tag="CyclopsePrincess_A2") and t.find_buff(tag="LRL_A2"):
                    t.give_buff(BT.ACT_PER_TURN, 0, -1, round_=1, max_stack=1, 
                                tag="CyclopsePrincess_P3_ACT_POINT", desc=desc)
