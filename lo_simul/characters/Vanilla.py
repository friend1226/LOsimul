from ..lo_char import *

id_ = 5
name = "바닐라"
code = "3P_Vanilla"
group = Group.BATTLE_MAID
isenemy = False
is21squad = False

def _active1(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        if targets[t] > 0:
            desc = "다리 노리기"
            t.give_buff(BT.ROOTED, 0, 1, round_=2, efft=BET.DEBUFF, desc=desc)
            t.give_buff(BT.SPD, 1, bv[0], round_=2, efft=BET.DEBUFF, desc=desc)
            if t.find_buff(type_={BT.ROOTED, BT.EVA}, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], round_=0, desc="직격")
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _active2(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        if targets[t] > 0:
            if t.find_buff(type_={BT.ROOTED, BT.EVA}, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0, data=D.FDmgInfo(element=E.FIRE), desc="정밀 사격")
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    desc = "뒷정리"
    if tt == TR.ATTACK:
        for p in self.get_passive_targets(targets):
            if p.type_[1] != CR.DEFENDER:
                p.give_buff(BT.FOLLOW_ATTACK, 0, 1, round_=2, efft=BET.BUFF, data=D.FollowAttack(self), desc=desc)
        if self.find_buff(type_={BT.FOLLOW_ATTACK, BT.TARGET_PROTECT}):
            self.give_buff(BT.ATK, 1, bv[0], round_=2, efft=BET.BUFF, max_stack=1, tag="Vanilla_P1_ATK", desc=desc)
            self.give_buff(BT.ACC, 0, bv[1], round_=2, efft=BET.BUFF, max_stack=1, tag="Vanilla_P1_ACC", desc=desc)
    if tt == TR.KILL:
        for p in self.get_passive_targets(targets):
            if p.type_[1] != CR.DEFENDER:
                p.give_buff(BT.AP, 0, bv[2], efft=BET.BUFF, desc=desc)

def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
    desc = "앞장서시죠"
    if tt == TR.ROUND_START:
        for p in self.get_passive_targets(targets):
            p.give_buff(BT.ROW_PROTECT, 0, 1, round_=1, efft=BET.BUFF, desc=desc)
            p.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            p.give_buff(BT.ACC, 0, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            p.give_buff(BT.SPD, 1, bv[2], round_=1, efft=BET.BUFF, desc=desc)
            p.give_buff(BT.FOLLOW_ATTACK, 0, 1, round_=1, efft=BET.BUFF, data=D.FollowAttack(self), desc=desc)
