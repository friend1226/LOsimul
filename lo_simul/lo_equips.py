from .lo_imports import *
from .lo_enum import *
from .lo_system import *

if TYPE_CHECKING:
    from lo_simul import Character


class Equip:
    EQUIP_TYPE: str
    nick: str = "???"
    name: str = "-"
    BASE_RARITY: int = R.B
    PROMOTION: int = R.SS
    owner: 'Character'

    def __init__(self, rarity: int = -1, lvl: int = 0, owner=None):
        if not isinstance(lvl, NUMBER) or lvl != lvl // 1:
            raise ValueError(f"잘못된 레벨 값 : {lvl}")
        if rarity < self.BASE_RARITY:
            self.rarity = self.BASE_RARITY
        elif rarity > self.PROMOTION:
            self.rarity = self.PROMOTION
        else:
            self.rarity = rarity
        self.lvl = lvl
        self.owner = owner
        self.buff = BuffList()
        self.init_buff()

    def init_buff(self):
        pass

    def passive(self, tt, args):
        pass

    def __repr__(self):
        return self.nick + '[' + list(R)[self.rarity].name + ']'


class Chip(Equip):
    EQUIP_TYPE = ET.CHIP


class OS(Equip):
    EQUIP_TYPE = ET.OS


class Gear(Equip):
    EQUIP_TYPE = ET.GEAR


class ATKChip(Chip):
    nick = "공칩"
    name = "출력 강화 회로"
    val = [(20, 2), (30, 3), (40, 4), (50, 5)]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ATK, 0,
                                  self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class ACCChip(Chip):
    nick = "적칩"
    name = "연산 강화 회로"
    val = [(15, d('1.5')), (20, 2), (25, d('2.5')), (35, d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ACC, 0,
                             self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class DEFChip(Chip):
    nick = "방칩"
    name = "내 충격 회로"
    val = [(16, d('3.2')), (24, d('4.4')), (30, d('6')), (36, d('7.2'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.DEF, 0,
                             self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class EVAChip(Chip):
    nick = "회칩"
    name = "반응 강화 회로"
    val = [(6, d('.3')), (8, d('.4')), (10, d('.5')), (15, d('.75'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.EVA, 0,
                             self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class CRITChip(Chip):
    nick = "치칩"
    name = "분석 회로"
    val = [(d('4'), d('0.2')), (d('5'), d('0.25')), (d('6'), d('0.3')), (d('8'), d('0.4'))]
    dval = (0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, self.val[self.rarity][0] * self.val[self.rarity][1] * self.dval[self.lvl], removable=False)
        )


class HPChip(Chip):
    nick = "체칩"
    name = "회로 내구 강화"
    val = [(80, 16), (120, 24), (160, 32), (200, 40)]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.HP, 0,
                                  self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class VaccineChip(Chip):
    nick = "백신칩"
    name = "백신 처리"
    bfval = [(5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25),
             (9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29),
             (15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35),
             (17, 19, 21, 23, 25, 27, 29, 33, 37, 43, 50)]
    chval = [(10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
             (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22),
             (15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30),
             (16, 17, 18, 19, 20, 22, 24, 28, 34, 42, 50)]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            desc = "백신 처리"
            value = self.bfval[self.rarity][self.lvl]
            self.owner.give_buff(BT.ACTIVE_RESIST, 1, value, round_=1, max_stack=1, tag=f'vaccine_{value}', desc=desc)
            if random.random() * 100 <= self.chval[self.rarity][self.lvl]:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc)


class SPDChip(Chip):
    nick = "행칩"
    name = "회로 최적화"
    val = [(d('.1'), d('.005')), (d('.12'), d('.006')), (d('.14'), d('.007')), (d('.15'), d('.0075'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.SPD, 0,
                                  self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class StandardOS(OS):
    nick = "표준OS"
    name = "표준형 전투 시스템"
    val = [(((d('.2'), d('.003')), (d('.026'), d('.003')), (d('.035'), d('.003')), (d('.047'), d('.003'))),
            ((d('4'), d('.75')), (d('5.5'), d('.75')), (d('7.75'), d('.75')), (d('10.75'), d('.75'))),
            ((5, 1), (7, 1), (10, 1), (14, 1)))]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            lvl = self.lvl
            if self.rarity == R.SS and self.lvl == 10:
                lvl += 1
            desc = "표준형 전투 OS"
            self.owner.give_buff(BT.ATK, 1, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * lvl,
                                 round_=1, efft=BET.BUFF, desc=desc)
            self.owner.give_buff(BT.DEF, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * lvl,
                                 round_=1, efft=BET.BUFF, desc=desc)
            self.owner.give_buff(BT.ACC, 0, self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * lvl,
                                 round_=1, efft=BET.BUFF, desc=desc)
            self.owner.give_buff(BT.EVA, 0, self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * lvl,
                                 round_=1, efft=BET.BUFF, desc=desc)


class OffenseOS(OS):
    nick = "돌격OS"
    name = "돌격형 전투 시스템"
    val = [((d('0.1'), d('0.105'), d('0.11'), d('0.115'), d('0.12'),
             d('0.125'), d('0.13'), d('0.135'), d('0.14'), d('0.145'), d('0.15')),
            (d('0.11'), d('0.115'), d('0.12'), d('0.125'), d('0.13'),
             d('0.135'), d('0.14'), d('0.145'), d('0.15'), d('0.155'), d('0.16')),
            (d('0.125'), d('0.13'), d('0.135'), d('0.14'), d('0.145'),
             d('0.15'), d('0.155'), d('0.16'), d('0.165'), d('0.17'), d('0.175')),
            (d('0.145'), d('0.15'), d('0.155'), d('0.16'), d('0.165'),
             d('0.17'), d('0.175'), d('0.18'), d('0.185'), d('0.19'), d('0.2'))),
           ((d('0.005'), d('0.0075'), d('0.01'), d('0.0125'), d('0.015'),
             d('0.0175'), d('0.02'), d('0.0225'), d('0.025'), d('0.0275'), d('0.03')),
            (d('0.01'), d('0.0125'), d('0.015'), d('0.0175'), d('0.02'),
             d('0.0225'), d('0.025'), d('0.0275'), d('0.03'), d('0.035'), d('0.04')),
            (d('0.0175'), d('0.02'), d('0.0225'), d('0.025'), d('0.275'),
             d('0.03'), d('0.035'), d('0.04'), d('0.045'), d('0.05'), d('0.055')),
            (d('0.0275'), d('0.03'), d('0.035'), d('0.04'), d('0.045'),
             d('0.05'), d('0.055'), d('0.06'), d('0.065'), d('0.07'), d('0.075')))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            desc = "돌격형 전투 OS"
            self.owner.give_buff(BT.ATK, 1, self.val[0][self.rarity][self.lvl], desc=desc)
            self.owner.give_buff(BT.TAKEDMGINC, 1, d('0.25'), desc=desc)
            self.owner.give_buff(BT.SPD, 0, self.val[1][self.rarity][self.lvl], desc=desc)


class DefenseOS(OS):
    nick = "방어OS"
    name = "방어형 전투 시스템"
    val = [((d('.1'), d('.01')), (d('.12'), d('.01')), (d('.15'), d('.01')), (d('.19'), d('.01'))),
           ((d('.05'), d('.005')), (d('.06'), d('.005')), (d('.075'), d('.005')), (d('.095'), d('.005')))]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            lvl = self.lvl
            if self.rarity == R.SS and lvl == 10:
                lvl += 1
            desc = "방어형 전투 OS"
            self.owner.give_buff(BT.DEF, 1,
                                 self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * lvl, round_=1, desc=desc)
            self.owner.give_buff(BT.TAKEDMGDEC, 1,
                                 self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * lvl, round_=1, desc=desc)


class CounterOS(OS):
    nick = "반격OS"
    name = "대응형 전투 시스템"
    val = [((30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60),
            (33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63),
            (45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75),
            (57, 60, 63, 66, 69, 72, 75, 80, 85, 90, 95, 100)),
           ((d('0.4'), d('0.42'), d('0.44'), d('0.46'), d('0.48'),
             d('0.5'), d('0.52'), d('0.54'), d('0.56'), d('0.58'), d('0.6')),
            (d('0.44'), d('0.46'), d('0.48'), d('0.5'), d('0.52'),
             d('0.54'), d('0.56'), d('0.58'), d('0.6'), d('0.62'), d('0.64')),
            (d('0.5'), d('0.52'), d('0.54'), d('0.56'), d('0.58'),
             d('0.6'), d('0.62'), d('0.64'), d('0.66'), d('0.68'), d('0.7')),
            (d('0.58'), d('0.6'), d('0.62'), d('0.64'), d('0.66'),
             d('0.68'), d('0.7'), d('0.72'), d('0.74'), d('0.76'), d('0.8')))]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if random.random() * 100 <= self.val[0][self.rarity][self.lvl]:
                self.owner.give_buff(BT.COUNTER_ATTACK, 1, self.val[1][self.rarity][self.lvl], round_=1,
                                     count=1, count_trig={TR.AFTER_COUNTER}, desc="대응형 OS")


class AssaultOS(OS):
    nick = "사감OS"
    name = "강습형 전투 시스템"
    val = [(d('.05'), d('.005')), (d('.06'), d('.005')), (d('.075'), d('.005')), (d('.095'), d('.005'))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            lvl = self.lvl
            if self.rarity == R.SS and lvl == 10:
                lvl += 1
            desc = "강습형 전투 OS"
            self.owner.give_buff(BT.ATK, 1, self.val[self.rarity][0] + self.val[self.rarity][1] * lvl, desc=desc)
            self.owner.give_buff(BT.RANGE, 0, -1, desc=desc)


class PrecisionOS(OS):
    nick = "행깎OS"
    name = "정밀형 전투 시스템"
    val = [((d('10'), d('1')), (d('15'), d('1.5')), (d('20'), d('2')), (d('25'), d('2.5'))),
           ((d('1'), d('.2')), (d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8'))),
           ((d('.08'), d('.005')), (d('.09'), d('.005')), (d('.105'), d('.005')), (d('.125'), d('.005')))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            desc = "정밀형 전투 OS"
            self.owner.give_buff(BT.ATK, 1, self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * self.lvl,
                                 round_=1, desc=desc)
            self.owner.give_buff(BT.SPD, 1, d('-0.08'), round_=1, desc=desc)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF), desc=desc)


class AntiFlyOS(OS):
    nick = "대기동OS"
    name = "대 기동 전투 시스템"
    val = [(d('0.1'), d('0.11'), d('0.12'), d('0.13'), d('0.14'),
            d('0.15'), d('0.16'), d('0.17'), d('0.18'), d('0.19'), d('0.2')),
           (d('0.12'), d('0.13'), d('0.14'), d('0.15'), d('0.16'),
            d('0.17'), d('0.18'), d('0.19'), d('0.2'), d('0.21'), d('0.22')),
           (d('0.15'), d('0.16'), d('0.17'), d('0.18'), d('0.19'),
            d('0.2'), d('0.21'), d('0.22'), d('0.23'), d('0.25'), d('0.27')),
           (d('0.19'), d('0.2'), d('0.21'), d('0.22'), d('0.23'),
            d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.33'), d('0.35'))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CharType.FLY], 1, self.val[self.rarity][self.lvl], desc="대 기동형 OS")


class AntiLightOS(OS):
    nick = "대경장OS"
    name = "대 경장 전투 시스템"
    val = [(d('0.1'), d('0.11'), d('0.12'), d('0.13'), d('0.14'),
            d('0.15'), d('0.16'), d('0.17'), d('0.18'), d('0.19'), d('0.2')),
           (d('0.12'), d('0.13'), d('0.14'), d('0.15'), d('0.16'),
            d('0.17'), d('0.18'), d('0.19'), d('0.2'), d('0.21'), d('0.22')),
           (d('0.15'), d('0.16'), d('0.17'), d('0.18'), d('0.19'),
            d('0.2'), d('0.21'), d('0.22'), d('0.23'), d('0.25'), d('0.27')),
           (d('0.19'), d('0.2'), d('0.21'), d('0.22'), d('0.23'),
            d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.33'), d('0.35'))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CharType.LIGHT], 1, self.val[self.rarity][self.lvl], desc="대 경장형 OS")


class AntiHeavyOS(OS):
    nick = "대중장OS"
    name = "대 중장 전투 시스템"
    val = [(d('0.1'), d('0.11'), d('0.12'), d('0.13'), d('0.14'),
            d('0.15'), d('0.16'), d('0.17'), d('0.18'), d('0.19'), d('0.2')),
           (d('0.12'), d('0.13'), d('0.14'), d('0.15'), d('0.16'),
            d('0.17'), d('0.18'), d('0.19'), d('0.2'), d('0.21'), d('0.22')),
           (d('0.15'), d('0.16'), d('0.17'), d('0.18'), d('0.19'),
            d('0.2'), d('0.21'), d('0.22'), d('0.23'), d('0.25'), d('0.27')),
           (d('0.19'), d('0.2'), d('0.21'), d('0.22'), d('0.23'),
            d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.33'), d('0.35'))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CharType.HEAVY], 1, self.val[self.rarity][self.lvl], desc="대 중장형 OS")


class EXPOS(OS):
    nick = "경험치OS"
    name = "고속 학습 시스템"
    val = [(d('.05'), d('.01')), (d('.07'), d('.01')), (d('.1'), d('.01')), (d('.14'), d('.01'))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            lvl = self.lvl
            if self.rarity == R.SS and lvl == 10:
                lvl += 1
            self.owner.give_buff(BT.EXP, 1,
                                 self.val[self.rarity][0] + self.val[self.rarity][1] * lvl, desc="고속 학습 OS")


class APpack(Gear):
    nick = "에너지팩"
    name = "보조 에너지 팩"
    val = [(d('.1'), d('.05')), (d('.2'), d('.05')), (d('.35'), d('.05')), (d('.55'), d('.05'))]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            lvl = self.lvl
            if self.rarity == R.SS and lvl == 10:
                lvl += 1
            self.owner.give_buff(BT.AP, 0,
                                 self.val[self.rarity][0] + self.val[self.rarity][1] * lvl, desc="보조 에너지 팩")


class Observation(Gear):
    nick = "관측 장비"
    name = nick
    val = [((10, 2), (15, 3), (20, 4), (30, 6)),
           ((5, 5), (15, 5), (35, 5), (55, 5))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, desc=self.name)
            if random.random() * 100 <= self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF),
                                     desc=self.name)


class SpaceArmor(Gear):
    nick = "공간 장갑"
    name = nick
    val = [((120, 24), (160, 32), (200, 60), (240, 48)),
           ((d('0.2'), d('0.22'), d('0.24'), d('0.26'), d('0.28'),
             d('0.3'), d('0.32'), d('0.35'), d('0.38'), d('0.41'), d('0.44')),
            (d('0.24'), d('0.26'), d('0.28'), d('0.30'), d('0.32'),
             d('0.35'), d('0.38'), d('0.41'), d('0.44'), d('0.47'), d('0.5')),
            (d('0.30'), d('0.32'), d('0.35'), d('0.38'), d('0.41'),
             d('0.44'), d('0.47'), d('0.5'), d('0.53'), d('0.56'), d('0.59')),
            (d('0.41'), d('0.44'), d('0.47'), d('0.5'), d('0.53'),
             d('0.56'), d('0.59'), d('0.62'), d('0.65'), d('0.68'), d('0.7'))),
           ((1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2),
            (1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2),
            (1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3),
            (2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.TAKEDMGDEC, 1,
                                 self.val[1][self.rarity][self.lvl], count=self.val[2][self.rarity][self.lvl],
                                 count_trig={TR.GET_HIT}, desc="공간 장갑")


class SubBooster(Gear):
    nick = "보조 부스터 유닛"
    name = nick
    val = [((d('8'), d('8.4'), d('8.8'), d('9.2'), d('9.6'),
             d('10'), d('10.4'), d('10.8'), d('11.2'), d('11.6'), d('12')),
            (d('10'), d('10.5'), d('11'), d('11.5'), d('12'),
             d('12.5'), d('13'), d('13.5'), d('14'), d('14.5'), d('15')),
            (d('12'), d('12.6'), d('13.2'), d('13.8'), d('14.4'),
             d('15'), d('15.6'), d('16.2'), d('16.8'), d('18'), d('20')),
            (d('15'), d('15.75'), d('16.5'), d('17.25'), d('18'),
             d('18.75'), d('19.5'), d('20.25'), d('21'), d('23'), d('25'))),
           ((35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65),
            (41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71),
            (50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80),
            (62, 65, 68, 71, 74, 77, 80, 85, 90, 95, 100))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.EVA, 0, self.val[0][self.rarity][self.lvl], removable=False))

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if random.random() * 100 <= self.val[1][self.rarity][self.lvl]:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.EVA, efft=BET.DEBUFF),
                                     desc="보조 부스터")


class UltraScope(Equip):
    nick = "스코프"
    name = "초정밀 조준기"
    val = [((d('4'), d('.4')), (d('6'), d('.6')), (d('8'), d('.8')), (d('10'), d('1'))),
           ((d('8'), d('.8')), (d('12'), d('1.2')), (d('16'), d('1.6')), (d('25'), d('2.5'))),
           ((35, 38, 41, 44, 47, 50, 53, 56, 59, 62, 65),
            (41, 44, 47, 50, 53, 56, 59, 62, 65, 68, 71),
            (50, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80),
            (62, 65, 68, 71, 74, 77, 80, 85, 90, 95, 100))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.ACC, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if random.random() * 100 <= self.val[2][self.rarity][self.lvl]:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF),
                                     desc=self.name)


class ArmorPierce(Gear):
    nick = "송곳"
    name = "대 장갑 장비"
    val = [((d('2'), d('.4')), (d('3'), d('.5')), (d('4'), d('.8')), (d('5'), d('1'))),
           ((d('0.1'), d('0.115'), d('0.13'), d('0.145'), d('0.16'),
             d('0.175'), d('0.19'), d('0.205'), d('0.22'), d('0.235'), d('0.25')),
            (d('0.13'), d('0.145'), d('0.16'), d('0.175'), d('0.19'),
             d('0.205'), d('0.22'), d('0.235'), d('0.25'), d('0.265'), d('0.28')),
            (d('0.175'), d('0.19'), d('0.205'), d('0.22'), d('0.235'),
             d('0.25'), d('0.265'), d('0.28'), d('0.295'), d('0.31'), d('0.325')),
            (d('0.235'), d('0.25'), d('0.265'), d('0.28'), d('0.295'),
             d('0.31'), d('0.325'), d('0.34'), d('0.36'), d('0.38'), d('0.4')))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 1, self.val[1][self.rarity][self.lvl], desc=self.name)


class EnergyConverter(Gear):
    nick = "에너지 전환기"
    name = nick
    val = [(d('0.03'), d('0.035'), d('0.04'), d('0.045'), d('0.05'),
            d('0.055'), d('0.06'), d('0.065'), d('0.07'), d('0.075'), d('0.08')),
           (d('0.045'), d('0.05'), d('0.055'), d('0.06'), d('0.065'),
            d('0.07'), d('0.075'), d('0.08'), d('0.085'), d('0.09'), d('0.095')),
           (d('0.06'), d('0.065'), d('0.07'), d('0.075'), d('0.08'),
            d('0.085'), d('0.09'), d('0.095'), d('0.1'), d('0.12'), d('0.14')),
           (d('0.075'), d('0.08'), d('0.085'), d('0.09'), d('0.095'),
            d('0.1'), d('0.12'), d('0.14'), d('0.16'), d('0.18'), d('0.2'))]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if self.owner.find_buff(type_=BT.BARRIER, efft=BET.BUFF):
                desc = "에너지 전환"
                self.owner.give_buff(BT.ATK, 1, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl,
                                     round_=1, desc=desc)
                self.owner.give_buff(BT.SPD, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl,
                                     round_=1, desc=desc)
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.BARRIER, efft=BET.BUFF), desc=desc)


class Barrier(Gear):
    nick = "방어막"
    name = "방어 역장"
    val = [(60, 75, 90, 105, 120, 135, 150, 165, 180, 200, 210),
           (90, 105, 120, 135, 150, 165, 180, 200, 210, 225, 240),
           (135, 150, 165, 180, 200, 210, 225, 240, 260, 280, 300),
           (200, 210, 225, 240, 260, 280, 300, 325, 350, 375, 400)]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.BARRIER, 0, self.val[self.rarity][self.lvl], round_=1, desc="방어막")


class ReconDrone(Gear):
    nick = "드론"
    name = "소형 정찰 드론"
    val = [(((d('10'), d('1')), (d('15'), d('1.5')), (d('20'), d('2')), (d('25'), d('2.5'))),
            ((d('.06'), d('.006')), (d('.08'), d('.008')), (d('.1'), d('.01')), (d('.15'), d('.015'))))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.SPD, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.RACON, 0, 1, removable=False, desc="정찰 드론")


class ExamKit(Gear):
    nick = "중화기용 조준기"
    name = nick
    val = [((d('8'), d('.8')), (d('12'), d('1.2')), (d('16'), d('1.6')), (d('20'), d('2'))),
           ((d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8')), (d('5'), d('1'))),
           ((30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60),
            (36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 67),
            (42, 45, 48, 51, 54, 57, 60, 63, 67, 71, 75),
            (57, 60, 63, 67, 71, 75, 80, 85, 90, 95, 100))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ATTACK:
            if random.random() * 100 <= self.val[2][self.rarity][self.lvl]:
                self.owner.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, count=1, count_trig={TR.AFTER_SKILL},
                                     desc="방어막 중화")


class AdvRadar(Gear):
    nick = "망원 조준 장치"
    name = nick
    val = [((d('0.01'), d('0.012'), d('0.014'), d('0.016'), d('0.018'),
             d('0.02'), d('0.022'), d('0.024'), d('0.026'), d('0.028'), d('0.03')),
            (d('0.016'), d('0.018'), d('0.02'), d('0.022'), d('0.024'),
             d('0.026'), d('0.028'), d('0.03'), d('0.032'), d('0.034'), d('0.036')),
            (d('0.022'), d('0.024'), d('0.026'), d('0.028'), d('0.03'),
             d('0.032'), d('0.034'), d('0.036'), d('0.038'), d('0.04'), d('0.042')),
            (d('0.028'), d('0.03'), d('0.032'), d('0.034'), d('0.036'),
             d('0.038'), d('0.04'), d('0.042'), d('0.044'), d('0.046'), d('0.05'))),
           ((d('25'), d('26.5'), d('28'), d('29.5'), d('31'),
             d('32.5'), d('34'), d('35.5'), d('37'), d('38.5'), d('40')),
            (d('29.5'), d('31'), d('32.5'), d('34'), d('35.5'),
             d('37'), d('38.5'), d('40'), d('41.5'), d('43'), d('45')),
            (d('34'), d('35.5'), d('37'), d('38.5'), d('40'),
             d('41.5'), d('43'), d('45'), d('47'), d('49'), d('51')),
            (d('38.5'), d('40'), d('41.5'), d('43'), d('45'),
             d('47'), d('49'), d('51'), d('53'), d('55'), d('60'))),
           ((d('5'), d('5.5'), d('6'), d('6.5'), d('7'),
             d('7.5'), d('8'), d('8.5'), d('9'), d('9.5'), d('10')),
            (d('6.5'), d('7'), d('7.5'), d('8'), d('8.5'),
             d('9'), d('9.5'), d('10'), d('11'), d('12'), d('13')),
            (d('8'), d('8.5'), d('9'), d('9.5'), d('10'),
             d('11'), d('12'), d('13'), d('14'), d('16'), d('18')),
            (d('9.5'), d('10'), d('11'), d('12'), d('13'),
             d('14'), d('16'), d('18'), d('20'), d('22'), d('24')))]

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            if self.owner.getposy() == 0:
                desc = "망원 조준 장치"
                self.owner.give_buff(BT.ATK, 1, self.val[0][self.rarity][self.lvl], round_=1, desc=desc)
                self.owner.give_buff(BT.ACC, 0, self.val[1][self.rarity][self.lvl], round_=1, desc=desc)
                self.owner.give_buff(BT.CRIT, 0, self.val[2][self.rarity][self.lvl], round_=1, desc=desc)


class Stimulant(Gear):
    nick = "전투 자극제"
    name = nick
    val = [((d('.025'), d('.005')), (d('.035'), d('.005')), (d('.05'), d('.005')), (d('.07'), d('.005'))),
           ((10, 15), (40, 15), (85, 15), (145, 15))]

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SPD, 0,
                                 self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, desc=self.name)
            hpv = self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl
            if self.rarity == R.SS and self.lvl == 10:
                hpv += 5
            self.owner.give_buff(BT.BATTLE_CONTINUATION, 0, hpv, desc=self.name)


class Hologram(Gear):
    nick = "홀로그램"
    name = "더미 홀로그램"
    val = [(d('5'), d('.5')), (d('7'), d('.7')), (d('9'), d('.9')), (d('12'), d('.12'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            c = 1
            if self.rarity == R.SS and self.lvl == 10:
                c += 1
            self.owner.give_buff(BT.MINIMIZE_DMG, 0, 9999999, count=c, desc=self.name)


class SpecialRifleBullet(Gear):
    BASE_RARITY = R.SS
    nick = "콘챠전장"
    name = "특수 코팅 라이플탄"
    val = [(d('30'), d('31.5'), d('33'), d('36'), d('40.5'),
            d('46.5'), d('51'), d('60'), d('72'), d('87'), d('105')),
           (d('5'), d('5.25'), d('5.5'), d('6'), d('6.75'),
            d('7.75'), d('8.5'), d('10'), d('12'), d('14.5'), d('17.5'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ATK, 0, self.val[0][self.lvl], removable=False),
                             Buff(BT.CRIT, 0, self.val[1][self.lvl], removable=False))

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 1, d('0.25') + d('0.05') * min(self.lvl, 1), desc=self.name)


class AMRAAMPod(Gear):
    BASE_RARITY = R.SS
    nick = "그리폰전장"
    name = "확장 AMRAAM 포드"
    val = [[d('0.15'), d('0.15'), d('0.16'), d('0.17'), d('0.18'),
            d('0.19'), d('0.2'), d('0.21'), d('0.22'), d('0.23'), d('0.25')],
           [d('0.15'), d('0.15'), d('0.17'), d('0.19'), d('0.21'),
            d('0.23'), d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.33')]]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ATK, 0, d('50') + d('5') * self.lvl, removable=False),
                             Buff(BT.ACC, 0, d('20') + d('4') * self.lvl, removable=False),
                             Buff(BT.CRIT, 0, d('5') + d('0.5') * self.lvl, removable=False))

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            desc = "AMRAAM"
            self.owner.give_buff(BT.ANTI_OS[CharType.FLY], 1, self.val[0][self.lvl], desc=desc)
            self.owner.give_buff(BT.DEFPEN, 1, self.val[1][self.lvl], desc=desc)
            if self.lvl == 10:
                self.owner.give_buff(BT.RANGE, 0, 1, desc=desc)


class SuperAlloyArmor(Gear):
    BASE_RARITY = R.SS
    nick = "요안나전장"
    name = "초합금 플레이트 아머"
    val = [15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('25') + d('2.5') * self.lvl, removable=False),
            Buff(BT.ELEMENT_RES[E.ICE], 0, d('25') + d('2.5') * self.lvl, removable=False),
            Buff(BT.ELEMENT_RES[E.ELEC], 0, d('25') + d('2.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.ACTIVE_RESIST, 1, d('0.15') + d('0.02') * self.lvl, round_=1, desc=self.name)
            if random.random() * 100 <= self.val[self.lvl]:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=self.name)


class DragonSlayer(Gear):
    BASE_RARITY = R.SS
    nick = "좌우좌전장"
    name = "용살자의 징표"
    val = [(d('27'), d('28.35'), d('29.7'), d('32.4'), d('36.45'),
            d('41.85'), d('45.9'), d('54'), d('64.8'), d('78.3'), d('94.5')),
           (d('10'), d('10'), d('11'), d('12'), d('13'),
            d('14'), d('15'), d('16'), d('17'), d('18'), d('20'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.CRIT, 0, d('10') + d('2') * self.lvl, removable=False),
                             Buff(BT.EVA, 0, self.val[0][self.lvl], removable=False))

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ACTIVE_RATE, 0, self.val[1][self.lvl], desc=self.name)


class FireSpray(Gear):
    nick = "화깡"
    name = "내열 코팅"
    val = [(d('20'), d('2')), (d('25'), d('2.5')), (d('30'), d('3')), (d('35'), d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, self.val[self.rarity][0] * self.val[self.rarity][1] * self.lvl,
                 removable=False, tag=self.name)
        )


class IceSpray(Gear):
    nick = "냉깡"
    name = "내한 코팅"
    val = [(d('20'), d('2')), (d('25'), d('2.5')), (d('30'), d('3')), (d('35'), d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl,
                 removable=False, tag=self.name)
        )


class ElectricSpray(Gear):
    nick = "전깡"
    name = "내전 코팅"
    val = [(d('20'), d('2')), (d('25'), d('2.5')), (d('30'), d('3')), (d('35'), d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ELEC], 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl,
                 removable=False, tag=self.name)
        )


class CounterTerrorismArmor(Gear):
    BASE_RARITY = R.SS
    nick = "불가사리전장"
    name = "테러진압용 외장아머"
    val = [(d('50'), d('52.5'), d('55'), d('60'), d('67.5'), 
            d('77.5'), d('85'), d('100'), d('120'), d('145'), d('175')), 
           (d('0.15'), d('0.15'), d('0.17'), d('0.19'), d('0.21'),
            d('0.23'), d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.35'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, d('200') + d('40') * self.lvl, removable=False),
            Buff(BT.DEF, 0, self.val[0][self.lvl], removable=False),
            Buff(BT.SPD, 0, d('0.12') + d('0.012') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            desc = "대 태러 외장 장갑"
            self.owner.give_buff(BT.ELEMENT_RES[E.FIRE], 0, self.val[1][self.lvl], desc=desc)
            self.owner.give_buff(BT.ELEMENT_RES[E.ICE], 0, self.val[1][self.lvl], desc=desc)
            self.owner.give_buff(BT.ELEMENT_RES[E.ELEC], 0, self.val[1][self.lvl], desc=desc)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, self.val[1][self.lvl]+d('.1'), desc=desc)
            self.owner.give_buff(BT.ROW_PROTECT, 0, 1, desc=desc)


class DUBullet(Gear):
    BASE_RARITY = R.SS
    nick = "네레이드전장"
    name = "40mm DU탄"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('60') + d('6') * self.lvl, removable=False),
            Buff(BT.CRIT, 0, d('10') + d('1') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('10') + d('1') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 1, d('0.25') + d('0.05') * min(self.lvl, 1), desc="열화 우라늄탄")


class ATFLIR(Chip):
    BASE_RARITY = R.SS
    nick = "실피드전장"
    name = "ATFLIR 강화 회로"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('40') + d('4') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('20') + d('2') * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('12') + d('0.6') * self.lvl, removable=False)
        )


class CM67SpaceBooster(Gear):
    BASE_RARITY = R.SS
    nick = "스팅어전장"
    name = "우주용 확장 부스터"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('47.5') + d('4.75') * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('70') + d('3.5') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.1') + d('.01') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            desc = "우주용 부스터"
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.EVA, efft=BET.DEBUFF), desc=desc)
            self.owner.give_buff(BT.CRIT, 0, d('5') + d('1') * self.lvl, round_=1, desc=desc)


class MG80ModKit(Gear):
    BASE_RARITY = R.SS
    nick = "님프전장"
    name = "MG80용 개조 키트"
    dval = [0, 1, 2, 4, 7, 11, 14, 20, 28, 40, 60]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('45') + d('4.5') * self.lvl + (d('.5') if self.lvl == 9 else 0), removable=False),
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[self.lvl], removable=False),
            Buff(BT.SPD, 0, d('.15') + d('.0075') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CT.LIGHT], 1,
                                 d('.15') + d('.01') * self.lvl - (d('.01') if 0 < self.lvl < 10 else 0), desc="LM탄")


class Steroid(Gear):
    BASE_RARITY = R.SS
    nick = "스카디전장"
    name = "수상한 보조제"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.SPD, 0, d('.12') + d('.012') * self.lvl, removable=False),
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CT.HEAVY], 1, d('.15') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.RANGE, 0, 1, desc=self.name)


class SK14ModKit(Gear):
    BASE_RARITY = R.SS
    nick = "미호전장"
    name = "SK-14 P.C.C"
    dval = [0, 1, 2, 4, 7, 11, 14, 20, 28, 40, 60]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, (d(125) if self.lvl == 10 else (d('35') + d('1.75') * self.dval[self.lvl])),
                 removable=False),
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[self.lvl], removable=False),
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF), desc=self.name)


class SowanLunchBox(Gear):
    BASE_RARITY = R.SS
    nick = "도시락"
    name = "소완제 수제 도시락"

    def passive(self, tt, args):
        if tt == TR.WAVE_START and not self.owner.isags:
            desc = "아니 이 맛은...!"
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.005') * self.lvl, tag='LunchBox', desc=desc)
            self.owner.give_buff(BT.SPD, 1, d('.05') + d('.005') * self.lvl, tag='LunchBox', desc=desc)


class Bombard(Gear):
    BASE_RARITY = R.SS
    nick = "전략 폭격 장비"
    name = nick

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, d(5) + self.lvl, removable=False),
            Buff(BT.EVA, 0, d(-75), removable=False),
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START and not self.owner.isags:
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.DEFPEN, 1, d('.15') + d('.03') * self.lvl, desc=self.name)


class SpATKChip(Chip):
    nick = "적깎칩"
    name = "출력 증폭 회로"
    val = [(40, 4), (45, d('4.5')), (55, d('5.5')), (65, d('6.5')), (-30, -3)]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.ACC, 0, self.val[-1][0] + self.val[-1][1] * self.lvl, removable=False),
        )


class EyesOfBeholderD(Gear):
    BASE_RARITY = R.SS
    nick = "마리전장"
    name = "주사위의 눈 D형 OS"
    dval = [0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, d('125') + d('12.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            desc = "E.O.B D형 OS"
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('0.15') + d('0.01') * self.dval[self.lvl], desc=desc)
            self.owner.give_buff(BT.ACTIVE_RESIST, 1, d('20') + d('1.5') * self.lvl, desc=desc)
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, d('.5') + d('.05') * self.lvl, desc=desc)


class ATKCRIChip(Chip):
    nick = "공치칩"
    name = "출력 안정 회로"
    val = [[(12, d('2.4')), (16, d('3.2')), (22, d('4.4')), (28, d('5.6'))],
           [(3, d('.3')), (4, d('.4')), (5, d('.5')), (6, d('.6'))]]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('-.1'), removable=False),
        )


class ExpChip(Chip):
    nick = "경험칩"
    name = "전투 기록 회로"
    val = [[2, d('.2'), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)],
           [d('2.6'), d('.2'), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11)],
           [d('3.2'), d('.2'), (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14)],
           [d('3.8'), d('.2'), (0, 1, 2, 3, 5, 7, 9, 12, 15, 18, 21)]]

    def init_buff(self):
        val = self.val[self.rarity][0] + self.val[self.rarity][1] * self.val[self.rarity][2][self.lvl]
        self.buff = BuffList(
            Buff(BT.EXP, 1, val, removable=False, desc="전투 기록", tag=f"ExpChip_{val}", max_stack=3)
        )


class AquaModule(Gear):
    nick = "아쿠아 모듈"
    name = nick
    val = [[(d('10'), d('1')), (d('15'), d('1.5')), (d('20'), d('2')), (d('25'), d('2.5'))],
           [(d('.05'), d('.005')), (d('.065'), d('0.005')), (d('.08'), d('.005')), (d('.095'), d('.005'))]]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl,
                 removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START and self.owner.find_buff(tag=G.FLOOD):
            v = self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl
            if self.rarity == R.SS and self.lvl == 10:
                v += self.val[1][self.rarity][1]
            self.owner.give_buff(BT.ATK, 1, v, round_=1, desc=self.name)
            self.owner.give_buff(BT.DEF, 1, v, round_=1, desc=self.name)
            self.owner.give_buff(BT.ACC, 1, v * 100, round_=1, desc=self.name)
            self.owner.give_buff(BT.EVA, 1, v * 100, round_=1, desc=self.name)
            self.owner.give_buff(BT.SPD, 1, v, round_=1, desc=self.name)


class Overclock(Gear):
    nick = "글카"
    name = "출력 제한 해제 장치"
    val = [[(d('.15'), d('.005')), (d('.165'), d('.005')), (d('.18'), d('.005')), (d('.195'), d('.005'))],
           [(d('.05'), d('.005')), (d('.065'), d('.005')), (d('.08'), d('.005')), (d('.095'), d('.005'))],
           [(d('-19.5'), d('-.5')), (d('-18'), d('-.5')), (d('-16.5'), d('-.5')), (d('-15'), d('-.5'))]]

    def passive(self, tt, args):
        if tt == TR.WAVE_START and self.owner.isags:
            desc = "출력 제한 해제"
            s1 = self.rarity == R.B and self.lvl == 0
            s2 = self.rarity == R.SS and self.lvl == 10
            self.owner.give_buff(BT.ATK, 1,
                                 self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * (self.lvl + s2), desc=desc)
            self.owner.give_buff(BT.SPD, 1,
                                 self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * (self.lvl + s2), desc=desc)
            self.owner.give_buff(BT.ACC, 0,
                                 self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * (self.lvl - s1), desc=desc)


class HManeuver(OS):
    nick = "고기동OS"
    name = "고기동 메뉴버 시스템"
    val = [[(d('5'), d('1')), (d('8'), d('1.6')), (d('10'), d('2')), (d('15'), d('3'))],
           [(d('4'), d('0.8')), (d('6'), d('1.2')), (d('8'), d('1.6')), (d('10'), d('2'))],
           [(d('.1'), d('.02')), (d('.16'), d('.02')), (d('.22'), d('.02')), (d('.28'), d('.02'))]]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.EVA, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1], removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START and self.owner.type_ == (CT.LIGHT, CR.DEFENDER):
            desc = "고기동 메뉴버"
            self.owner.give_buff(
                BT.TAKEDMGDEC, 1,
                self.val[2][self.rarity][0] + self.val[2][self.rarity][1] *
                (self.lvl + (self.rarity == R.SS and self.lvl == 10)),
                desc=desc, max_stack=1, tag=desc, count=1, count_trig={TR.GET_HIT})


class EXAM(OS):
    nick = "정찰OS"
    name = "전황 분석 시스템"
    val = [[(d('.05'), d('.005')), (d('.065'), d('.005')), (d('.08'), d('.005')), (d('.095'), d('.005'))],
           [(d('2'), d('.4')), (d('3.2'), d('.4')), (d('4.4'), d('.4')), (d('5.6'), d('.4'))],
           [(d('10'), d('.5')), (d('11.5'), d('.5')), (d('13'), d('.5')), (d('14.5'), d('.5'))],
           [(d('.01'), d('.002')), (d('.016'), d('.002')), (d('.022'), d('.002')), (d('.028'), d('.002'))]]

    def passive(self, tt, args):
        if tt == TR.WAVE_START and self.owner.find_buff(type_=BT.RACON):
            desc = "전황 분석 OS"
            lvl = self.lvl + (self.rarity == R.SS and self.lvl == 10)
            self.owner.give_buff(BT.ATK, 1, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * lvl, desc=desc)
            self.owner.give_buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * lvl, desc=desc)
            self.owner.give_buff(BT.ACC, 0, self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * lvl, desc=desc)
            self.owner.give_buff(BT.EVA, 0, self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * lvl, desc=desc)
            self.owner.give_buff(BT.SPD, 1, self.val[3][self.rarity][0] + self.val[3][self.rarity][1] * lvl, desc=desc)


class IcePack(Gear):
    BASE_RARITY = R.SS
    nick = "냉각 팩"
    name = nick

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('25') + d('2.5') * self.lvl, removable=False),
        )

    def passive(self, tt, args):
        if tt == TR.ATTACK:
            self.owner.give_buff(BT.AP, 0, d('.5') + d('.05') * self.lvl, desc=self.name)


class SunCream(Gear):
    BASE_RARITY = R.SS
    nick = "선 크림"
    name = nick

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('25') + d('2.5') * self.lvl, removable=False),
        )

    def passive(self, tt, args):
        if tt == TR.GET_HIT and args == E.FIRE:
            self.owner.give_buff(BT.AP, 0, d('.5') + d('.05') * self.lvl, desc=self.name)


class ASN6G(Gear):
    BASE_RARITY = R.SS
    nick = "운디네전장"
    name = "ASN-6G"
    dval = [(0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50), (0, 1, 2, 4, 7, 11, 14, 20, 30, 40, 60)]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('50') + d('2.5') * self.dval[0][self.lvl], removable=False),
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[1][self.lvl], removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 1, d('.15') + d('.03') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.ANTI_OS[CT.HEAVY], 1, d('.15') + d('.01') * self.lvl, desc=self.name)


class Interceptor(Gear):
    BASE_RARITY = R.SS
    nick = "개량형 관측 장비"
    name = nick

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, d('15') + d('3') * self.lvl, removable=False),
            Buff(BT.CRIT, 0, d('5') + d('1') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            desc = "정밀형 관측 장비"
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, desc=desc)
            if random.random() * 100 <= 50 + 5 * self.lvl:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF), desc=desc)
            if random.random() * 100 <= 50 + 5 * self.lvl:
                self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF), desc=desc)


class ATKSPDChip(Chip):
    BASE_RARITY = R.SS
    nick = "공행칩"
    name = "개량형 출력 강화 회로"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.05') + d('.005') * self.lvl, removable=False)
        )


class LightWeight(Chip):
    nick = "경량칩"
    name = "경량화 회로"
    val = [((d('10'), d('1')), (d('12'), d('1.2')), (d('15'), d('1.5')), (d('20'), d('2'))),
           ((d('3'), d('.3')), (d('5'), d('.5')), (d('6'), d('.6')), (d('9'), d('.9'))),
           ((d('.01'), d('.002')), (d('.02'), d('.004')), (d('.03'), d('.006')), (d('.04'), d('.008')))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] * self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.EVA, 0, self.val[1][self.rarity][0] * self.val[1][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.SPD, 0, self.val[2][self.rarity][0] * self.val[2][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, d('-.08'), round_=1, removable=False, max_stack=1,
                                 tag='LightWeight', desc="무장 경량칩")


class GrandCruChocolate(Gear):
    BASE_RARITY = R.SS
    nick = "초코"
    name = "그랑크뤼 초콜릿"

    val = [d('.5'), d('.6'), d('.7'), d('.8'), d('.9'),
           d('1'), d('1.2'), d('1.4'), d('1.6'), d('1.8'), d('2')]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('50') + d('5') * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('5') + d('1') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.AP, 0, self.val[self.lvl], desc="녹아내릴 듯한 달콤함")


class MiniPerralut(Gear):
    BASE_RARITY = R.SS
    nick = "페로"
    name = "미니 페로"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, d('7') + d('1.4') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('15') + d('1.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ATTACK:
            self.owner.give_buff(BT.AP, 0, d('0.05') * (1 + self.lvl), desc="애옹? 애옹!")


class MiniLilith(Gear):
    BASE_RARITY = R.SS
    nick = "리리스"
    name = "미니 블랙 리리스"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('15') + d('1.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.TAKEDMGDEC, 1, min(d('.005'), d('.01') * self.lvl), desc="착한 리리스가 가욧!")


class EnhancedCombatOS(OS):
    BASE_RARITY = R.SS
    nick = "영전OS"
    name = "개량형 전투 시스템"
    val = [d('.005'), d('.0075'), d('.01'), d('.015'), d('.02'),
           d('.025'), d('.03'), d('.035'), d('.04'), d('.045'), d('.05')]

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.ATK, 1, d('.04') + d('.008') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.05') + d('.005') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.EVA, 0, d('10') + d('2') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.SPD, 1, self.val[self.lvl], round_=1, desc=self.name)


class VerminEliminator(Gear):
    BASE_RARITY = R.SS
    nick = "리제전장"
    name = "해충 파쇄기"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('60') + d('6') * self.lvl, removable=False),
            Buff(BT.CRIT, 0, d('5') + d('1') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('10') + d('2') * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.DEFPEN, 1, d('0.25') + d('0.04') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ATK, efft=BET.DEBUFF), desc=self.name)


class QMObserver(Equip):
    BASE_RARITY = R.SS
    nick = "레오나전장"
    name = "전투 관측 프레임"

    val = [(d('20'), d('21'), d('22'), d('24'), d('27'),
            d('31'), d('34'), d('40'), d('48'), d('58'), d('70')),
           (d('12'), d('12.6'), d('13.2'), d('14.4'), d('16.2'),
            d('18.6'), d('20.4'), d('24'), d('28.8'), d('34.8'), d('42')),
           ]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.lvl], removable=False),
            Buff(BT.EVA, 0, self.val[1][self.lvl], removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.RACON, 0, 1, desc=self.name)


class ATKChipBETA(Chip):
    nick = "공베칩"
    name = "출력 강화 회로 베타"
    val = [(d('24'), d('2.4')), (d('36'), d('3.6')), (d('48'), d('4.8')), (d('60'), d('6'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('-6') + d('-.6') * self.lvl, removable=False)
        )


class ACCChipBETA(Chip):
    nick = "적베칩"
    name = "연산 강화 회로 베타"
    val = [(d('18'), d('1.8')), (d('24'), d('2.4')), (d('30'), d('3')), (d('42'), d('4.2'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.DEF, 0, d('-27') + d('-2.7') * self.lvl, removable=False)
        )


class DEFChipBETA(Chip):
    nick = "방베칩"
    name = "내 충격 강화 회로 베타"
    val = [(d('30'), d('3')), (d('43'), d('4.3')), (d('54'), d('5.4')), (d('65'), d('6.5'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.DEF, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.ATK, 0, d('-25') + d('-2.5') * self.lvl, removable=False)
        )


class EVAChipBETA(Chip):
    nick = "회베칩"
    name = "반응 강화 회로 베타"
    val = [(d('72'), d('.36')), (d('9.6'), d('.48')), (d('12'), d('.6')), (d('18'), d('.9'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.ATK, 0, d('-25') + d('-2.5') * self.lvl, removable=False)
        )


class CRITChipBETA(Chip):
    nick = "치베칩"
    name = "분석 회로 베타"
    val = [((d('4.8'), d('.24')), (d('6'), d('.3')), (d('7.2'), d('.36')), (d('9.6'), d('.48'))),
           (0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50)]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, 
                 self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.val[1][self.lvl], removable=False), 
            Buff(BT.DEF, 0, d('-27') + d('-2.7') * self.lvl, removable=False)
        )


class HPChipBETA(Chip):
    nick = "체베칩"
    name = "회로 내구 강화 베타"
    val = [(d('96'), d('19.2')), (d('144'), d('28.8')), (d('192'), d('38.6')), (d('240'), d('48'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.ATK, 0, d('-25') + d('-2.5') * self.lvl, removable=False)
        )


class SPDChipBETA(Chip):
    nick = "행베칩"
    name = "회로 최적화 베타"
    val = [(d('.12'), d('.006')), (d('.144'), d('.0072')), (d('.168'), d('.0084')), (d('.18'), d('.009'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.SPD, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('-6') + d('-.6') * self.lvl, removable=False)
        )


class AWThruster(Gear):
    nick = "공중화기용 추력기"
    name = nick
    val = [((d('8'), d('.8')), (d('12'), d('1.2')), (d('16'), d('1.6')), (d('20'), d('2'))),
           ((d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8')), (d('5'), d('1'))),
           ((d('.07'), d('.02')), (d('.11'), d('.02')), (d('.15'), d('.02')), (d('.25'), d('.02')))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SKILL_RATE, 0,
                                 self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * self.lvl, desc=self.name)


class EquipPools:
    CHIP_NAME: Dict[str, Type[Chip]]
    OS_NAME: Dict[str, Type[OS]]
    GEAR_NAME: Dict[str, Type[Gear]]
    ALL_NAME_LIST: List[Dict[str, Type[Equip]]]
    ALL_NAME: Dict[str, Type[Equip]]

    @classmethod
    def update(cls):
        cls.CHIP_NAME = {}
        for klass in Chip.__subclasses__():
            cls.CHIP_NAME[klass.nick] = klass
        cls.OS_NAME = {}
        for klass in OS.__subclasses__():
            cls.OS_NAME[klass.nick] = klass
        cls.GEAR_NAME = {}
        for klass in Gear.__subclasses__():
            cls.GEAR_NAME[klass.nick] = klass
        cls.ALL_NAME_LIST = [cls.CHIP_NAME, cls.OS_NAME, cls.GEAR_NAME]
        cls.ALL_NAME = {**cls.CHIP_NAME, **cls.OS_NAME, **cls.GEAR_NAME}


EquipPools.update()
