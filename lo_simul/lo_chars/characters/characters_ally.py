from lo_simul.lo_char_base import *
from lo_simul.lo_equips import *


class DummyAlly(Character):
    id_ = "DummyAlly"
    name = "더미(아군)"
    code = "DummyAlly"
    group = None
    isenemy = False

    stats = ('50', '20', '20', '2', '0', '0', '3', '0', '75', '0', '0', '0', '0')
    skills = [[
        {
            'apcost': (None, 4),
            'atkrate': (None, '1'),
            'accbonus': (None, 0),
            'range': (None, 2),
            'isattack': 2046,
            'isgrid': 0,
            'isignoreprot': 0,
            'element': (None, 0),
            'aoe': ((0, True, ((0, 0, 1),)),),
            'buff': ('.2',)
        },
        {
            'apcost': (None, 6),
            'atkrate': (None, '1.2'),
            'accbonus': (None, 0),
            'range': (None, 1),
            'isattack': 2046,
            'isgrid': 0,
            'isignoreprot': 0,
            'element': ((0, True, ((0, 0, 1),)),),
            'aoe': (None, 0),
            'buff': ('.2',)
        },
        None, None, None
    ], [None, None, None, None, None], None]
    type_ = (0, 0)
    isags = 0
    link_bonus = BuffList()
    full_link_bonuses = [None]

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def extra_passive(self, tt, args=None):
        if tt == TR.IDLE:
            self.give_buff(BT.RANGE, 0, 2, efft=0, _round=2)


class Labiata(Character):
    id_ = 2
    name = "라비아타"
    code = "3P_Labiata"
    group = Group.BATTLE_MAID
    isenemy = False
    is21squad = True

    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        if any(targets[t] for t in targets):
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, max_stack=3, tag=G.LABIATA, desc=G.LABIATA)
        for t in targets:
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], _round=0, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        if self.stack_limited_buff_tags[G.LABIATA] == 3:
            for t in targets:
                if targets[t] > 0:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="최대 출력 강타")
            self.remove_buff(tag=G.LABIATA, limit=1)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "강화 근력"
            self.give_buff(BT.SPD, 1, bv[0], _round=1, efft=0, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[1], _round=1, efft=0, desc=desc)
            if self.stack_limited_buff_tags[G.LABIATA] == 3:
                desc = "초" + desc
                self.give_buff(BT.SPD, 1, bv[0] * d(.5), _round=1, efft=0, desc=desc)
                self.give_buff(BT.TAKEDMGDEC, 1, bv[1] * d(.5), _round=1, efft=0, desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            self.give_buff(BT.DEFPEN, 1, bv[0], _round=1, efft=0, desc="P.G 활성화")
            if self.stack_limited_buff_tags[G.LABIATA] == 2:
                self.give_buff(BT.DEFPEN, 1, bv[0], _round=1, efft=0, desc="P.G 출력 강화")
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, _round=1, efft=0, desc="P.G 출력 강화")

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                desc = "든든한 큰언니"
                t.give_buff(BT.CRIT, 0, bv[0], _round=1, efft=0, desc=desc)
                t.give_buff(BT.ATK, 1, bv[1], _round=1, efft=0, desc=desc)
                t.give_buff(BT.ACC, 0, bv[2], _round=1, efft=0, desc=desc)


class Constantia(Character):
    id_ = 3
    name = "콘스탄챠S2"
    code = "3P_ConstantiaS2"
    group = Group.BATTLE_MAID
    isenemy = False
    is21squad = True

    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 1:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="정밀 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.SPD, 1, bv[0], efft=BET.DEBUFF, _round=1)
                t.give_buff(BT.ROOTED, 0, 1, efft=BET.DEBUFF, _round=2)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, _round=2)
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, _round=2)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc="준비 만전")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ATTACK:
            for t in self.get_passive_targets(targets):
                desc = "사냥감 몰이"
                t.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, _round=3, max_stack=1,
                            tag='Constantia_P2_ATK', desc=desc)
                t.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, _round=3, max_stack=1,
                            tag='Constantia_P2_ACC', desc=desc)
                t.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, _round=3, max_stack=1,
                            tag='Constantia_P2_CRIT', desc=desc)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass


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
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, _round=2, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], efft=BET.DEBUFF, _round=2, desc=desc)
                t.give_buff(BT.EVA, 0, bv[1], efft=BET.DEBUFF, _round=2, desc=desc)
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
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="정밀 폭격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.hp / self.maxhp >= d('.5'):
                desc = "강자의 품격"
                self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, _round=1, desc=desc)
                self.give_buff(BT.GIVEDMGINC, 1, bv[1], efft=BET.BUFF, _round=1, data=D.DmgHPInfo(type_=4), desc=desc)
                self.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, _round=1, desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "가학의 기쁨"
        if tt == TR.ATTACK:
            self.give_buff(BT.SPD, 1, bv[0], efft=BET.BUFF, max_stack=3, tag="Alice_P2", desc=desc)
        elif tt == TR.KILL and self.judge_active(10):
            self.give_buff(BT.AP, 0, self.get_skill_cost(args), efft=BET.BUFF, desc=desc)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "학살 본능"
        if tt == TR.ROUND_START:
            self.give_buff(BT.ANTI_OS[CharType.LIGHT], 1, bv[0], efft=BET.BUFF, _round=1, desc=desc)
        elif tt == TR.WAVE_START or tt == TR.IDLE:
            self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, efft=BET.BUFF,
                           count=2+(self.skillvl[4] == 10), max_stack=1, tag="Alice_P3", desc=desc,
                           count_trig={TR.AFTER_SKILL})


class Vanilla(Character):
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
                t.give_buff(BT.ROOTED, 0, 1, _round=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.SPD, 1, bv[0], _round=2, efft=BET.DEBUFF, desc=desc)
                if t.find_buff(type_={BT.ROOTED, BT.EVA}, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], _round=0, desc="직격")
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
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, data=D.FDmgInfo(element=E.FIRE), desc="정밀 사격")
                if t.find_buff(tag=G.PHOSPHIDE):
                    t.give_buff(BT.INSTANT_DMG, 0, d('.5'), data=D.FDmgInfo(subject=self), desc=G.PHOSPHIDE_DESC)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "뒷정리"
        if tt == TR.ATTACK:
            for p in self.get_passive_targets(targets):
                if p.type_[1] != CR.DEFENDER:
                    p.give_buff(BT.FOLLOW_ATTACK, 0, 1, _round=2, efft=BET.BUFF, data=D.FollowAttack(self), desc=desc)
            if self.find_buff(type_={BT.FOLLOW_ATTACK, BT.TARGET_PROTECT}):
                self.give_buff(BT.ATK, 1, bv[0], _round=2, efft=BET.BUFF, max_stack=1, tag="Vanilla_P1_ATK", desc=desc)
                self.give_buff(BT.ACC, 0, bv[1], _round=2, efft=BET.BUFF, max_stack=1, tag="Vanilla_P1_ACC", desc=desc)
        if tt == TR.KILL:
            for p in self.get_passive_targets(targets):
                if p.type_[1] != CR.DEFENDER:
                    p.give_buff(BT.AP, 0, bv[2], efft=BET.BUFF, desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "앞장서시죠"
        if tt == TR.ROUND_START:
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.ROW_PROTECT, 0, 1, _round=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ATK, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACC, 0, bv[1], _round=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.SPD, 1, bv[2], _round=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.FOLLOW_ATTACK, 0, 1, _round=1, efft=BET.BUFF, data=D.FollowAttack(self), desc=desc)


class Titania(Character):
    id_ = 10
    name = "티타니아"
    code = "3P_Titania"
    group = Group.FAIRY
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
                desc = "차가운 고통"
                t.give_buff(BT.DOT_DMG, 0, bv[0], _round=2, efft=BET.DEBUFF,
                            data=D.FDmgInfo(element=E.ICE), desc=desc)
                t.give_buff(BT.ROOTED, 0, 1, _round=2, efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ELEMENT_RES[E.ICE], 0, bv[1], _round=2, efft=BET.DEBUFF,
                            max_stack=2, tag="Titania_A1_RES", desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "서리 폭풍"
        for t in targets:
            if targets[t] > 0 and t.find_buff(type_=BT.ELEMENT_RES[E.ICE], efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, data=D.FDmgInfo(element=E.ICE), desc=desc)
        self.give_buff(BT.SPD, 1, d('-.55'), _round=2, desc=desc, tag="Titania_A2_SPD_DEC")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "피해의식"
            self.give_buff(BT.ANTI_OS[CharType.HEAVY], 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ATK, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "천년서리"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.ELEMENT_RES[E.FIRE], 0, bv[0], _round=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ANTI_OS[CT.HEAVY], 1, bv[1], _round=1, efft=BET.BUFF, desc=desc)
                if p.type_[1] == CR.DEFENDER:
                    p.give_buff(BT.IMMUNE_BUFF, 0, 1, _round=1, efft=BET.BUFF, desc=desc,
                                data=D.BuffCond(type_=BT.ELEMENT_RES[E.FIRE], efft=BET.DEBUFF))

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(tag="Titania_A2_SPD_DEC"):
            desc = "끝없는 증오"
            self.give_buff(BT.RANGE, 0, 2, _round=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.ATK, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.EVA, 0, bv[1], _round=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[2], _round=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.COUNTER_ATTACK, 1, d('.8'), _round=1, efft=BET.BUFF, desc=desc)


class Emily(Character):
    id_ = 68
    name = "에밀리"
    code = "BR_Emily"
    group = Group.AA_CANNONIERS
    isenemy = False
    is21squad = False

    def isformchanged(self):
        return bool(self.find_buff(type_=BT.GIMMICK, tag=Gimmick.EMILY))

    def skill_no_convert(self, skill_no):
        if skill_no == 2 and self.isformchanged():
            return 7
        else:
            return skill_no

    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], efft=BET.BUFF, _round=0, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        if self.find_buff(tag="Emily_P1"):
            pbuffs = True
        else:
            pbuffs = False
        for t in targets:
            if targets[t] > 0:
                if pbuffs:
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BARRIER, efft=BET.BUFF))
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF))
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.IDLE:
            desc = "출력 강화"
            self.give_buff(BT.CRIT, 0, bv[0], _round=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_CRIT")
            self.give_buff(BT.DEFPEN, 1, bv[1], _round=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_DEFPEN")
            self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, _round=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_IGN")
            self.give_buff(BT.ATK, 1, bv[2], _round=3, efft=BET.BUFF, desc=desc, tag="Emily_P1_ATK")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ATTACK:
            if self.find_buff(type_=BT.FOLLOW_ATTACK, efft=BET.BUFF):
                self.give_buff(BT.AP, 0, bv[0], desc="급속 충전")
            if self.find_buff(type_=BT.TARGET_PROTECT):
                self.give_buff(BT.AP, 0, bv[0], desc="급속 충전")

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt in {TR.ROUND_START, TR.ATTACK, TR.GET_ATTACKED} and self.hp / self.maxhp <= d('.33'):
            self.give_buff(BT.GIMMICK, 0, 1, max_stack=1, tag=Gimmick.EMILY, desc=Gimmick.EMILY)
            self.give_buff(BT.ATK, 1, bv[1], max_stack=1, efft=BET.BUFF, desc=Gimmick.EMILY, tag="Emily_P3_ATK")
            self.give_buff(BT.SPD, 1, bv[1], max_stack=1, efft=BET.BUFF, desc=Gimmick.EMILY, tag="Emily_P3_SPD")
            self.give_buff(BT.EVA, 0, bv[2], max_stack=1, efft=BET.BUFF, desc=Gimmick.EMILY, tag="Emily_P3_EVA")
        if tt == TR.ATTACK:
            self.give_buff(BT.DOT_DMG, 0, bv[0], _round=1, desc="과부하")

    def _factive2(self, 
                  targets: Dict['Character', NUM_T],
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                  bv: Sequence[NUM_T],
                  wr: NUM_T,
                  element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BARRIER, efft=BET.BUFF))
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF))
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="회심의 일격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}


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
                t.give_buff(BT.DEF, 1, bv[0], efft=BET.DEBUFF, _round=2, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0] * 100, efft=BET.DEBUFF, _round=2, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(type_={BT.DEF, BT.EVA}, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="소환!! 데모닉 웨폰")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt in {TR.ROUND_START, TR.GET_ATTACKED, TR.ATTACK}:
            if self.hp / self.maxhp >= d('.9'):
                if len(list(filter(lambda c: c.isags, self.game.get_chars(field=self.isenemy).values()))) > 3:
                    self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[0], max_stack=1, count=1,
                                   count_trig={TR.BATTLE_CONTINUED, }, tag=G.GOLTARION, desc=G.GOLTARION)
            elif self.find_buff(tag=G.GOLTARION):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag=G.GOLTARION, force=True),
                               desc="내부 부품 손상")
        if tt == TR.ROUND_START:
            if 171 in set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values())):  # 뽀끄루
                desc = "세뇌의 파동"
                self.give_buff(BT.ATK, 1, bv[1], efft=BET.BUFF, _round=1, max_stack=1,
                               tag="Goltarion_P1_ATK", desc=desc)
                self.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, _round=1, max_stack=1,
                               tag="Goltarion_P1_CRIT", desc=desc)
                self.give_buff(BT.ACC, 0, bv[1] * 100, efft=BET.BUFF, _round=1, max_stack=1,
                               tag="Goltarion_P1_ACC", desc=desc)
                self.give_buff(BT.DEFPEN, 1, bv[1], efft=BET.BUFF, _round=1, max_stack=1,
                               tag="Goltarion_P1_DEFPEN", desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "마왕님, 조심하십시오!"
            for t in self.get_passive_targets(targets):
                if t.type_[0] == CharType.LIGHT:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, _round=1,
                                data=D.TargetProtect(self), desc=desc)
            if 127 in set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values())):  # 백토
                for t in self.get_passive_targets(targets):
                    self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(func=lambda b: b.desc == desc, limit=5),
                                   desc="네놈은 뭐냐?!")
        elif tt == TR.ATTACK:
            desc = "마왕님, 조심하십시오!"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ACTIVE_RESIST, 1, bv[0], efft=BET.BUFF, _round=2, desc=desc)
                for i in range(1, 4):
                    t.give_buff(BT.ELEMENT_RES[i], 0, bv[0] * 100, efft=BET.BUFF, _round=2, desc=desc)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        ally_ids = set(map(lambda c: c.id_, self.game.get_chars(field=self.isenemy).values()))
        momo = 123 in ally_ids
        baekto = 127 in ally_ids
        faucre = 171 in ally_ids
        if tt == TR.ROUND_START:
            desc = "마왕님의 명이라면...!"
            for t in self.get_passive_targets(targets):
                if t.id_ == 123 or t.id_ == 127:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, efft=BET.BUFF, _round=1,
                                data=D.TargetProtect(self), desc=desc)
            if faucre:
                self.give_buff(BT.DEFPEN, 1, bv[0], _round=1, desc=desc+" (뽀끄루)")
                self.give_buff(BT.ATK, 1, bv[0], _round=1, desc=desc+" (뽀끄루)")
            if momo:
                self.give_buff(BT.SKILL_RATE, 0, bv[1], _round=1, desc=desc+" (모모)")
            if baekto:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, _round=1, desc=desc+" (백토)")
        if tt in {TR.ROUND_START, TR.GET_ATTACKED, TR.ATTACK}:
            if self.hp / self.maxhp >= d('.9'):
                if momo and baekto and faucre:
                    self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[2], max_stack=1, count=1,
                                   count_trig={TR.BATTLE_CONTINUED,}, tag=G.GOLTARION, desc=G.GOLTARION)
            elif self.find_buff(tag=G.GOLTARION):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(tag=G.GOLTARION, force=True), desc="내부 부품 손상")


class Ellie(Character):
    id_ = 230
    name = "엘리"
    code = "BR_Ellie"
    group = Group.AGENCY_080
    isenemy = False
    is21squad = False

    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "테이저 니들"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                if t.get_spd() > self.get_spd():
                    t.give_buff(BT.AP, 0, bv[1], efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "방호 모드"
        self.give_buff(BT.IMMUNE_DMG, 0, 1, _round=2, efft=BET.BUFF, desc=desc)
        self.give_buff(BT.ROW_PROTECT, 0, 1, _round=2, efft=BET.BUFF, desc=desc)
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.WIDE_TAKEDMG, 1, bv[0], _round=2, efft=BET.BUFF, desc=desc)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "노블레스 오블리주"
            self.give_buff(BT.COLUMN_PROTECT, 0, 1, _round=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "편안한 티타임"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.WIDE_TAKEDMG, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)
                t.give_buff(BT.BARRIER, 0, bv[1], _round=1, efft=BET.BUFF, desc=desc)


"""
class Foo(Character):
    id_ = 
    name = 
    code = 
    group = 
    isenemy = False
    is21squad = 

    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            pass
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        pass

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass
"""
