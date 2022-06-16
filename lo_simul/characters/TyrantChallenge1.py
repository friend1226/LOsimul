from ..lo_char import *


class TyrantChallenge1(Character):
    id_ = "Tyrant_Challenge1"
    name = "폭군 타이런트"
    code = "Tyrant_Challenge1"
    group = Group.PARASITE
    isenemy = True
    isags = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "타이런트 바이트"
        for t in targets:
            if targets[t] > 0:
                self.give_buff(BT.GIVEDMGINC, 1, bv[0], round_=0, efft=BET.BUFF, data=D.DmgHPInfo(type_=4), desc=desc)
                t.give_buff(BT.DEF, 1, bv[1], round_=2, max_stack=1, efft=BET.DEBUFF, tag="TyrantCh1_A1_DEF", desc=desc)
                if t.hp / t.maxhp >= d(.5):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF),
                                desc="회심의 분쇄")
                self.give_buff(BT.GIMMICK, 0, 1, max_stack=3, tag=G.Tyrant_Challenge_1, desc="포식자")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.ELEMENT_RES[E.FIRE], 0, bv[min(self.stack_limited_buff_tags[G.Tyrant_Challenge_1], 2)],
                            round_=2, max_stack=1, efft=BET.DEBUFF, tag="TyrantCh1_A2_FIRERES", desc="프라이멀 파이어")
                self.remove_buff(tag=G.Tyrant_Challenge_1)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            hprate = self.hp / self.maxhp
            if hprate >= d('.6'):
                self.give_buff(BT.GIMMICK, 0, 1, round_=1, tag="TyrantCh1_P1_HEAVY", desc="먹잇감 탐색 (중장형)")
            if hprate <= d('.5999'):
                self.give_buff(BT.GIMMICK, 0, 1, round_=1, tag="TyrantCh1_P1_LIGHT", desc="먹잇감 탐색 (경장형)")
            if hprate <= d('.2999'):
                self.give_buff(BT.GIMMICK, 0, 1, round_=1, tag="TyrantCh1_P1_FLY", desc="먹잇감 탐색 (기동형)")
            if len(self.game.get_chars(field=self.isenemy)) == 1:
                desc = "먹잇감 독식"
                self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, max_stack=1, count=3, count_trig={TR.GET_HIT, },
                               tag="TyrantCh1_P1_ATK", desc=desc)
                self.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, max_stack=1, count=3, count_trig={TR.GET_HIT, },
                               tag="TyrantCh1_P1_ACC", desc=desc)
        elif tt == TR.GET_HIT:
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.PROVOKED), desc="먹잇감 집중")
            if args["element"] > 0:
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag="TyrantCh1_P1"),
                               desc="먹잇감 탐색")
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc1 = "원시의 본능"
        desc2 = "최후의 포효"
        if tt == TR.ROUND_START:
            self.give_buff(BT.DEF, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc1)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[1], round_=1, efft=BET.BUFF, desc=desc1)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc1)
        elif tt == TR.ATTACK:
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TARGET_PROTECT, efft=BET.BUFF), desc=desc1)
            self.give_buff(BT.MARKED, 0, 1, round_=2, efft=BET.BUFF, max_stack=1, tag="TyrantCh1_P2_MARKED", desc=desc1)
        elif tt == TR.WAVE_START:
            self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[0], max_stack=1, tag="TyrantCh1_P2_B.C.", desc=desc2)
        elif tt == TR.BATTLE_CONTINUED:
            self.give_buff(BT.SPD, 1, bv[2], max_stack=1, tag="TyrantCh1_P2_SPD", desc=desc2)
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BATTLE_CONTINUATION))
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            for t in self.get_passive_targets(targets, field=not self.isenemy):
                t.give_buff(BT.INABILLITY_SKILL, 0, 1, round_=2, efft=BET.DEBUFF, desc="폭군의 포효", chance=50,
                            overlap_type=BOT.RENEW)
        elif tt == TR.DEAD:
            for t in self.get_passive_targets(targets, field=not self.isenemy):
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], data=D.FDmgInfo(self, E.FIRE), desc="최후의 포효")
