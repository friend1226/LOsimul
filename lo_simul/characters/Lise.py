from ..lo_char import *

id_ = 7
name = "리제"
code = "3P_ScissorsLise"
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
            t.give_buff(BT.DEF, 1, -bv[0], efft=BET.DEBUFF, round_=3, desc="장갑 오려내기")
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc="회심의 일격")
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _active2(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        if targets[t] > 0:
            desc = "약점 공격"
            if t.find_buff(type_=BT.TAKEDMGINC, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc=desc)
            if t.find_buff(type_=BT.DEF, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, desc=desc)
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.ROUND_START:
        desc = "정원사의 본성"
        self.give_buff(BT.DEFPEN, 1, bv[0], efft=BET.BUFF, round_=1, desc=desc)
        self.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, round_=1, desc=desc)
    elif tt == TR.HIT:
        desc = "숨겨진 본성"
        self.give_buff(BT.ATK, 1, bv[2], round_=2, max_stack=1, desc=desc, tag="Lise_P1_ATK")
        self.give_buff(BT.TAKEDMGINC, 1, bv[3], round_=2, max_stack=1, desc=desc, tag="Lise_P1_TAKEDMGINC")

def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    if tt == TR.WAVE_START:
        self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc="해충 처리")
        allys = set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values()))
        if 12 in allys:
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, max_stack=1, tag="Lise_P2_LILITHSPD",
                           desc="나랑 처리할 일이 있지 않아?")
        if 16 in allys:
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, max_stack=1, tag="Lise_P2_SOWANSPD",
                           desc="네가 그랬지?")
    elif tt == TR.KILL:
        self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, max_stack=1, tag="Lise_P2_KILLSPD", desc="히히히...")
