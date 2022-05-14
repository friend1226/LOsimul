from ..lo_char import *


class Goltarion(Character):
    id_ = 128
    name = "골타리온"
    code = "AGS_Goltarion"
    group = Group.D_ENTERTAINMENT
    isenemy = False
    is21squad = False
    isags = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "작열! 헬파이어 빔"
                t.give_buff(BT.DEF, 1, bv[0], efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0] * 100, efft=BET.DEBUFF, round_=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(type_={BT.DEF, BT.EVA}, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="소환!! 데모닉 웨폰")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt in {TR.ROUND_START, TR.GET_ATTACKED, TR.ATTACK}:
            if self.hp / self.maxhp >= d('.9'):
                if len(list(filter(lambda c: c.isags, self.game.get_chars(field=self.isenemy).values()))) > 3:
                    self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[0], max_stack=1, count=1,
                                   count_trig={TR.BATTLE_CONTINUED, }, tag=G.GOLTARION)
            elif self.find_buff(tag=G.GOLTARION):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag=G.GOLTARION, force=True),
                               desc="내부 부품 손상")
        if tt == TR.ROUND_START:
            if 171 in set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values())):  # 뽀끄루
                desc = "세뇌의 파동"
                self.give_buff(BT.ATK, 1, bv[1], efft=BET.BUFF, round_=1, max_stack=1,
                               tag="Goltarion_P1_ATK", desc=desc)
                self.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, round_=1, max_stack=1,
                               tag="Goltarion_P1_CRIT", desc=desc)
                self.give_buff(BT.ACC, 0, bv[1] * 100, efft=BET.BUFF, round_=1, max_stack=1,
                               tag="Goltarion_P1_ACC", desc=desc)
                self.give_buff(BT.DEFPEN, 1, bv[1], efft=BET.BUFF, round_=1, max_stack=1,
                               tag="Goltarion_P1_DEFPEN", desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "마왕님, 조심하십시오!"
            for t in self.get_passive_targets(targets):
                if t.type_[0] == CharType.LIGHT:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, round_=1,
                                data=D.TargetProtect(self), desc=desc)
            if 127 in set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values())):  # 백토
                for t in self.get_passive_targets(targets):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(func=lambda b: b.desc == desc, limit=5),
                                desc="네놈은 뭐냐?!")
        elif tt == TR.ATTACK:
            desc = "마왕님, 조심하십시오!"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ACTIVE_RESIST, 1, bv[0], efft=BET.BUFF, round_=2, desc=desc)
                for i in range(1, 4):
                    t.give_buff(BT.ELEMENT_RES[i], 0, bv[0] * 100, efft=BET.BUFF, round_=2, desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        ally_ids = set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values()))
        momo = 123 in ally_ids
        baekto = 127 in ally_ids
        faucre = 171 in ally_ids
        if tt == TR.ROUND_START:
            desc = "마왕님의 명이라면...!"
            for t in self.get_passive_targets(targets):
                if t.id_ == 123 or t.id_ == 127:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, round_=1,
                                data=D.TargetProtect(self), desc=desc)
            if faucre:
                self.give_buff(BT.DEFPEN, 1, bv[0], round_=1, desc=desc + " (뽀끄루)")
                self.give_buff(BT.ATK, 1, bv[0], round_=1, desc=desc + " (뽀끄루)")
            if momo:
                self.give_buff(BT.SKILL_RATE, 0, bv[1], round_=1, desc=desc + " (모모)")
            if baekto:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, desc=desc + " (백토)")
        if tt in {TR.ROUND_START, TR.GET_ATTACKED, TR.ATTACK}:
            if self.hp / self.maxhp >= d('.9'):
                if momo and baekto and faucre:
                    self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[2], max_stack=1, count=1,
                                   count_trig={TR.BATTLE_CONTINUED, }, tag=G.GOLTARION)
            elif self.find_buff(tag=G.GOLTARION):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag=G.GOLTARION, force=True), desc="내부 부품 손상")
