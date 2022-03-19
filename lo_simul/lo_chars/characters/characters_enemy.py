from lo_simul.lo_char_base import *
from lo_simul.lo_equips import *


class DummyEnemy(Character):
    id_ = "DummyEnemy"
    name = "더미(적군)"
    code = "DummyEnemy"
    group = None
    isenemy = True

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


class UnderWatcher1(Character):
    id_ = "UnderWatcher_B05"
    name = "언더왓쳐"
    code = "UnderWatcher_B05"
    group = None
    isenemy = True
    isboss = True

    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "특수 합금"
        if tt == TR.ROUND_START:
            if self.find_buff(tag=G.UNDER_WATCHER_GENERATOR_B05):
                self.give_buff(BT.DEF, 1, bv[0], _round=1, tag="UWB05_P1_DEF", desc=desc)
                self.give_buff(BT.ACTIVE_RESIST, 1, bv[1], _round=1, tag="UWB05_P1_ACTIVE_RES", desc=desc)
        elif tt == TR.ATTACK:
            self.remove_buff(tag="UWB05_P1")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_B05] >= 4:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, _round=1, efft=BET.BUFF)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.DEAD:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], desc="시스템 정지", data=D.FDmgInfo(self))

    def extra_passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            desc = "해킹 (스카디)"
            self.give_buff(BT.ATK, 1, d('.-5'), _round=3, desc=desc)
            self.give_buff(BT.SPD, 1, d('.-25'), _round=3, desc=desc)


class UnderWatcherGenerator1(Character):
    id_ = "UnderWatcherGenerator_B05"
    name = "언더왓쳐 제네레이터"
    code = "UnderWatcherGenerator_B05"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            t.give_buff(BT.ATK, 1, bv[0], _round=15, max_stack=5, efft=BET.BUFF,
                        tag=G.UNDER_WATCHER_GENERATOR_B05, desc="충전")

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "에너지 실드"
        for t in targets:
            t.give_buff(BT.BARRIER, 0, bv[0], _round=9, efft=BET.BUFF, desc=desc)
            t.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.BUFF, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.hp / self.maxhp <= d('.5'):
            desc = "재충전 개시"
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=1, desc=desc)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[0], _round=1, desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.GET_HIT:
            chance = 10
            if self.find_buff(type_=BT.DEF, efft=BET.DEBUFF):
                chance = 50
            if self.judge_active(chance):
                self.give_buff(BT.INABILLITY_ACT, 0, 1, _round=2, efft=BET.DEBUFF, desc="제네레이터 쇼트")

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.DEAD:
            desc = "제네레이터 파괴"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
                t.give_buff(BT.INABILLITY_ACT, 0, 1, _round=1, desc=desc)


class UnderWatcherSensor1(Character):
    id_ = "UnderWatcherSensor_B05"
    name = "언더왓쳐 센서"
    code = "UnderWatcherSensor_B05"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, _round=3)
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, _round=3)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, _round=3, max_stack=1,
                            tag="UWS1_A1", desc="록 온")

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, _round=3)
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, _round=3)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, _round=3)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            hprate = self.hp / self.maxhp
            ts = self.get_passive_targets(targets)
            if hprate >= d('.75'):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[0], efft=BET.BUFF, _round=1)
            if hprate >= d('.5') and self.judge_active(d('.5')):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, _round=1)
            if hprate >= d('.25') and self.judge_active(d('.2')):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[2], efft=BET.BUFF, _round=1)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_B05] >= 3:
                self.give_buff(BT.ACTIVE_RATE, 0, bv[0], efft=BET.BUFF, _round=1)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass


class UnderWatcherArm1(Character):
    id_ = "UnderWatcherArm_B05"
    name = "언더왓쳐 암"
    code = "UnderWatcherArm_B05"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.type_[0] == CharType.FLY:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.HIT:
            if self.find_buff(type_=BT.ACC, efft=BET.BUFF):
                self.give_buff(BT.ACC, 0, bv[0], _round=1, efft=BET.BUFF, desc="재 조준")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_B05] >= 5:
                self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], efft=BET.BUFF, _round=1)
                self.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, _round=1)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass


class UnderWatcher2(Character):
    id_ = "UnderWatcher_TU2"
    name = "언더왓쳐"
    code = "UnderWatcher_TU2"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "포착"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc=desc)
                    t.give_buff(BT.DEF, 1, bv[1], _round=5, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="포착")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "특수 합금"
        if tt == TR.GET_ATTACKED:
            if self.find_buff(tag=G.UNDER_WATCHER_GENERATOR_TU2) and self.judge_active(90):
                self.give_buff(BT.MINIMIZE_DMG, 0, bv[0], count=1, max_stack=1, tag="UWTU2_P1", desc=desc,
                               efft=BET.BUFF, count_trig={TR.GET_HIT})

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_TU2] >= 4:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, _round=1, efft=BET.BUFF)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.DEAD:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], desc="시스템 정지", data=D.FDmgInfo(self))


class UnderWatcherGenerator2(Character):
    id_ = "UnderWatcherGenerator_TU2"
    name = "언더왓쳐 제네레이터"
    code = "UnderWatcherGenerator_TU2"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "충전"
        for t in targets:
            t.give_buff(BT.ATK, 1, bv[0], _round=99, max_stack=5, efft=BET.BUFF,
                        tag=G.UNDER_WATCHER_GENERATOR_TU2, desc=desc)
            t.give_buff(BT.IMMUNE_DMG, 0, bv[1], _round=9, efft=BET.BUFF, desc=desc)
            t.give_buff(BT.ACTIVE_RESIST, 1, bv[2], _round=1, efft=BET.BUFF, desc=desc)

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "에너지 실드"
        for t in targets:
            t.give_buff(BT.BARRIER, 0, bv[0], _round=9, efft=BET.BUFF, desc=desc)
            t.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.BUFF, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.HIT:
            desc = "에너지 코팅"
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=3, desc=desc)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[1], _round=3, desc=desc)
            self.give_buff(BT.IMMUNE_DMG, 0, bv[2], _round=3, max_stack=1, tag="UWG2_P1", desc=desc)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.GET_HIT:
            desc = "제네레이터 쇼트"
            if self.judge_active(75):
                self.give_buff(BT.AP, 0, bv[0], desc=desc)
            if self.judge_active(4):
                self.give_buff(BT.INABILLITY_ACT, 0, 1, _round=2, desc=desc)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.DEAD:
            desc = "제네레이터 파괴"
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.BUFF), desc=desc)
                t.give_buff(BT.INABILLITY_ACT, 0, 1, _round=2, desc=desc)


class UnderWatcherSensor2(Character):
    id_ = "UnderWatcherSensor_TU2"
    name = "언더왓쳐 센서"
    code = "UnderWatcherSensor_TU2"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "록 온"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, _round=9, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, _round=9, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, _round=9, desc=desc)
                t.give_buff(BT.AP, 0, bv[2], efft=BET.DEBUFF, desc=desc)
                if self.judge_active(25):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.DEBUFF, data=D.BuffCond(efft=BET.BUFF),
                                desc=desc)

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "록 온"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.MARKED, 0, 1, efft=BET.DEBUFF, _round=9, desc=desc)
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, _round=9, desc=desc)
                t.give_buff(BT.TAKEDMGINC, 1, bv[1], efft=BET.DEBUFF, _round=9, desc=desc)
                t.give_buff(BT.AP, 0, bv[2], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.DEBUFF, data=D.BuffCond(efft=BET.BUFF), desc=desc)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            hprate = self.hp / self.maxhp
            ts = self.get_passive_targets(targets)
            if hprate >= d('.75'):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[0], efft=BET.BUFF, _round=1)
            if hprate >= d('.5') and self.judge_active(d('.5')):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, _round=1)
            if hprate >= d('.25') and self.judge_active(d('.2')):
                for t in ts:
                    t.give_buff(BT.ACC, 0, bv[2], efft=BET.BUFF, _round=1)

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_TU2] >= 3:
                self.give_buff(BT.ACTIVE_RATE, 0, bv[0], efft=BET.BUFF, _round=1)
                self.give_buff(BT.EVA, 0, bv[1], efft=BET.BUFF, _round=1)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.hp / self.maxhp <= d('.5'):
                self.give_buff(BT.EVA, 0, bv[0], efft=BET.BUFF, _round=9, max_stack=3,
                               tag="UWS2_P3", desc="반응 강화")


class UnderWatcherArm2(Character):
    id_ = "UnderWatcherArm_TU2"
    name = "언더왓쳐 암"
    code = "UnderWatcherArm_TU2"
    group = None
    isenemy = True
    isboss = True

    def _active1(self,
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "포착"
        for t in targets:
            if targets[t] > 0:
                if t.find_buff(type_=BT.MARKED, efft=BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc=desc, efft=BET.DEBUFF)
                    t.give_buff(BT.DEF, 1, bv[1], _round=9, desc=desc, efft=BET.DEBUFF)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                if t.type_[0] == CharType.FLY:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.HIT:
            if self.find_buff(type_=BT.ACC, efft=BET.BUFF):
                self.give_buff(BT.ACC, 0, bv[0], _round=1, efft=BET.BUFF, desc="재 조준")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.stack_limited_buff_tags[G.UNDER_WATCHER_GENERATOR_TU2] >= 5:
                self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], efft=BET.BUFF, _round=1)
                self.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, _round=1)
                self.give_buff(BT.CRIT, 0, bv[2], efft=BET.BUFF, _round=1)

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            if self.hp / self.maxhp <= d('.5'):
                self.give_buff(BT.AP, 0, bv[0], efft=BET.BUFF, desc="긴급 요격")


class TyrantChallenge1(Character):
    id_ = "Tyrant_Challenge1"
    name = "폭군 타이런트"
    code = "Tyrant_Challenge1"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "타이런트 바이트"
        for t in targets:
            if targets[t] > 0:
                self.give_buff(BT.GIVEDMGINC, 1, bv[0], _round=0, efft=BET.DEBUFF, data=D.DmgHPInfo(type_=4), desc=desc)
                t.give_buff(BT.DEF, 1, bv[1], _round=2, max_stack=1, efft=BET.DEBUFF, tag="TyrantCh1_A1_DEF", desc=desc)
                if t.hp / t.maxhp >= d(.5):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF), desc="회심의 분쇄")
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
                            _round=2, max_stack=1, efft=BET.DEBUFF, tag="TyrantCh1_A2_FIRERES", desc="프라이멀 파이어")
                self.remove_buff(tag=G.Tyrant_Challenge_1)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            hprate = self.hp / self.maxhp
            if hprate >= d('.6'):
                self.give_buff(BT.GIMMICK, 0, 1, _round=1, tag="TyrantCh1_P1_HEAVY", desc="먹잇감 탐색 (중장형)")
            if hprate <= d('.5999'):
                self.give_buff(BT.GIMMICK, 0, 1, _round=1, tag="TyrantCh1_P1_LIGHT", desc="먹잇감 탐색 (경장형)")
            if hprate <= d('.2999'):
                self.give_buff(BT.GIMMICK, 0, 1, _round=1, tag="TyrantCh1_P1_FLY", desc="먹잇감 탐색 (기동형)")
            if len(self.game.get_chars(field=self.isenemy)) == 1:
                desc = "먹잇감 독식"
                self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, max_stack=1, count=3, count_trig={TR.GET_HIT, },
                               tag="TyrantCh1_P1_ATK", desc=desc)
                self.give_buff(BT.ACC, 0, bv[1], efft=BET.BUFF, max_stack=1, count=3, count_trig={TR.GET_HIT, },
                               tag="TyrantCh1_P1_ACC", desc=desc)
        elif tt == TR.GET_HIT:
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.PROVOKED), desc="먹잇감 집중")
            if args.element > 0:
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.GIMMICK, tag="TyrantCh1_P1"),
                               desc="먹잇감 탐색")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc1 = "원시의 본능"
        desc2 = "최후의 포효"
        if tt == TR.ROUND_START:
            self.give_buff(BT.DEF, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc1)
            self.give_buff(BT.ACTIVE_RESIST, 1, bv[1], _round=1, efft=BET.BUFF, desc=desc1)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc1)
        elif tt == TR.ATTACK:
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TARGET_PROTECT, efft=BET.BUFF), desc=desc1)
            self.give_buff(BT.MARKED, 0, 1, _round=2, efft=BET.BUFF, max_stack=1, tag="TyrantCh1_P2_MARKED", desc=desc1)
        elif tt == TR.WAVE_START:
            self.give_buff(BT.BATTLE_CONTINUATION, 1, bv[0], max_stack=1, tag="TyrantCh1_P2_B.C.", desc=desc2)
        elif tt == TR.BATTLE_CONTINUED:
            self.give_buff(BT.SPD, 1, bv[2], max_stack=1, tag="TyrantCh1_P2_SPD", desc=desc2)
            self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BATTLE_CONTINUATION))

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
           for t in self.get_passive_targets(targets, field=not self.isenemy):
               if self.judge_active(50):
                   t.give_buff(BT.INABILLITY_SKILL, 0, 1, _round=2, efft=BET.DEBUFF, desc="폭군의 포효")
        elif tt == TR.DEAD:
            for t in self.get_passive_targets(targets, field=not self.isenemy):
                t.give_buff(BT.INSTANT_DMG, 1, bv[0], data=D.FDmgInfo(self, E.FIRE), desc="최후의 포효")


class NightChickModifiedEX3(Character):
    id_ = "NightChickMEX_TU3"
    name = "강화형 칙 런처"
    code = "NightChickMEX_TU3"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="직격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="직격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.MOVE:
            desc = "기동 사격"
            self.give_buff(BT.RANGE, 0, 1, efft=BET.BUFF, _round=4, desc=desc)
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, _round=4, desc=desc)
            self.give_buff(BT.SPD, 1, bv[1], efft=BET.BUFF, _round=4, desc=desc)


class LegionEX1(Character):
    id_ = "LegionEX_TU"
    name = "정예 레기온"
    code = "LegionEX_TU"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.type_[0] == CT.FLY:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                desc = "강화 점착탄"
                t.give_buff(BT.ROOTED, 0, 1, _round=3, efft=BET.DEBUFF, desc=desc)
                if self.judge_active(75):
                    t.give_buff(BT.EVA, 0, bv[0], _round=3, efft=BET.DEBUFF, desc=desc)
                if self.judge_active(75):
                    t.give_buff(BT.SPD, 1, bv[1], _round=3, efft=BET.DEBUFF, desc=desc)
                if self.judge_active(50):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, _round=3, efft=BET.DEBUFF, desc=desc,
                                data=D.BuffCond(type_=BT.EVA, efft=BET.BUFF))
                if self.judge_active(50):
                    t.give_buff(BT.REMOVE_BUFF, 0, 1, _round=3, efft=BET.DEBUFF, desc=desc,
                                data=D.BuffCond(type_=BT.SPD, efft=BET.BUFF))
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ALLY_DEAD:
            desc = "경계 태세"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.SPD, 1, bv[0], _round=3, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.FOLLOW_ATTACK, 0, 1, _round=3, efft=BET.BUFF, desc=desc, data=D.FollowAttack(self))


class Phalangites1(Character):
    id_ = "Phalangites_TU"
    name = "팔랑스"
    code = "Phalangites_TU"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.type_[0] == CT.FLY:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="대공 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        self.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=3, efft=BET.BUFF)
        self.give_buff(BT.COLUMN_PROTECT, 0, 1, _round=3, efft=BET.BUFF)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=1, efft=BET.BUFF, desc="밀집 대형", tag="Phalagites1_P1", max_stack=1)


class NightChickSniper1(Character):
    id_ = "NightChickSP_N"
    name = "칙 스나이퍼"
    code = "NightChickSP_N"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="정밀 사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        self.give_buff(BT.EVA, 0, bv[0], _round=3, efft=BET.BUFF, tag="NightChickSP_N_A2_EVA")
        self.give_buff(BT.CRIT, 0, bv[1], _round=3, efft=BET.BUFF, tag="NightChickSP_N_A2_CRIT")
        self.give_buff(BT.TAKEDMGINC, 1, bv[2], _round=3, efft=BET.BUFF, tag="NightChickSP_N_A2_TAKEDMGINC")

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(tag="NightChickSP_N_A2"):
            self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], _round=1, efft=BET.BUFF, desc="대응 저격")


class NightChickEX3(Character):
    id_ = "NightChickEX_TU3"
    name = "강화형 나이트 칙"
    code = "NightChickEX_TU3"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.EVA, 0, bv[0], _round=2, efft=BET.DEBUFF)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.EVA, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="집중사격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.IDLE:
            self.give_buff(BT.ACC, 0, bv[0], efft=BET.BUFF, _round=3)
            self.give_buff(BT.RANGE, 0, 1, efft=BET.BUFF, _round=3)
            self.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, _round=3)


class NightChickShielder3(Character):
    id_ = "NightChickSI_TU3"
    name = "나이트 칙 실더 개"
    code = "NightChickSI_TU3"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.EVA, efft=BET.DEBUFF) and self.judge_active(50):
                t.give_buff(BT.INABILLITY_ACT, 0, 1, _round=1, efft=BET.DEBUFF)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        self.give_buff(BT.ROW_PROTECT, 0, 1, _round=3, efft=BET.BUFF)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], _round=1, efft=BET.BUFF, max_stack=1, tag="NightChickSI_TU3_P1",
                           desc="강화 방패")


class NightChickDetector3(Character):
    id_ = "NightChickDE_TU3"
    name = "나이트 칙 디텍터"
    code = "NightChickDE_TU3"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=2, efft=BET.DEBUFF)
                t.give_buff(BT.EVA, 0, bv[1], _round=2, efft=BET.DEBUFF)
                t.give_buff(BT.MARKED, 0, 1, _round=2, efft=BET.DEBUFF)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.ACC, 0, bv[0], _round=2, efft=BET.DEBUFF)
                t.give_buff(BT.AP, 0, bv[1], _round=2, efft=BET.DEBUFF)

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.GET_HIT:
            desc = "레이더 공유"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.AP, 0, 1, _round=2, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACC, 0, bv[0], _round=2, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.RANGE, 0, 1, _round=2, efft=BET.BUFF, desc=desc)
        elif tt == TR.DEAD:
            desc = "레이더 재밍"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.REMOVE_BUFF, 0, 1, efft=BET.DEBUFF, desc=desc,
                            data=D.BuffCond(type_=BT.ACC, efft=BET.BUFF))
                p.give_buff(BT.ACC, 0, -bv[0], _round=1, efft=BET.DEBUFF, desc=desc)


class EliteCenturion1(Character):
    id_ = "CenturionEX_TU"
    name = "엘리트 센츄리온"
    code = "CenturionEX_TU"
    group = None
    isenemy = True

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
                t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=0, desc="직격")
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        for t in targets:
            desc = "일제 공격 표식"
            t.give_buff(BT.TAKEDMGINC, 1, bv[0], _round=2, efft=BET.DEBUFF, desc=desc)
            t.give_buff(BT.MARKED, 0, 1, _round=2, efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ALLY_DEAD:
            desc = "역습 태세"
            self.give_buff(BT.ATK, 1, bv[0], efft=BET.BUFF, _round=2, desc=desc, tag="CenturionEX_TU_P1_ATK")
            self.give_buff(BT.CRIT, 0, bv[1], efft=BET.BUFF, _round=2, desc=desc, tag="CenturionEX_TU_P1_CRIT")
            self.give_buff(BT.COUNTER_ATTACK, 1, bv[2], efft=BET.BUFF, _round=2, desc=desc, tag="CenturionEX_TU_P1_CNT")

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START and self.find_buff(tag="CenturionEX_TU_P1"):
            desc = "부대 재 정비"
            for p in self.get_passive_targets(targets):
                p.give_buff(BT.SPD, 1, bv[0], _round=1, efft=BET.BUFF, desc=desc)
                p.give_buff(BT.ACC, 0, bv[1], _round=1, efft=BET.BUFF, desc=desc)


"""
class Foo(Character):
    id_ = ""
    name = ""
    code = ""
    group = None
    isenemy = True
    
    stats = ('')
    # hp, dhp, atk, datk, def, ddef, spd, cri, acc, ev, iceres, fireres, elecres
    skills = (
        (
            (None, 4),  # cost
            (None, '1'),  # atk rate
            (None, 0),  # acc bonus
            (None, 2),  # range
            2046, 0, 0,  # is_attack, is_ignore_protect, is_grid
            (None, 0),  # element
            ((0, True, ((0, 0, 1),)),),  # aoe / atk rate
            ('.2',)  # buff value
        ),
        (
            (None, 6),
            (None, '1.2'),
            (None, 0),
            (None, 1),
            2046, 0, 0,
            (None, 0),  # element
            ((0, True, ((0, 0, 1),)),),
            ('.2',)
        ),
        (
            ((0, True, ((0, 0),)),),
            ('2',)
        )
    )
    type_ = (0, 0)
    isags = 0
    link_bonus = BuffList()
    full_link_bonuses = [None]
    base_rarity = R.B

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


