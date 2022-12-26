from ..lo_char import *


class Faucre(Character):
    _id = 171
    name = "뽀끄루 대마왕"
    code = "DS_Faucre"
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
                desc = "헬 인페르노"
                if t.find_buff(tag=BT.FIRE_DOT_DMG, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], efft=BET.DEBUFF, round_=1, desc=desc)
                    t.give_buff(BT.FIRE_DOT_DMG, 0, bv[1], efft=BET.DEBUFF, round_=1, desc=desc)
                    t.give_buff(BT.FIRE_RES, 0, bv[2], efft=BET.DEBUFF, round_=1, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], efft=BET.DEBUFF, round_=2, 
                            max_stack=1, tag="Faucre_A1_TDI", desc=desc)
                t.give_buff(BT.FIRE_RES, 0, bv[2], efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.FIRE_DOT_DMG, 0, bv[1], efft=BET.DEBUFF, round_=2, desc=desc, overlap_type=BOT.SINGLE)
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, round_=2, desc=desc, 
                            tag="Faucre_MARKED", overlap_type=BOT.RENEW)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "크림슨 익스큐션"
        for t in targets:
            if targets[t] > 0:
                if targets[t] > 1:
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], data=D.DmgInfo(element=E.FIRE), 
                                overlap_type=BOT.INSTANCE, desc=desc)
                t.give_buff(BT.AP, 0, bv[1], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.FIRE_DOT_DMG, 0, bv[2], round_=1, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, round_=2, desc=desc, 
                            tag="Faucre_MARKED", overlap_type=BOT.RENEW)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "세뇌의 파동"
        golt = "AGS_Goltarion"
        horn = self.find_buff(tag=HornOfBADK.code)
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                if t.isenemy or not t.isags or t.code == golt:
                    t.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.ACC, 0, bv[0] * 100, round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.CRIT, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.DEFPEN, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            if horn:
                desc1 = "피휘"
                bval = {}
                bid = set()
                for _b in horn:
                    bval[_b.type] = _b.value * 2
                    bid.add(_b.id)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(id_=bid), desc=desc1 + " (부작용 극복)")
                t.give_buff(BT.CRIT, 0, bval[BT.CRIT], round_=1, desc=desc1)
                t.give_buff(BT.SPD, 1, bval[BT.CRIT], round_=1, desc=desc1)
        elif tt == TR.IDLE:
            desc += "!"
            for t in self.get_passive_targets(targets):
                if t.isenemy or not t.isags or t.code == golt:
                    t.give_buff(BT.ATK, 1, bv[0], round_=2, efft=BET.BUFF, 
                                max_stack=1, tag="Faucre_P1_ATK", desc=desc)
                    t.give_buff(BT.ACC, 0, bv[0] * 100, round_=2, efft=BET.BUFF, 
                                max_stack=1, tag="Faucre_P1_ACC", desc=desc)
                    t.give_buff(BT.CRIT, 0, bv[1], round_=2, efft=BET.BUFF, 
                                max_stack=1, tag="Faucre_P1_CRIT", desc=desc)
                    t.give_buff(BT.DEFPEN, 1, bv[0], round_=2, efft=BET.BUFF, 
                                max_stack=1, tag="Faucre_P1_DEFPEN", desc=desc)
                    if not horn:
                        t.give_buff(BT.PHYSICAL_DOT_DMG, 0, bv[2], round_=2, efft=BET.BUFF,
                                    max_stack=1, tag="Faucre_P1_DOTDMG", desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "마왕 강림"
        if tt == TR.ROUND_START:
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ACC, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.SPD, 1, bv[2], round_=1, efft=BET.BUFF, desc=desc)
            if self.hp_rate >= .5:
                desc1 = f"대{desc}!"
                self.give_buff(BT.ATK, 1, bv[0] * d('.5'), round_=1, efft=BET.BUFF, desc=desc1)
                self.give_buff(BT.ACC, 0, bv[1] * d('.5'), round_=1, efft=BET.BUFF, desc=desc1)
                self.give_buff(BT.SPD, 1, bv[2] * d('.5'), round_=1, efft=BET.BUFF, desc=desc1)
            if self.hp_rate <= .5:
                self.give_buff(BT.EVA, 0, bv[2] * 100, round_=1, efft=BET.BUFF, desc="컷...컷트!")
                self.give_buff(BT.TAKEDMGDEC, 1, bv[3], round_=1, efft=BET.BUFF, desc="아픈 건 싫어!")
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "마의 장막"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.MARKED, efft=BET.DEBUFF), 
                            round_=1, efft=BET.BUFF, desc=desc)
                if t.code == "AGS_Goltarion":
                    t.give_buff(BT.TAKEDMGINC, 1, d('.2'), round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.SKILL_RATE, 0, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                else:
                    t.give_buff(BT.TAKEDMGINC, 1, d('.1'), round_=1, efft=BET.BUFF, desc=desc)
                    t.give_buff(BT.SKILL_RATE, 0, bv[0] / 2, round_=1, efft=BET.BUFF, desc=desc)
