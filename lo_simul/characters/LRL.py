from ..lo_char import *


class LRL(Character):
    id_ = 118
    name = "LRL"
    code = "PECS_LRL"
    group = Group.PUBLIC_SERVANT
    isenemy = False
    is21squad = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "럭키 히트!"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc=desc, chance=19)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "이터널 빔!"
        for t in targets:
            t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.BUFF), efft=BET.DEBUFF, desc=desc)
            t.give_buff(BT.ACC, 0, bv[0], efft=BET.DEBUFF, round_=2, desc=desc, tag="LRL_A2_ACC")
            t.give_buff(BT.AP, 0, bv[1], efft=BET.DEBUFF, round_=2, desc=desc, tag="LRL_A2_AP")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ATTACK:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.EVA, 0, bv[0]*100, efft=BET.BUFF, round_=2, desc="부끄러움은 우리의 몫")
                t.give_buff(BT.SPD, 1, bv[0], efft=BET.BUFF, round_=2, desc="어서 빠져나가고 싶다...")
                t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=2, desc="여기서 벗어나야겠어...")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "진조의 힘?"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.CRIT, 0, bv[0], efft=BET.BUFF, round_=1, desc=desc, tag="LRL_P2_CRIT")
                t.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, round_=1, desc=desc, tag="LRL_P2_ACC")
                t.give_buff(BT.ACTIVE_RATE, 0, bv[2], efft=BET.BUFF, round_=1, desc=desc, tag="LRL_P2_ACTIVE_RATE")
        elif tt == TR.HIT:
            if self.find_buff(tag="LRL_P2"):
                if args["skill_no"] == 1:
                    if any(args["targets"].values()):
                        desc = "슈퍼 럭키 히트!"
                        self.give_buff(BT.DEFPEN, 1, d('1.5'), efft=BET.BUFF, round_=0, desc=desc, chance=19)
                        self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, efft=BET.BUFF, round_=0, desc=desc, chance=19)
                if args["skill_no"] == 2:
                    for t in args["targets"]:
                        if args["targets"][t] > 0:
                            t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_={BT.ATK, BT.CRIT}, efft=BET.BUFF),
                                        desc="진! 이터널 빔!")

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "진조를 계승하는 자"
        if tt == TR.WAVE_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.SKILL_RATE, 0, bv[0], desc=desc)
        elif tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.find_buff(tag="CyclopsePrincess_P3"):
                    t.give_buff(BT.SKILL_RATE, 0, bv[0], desc=desc)
        elif tt == TR.HIT:
            if args["skill_no"] == 1:
                for t in args["targets"]:
                    if args["targets"][t] > 1:
                        t.give_buff(BT.TAKEDMGINC, 1, d('.25'), efft=BET.DEBUFF, round_=2, desc=desc)
                        t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), efft=BET.DEBUFF, round_=2,
                                    desc=desc, max_stack=1, tag="LRL_P3_IMMUNE_BUFF")
            if args["skill_no"] == 2:
                for t in args["targets"]:
                    if args["targets"][t] > 1:
                        t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.IGNORE_BARRIER_DMGDEC), desc=desc)
