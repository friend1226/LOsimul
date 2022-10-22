from ..lo_char import *


class MagicalBaekto(Character):
    id_ = 127
    name = "마법소녀 매지컬 백토"
    code = "DS_Baekto"
    group = Group.D_ENTERTAINMENT
    isenemy = False
    is21squad = False
    isags = False
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "조용히 하세요!"
                t.give_buff(BT.PROVOKED, 0, 1, round_=2, efft=BET.DEBUFF, overlap_type=BOT.RENEW, desc=desc)
                t.give_buff(BT.ATK, 1, bv[0], round_=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ACC, 0, bv[0] * 200, round_=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, -bv[0], round_=2, efft=BET.DEBUFF, desc=desc)
                if t.find_buff(type_=BT.DEF, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], overlap_type=BOT.INSTANCE, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.DEF, 1, bv[0], round_=2, efft=BET.DEBUFF, desc="문 라이트 체인소")
                if targets[t] > 1:
                    desc = "매지컬 파워! (물리)"
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.DEF, efft=BET.BUFF), desc=desc)
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], overlap_type=BOT.INSTANCE, desc=desc)
                momo_id = CP.get("DS_MoMo").id_
                for p in self.game.get_chars(field=self.isenemy).values():
                    if p.id_ == momo_id:
                        self.give_buff(BT.COOP_ATTACK, 0, 1, data=D.CoopAttack(p, 2), round_=1, efft=BET.BUFF, 
                                       desc="Fatality - 마법소녀 매지컬 모모")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "정의는 지지 않아!"
        if tt == TR.ROUND_START:
            self.give_buff(BT.EVA, 0, bv[0], round_=1, efft=BET.BUFF, desc="월인 비전 체술")
            self.give_buff(BT.TAKEDMGDEC, 1, bv[1], count=1, count_trig={TR.GET_HIT, }, efft=BET.BUFF, 
                           max_stack=1, tag="Baekto_P1_TDD", desc=desc)
        elif tt == TR.EVADE:
            self.give_buff(BT.ATK, 1, bv[2], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.CRIT, 0, 200, round_=1, efft=BET.BUFF, desc=desc)
        elif tt == TR.GET_HIT:
            self.give_buff(BT.ATK, 1, bv[2], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, round_=1, efft=BET.BUFF, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "달의 가호"
        if tt == TR.ROUND_START:
            my_eva = self.get_stats(BT.EVA)
            for t in self.get_passive_targets(targets):
                if t == self or (t.get_stats(BT.EVA) < my_eva and t.type_[1] != CR.DEFENDER):
                    if t != self:
                        t.give_buff(BT.TARGET_PROTECT, 0, 1, round_=1, efft=BET.BUFF, 
                                    data=D.TargetProtect(self), desc=desc)
                    flags = {BT.ATK: False, BT.ACC: False, BT.SPD: False}
                    for b in t.find_buff(type_={BT.ATK, BT.ACC, BT.SPD}, efft=BET.BUFF):
                        flags[b.type] = True
                    if flags[BT.ATK]:
                        t.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, 
                                    max_stack=1, tag="Baekto_P2_ATK", desc=desc)
                    if flags[BT.ACC]:
                        t.give_buff(BT.ACC, 0, bv[1], round_=1, efft=BET.BUFF, 
                                    max_stack=1, tag="Baekto_P2_ACC", desc=desc)
                    if flags[BT.SPD]:
                        t.give_buff(BT.SPD, 1, bv[2], round_=1, efft=BET.BUFF, 
                                    max_stack=1, tag="Baekto_P2_SPD", desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "문 라이트 파워"
        if tt == TR.ROUND_START:
            self.give_buff(BT.SKILL_RATE, 1, bv[0] / 100, proportion=(self, BT.EVA), round_=1, 
                           efft=BET.BUFF, desc=desc)
            desc = "어디까지나 '임시'라구요"
            for t in self.get_passive_targets(targets):
                if t.code == "AGS_Goltarion":
                    flags = {BT.ATK: False, BT.ACC: False, BT.SPD: False}
                    for b in t.find_buff(type_={BT.ATK, BT.ACC, BT.SPD}, efft=BET.BUFF):
                        flags[b.type] = True
                    if flags[BT.ATK]:
                        t.give_buff(BT.ATK, 1, bv[2], round_=1, efft=BET.BUFF, 
                                    max_stack=1, tag="Baekto_P2_ATK", desc=desc)
                    if flags[BT.ACC]:
                        t.give_buff(BT.ACC, 0, bv[3], round_=1, efft=BET.BUFF, 
                                    max_stack=1, tag="Baekto_P2_ACC", desc=desc)
                    if flags[BT.SPD]:
                        t.give_buff(BT.SPD, 1, bv[0] * d('.3'), round_=1, efft=BET.BUFF, 
                                    max_stack=1, tag="Baekto_P2_SPD", desc=desc)
        elif tt == TR.GET_ATTACKED:
            self.give_buff(BT.COUNTER_ATTACK, 1, bv[1], count=1, count_trig={TR.AFTER_COUNTER, }, 
                           efft=BET.BUFF, desc=desc)
        elif tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, tag="Baekto_P3", desc="완전한 달의 가호")
