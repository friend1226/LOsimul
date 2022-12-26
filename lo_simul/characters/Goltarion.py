from ..lo_char import *


class Goltarion(Character):
    _id = 128
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
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="소환!! 데모닉 웨폰")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt in {TR.ROUND_START, TR.GET_ATTACKED, TR.ATTACK}:
            if self.hp / self.maxhp >= d('.9'):
                if len(list(filter(lambda c: c.isags, self.game.get_chars(field=self.isenemy).values()))) > 3:
                    self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[0], max_stack=1, count=1, 
                                   tag=G.GOLTARION, overlap_type=BOT.SINGLE)
            elif self.find_buff(tag=G.GOLTARION):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag=G.GOLTARION, force=True),
                               desc="내부 부품 손상")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "마왕님, 조심하십시오!"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.type_[0] == CharType.LIGHT and t.type_[1] != CharRole.DEFENDER:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, round_=1,
                                data=D.TargetProtect(self), desc=desc)
        elif tt == TR.ATTACK:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ACTIVE_RESIST, 1, bv[0], efft=BET.BUFF, round_=2, desc=desc)
                for i in range(1, 4):
                    t.give_buff(BT_ELEMENT_RES[i], 0, bv[0], efft=BET.BUFF, round_=2, desc=desc)
            for t in args["targets"]:
                if t.find_buff(type_=BT.MARKED, tag="Faucre_MARKED"):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], overlap_type=BOT.INSTANCE, desc="깊어지는 낙인")
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        ally_codes = set(map(lambda c: c.code, self.game.get_chars(field=self.isenemy).values()))
        momo_code = "DS_MoMo"
        baekto_code = "DS_Baekto"
        momo = momo_code in ally_codes
        baekto = baekto_code in ally_codes
        faucre = "DS_Faucre" in ally_codes
        if tt == TR.ROUND_START:
            desc = "마왕님의 명이라면...!"
            for t in self.get_passive_targets(targets):
                if t.code == momo_code or t.code == baekto_code:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, round_=1,
                                data=D.TargetProtect(self), desc=desc)
            if faucre:
                self.give_buff(BT.DEFPEN, 0, bv[0], round_=1, desc=desc + " (마왕님))")
                self.give_buff(BT.ATK, 1, bv[0], round_=1, desc=desc + " (마왕님))")
            if momo:
                self.give_buff(BT.SKILL_RATE, 0, bv[1], round_=1, desc=desc + " (모모)")
            if baekto:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, desc=desc + " (백토)")
        elif tt == TR.ATTACK:
            desc = "이번만이다, 마법소녀!"
            for t in self.get_passive_targets(targets):
                if t.code == momo_code or t.code == baekto_code:
                    t.give_buff(BT.ACTIVE_RESIST, 1, bv[3], efft=BET.BUFF, round_=2, desc=desc)
                    for i in range(1, 4):
                        t.give_buff(BT_ELEMENT_RES[i], 0, bv[3], efft=BET.BUFF, round_=2, desc=desc)
                    self.give_buff(BT.ACTIVE_RESIST, 1, bv[3], efft=BET.BUFF, round_=2, 
                                   max_stack=1, tag="Goltarion_P3_AR", desc="마왕님, 조심하십시오!")
        if tt in {TR.ROUND_START, TR.GET_ATTACKED, TR.ATTACK}:
            if self.hp / self.maxhp >= d('.9'):
                if faucre:
                    self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[2], max_stack=1, count=1,
                                   tag=G.GOLTARION, overlap_type=BOT.SINGLE)
            elif self.find_buff(tag=G.GOLTARION):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag=G.GOLTARION, force=True), desc="내부 부품 손상")
