from ..lo_char import *


class Erato(Character):
    id_ = 208
    name = "에라토"
    code = "PECS_Erato"
    group = Group.AMUSE_ATTENDANT
    isenemy = False
    is21squad = False

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "넌 이미☆나의 FAN"
        for t in targets:
            t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.EVA, efft=BET.BUFF), desc=desc)
            t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, round_=3, desc=desc, tag="Erato_A1_EVA")
            if targets[t] > 0:
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.COUNTER_ATTACK, efft=BET.BUFF), desc=desc)
                movebuff = t.give_buff(BT.FORCE_MOVE, 0, -1, efft=BET.DEBUFF, round_=3, max_stack=1, desc=desc,
                                       tag="Earto_A1_MOVE")

                def temppassive(self, tt, args=None):
                    if tt == TR.GET_HIT:
                        self.owner.give_buff(BT.FORCE_MOVE, 0, -1, round_=0)
                movebuff.passive = temppassive
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "With You"
        bval = bv[0] * (1 + len(self.game.get_chars(field=self.isenemy))) / 2
        for t in targets:
            t.give_buff(BT.ATK, 0, bval, proportion=(self, BT.ATK), efft=BET.BUFF, round_=2, desc=desc,
                        overlap_type=BOT.RENEW)
        self.give_buff(BT.ATK, 1, d('-.4'), desc="성대 결절", tag='Erato_A2_ATK_DOWN')
        return {}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "감미로운 멜로디"
        if tt == TR.WAVE_START:
            myspd = self.get_stats(BT.SPD)
            for t in self.get_passive_targets(targets):
                if myspd > t.get_stats(BT.SPD):
                    t.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc=desc)
        elif tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.type_[1] == CR.ATTACKER:
                    t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ATK, efft=BET.DEBUFF),
                                round_=1, efft=BET.BUFF, desc=desc)
                if t.type_[1] == CR.DEFENDER:
                    t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.DEF, efft=BET.DEBUFF),
                                round_=1, efft=BET.BUFF, desc=desc)
                if t.type_[1] == CR.SUPPORTER:
                    t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.AP, efft=BET.DEBUFF),
                                round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ATK, efft=BET.DEBUFF),
                           round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.DEF, efft=BET.DEBUFF),
                           round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.AP, efft=BET.DEBUFF),
                           round_=1, efft=BET.BUFF, desc=desc)
        if tt == TR.ROUND_START or tt == TR.HIT:
            self.give_buff(BT.REMOVE_BUFF, 0, 1,
                           data=D.BuffCond(
                               type_=BT.ATK, func=lambda b: b.proportion is not None and b.proportion[1] == BT.ATK),
                           desc="솔로 라이브!")

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            self.give_buff(BT.ATK, 1, bv[0], round_=1, desc="꿈을 묶는 여로")
            if not self.find_buff(tag='Erato_A2_ATK_DOWN'):
                self.give_buff(BT.SPD, 1, bv[1], round_=1, efft=BET.BUFF, desc="성대 준비 완료!")
        elif tt == TR.ENEMY_DEAD:
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag='Erato_A2_ATK_DOWN'))
        elif tt == TR.WAVE_START and 209 in {ch.id_ for ch in self.game.get_chars(field=self.isenemy).values()}:
            self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[2], desc="작곡가님...!")

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "형광팬"
            for t in self.get_passive_targets(targets, True):
                fan_stack = len(t.find_buff(tag='Erato_A1_EVA'))
                colpos = t.getposy() if t.isenemy else 2 - t.getposy()
                if fan_stack >= 1:
                    t.give_buff(BT.SPD, 1, bv[0] * (4 - colpos) / 4, round_=1, desc=desc[2:])
                if fan_stack >= 2:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0] * (4 - colpos) / 2, round_=1, desc=desc[1:])
                if fan_stack >= 3:
                    t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), round_=1, desc=desc)
                    if colpos == 0:
                        t.give_buff(BT.INABILLITY_ACT, 0, 1, round_=1, desc=desc)
