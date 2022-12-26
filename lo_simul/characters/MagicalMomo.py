from ..lo_char import *


class MagicalMomo(Character):
    _id = 123
    name = "마법소녀 매지컬 모모"
    code = "DS_MoMo"
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
        desc = "회심의 일격"
        for t in targets:
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc=desc)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="회심의 일격")
                _promotion = bool(self.find_buff(tag="Momo_P3"))
                if (_promotion and t.hp_rate <= .5) or (not _promotion and t.hp_rate <= .25):
                    desc = "절명오의" + ("!" if _promotion else "")
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0] * d('1.25'), overlap_type=BOT.INSTANCE, desc=desc)
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
                else:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0] * d('1.25'), 
                                overlap_type=BOT.INSTANCE, desc="급소 찌르기!", chance=10)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            bv2 = bv[0] * 200 / 3
            if self.find_buff(tag="Momo_P3"):
                desc = "마법신의 가호"
                self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc, chance=40)
                self.give_buff(BT.CRIT, 0, bv2, round_=1, efft=BET.BUFF, desc=desc, chance=30)
                self.give_buff(BT.ACC, 0, bv2 * 2, round_=1, efft=BET.BUFF, desc=desc, chance=40)
                self.give_buff(BT.EVA, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc, chance=40)
                self.give_buff(BT.TAKEDMGDEC, 1, bv2 * 2 / 100, round_=1, efft=BET.BUFF, desc=desc, chance=15)
            if "DS_Baekto" in set(map(lambda c: c.code, 
                                      self.game.get_chars(field=self.isenemy).values())):
                desc1 = "꿈과 희망"
                self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc1)
                self.give_buff(BT.CRIT, 0, bv2, round_=1, efft=BET.BUFF, desc=desc1)
                self.give_buff(BT.ACC, 0, bv2 * 2, round_=1, efft=BET.BUFF, desc=desc1)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "기억할게!"
        if tt == TR.INCAPABLE:
            lr = 2 + (self.skillvl[3] == 10)
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)
                t.give_buff(BT.ATK, 1, bv[0], round_=lr, desc=desc)
                t.give_buff(BT.CRIT, 0, bv[0] * 100, round_=lr, desc=desc)
                t.give_buff(BT.SPD, 1, bv[0], round_=lr, desc=desc)
                t.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=lr, desc=desc)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "성장형 마법소녀"
        if tt == TR.ROUND_START:
            bv2 = bv[0] * 200 / 3
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.CRIT, 0, bv2, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ACC, 0, bv2 * 2, round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.EVA, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv2 * 2 / 100, round_=1, efft=BET.BUFF, desc=desc)
        elif tt == TR.WAVE_START:
            self.give_buff(BT.BATTLE_CONTINUATION, 0, 300, count=1, desc=desc)
            self.give_buff(BT.GIMMICK, 0, 1, tag="Momo_P3", desc="성장 완료!")
