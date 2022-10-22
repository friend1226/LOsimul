from ..lo_char import *


class Alice(Character):
    id_ = 4
    name = "앨리스"
    code = "3P_Alice"
    group = Group.BATTLE_MAID
    isenemy = False
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "찌르는 강철"
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, round_=2, desc=desc, overlap_type=BOT.RENEW)
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], efft=BET.DEBUFF, round_=2, desc=desc)
                t.give_buff(BT.EVA, 0, bv[1], efft=BET.DEBUFF, round_=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_={BT.ROOTED, BT.MARKED}, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc="정밀 폭격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.hp / self.maxhp >= d('.5'):
                desc = "강자의 품격"
                self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
                self.give_buff(BT.GIVEDMGINC, 1, bv[1], efft=BET.BUFF, round_=1, data=D.DmgInfo(hp_type=4), desc=desc)
                self.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, round_=1, desc=desc)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "가학의 기쁨"
        if tt == TR.ATTACK:
            self.give_buff(BT.SPD, 1, bv[0], efft=BET.BUFF, max_stack=3, tag="Alice_P2", desc=desc)
        elif tt == TR.KILL:
            self.give_buff(BT.AP, 0, self.get_skill_cost(args["skill_no"]), efft=BET.BUFF, desc=desc, chance=10)
    
    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "학살 본능"
        if tt == TR.ROUND_START:
            self.give_buff(BT_ANTI_OS[CharType.LIGHT], 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
        elif tt == TR.WAVE_START or tt == TR.IDLE:
            self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, efft=BET.BUFF, count=2+(self.skillvl[4] == 10),
                           desc=desc, count_trig={TR.AFTER_SKILL}, overlap_type=BOT.RENEW)
