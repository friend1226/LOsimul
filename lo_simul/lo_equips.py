from .lo_imports import *
from .lo_enum import *
from .lo_system import *

if TYPE_CHECKING:
    from lo_simul import Character


class EquipPools:
    CHIP_NAME: Dict[str, Type['Chip']] = {}
    OS_NAME: Dict[str, Type['OS']] = {}
    GEAR_NAME: Dict[str, Type['Gear']] = {}
    ALL_NAME_LIST: List[Dict[str, Type['Equip']]] = [CHIP_NAME, OS_NAME, GEAR_NAME]
    ALL_NAME: Dict[str, Type['Equip']] = {}


EQUIP_TYPE_CODE = ['Chip', 'System', 'Sub']
META_CLASS_SET = {"Chip", "OS", "Gear"}


class Equip:
    EQUIP_TYPE: int
    nick: str = "???"
    name: str = "-"
    code: str = "None"
    BASE_RARITY: R = R.B
    PROMOTION: R = R.SS
    owner: 'Character'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if cls.__name__ in META_CLASS_SET:
            return
        EquipPools.ALL_NAME_LIST[cls.EQUIP_TYPE][cls.nick] = cls
        EquipPools.ALL_NAME[cls.nick] = cls

    def __init__(self, rarity: int = -1, lvl: int = 0, owner=None):
        if not isinstance(lvl, NUMBER) or lvl != lvl // 1:
            raise ValueError(f"잘못된 레벨 값 : {lvl}")
        if rarity < self.BASE_RARITY:
            self.rarity = self.BASE_RARITY
        elif rarity > self.PROMOTION:
            self.rarity = self.PROMOTION
        else:
            self.rarity = list(R)[rarity]
        self.lvl = lvl
        self.owner = owner
        self.buff = BuffList()
        self.init_buff()

    def isfit(self, char: 'Character'):
        return True
        
    def get_icon_filename(self):
        return f"UI_Icon_Equip_{EQUIP_TYPE_CODE[self.EQUIP_TYPE]}_{self.code}_T{self.rarity + 1}"

    def init_buff(self):
        pass

    def passive(self, tt, args=None):
        pass

    def __str__(self):
        return f"{self.nick}[{self.rarity.name}/Lv.{self.lvl}]"

    def __repr__(self):
        return f"<{self.name}[{self.rarity.name}/Lv.{self.lvl}] owner={self.owner}>"


class Chip(Equip):
    EQUIP_TYPE = ET.CHIP


class OS(Equip):
    EQUIP_TYPE = ET.OS


class Gear(Equip):
    EQUIP_TYPE = ET.GEAR


class ATKChip(Chip):
    nick = "공칩"
    name = "출력 강화 회로"
    code = "Atk"
    val = [(20, 2), (30, 3), (40, 4), (50, 5)]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ATK, 0,
                                  self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class ACCChip(Chip):
    nick = "적칩"
    name = "연산 강화 회로"
    code = "Acc"
    val = [(15, d('1.5')), (20, 2), (25, d('2.5')), (35, d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ACC, 0,
                             self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class DEFChip(Chip):
    nick = "방칩"
    name = "내 충격 회로"
    code = "Def"
    val = [(16, d('3.2')), (24, d('4.4')), (30, d('6')), (36, d('7.2'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.DEF, 0,
                             self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class EVAChip(Chip):
    nick = "회칩"
    name = "반응 강화 회로"
    code = "Ev"
    val = [(6, d('.3')), (8, d('.4')), (10, d('.5')), (15, d('.75'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.EVA, 0,
                             self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class CRITChip(Chip):
    nick = "치칩"
    name = "분석 회로"
    code = "Cri"
    val = [(d('4'), d('0.2')), (d('5'), d('0.25')), (d('6'), d('0.3')), (d('8'), d('0.4'))]
    dval = (0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.dval[self.lvl], removable=False)
        )


class HPChip(Chip):
    nick = "체칩"
    name = "회로 내구 강화"
    code = "Hp"
    val = [(80, 16), (120, 24), (160, 32), (200, 40)]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.HP, 0,
                                  self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class VaccineChip(Chip):
    nick = "백신칩"
    name = "백신 처리"
    code = "Debuff_Res"
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
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=desc,
                                 chance=self.chval[self.rarity][self.lvl])


class SPDChip(Chip):
    nick = "행칩"
    name = "회로 최적화"
    code = "Spd"
    val = [(d('.1'), d('.005')), (d('.12'), d('.006')), (d('.14'), d('.007')), (d('.15'), d('.0075'))]

    def init_buff(self):
        self.buff = BuffList(Buff(BT.SPD, 0,
                                  self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False))


class StandardOS(OS):
    nick = "표준OS"
    name = "표준형 전투 시스템"
    code = "Normal"
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
    code = "Assault"
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
            self.owner.give_buff(BT.SPD, 1, self.val[1][self.rarity][self.lvl], desc=desc)


class DefenseOS(OS):
    nick = "방어OS"
    name = "방어형 전투 시스템"
    code = "Defense"
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
    code = "Sniper"
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

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.SUPPORTER
        
    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, self.val[1][self.rarity][self.lvl], round_=1, count=1,
                                 count_trig={TR.AFTER_COUNTER}, desc="대응형 OS",
                                 chance=self.val[0][self.rarity][self.lvl])


class AssaultOS(OS):
    nick = "사감OS"
    name = "강습형 전투 시스템"
    code = "Highspd"
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
    code = "Maneuver"
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
    code = "AntiAir"
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
    code = "AntiTrooper"
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
    code = "AntiArmor"
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
    code = "Exp"
    val = [(d('.05'), d('.01')), (d('.07'), d('.01')), (d('.1'), d('.01')), (d('.14'), d('.01'))]

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            lvl = self.lvl
            if self.rarity == R.SS and lvl == 10:
                lvl += 1
            self.owner.give_buff(BT.EXP, 1,
                                 self.val[self.rarity][0] + self.val[self.rarity][1] * lvl, desc="고속 학습 OS")


class APpack(Gear):
    nick = "에팩"
    name = "보조 에너지 팩"
    code = "EnergyPack"
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
    code = "Observer"
    val = [((10, 2), (15, 3), (20, 4), (30, 6)),
           ((5, 5), (15, 5), (35, 5), (55, 5))]

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.ATTACKER
        
    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF), desc=self.name,
                                 chance = self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl)


class SpaceArmor(Gear):
    nick = "공간 장갑"
    name = nick
    code = "SpaceArmor"
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

    def isfit(self, char: 'Character'):
        return char.type_[0] == CT.HEAVY
        
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
    code = "SubBooster"
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

    def isfit(self, char: 'Character'):
        return char.type_[0] == CT.FLY
        
    def init_buff(self):
        self.buff = BuffList(Buff(BT.EVA, 0, self.val[0][self.rarity][self.lvl], removable=False))

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.EVA, efft=BET.DEBUFF),
                                 desc="보조 부스터", chance=self.val[1][self.rarity][self.lvl])


class UltraScope(Gear):
    nick = "스코프"
    name = "초정밀 조준기"
    code = "SpSight"
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
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF),
                                 desc=self.name, chance=self.val[2][self.rarity][self.lvl])


class ArmorPierce(Gear):
    nick = "송곳"
    name = "대 장갑 장비"
    code = "ArmorPierce"
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
            self.owner.give_buff(BT.DEFPEN, 0, self.val[1][self.rarity][self.lvl], desc=self.name)


class EnergyConverter(Gear):
    nick = "에너지 전환기"
    name = nick
    code = "AntiBarrier"
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
    code = "Barrier"
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
    code = "SpyDrone"
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
    code = "ExamKit"
    val = [((d('8'), d('.8')), (d('12'), d('1.2')), (d('16'), d('1.6')), (d('20'), d('2'))),
           ((d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8')), (d('5'), d('1'))),
           ((30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60),
            (36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 67),
            (42, 45, 48, 51, 54, 57, 60, 63, 67, 71, 75),
            (57, 60, 63, 67, 71, 75, 80, 85, 90, 95, 100))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.HEAVY, CR.ATTACKER)
        
    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ATTACK:
            self.owner.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, count=1, count_trig={TR.AFTER_SKILL},
                                 desc="방어막 중화", chance=self.val[2][self.rarity][self.lvl])


class AdvRadar(Gear):
    nick = "망원 조준 장치"
    name = nick
    code = "AdvRadar"
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

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.ATTACKER
        
    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if self.owner.getposy() == self.owner.isenemy * 2:
                desc = "망원 조준 장치"
                self.owner.give_buff(BT.ATK, 1, self.val[0][self.rarity][self.lvl], round_=1, desc=desc)
                self.owner.give_buff(BT.ACC, 0, self.val[1][self.rarity][self.lvl], round_=1, desc=desc)
                self.owner.give_buff(BT.CRIT, 0, self.val[2][self.rarity][self.lvl], round_=1, desc=desc)


class Stimulant(Gear):
    nick = "전투 자극제"
    name = nick
    code = "Stimulant"
    val = [((d('.025'), d('.005')), (d('.035'), d('.005')), (d('.05'), d('.005')), (d('.07'), d('.005'))),
           ((10, 15), (40, 15), (85, 15), (145, 15))]

    def passive(self, tt, args=None):
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
    code = "Hologram"
    val = [(d('5'), d('.5')), (d('7'), d('.7')), (d('9'), d('.9')), (d('12'), d('.12'))]
    
    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.SUPPORTER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            c = 1
            if self.rarity == R.SS and self.lvl == 10:
                c += 1
            self.owner.give_buff(BT.MINIMIZE_DMG, 0, 9999999, count=c, desc=self.name)


class SpecialRifleBullet(Gear):
    BASE_RARITY = R.SS
    nick = "콘챠전장"
    name = "특수 코팅 라이플탄"
    code = "SpRifleBullet"
    val = [(d('30'), d('31.5'), d('33'), d('36'), d('40.5'),
            d('46.5'), d('51'), d('60'), d('72'), d('87'), d('105')),
           (d('5'), d('5.25'), d('5.5'), d('6'), d('6.75'),
            d('7.75'), d('8.5'), d('10'), d('12'), d('14.5'), d('17.5'))]

    def isfit(self, char: 'Character'):
        return char.id_ == 3

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ATK, 0, self.val[0][self.lvl], removable=False),
                             Buff(BT.CRIT, 0, self.val[1][self.lvl], removable=False))

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('0.25') + d('0.05') * min(self.lvl, 1), desc=self.name)


class AMRAAMPod(Gear):
    BASE_RARITY = R.SS
    nick = "그리폰전장"
    name = "확장 AMRAAM 포드"
    code = "AMRAAMPod"
    val = [[d('0.15'), d('0.15'), d('0.16'), d('0.17'), d('0.18'),
            d('0.19'), d('0.2'), d('0.21'), d('0.22'), d('0.23'), d('0.25')],
           [d('0.15'), d('0.15'), d('0.17'), d('0.19'), d('0.21'),
            d('0.23'), d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.33')]]

    def isfit(self, char: 'Character'):
        return char.id_ == 92

    def init_buff(self):
        self.buff = BuffList(Buff(BT.ATK, 0, d('50') + d('5') * self.lvl, removable=False),
                             Buff(BT.ACC, 0, d('20') + d('4') * self.lvl, removable=False),
                             Buff(BT.CRIT, 0, d('5') + d('0.5') * self.lvl, removable=False))

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            desc = "AMRAAM"
            self.owner.give_buff(BT.ANTI_OS[CharType.FLY], 1, self.val[0][self.lvl], desc=desc)
            self.owner.give_buff(BT.DEFPEN, 0, self.val[1][self.lvl], desc=desc)
            if self.lvl == 10:
                self.owner.give_buff(BT.RANGE, 0, 1, desc=desc)


class SuperAlloyArmor(Gear):
    BASE_RARITY = R.SS
    nick = "요안나전장"
    name = "초합금 플레이트 아머"
    code = "SpAlloyArmor"
    val = [15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30]

    def isfit(self, char: 'Character'):
        return char.id_ == 121

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('25') + d('2.5') * self.lvl, removable=False),
            Buff(BT.ELEMENT_RES[E.ICE], 0, d('25') + d('2.5') * self.lvl, removable=False),
            Buff(BT.ELEMENT_RES[E.ELEC], 0, d('25') + d('2.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.ACTIVE_RESIST, 1, d('0.15') + d('0.02') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(efft=BET.DEBUFF), desc=self.name,
                                 chance=self.val[self.lvl])


class DragonSlayer(Gear):
    BASE_RARITY = R.SS
    nick = "좌우좌전장"
    name = "용살자의 징표"
    code = "MarkOfDS"
    val = [(d('27'), d('28.35'), d('29.7'), d('32.4'), d('36.45'),
            d('41.85'), d('45.9'), d('54'), d('64.8'), d('78.3'), d('94.5')),
           (d('10'), d('10'), d('11'), d('12'), d('13'),
            d('14'), d('15'), d('16'), d('17'), d('18'), d('20'))]

    def isfit(self, char: 'Character'):
        return char.id_ == 118

    def init_buff(self):
        self.buff = BuffList(Buff(BT.CRIT, 0, d('10') + d('2') * self.lvl, removable=False),
                             Buff(BT.EVA, 0, self.val[0][self.lvl], removable=False))

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ACTIVE_RATE, 0, self.val[1][self.lvl], desc=self.name)


class FireSpray(Gear):
    nick = "화깡"
    name = "내열 코팅"
    code = "AntiFire"
    val = [(d('20'), d('2')), (d('25'), d('2.5')), (d('30'), d('3')), (d('35'), d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, self.val[self.rarity][0] * self.val[self.rarity][1] * self.lvl,
                 removable=False, tag=self.name)
        )


class IceSpray(Gear):
    nick = "냉깡"
    name = "내한 코팅"
    code = "AntiCold"
    val = [(d('20'), d('2')), (d('25'), d('2.5')), (d('30'), d('3')), (d('35'), d('3.5'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl,
                 removable=False, tag=self.name)
        )


class ElectricSpray(Gear):
    nick = "전깡"
    name = "내전 코팅"
    code = "AntiLightning"
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
    code = "T60ExtArmor"
    val = [(d('50'), d('52.5'), d('55'), d('60'), d('67.5'), 
            d('77.5'), d('85'), d('100'), d('120'), d('145'), d('175')), 
           (d('0.15'), d('0.15'), d('0.17'), d('0.19'), d('0.21'),
            d('0.23'), d('0.25'), d('0.27'), d('0.29'), d('0.31'), d('0.35'))]

    def isfit(self, char: 'Character'):
        return char.id_ == 84

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, d('200') + d('40') * self.lvl, removable=False),
            Buff(BT.DEF, 0, self.val[0][self.lvl], removable=False),
            Buff(BT.SPD, 0, d('0.12') + d('0.012') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
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
    code = "40mmDUBullet"
    
    def isfit(self, char: 'Character'):
        return char.id_ == 87

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('60') + d('6') * self.lvl, removable=False),
            Buff(BT.CRIT, 0, d('10') + d('1') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('10') + d('1') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('0.25') + d('0.05') * min(self.lvl, 1), desc="열화 우라늄탄")


class ATFLIR(Chip):
    BASE_RARITY = R.SS
    nick = "실피드전장"
    name = "ATFLIR 강화 회로"
    code = "ATFLIR"

    def isfit(self, char: 'Character'):
        return char.id_ == 55

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
    code = "CM67SpaceBooster"

    def isfit(self, char: 'Character'):
        return char.id_ == 103

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('47.5') + d('4.75') * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('70') + d('3.5') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.1') + d('.01') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            desc = "우주용 부스터"
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.EVA, efft=BET.DEBUFF), desc=desc)
            self.owner.give_buff(BT.CRIT, 0, d('5') + d('1') * self.lvl, round_=1, desc=desc)


class MG80ModKit(Gear):
    BASE_RARITY = R.SS
    nick = "님프전장"
    name = "MG80용 개조 키트"
    code = "MG80MODKit"
    dval = [0, 1, 2, 4, 7, 11, 14, 20, 28, 40, 60]
    
    def isfit(self, char: 'Character'):
        return char.id_ == 33

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('45') + d('4.5') * self.lvl + (d('.5') if self.lvl == 9 else 0), removable=False),
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[self.lvl], removable=False),
            Buff(BT.SPD, 0, d('.15') + d('.0075') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CT.LIGHT], 1,
                                 d('.15') + d('.01') * self.lvl - (d('.01') if 0 < self.lvl < 10 else 0), desc="LM탄")


class Steroid(Gear):
    BASE_RARITY = R.SS
    nick = "스카디전장"
    name = "수상한 보조제"
    code = "STEROID"

    def isfit(self, char: 'Character'):
        return char.id_ == 122

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.SPD, 0, d('.12') + d('.012') * self.lvl, removable=False),
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CT.HEAVY], 1, d('.15') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.RANGE, 0, 1, desc=self.name)


class SK14ModKit(Gear):
    BASE_RARITY = R.SS
    nick = "미호전장"
    name = "SK-14 P.C.C"
    code = "SK14MODKit"
    dval = [0, 1, 2, 4, 7, 11, 14, 20, 28, 40, 60]

    def isfit(self, char: 'Character'):
        return char.id_ == 82

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, (d(125) if self.lvl == 10 else (d('35') + d('1.75') * self.dval[self.lvl])),
                 removable=False),
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[self.lvl], removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF), desc=self.name)


class SowanLunchBox(Gear):
    BASE_RARITY = R.SS
    nick = "도시락"
    name = "소완제 수제 도시락"
    code = "LunchBox"

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START and not self.owner.isags:
            desc = "아니 이 맛은...!"
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.005') * self.lvl, tag='LunchBox', desc=desc)
            self.owner.give_buff(BT.SPD, 1, d('.05') + d('.005') * self.lvl, tag='LunchBox', desc=desc)


class Bombard(Gear):
    BASE_RARITY = R.SS
    nick = "전략 폭격 장비"
    name = nick
    code = "Bombard"

    def isfit(self, char: 'Character'):
        return char.type_[0] == CT.FLY

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, d(5) + self.lvl, removable=False),
            Buff(BT.EVA, 0, d(-75), removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START and not self.owner.isags:
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.DEFPEN, 0, d('.15') + d('.03') * self.lvl, desc=self.name)


class SpATKChip(Chip):
    nick = "적깎칩"
    name = "출력 증폭 회로"
    code = "SpAtk"
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
    code = "EyesOfBeholderD"
    dval = [0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15]

    def isfit(self, char: 'Character'):
        return char.id_ == 21

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, d('125') + d('12.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            desc = "E.O.B D형 OS"
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('0.15') + d('0.01') * self.dval[self.lvl], desc=desc)
            self.owner.give_buff(BT.ACTIVE_RESIST, 1, d('20') + d('1.5') * self.lvl, desc=desc)
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, d('.5') + d('.05') * self.lvl, desc=desc)


class ATKCRIChip(Chip):
    nick = "공치칩"
    name = "출력 안정 회로"
    code = "ATKCRI"
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
    code = "KillExp"
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
    code = "AquaModule"
    val = [[(d('10'), d('1')), (d('15'), d('1.5')), (d('20'), d('2')), (d('25'), d('2.5'))],
           [(d('.05'), d('.005')), (d('.065'), d('0.005')), (d('.08'), d('.005')), (d('.095'), d('.005'))]]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl,
                 removable=False)
        )

    def passive(self, tt, args=None):
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
    code = "Overclock"
    val = [[(d('.15'), d('.005')), (d('.165'), d('.005')), (d('.18'), d('.005')), (d('.195'), d('.005'))],
           [(d('.05'), d('.005')), (d('.065'), d('.005')), (d('.08'), d('.005')), (d('.095'), d('.005'))],
           [(d('-19.5'), d('-.5')), (d('-18'), d('-.5')), (d('-16.5'), d('-.5')), (d('-15'), d('-.5'))]]

    def passive(self, tt, args=None):
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
    code = "HManeuver"
    val = [[(d('5'), d('1')), (d('8'), d('1.6')), (d('10'), d('2')), (d('15'), d('3'))],
           [(d('4'), d('0.8')), (d('6'), d('1.2')), (d('8'), d('1.6')), (d('10'), d('2'))],
           [(d('.1'), d('.02')), (d('.16'), d('.02')), (d('.22'), d('.02')), (d('.28'), d('.02'))]]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.FLY, CR.DEFENDER)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.EVA, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1], removable=False)
        )

    def passive(self, tt, args=None):
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
    code = "EXAM"
    val = [[(d('.05'), d('.005')), (d('.065'), d('.005')), (d('.08'), d('.005')), (d('.095'), d('.005'))],
           [(d('2'), d('.4')), (d('3.2'), d('.4')), (d('4.4'), d('.4')), (d('5.6'), d('.4'))],
           [(d('10'), d('.5')), (d('11.5'), d('.5')), (d('13'), d('.5')), (d('14.5'), d('.5'))],
           [(d('.01'), d('.002')), (d('.016'), d('.002')), (d('.022'), d('.002')), (d('.028'), d('.002'))]]

    def passive(self, tt, args=None):
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
    code = "IcePack"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('25') + d('2.5') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ATTACK:
            self.owner.give_buff(BT.AP, 0, d('.5') + d('.05') * self.lvl, desc=self.name)


class SunCream(Gear):
    BASE_RARITY = R.SS
    nick = "선 크림"
    name = nick
    code = "SunCream"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('25') + d('2.5') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.GET_HIT and args == E.FIRE:
            self.owner.give_buff(BT.AP, 0, d('.5') + d('.05') * self.lvl, desc=self.name)


class ASN6G(Gear):
    BASE_RARITY = R.SS
    nick = "운디네전장"
    name = "ASN-6G"
    code = "ASN6G"
    dval = [(0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50), (0, 1, 2, 4, 7, 11, 14, 20, 30, 40, 60)]

    def isfit(self, char: 'Character'):
        return char.id_ == 88

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('50') + d('2.5') * self.dval[0][self.lvl], removable=False),
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[1][self.lvl], removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('.15') + d('.03') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.ANTI_OS[CT.HEAVY], 1, d('.15') + d('.01') * self.lvl, desc=self.name)


class HornOfBADK(Gear):
    BASE_RARITY = R.SS
    nick = "뽀끄루전장"
    name = "뽀끄루 대마왕의 뿔"
    code = "HornOfBADK"
    dval = [(0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15), (0, 1, 2, 3, 4, 5, 7, 10, 13, 16, 20)]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START and not self.owner.isags:
            desc = "뽀끄루...뽀끄루..."
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.01') * self.lvl, round_=1, desc=desc)
            self.owner.give_buff(BT.ACC, 0, d('5') + self.dval[1][self.lvl], round_=1, desc=desc)
            self.owner.give_buff(BT.CRIT, 0, d('2.5') + d('.5') * self.dval[0][self.lvl], round_=1, desc=desc)
            self.owner.give_buff(BT.DEFPEN, 0, d('.1') + d('.01') * self.dval[0][self.lvl], round_=1, desc=desc)
            self.owner.give_buff(BT.INABILLITY_SKILL, 0, 1, round_=1, desc="뽀끄루...?", chance=10)


class MoonCake(Gear):
    BASE_RARITY = R.SS
    nick = "송편"
    name = "달의 마력이 담긴 송편"
    code = "MoonCake"

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            desc = "달의 가호"
            self.owner.give_buff(BT.ATK, 1, d('.15') + d('.03') * self.lvl, round_=1, desc=desc, chance=33)
            self.owner.give_buff(BT.ACC, 0, d('25') + d('5') * self.lvl, round_=1, desc=desc, chance=33)
            self.owner.give_buff(BT.EVA, 0, d('25') + d('5') * self.lvl, round_=1, desc=desc, chance=25)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.15') + d('.03') * self.lvl, round_=1, desc=desc, chance=15)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, round_=1, desc=desc,
                                 data=D.BuffCond(type_=BT.ATK, efft=BET.DEBUFF),
                                 chance=10+2*self.lvl+(self.lvl == 10)*3)


class Interceptor(Gear):
    BASE_RARITY = R.SS
    nick = "개량형 관측 장비"
    name = nick
    code = "Interceptor"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, d('15') + d('3') * self.lvl, removable=False),
            Buff(BT.CRIT, 0, d('5') + d('1') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            desc = "정밀형 관측 장비"
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, desc=desc)
            chance = 50 + 5 * self.lvl
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF),
                                 desc=desc, chance=chance)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF),
                                 desc=desc, chance=chance)


class ATKSPDChip(Chip):
    BASE_RARITY = R.SS
    nick = "공행칩"
    name = "개량형 출력 강화 회로"
    code = "AtkSpd"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.05') + d('.005') * self.lvl, removable=False)
        )


class FortuneOrb(Gear):
    BASE_RARITY = R.SS
    nick = "수정구"
    name = "운명의 수정구"
    code = "FortuneOrb"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, 5 + self.lvl, removable=False),
            Buff(BT.EVA, 0, 5 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.RACON, 0, 1, desc=self.name)
            self.owner.give_buff(BT.SPD, 1, d('.05') + d('.01') * self.lvl, desc=self.name)


class ElectroGenerator(Gear):
    BASE_RARITY = R.SS
    nick = "영전에팩"
    name = "고출력 제너레이터"
    code = "ElectroGenerator"
    dval = (0, 2, 4, 6, 8, 10, 12, 14, 18, 23, 28)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 25 + 5 * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.AP, 0, d('.44') + d('.2') * self.dval[self.lvl], desc=self.name)


class Recycler(Gear):
    BASE_RARITY = R.SS
    nick = "쓰레기통"
    name = "리사이클 모듈"
    code = "Recycler"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 150 + 15 * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.AP, 0, d('.3') + d('.05') * self.lvl, desc=self.name)


class LightWeight(Chip):
    nick = "경량칩"
    name = "경량화 회로"
    code = "LTWT"
    val = [((d('10'), d('1')), (d('12'), d('1.2')), (d('15'), d('1.5')), (d('20'), d('2'))),
           ((d('3'), d('.3')), (d('5'), d('.5')), (d('6'), d('.6')), (d('9'), d('.9'))),
           ((d('.01'), d('.002')), (d('.02'), d('.004')), (d('.03'), d('.006')), (d('.04'), d('.008')))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.EVA, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.SPD, 0, self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, d('-.08'), round_=1, removable=False, max_stack=1,
                                 tag='LightWeight', desc="무장 경량칩")


class CriAccCHIP(Chip):
    BASE_RARITY = R.SS
    nick = "치적칩"
    name = "개량형 분석 회로"
    code = "CriAccEx"
    dval = [(0, 1, 2, 4, 7, 11, 14, 20, 28, 40, 60),
            (0, 1, 2, 4, 7, 11, 14, 20, 28, 36, 50)]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, d('5') + d('.25') * self.dval[0][self.lvl], removable=False),
            Buff(BT.ACC, 0, d('10') + d('.5') * self.dval[1][self.lvl], removable=False),
        )


class Nitro3000(Gear):
    BASE_RARITY = R.SS
    nick = "부스터"
    name = "니트로 EX 3000"
    code = "NitroEx3000"

    val = [1, d('.9'), d('.8'), d('.7'), d('.6'), d('.5'), d('.4'), d('.3'), d('.2'), d('.1'), d('.03')]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, d('25') + d('2.5') * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('10') + d('2') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.1') + d('.02') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START and not self.owner.isags:
            self.owner.give_buff(BT.ACC, 0, -100, round_=1, efft=BET.DEBUFF, desc="속이 안 좋아...",
                                 chance=self.val[self.lvl])


class MiniPerralut(Gear):
    BASE_RARITY = R.SS
    nick = "미니 페로"
    name = "미니 페로"
    code = "MiniPerralut"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, d('7') + d('1.4') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('15') + d('1.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ATTACK:
            self.owner.give_buff(BT.AP, 0, d('0.05') * (1 + self.lvl), desc="애옹? 애옹!")


class MiniHachiko(Gear):
    BASE_RARITY = R.SS
    nick = "미니 하치코"
    name = "미니 하치코"
    code = "MiniHachiko"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, d('150') + d('30') * self.lvl, removable=False),
            Buff(BT.DEF, 0, d('30') + d('3') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.BATTLE_CONTINUATION, 0, 100 + 50 * self.lvl, desc="민트 미트파이 드세여!",
                                 max_stack=1, tag="MiniHachiko_BC")


class MiniLilith(Gear):
    BASE_RARITY = R.SS
    nick = "미니 리리스"
    name = "미니 블랙 리리스"
    code = "MinLilith"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('15') + d('1.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.TAKEDMGDEC, 1, min(d('.005'), d('.01') * self.lvl), desc="착한 리리스가 가욧!")


class EnhancedCombatOS(OS):
    BASE_RARITY = R.SS
    nick = "영전OS"
    name = "개량형 전투 시스템"
    code = "Advanced"
    val = [d('.005'), d('.0075'), d('.01'), d('.015'), d('.02'),
           d('.025'), d('.03'), d('.035'), d('.04'), d('.045'), d('.05')]

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.ATK, 1, d('.04') + d('.008') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.05') + d('.005') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.EVA, 0, d('10') + d('2') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.SPD, 1, self.val[self.lvl], round_=1, desc=self.name)


class GrandCruChocolate(Gear):
    BASE_RARITY = R.SS
    nick = "초코"
    name = "그랑크뤼 초콜릿"
    code = "GrandCruChocolate"
    val = [d('.5'), d('.6'), d('.7'), d('.8'), d('.9'),
           d('1'), d('1.2'), d('1.4'), d('1.6'), d('1.8'), d('2')]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('50') + d('5') * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('5') + d('1') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.AP, 0, self.val[self.lvl], desc="녹아내릴 듯한 달콤함")


class ATKControl(Chip):
    nick = "치씹칩"
    name = "출력 제어 회로"
    code = "AtkControl"

    val = [(d('20'), d('4')), (d('30'), d('6')), (d('40'), d('8')), (d('50'), d('10'))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, -12, removable=False)
        )


class ExoSkeleton(Gear):
    nick = "보조 외골격"
    name = "보조 외골격"
    code = "ExoSkeleton"
    val = [((d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8')), (d('5'), d('1'))),
           ((d('.02'), d('.002')), (d('.03'), d('.003')), (d('.04'), d('.004')), (d('.05'), d('.005'))),
           ((d('0'), d('.005')), (d('.015'), d('.005')), (d('.03'), d('.005')), (d('.05'), d('.005')))]

    def isfit(self, char: 'Character'):
        return char.type_[0] == CT.LIGHT

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, self.val[0][self.rarity][0] * self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.SPD, 0, self.val[1][self.rarity][0] * self.val[1][self.rarity][1] * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.TAKEDMGDEC, 1,
                                 max(d('.0025'), self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl),
                                 round_=1, desc=self.name)


class ODAmplifier(Gear):
    BASE_RARITY = R.SS
    nick = "O.D 증폭기"
    name = "O.D 증폭기"
    code = "Odamplifier"

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START and not self.owner.isags:
            self.owner.give_buff(BT.ATK, 1, d('.15') + d('.075') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.DOT_DMG, 0, d(525), round_=1, desc=self.name)


class CMIIShield(Gear):
    BASE_RARITY = R.SS
    nick = "켈베전장"
    name = "촙 메이커 II"
    code = "CMIIShield"
    dval = (0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15)

    def isfit(self, char: 'Character'):
        return char.id_ == 113

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('30') + d('6') * self.lvl, removable=False),
            Buff(BT.ELEMENT_RES[E.FIRE], 0, d('20') + d('4') * self.lvl, removable=False),
            Buff(BT.ELEMENT_RES[E.ELEC], 0, d('20') + d('4') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, d('50') + d('5') * self.dval[self.lvl], round_=1, desc=self.name)
            self.owner.give_buff(BT.DEF, 1, d('.1') + d('.025') * self.lvl, round_=1, desc="강화 티타늄 실드")


class VerminEliminator(Gear):
    BASE_RARITY = R.SS
    nick = "리제전장"
    name = "해충 파쇄기"
    code = "VerminEliminator"

    def isfit(self, char: 'Character'):
        return char.id_ == 7

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('60') + d('6') * self.lvl, removable=False),
            Buff(BT.CRIT, 0, d('5') + d('1') * self.lvl, removable=False),
            Buff(BT.ACC, 0, d('10') + d('2') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('0.25') + d('0.04') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ATK, efft=BET.DEBUFF), desc=self.name)


class GigantesArmor(Gear):
    BASE_RARITY = R.SS
    nick = "기간테스전장"
    name = "개량형 복합 장갑"
    code = "GigantesArmor"
    dval1 = (0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50)
    dval2 = (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15)

    def isfit(self, char: 'Character'):
        return char.id_ == 203

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, d('25') + d('2.5') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.1') + d('.005') * self.dval1[self.lvl], removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.5') + d('.005') * self.dval2[self.lvl], desc=self.name)
            self.owner.give_buff(BT.ELEMENT_RES[E.FIRE], 0, d('20') + self.dval1[self.lvl], desc=self.name)
            self.owner.give_buff(BT.ELEMENT_RES[E.ICE], 0, d('20') + self.dval1[self.lvl], desc=self.name)
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, d('.8') + d('.05') * self.lvl, desc=self.name)


class QMObserver(Gear):
    BASE_RARITY = R.SS
    nick = "레오나전장"
    name = "전투 관측 프레임"
    code = "QMObserver"

    val = [(d('20'), d('21'), d('22'), d('24'), d('27'),
            d('31'), d('34'), d('40'), d('48'), d('58'), d('70')),
           (d('12'), d('12.6'), d('13.2'), d('14.4'), d('16.2'),
            d('18.6'), d('20.4'), d('24'), d('28.8'), d('34.8'), d('42')),
           ]

    def isfit(self, char: 'Character'):
        return char.id_ == 31

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.lvl], removable=False),
            Buff(BT.EVA, 0, self.val[1][self.lvl], removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.RACON, 0, 1, desc=self.name)


class ATKChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "공베칩"
    name = "출력 강화 회로 베타"
    code = "AtkTypeB"
    val = [(d('24'), d('2.4')), (d('36'), d('3.6')), (d('48'), d('4.8')), (d('60'), d('6')),
           (70, 75, 80, 85, 90, 100, 107, 114, 121, 128, 135)]

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.ATK, 0, d(self.val[self.rarity][self.lvl]), removable=False),
                Buff(BT.EVA, 0, d('-11') + (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.ATK, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.EVA, 0, d('-6') + d('-.6') * self.lvl, removable=False)
            )


class ACCChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "적베칩"
    name = "연산 강화 회로 베타"
    code = "AccTypeB"
    val = [(d('18'), d('1.8')), (d('24'), d('2.4')), (d('30'), d('3')), (d('42'), d('4.2')),
           (45, 49, 53, 57, 61, 65, 70, 75, 80, 85, 90)]

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.ACC, 0, d(self.val[self.rarity][self.lvl]), removable=False),
                Buff(BT.DEF, 0, d('-49') + d('4') * (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.ACC, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.DEF, 0, d('-27') + d('-2.7') * self.lvl, removable=False)
            )


class DEFChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "방베칩"
    name = "내 충격 강화 회로 베타"
    code = "DefTypeB"
    val = [(d('30'), d('3')), (d('43'), d('4.3')), (d('54'), d('5.4')), (d('65'), d('6.5')), (d('100'), d('10'))]

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.DEF, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.ATK, 0, d('-35') + d('3') * (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.DEF, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.ATK, 0, d('-25') + d('-2.5') * self.lvl, removable=False)
            )


class EVAChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "회베칩"
    name = "반응 강화 회로 베타"
    code = "EvTypeB"
    val = [(d('72'), d('.36')), (d('9.6'), d('.48')), (d('12'), d('.6')), (d('18'), d('.9')), (d('20'), d('1'))]

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.EVA, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.ATK, 0, d('-35') + d('3') * (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.EVA, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.ATK, 0, d('-25') + d('-2.5') * self.lvl, removable=False)
            )


class CRITChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "치베칩"
    name = "분석 회로 베타"
    code = "CriTypeB"
    val = [((d('4.8'), d('.24')), (d('6'), d('.3')), (d('7.2'), d('.36')), (d('9.6'), d('.48'))),
           (0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50)]

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.CRIT, 0, d('12') + d('2.4') * self.lvl, removable=False),
                Buff(BT.DEF, 0, d('-55') + d('5') * (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.CRIT, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.val[1][self.lvl],
                     removable=False),
                Buff(BT.DEF, 0, d('-27') + d('-2.7') * self.lvl, removable=False)
            )


class HPChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "체베칩"
    name = "회로 내구 강화 베타"
    code = "HpTypeB"
    val = [(d('96'), d('19.2')), (d('144'), d('28.8')), (d('192'), d('38.6')), (d('240'), d('48')), (d('300'), d('15'))]
    dval = (0, 1, 2, 4, 7, 11, 14, 20, 28, 38, 50)

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.HP, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.dval[self.lvl],
                     removable=False),
                Buff(BT.ATK, 0, d('-35') + d('3') * (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.HP, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.ATK, 0, d('-25') + d('-2.5') * self.lvl, removable=False)
            )


class SPDChipBETA(Chip):
    PROMOTION = R.SSS
    nick = "행베칩"
    name = "회로 최적화 베타"
    code = "SpdTypeB"
    val = [(d('.12'), d('.006')), (d('.144'), d('.0072')), (d('.168'), d('.0084')), (d('.18'), d('.009')),
           (d('.19'), d('.01'))]

    def init_buff(self):
        if self.rarity == R.SSS:
            self.buff = BuffList(
                Buff(BT.SPD, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.EVA, 0, d('-11') + (self.lvl == 0), removable=False)
            )
        else:
            self.buff = BuffList(
                Buff(BT.SPD, 0, self.val[self.rarity][0] + self.val[self.rarity][1] * self.lvl, removable=False),
                Buff(BT.EVA, 0, d('-6') + d('-.6') * self.lvl, removable=False)
            )


class Precision(Gear):
    BASE_RARITY = R.SS
    nick = "정밀형 관측 장비"
    name = "정밀형 관측 장비"
    code = "Precision"

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.RANGE, 0, 2, round_=1, desc=self.name)
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.RANGE, efft=BET.DEBUFF),
                                 desc=self.name, chance = 50 + 5 * self.lvl)


class RangerSet(Gear):
    BASE_RARITY = R.SS
    nick = "다크엘븐전장"
    name = "레인저용 전투장비 세트"
    code = "RangerSet"

    def isfit(self, char: 'Character'):
        return char.id_ == 135

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 75 + d('7.5') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 10 + self.lvl, removable=False),
            Buff(BT.CRIT, 0, 10 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('.1') + d('.01') * self.lvl, round_=1, efft=BET.BUFF, desc=self.name)
            self.owner.give_buff(BT.RANGE, 0, 1, round_=1, efft=BET.BUFF, desc=self.name)


class UnevenTerrain(Gear):
    BASE_RARITY = R.SS
    nick = "엘븐전장"
    name = "험지용 특수 프레임"
    code = "UnevenTerrain"

    def isfit(self, char: 'Character'):
        return char.id_ == 133

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.DEF, 0, 95 + d('9.5') * self.lvl, removable=False),
            Buff(BT.HP, 0, 250 + 25 * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.COLUMN_PROTECT, 0, 1, round_=1, efft=BET.BUFF, desc=self.name,
                                 overlap_type=BOT.RENEW)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.05') + d('.01') * self.lvl, round_=1, efft=BET.BUFF,
                                 desc=self.name)
            for i in range(1, 4):
                self.owner.give_buff(BT.ELEMENT_RES[i], 1, 15 + 2 * self.lvl, round_=1, efft=BET.BUFF, desc=self.name)


class ThornNecklace(Gear):
    BASE_RARITY = R.SS
    nick = "베로니카전장"
    name = "특수 대원용 가시 목걸이"
    code = "ThornNecklace"
    val = (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14)

    def isfit(self, char: 'Character'):
        return char.id_ == 138

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 100 + 10 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 5 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('.1') + d('.01') * self.val[self.lvl], desc=self.name)
            self.owner.give_buff(BT.DOT_DMG, 0, 650, round_=1, desc=self.name)


class OverFlow(OS):
    BASE_RARITY = R.SS
    nick = "타이런트전장"
    name = "폭주 유도 시스템 OS"
    code = "OverFlow"

    def isfit(self, char: 'Character'):
        return char.id_ == 224

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 75 + d('7.5') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 25 + d('2.5') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ENEMY_DEAD:
            self.owner.give_buff(BT.ATK, 1, d('.02') + d('.003') * self.lvl, round_=2, efft=BET.BUFF, desc=self.name)


class FCS(Gear):
    BASE_RARITY = R.SS
    nick = "셀주크전장"
    name = "F.C.S"
    code = "FCS"

    def isfit(self, char: 'Character'):
        return char.id_ == 202

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 60 + 6 * self.lvl, removable=False),
            Buff(BT.ACC, 0, 10 + self.lvl, removable=False),
            Buff(BT.CRIT, 0, 10 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.AP, 0, d('.2') + d('.03') * self.lvl, efft=BET.BUFF, desc=self.name)


class ImprovedUltraScope(Gear):
    BASE_RARITY = R.SS
    nick = "영전스코프"
    name = "초정밀 조준기"
    code = "ImSpSight"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, d('12.5') + d('1.25') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 40 + 4 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF),
                                 desc=self.name, chance = 50 + 5 * self.lvl)


class AntiLightFlyOS(OS):
    nick = "대경장기동OS"
    name = "대 경장/기동 전투 시스템"
    code = "AntiTrooperAir"
    val = (d('.1'), d('.11'), d('.125'), d('.145'))

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            v = self.val[self.rarity] + d('.005') * (self.lvl + (self.rarity == R.SS and self.lvl == 10))
            self.owner.give_buff(BT.ANTI_OS[CharType.LIGHT], 1, v, desc="대 경장/기동형 OS")
            self.owner.give_buff(BT.ANTI_OS[CharType.FLY], 1, v, desc="대 경장/기동형 OS")


class AntiFlyHeavyOS(OS):
    nick = "대기동중장OS"
    name = "대 기동/중장 전투 시스템"
    code = "AntiAirArmor"
    val = (d('.1'), d('.11'), d('.125'), d('.145'))

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            v = self.val[self.rarity] + d('.005') * (self.lvl + (self.rarity == R.SS and self.lvl == 10))
            self.owner.give_buff(BT.ANTI_OS[CharType.FLY], 1, v, desc="대 기동/중장형 OS")
            self.owner.give_buff(BT.ANTI_OS[CharType.HEAVY], 1, v, desc="대 기동/중장형 OS")


class AntiHeavyLightOS(OS):
    nick = "대중장경장OS"
    name = "대 중장/경장 전투 시스템"
    code = "AntiArmorTrooper"
    val = (d('.1'), d('.11'), d('.125'), d('.145'))

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            v = self.val[self.rarity] + d('.005') * (self.lvl + (self.rarity == R.SS and self.lvl == 10))
            self.owner.give_buff(BT.ANTI_OS[CharType.HEAVY], 1, v, desc="대 중장/경장형 OS")
            self.owner.give_buff(BT.ANTI_OS[CharType.LIGHT], 1, v, desc="대 중장/경장형 OS")


class ImprovedEXPOS(OS):
    BASE_RARITY = R.SS
    nick = "영전경험치OS"
    name = "개량형 고속 학습 시스템"
    code = "ImExp"

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.EXP, 1, d('.155') + d('.011') * self.lvl + d('.01') * (self.lvl == 10),
                                 desc="개량형 고속 학습 OS")
            self.owner.give_buff(BT.SPD, 1, d('-.2') + d('-.01') * self.lvl, desc="개량형 고속 학습 OS")


class ParticleAcceleratorATK(Gear):
    BASE_RARITY = R.SS
    nick = "입자가속기 력"
    name = "입자 가속기 력"
    code = "ParticleAcceleratorATK"

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.ATK, 1, d('.15') + d('.02') * self.lvl, round_=1, desc="입자 가속기 [력]")
            self.owner.give_buff(BT.TAKEDMGINC, 1, d('.1') + d('.01') * self.lvl, round_=1, desc="입자 가속기 [력]")


class ImprovedNitro3500(Gear):
    BASE_RARITY = R.SS
    nick = "영전부스터"
    name = "개량형 니트로 EX 3500"
    code = "ImNitroEx3500"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, 30 + 3 * self.lvl, removable=False),
            Buff(BT.EVA, 0, d('18') + d('1.8') * self.lvl, removable=False),
            Buff(BT.SPD, 0, d('.2') + d('.02') * self.lvl, removable=False),
        )


class ImprovedBarrier(Gear):
    BASE_RARITY = R.SS
    nick = "영전방어막"
    name = "개량형 방어 역장"
    code = "ImBarrier"
    val = (400, 420, 450, 480, 520, 560, 600, 650, 700, 750, 800)

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.BARRIER, 0, self.val[self.lvl], round_=1, desc=self.name)
            self.owner.give_buff(BT.SPD, 1, d('-.1') + d('-.01') * self.lvl, round_=1, desc=self.name)


class DustStorm(Gear):
    BASE_RARITY = R.SS
    nick = "더스트스톰(칸)"
    name = "더스트 스톰"
    code = "AngelLegs"

    def isfit(self, char: 'Character'):
        return char.id_ == 41

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.MARKED, 0, 1, round_=1, desc=self.name)
            self.owner.give_buff(BT.EVA, 0, 100 + 10 * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.2') + d('.03') * self.lvl, round_=1, desc=self.name)


class LRCannon(Gear):
    BASE_RARITY = R.SS
    nick = "LRC(칸)"
    name = "L.R.C 탄환"
    code = "LRCannon"

    def isfit(self, char: 'Character'):
        return char.id_ == 41
    
    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ANTI_OS[CT.LIGHT], 1, d('.2') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.ANTI_OS[CT.HEAVY], 1, d('.2') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.DEFPEN, 0, d('.2') + d('.03') * self.lvl, desc=self.name)


class OptimizeLightAttackerOS(OS):
    PROMOTION = R.SSS
    nick = "영전 경장공격OS"
    name = "경장 공격 최적화 시스템"
    code = "RogTrooperNukerATK"
    val = [(d('.135'), 13), (d('.155'), 14), (d('.185'), d('15.5')), (d('.225'), d('17.5')), (d('.275'), 20)]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.LIGHT, CR.ATTACKER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, self.val[self.rarity][0] + d('.1') * self.lvl)
            self.owner.give_buff(BT.ACC, 0, self.val[self.rarity][1] + d('.5') * self.lvl)


class OptimizeFlyAttackerOS(OS):
    PROMOTION = R.SSS
    nick = "영전 기동공격OS"
    name = "기동 공격 최적화 시스템"
    code = "RogMobilityNukerATK"
    val = [(d('.11'), d('.002')), (d('.13'), d('.006')), (d('.16'), d('.012')),
           (d('.2'), d('.02')), (d('.25'), d('.03'))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.FLY, CR.ATTACKER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, self.val[self.rarity][0] + d('.1') * self.lvl)
            self.owner.give_buff(BT.SPD, 1, self.val[self.rarity][1] + d('.002') * self.lvl)


class OptimizeHeavyAttackerOS(OS):
    PROMOTION = R.SSS
    nick = "영전 중장공격OS"
    name = "중장 공격 최적화 시스템"
    code = "RogArmoredNukerATK"
    val = [(d('.135'), d('5.2')), (d('.155'), d('5.6')), (d('.185'), d('6.2')), (d('.225'), 7), (d('.275'), 8)]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.HEAVY, CR.ATTACKER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, self.val[self.rarity][0] + d('.1') * self.lvl)
            self.owner.give_buff(BT.CRIT, 0, self.val[self.rarity][1] + d('.2') * self.lvl)


class OptimizeLightDefenderOS(OS):
    PROMOTION = R.SSS
    nick = "영전 경장보호OS"
    name = "경장 보호 최적화 시스템"
    code = "RogTrooperTankerDEF"
    val = [(d('.13'), d('.03')), (d('.15'), d('.04')), (d('.18'), d('.055')),
           (d('.22'), d('.075')), (d('.27'), d('.1'))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.LIGHT, CR.DEFENDER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEF, 1, self.val[self.rarity][0] + d('.1') * self.lvl)
            self.owner.give_buff(BT.TAKEDMGDEC, 0, self.val[self.rarity][1] + d('.005') * self.lvl)


class OptimizeFlyDefenderOS(OS):
    PROMOTION = R.SSS
    nick = "영전 기동보호OS"
    name = "기동 보호 최적화 시스템"
    code = "RogMobilityTankerEVA"
    val = [(16, d('.052')), (18, d('.056')), (21, d('.062')), (25, d('.07')), (30, d('.08'))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.FLY, CR.DEFENDER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.EVA, 0, self.val[self.rarity][0] + self.lvl)
            self.owner.give_buff(BT.SPD, 1, self.val[self.rarity][1] + d('.002') * self.lvl)


class OptimizeHeavyDefenderOS(OS):
    PROMOTION = R.SSS
    nick = "영전 중장보호OS"
    name = "중장 보호 최적화 시스템"
    code = "RogArmoredTankerDEF"
    val = [(60, d('.16')), (100, d('.18')), (140, d('.21')), (180, d('.25')), (200, d('.3'))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.HEAVY, CR.DEFENDER)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, self.val[self.rarity][0] * (1 + d('.2') * self.lvl), removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEF, 1, self.val[self.rarity][1] + d('.1') * self.lvl)


class OptimizeLightSupporterOS(OS):
    PROMOTION = R.SSS
    nick = "영전 경장지원OS"
    name = "경장 지원 최적화 시스템"
    code = "RogTrooperSupporterSPd"
    val = [(d('.055'), 32), (d('.065'), 36), (d('.08'), 42), (d('.1'), 50), (d('.125'), 60)]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.LIGHT, CR.SUPPORTER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SPD, 1, self.val[self.rarity][0] + d('.005') * self.lvl)
            self.owner.give_buff(BT.ACC, 0, self.val[self.rarity][1] + 2 * self.lvl)


class OptimizeFlySupporterOS(OS):
    PROMOTION = R.SSS
    nick = "영전 기동지원OS"
    name = "기동 지원 최적화 시스템"
    code = "RogMobilitySupporterSPd"
    val = [(d('.08'), 22), (d('.09'), 26), (d('.105'), 32), (d('.125'), 40), (d('.15'), 50)]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.FLY, CR.SUPPORTER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SPD, 1, self.val[self.rarity][0] + d('.005') * self.lvl)
            self.owner.give_buff(BT.ACC, 0, self.val[self.rarity][1] + 2 * self.lvl)


class OptimizeHeavySupporterOS(OS):
    PROMOTION = R.SSS
    nick = "영전 중장지원OS"
    name = "중장 지원 최적화 시스템"
    code = "RogArmoredSupporterSPD"
    val = [(d('.03'), d('.8')), (d('.04'), d('.9')), (d('.055'), d('1.05')),
           (d('.075'), d('1.25')), (d('.1'), d('1.5'))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.HEAVY, CR.SUPPORTER)

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SPD, 1, self.val[self.rarity][0] + d('.005') * self.lvl)
            self.owner.give_buff(BT.AP, 0, self.val[self.rarity][1] + d('.05') * self.lvl)


class ParticleAcceleratorHP(Gear):
    BASE_RARITY = R.SS
    nick = "입자가속기 량"
    name = "입자 가속기 량"
    code = "ParticleAcceleratorHP"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 400 + 60 * self.lvl, removable=False)
        )


class ImprovedAssaultOS(OS):
    BASE_RARITY = R.SS
    nick = "영전사감os"
    name = "개량 강습형 전투 시스템"
    code = "ImHighspd"

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            desc = "개량 강습형 전투 OS"
            self.owner.give_buff(BT.ATK, 1, d('.1') + d('.01') * self.lvl, desc=desc)
            self.owner.give_buff(BT.RANGE, 0, -2, desc=desc)
            self.owner.give_buff(BT.CRIT, 0, d('.1') if self.lvl == 0 else d('.5') * self.lvl, desc=desc)


class TuinStone(Gear):
    BASE_RARITY = R.SS
    nick = "타치전장 화염"
    name = "투인석"
    code = "FlameStone"

    def isfit(self, char: 'Character'):
        return char.id_ == 206

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 100 + 5 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 5 + d('.5') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 10 + self.lvl, removable=False),
        )
    
    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.GIVEDMGINC, 1, d('.2') + d('.01') * self.lvl,
                                 data=D.DmgInfo(element=E.FIRE), desc=self.name)


class SumaStone(Gear):
    BASE_RARITY = R.SS
    nick = "타치전장 냉기"
    name = "수마석"
    code = "FrostStone"

    def isfit(self, char: 'Character'):
        return char.id_ == 206

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 100 + 5 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 5 + d('.5') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 10 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.GIVEDMGINC, 1, d('.2') + d('.01') * self.lvl,
                                 data=D.DmgInfo(element=E.ICE), desc=self.name)


class JowiStone(Gear):
    BASE_RARITY = R.SS
    nick = "타치전장 전기"
    name = "조위석"
    code = "ThunderStone"

    def isfit(self, char: 'Character'):
        return char.id_ == 206

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 100 + 5 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 5 + d('.5') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 10 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.GIVEDMGINC, 1, d('.2') + d('.01') * self.lvl,
                                 data=D.DmgInfo(element=E.ELEC), desc=self.name)


class LRAD(OS):
    BASE_RARITY = R.SS
    nick = "드라큐리나OS"
    name = "LRAD 강화 시스템"
    code = "LRAD"

    def isfit(self, char: 'Character'):
        return char.id_ == 141

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            val = d('14.5') + d('.5') * (self.lvl + (self.lvl == 10))
            for antios in BT.ANTI_OS:
                self.owner.give_buff(antios, 1, val, desc="LRAD 강화")
            self.owner.give_buff(BT.RANGE, 0, 1, desc="LRAD 강화")


class S42Adlib(Chip):
    BASE_RARITY = R.SS
    nick = "골타전장"
    name = "S#.42 ad-lib 회로"
    code = "S42Adlib"

    def isfit(self, char: 'Character'):
        return char.id_ == 128

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ATK, 0, 100 + 10 * self.lvl, removable=False),
            Buff(BT.HP, 0, -30 - 3 * self.lvl, removable=False),
            Buff(BT.DEF, 0, 27 + d('.27') * self.lvl, removable=False),
        )


class ASEARadar(Gear):
    BASE_RARITY = R.SS
    nick = "블하전장"
    name = "능동형 항공 레이더"
    code = "ASEARadar"
    val = (0, 2, 4, 6, 8, 10, 12, 14, 18, 23, 28)
    
    def isfit(self, char: 'Character'):
        return char.id_ == 95

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, 12 + d('1.2') * self.lvl + (self.lvl == 0), removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.AP, 0, d('.44') + d('.02') * self.val[self.lvl], desc=self.name)
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, d('.5') + d('.05') * self.lvl, round_=1, desc=self.name)


class MKEngine(Gear):
    BASE_RARITY = R.SS
    nick = "린트불룸전장"
    name = "개량형 MK 엔진"
    code = "MKEngine"
    val = (0, 2, 4, 6, 8, 10, 12, 14, 18, 23, 28)
    
    def isfit(self, char: 'Character'):
        return char.id_ == 96
    
    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.AP, 0, d('.44') + d('.02') * self.val[self.lvl], desc=self.name)
            self.owner.give_buff(BT.DEFPEN, 0, d('.05') + d('.03') * self.lvl, round_=1, desc=self.name)
            self.owner.give_buff(BT.FOLLOW_ATTACK, 0, 1, round_=1, desc=self.name)


class PileBunker(Gear):
    BASE_RARITY = R.SS
    nick = "불가사리벙커"
    name = "전격형 파일벙커"
    code = "BulgasariPileBunker"

    def isfit(self, char: 'Character'):
        return char.id_ == 84
    
    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.01') * self.lvl, desc=self.name)


class ImprovedOverclock(Gear):
    BASE_RARITY = R.SS
    nick = "영전글카"
    name = "개량형 출력 제한 해제 장치"
    code = "ImOverclock"

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START and self.owner.isags:
            self.owner.give_buff(BT.ATK, 1, d('.2') + d('.015') * (self.lvl + (self.lvl == 0)), desc=self.name[:-3])
            self.owner.give_buff(BT.SPD, 1, d('.15') + d('.01') * (self.lvl - (0 < self.lvl < 10)), desc=self.name[:-3])


class HQ1Commander(OS):
    BASE_RARITY = R.SS
    nick = "알바OS"
    name = "HQ1 커맨더 시스템"
    code = "HQ1Commander"

    def isfit(self, char: 'Character'):
        return char.id_ == 201

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.AP, 0, 1, desc=self.name)
            self.owner.give_buff(BT.EVA, 0, d(15) + d('2.5') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.1') + d('.005') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.INABILLITY_SKILL, 0, 1, count=1, count_trig={TR.IDLE, }, desc=self.name)


class TuinOrellia(Gear):
    BASE_RARITY = R.SS
    nick = "오렐리아전장 화염"
    name = "원소의 심장(화염)"
    code = "TuinOrellia"

    def isfit(self, char: 'Character'):
        return char.id_ == 205

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, 30 + 3 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.BATTLE_CONTINUATION, 1, d('.3') + d('.03') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.3') + d('.03') * self.lvl, desc=self.name)
        elif tt == TR.HIT:
            if args.get("skill_no") == 2:
                targets = args.get("targets")
                for t in targets:
                    if targets[t]:
                        t.give_buff(BT.TAKEDMGINC, 1, d('.2') + d('.01') * self.lvl,
                                    data=D.DmgInfo(element=E.FIRE), round_=0, desc=self.name)
                        t.give_buff(BT.ELEMENT_RES[E.FIRE], 0, -50 - 3 * self.lvl,
                                    efft=BET.DEBUFF, max_stack=1, tag=f"{self.code}_ER", desc=self.name)


class SumaOrellia(Gear):
    BASE_RARITY = R.SS
    nick = "오렐리아전장 냉기"
    name = "원소의 심장(냉기)"
    code = "SumaOrellia"

    def isfit(self, char: 'Character'):
        return char.id_ == 205

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, 30 + 3 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.BATTLE_CONTINUATION, 1, d('.3') + d('.03') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.3') + d('.03') * self.lvl, desc=self.name)
        elif tt == TR.HIT:
            if args.get("skill_no") == 2:
                targets = args.get("targets")
                for t in targets:
                    if targets[t]:
                        t.give_buff(BT.TAKEDMGINC, 1, d('.2') + d('.01') * self.lvl,
                                    data=D.DmgInfo(element=E.ICE), round_=0, desc=self.name)
                        t.give_buff(BT.ELEMENT_RES[E.ICE], 0, -50 - 3 * self.lvl,
                                    efft=BET.DEBUFF, max_stack=1, tag=f"{self.code}_ER", desc=self.name)


class ZoweOrellia(Gear):
    BASE_RARITY = R.SS
    nick = "오렐리아전장 전기"
    name = "원소의 심장(전기)"
    code = "ZoweOrellia"

    def isfit(self, char: 'Character'):
        return char.id_ == 205

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, 30 + 3 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.BATTLE_CONTINUATION, 1, d('.3') + d('.03') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.TAKEDMGDEC, 1, d('.3') + d('.03') * self.lvl, desc=self.name)
        elif tt == TR.HIT:
            if args.get("skill_no") == 2:
                targets = args.get("targets")
                for t in targets:
                    if targets[t]:
                        t.give_buff(BT.TAKEDMGINC, 1, d('.2') + d('.01') * self.lvl,
                                    data=D.DmgInfo(element=E.ELEC), round_=0, desc=self.name)
                        t.give_buff(BT.ELEMENT_RES[E.ELEC], 0, -50 - 3 * self.lvl,
                                    efft=BET.DEBUFF, max_stack=1, tag=f"{self.code}_ER", desc=self.name)


class LWLoader(Gear):
    nick = "경화기용 장전기"
    name = nick
    code = "LWLoader"
    val = [((d('8'), d('.8')), (d('12'), d('1.2')), (d('16'), d('1.6')), (d('20'), d('2'))),
           ((d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8')), (d('5'), d('1'))),
           (50, 55, 60, d('72.5'))]

    def isfit(self, char: 'Character'):
        return char.type_ == (CT.LIGHT, CR.ATTACKER)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ATTACK:
            chance = self.val[2][self.rarity] + d('2.5') * self.lvl
            if self.rarity == R.SS and self.lvl > 5:
                chance += d('.5') * (self.lvl - 5)
            self.owner.give_buff(BT.FOLLOW_ATTACK, 0, 1, data=D.FollowAttack(attacker=self, chance=chance),
                                 round_=1, max_stack=1, tag="LWLoader_FA", desc=self.name)


class AWThruster(Gear):
    nick = "공중화기용 추력기"
    name = nick
    code = "AWThruster"
    val = [((d('8'), d('.8')), (d('12'), d('1.2')), (d('16'), d('1.6')), (d('20'), d('2'))),
           ((d('2'), d('.4')), (d('3'), d('.6')), (d('4'), d('.8')), (d('5'), d('1'))),
           ((d('.07'), d('.02')), (d('.11'), d('.02')), (d('.15'), d('.02')), (d('.25'), d('.02')))]

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, self.val[0][self.rarity][0] + self.val[0][self.rarity][1] * self.lvl, removable=False),
            Buff(BT.CRIT, 0, self.val[1][self.rarity][0] + self.val[1][self.rarity][1] * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SKILL_RATE, 0,
                                 self.val[2][self.rarity][0] + self.val[2][self.rarity][1] * self.lvl, desc=self.name)


class CMDProtocol(Gear):
    BASE_RARITY = R.SS
    nick = "영전구슬"
    name = "응용 지휘 프로토콜"
    code = "CMDProtocol"

    def isfit(self, char: 'Character'):
        return char.type_[0] == CT.LIGHT

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, 15 + 3 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.RANGE_1SKILL, 0, -1, round_=1, desc=self.name)
            self.owner.give_buff(BT.RANGE_2SKILL, 0, 1, round_=1, desc=self.name)


class ImprovedAdvRadar(Gear):
    BASE_RARITY = R.SS
    nick = "영전망원조준"
    name = "시작형 망원 조준장치"
    code = "ImAdvRadar"
    val = [(0, 1, 2, 3, 4, 5, 7, 9, 11, 15, 19), (0, 1, 3, 5, 7, 9, 13, 17, 21, 25, 29)]

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.ATTACKER

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            if self.owner.getposy() == self.owner.isenemy * 2:
                self.owner.give_buff(BT.ACC, 0, 50 + 50 * self.val[0][self.lvl], round_=2, desc=self.name)
                self.owner.give_buff(BT.CRIT, 0, d('9.5') + d('.5') * self.val[1][self.lvl], desc=self.name)
                self.owner.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.ACC, efft=BET.DEBUFF),
                                     round_=2, desc=self.name)


class BattleAssist(Gear):
    BASE_RARITY = R.SS
    nick = "목뼈"
    name = "강행 전투 보조장치"
    code = "BattleASST"
    val = (0, 1, 2, 3, 4, 5, 10, 15, 20, 30, 45)

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.SPD, 0, d('.1') + d('.01') * self.val[self.lvl], removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, d('-.2') + d('.01') * self.lvl, desc=self.name)
            self.owner.give_buff(BT.ACT_PER_TURN, 0, 1, desc=self.name)


class SpikeShield(Gear):
    BASE_RARITY = R.SS
    nick = "변소방패"
    name = "스파이크 실드"
    code = "SpikeShield"
    val = [(0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16),
           (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14),
           (d('.3'), d('.6'), d('.9'), d('1.2'), d('1.5'), d('1.8'), d('2.1'), d('2.5'), d('3'), d('3.5'), d('4'))]

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.DEFENDER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 200 + 50 * self.val[0][self.lvl], removable=False),
            Buff(BT.DEF, 0, 50 + 5 * self.val[1][self.lvl], removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.SKILL_RATE, 1, self.val[2][self.lvl] / 100,
                                 proportion=(self, BT.DEF), desc=self.name)


class Backstab(OS):
    BASE_RARITY = R.SS
    nick = "암습OS"
    name = "암습형 전투 시스템"
    code = "Backstab"

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.ATTACKER
    
    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ATK, 1, d('.05') + d('.015') * self.lvl, round_=1 + (self.lvl == 10),
                                 desc=self.name)
            self.owner.give_buff(BT.SPD, 1, d('-.2') + d('.025') * self.lvl, round_=2, desc=self.name)
            self.owner.give_buff(BT.IGNORE_PROTECT, 0, 1, round_=1, desc=self.name)


class RebootAlpha(OS):
    BASE_RARITY = R.SS
    nick = "변소알파OS"
    name = "전장 리부트 시스템 알파"
    code = "RebootAlpha"
    
    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.DEF, 0, 100 + 10 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 5 + d('.5') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 10 + self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if self.owner.hp / self.owner.maxhp >= 1:
                self.owner.give_buff(BT.INABILLITY_SKILL, 0, 1, round_=1, desc=self.name)
                self.owner.give_buff(BT.DOT_DMG, 0, 10, round_=1, desc=self.name)


class RebootBeta(OS):
    BASE_RARITY = R.SS
    nick = "변소베타OS"
    name = "전장 리부트 시스템 베타"
    code = "RebootBeta"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.DEF, 0, 120 + 12 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 6 + d('.6') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 12 + d('1.2') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if self.owner.game.round % 2:  # ROUND_START 트리거는 Game.round 값이 증가하기 전에 발동됨
                self.owner.give_buff(BT.INABILLITY_SKILL, 0, 1, round_=1, desc=self.name)


class RebootGamma(OS):
    BASE_RARITY = R.SS
    nick = "변소감마OS"
    name = "전장 리부트 시스템 감마"
    code = "RebootGamma"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.DEF, 0, 120 + 12 * self.lvl, removable=False),
            Buff(BT.CRIT, 0, 6 + d('.6') * self.lvl, removable=False),
            Buff(BT.ACC, 0, 12 + d('1.2') * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            if not self.owner.game.round % 2:  # ROUND_START 트리거는 Game.round 값이 증가하기 전에 발동됨
                self.owner.give_buff(BT.INABILLITY_SKILL, 0, 1, round_=1, desc=self.name)


class WRII(OS):
    BASE_RARITY = R.SS
    nick = "WRII"
    name = "W.R.I.I 시스템"
    code = "Circulation"
    
    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.DEFENDER
    
    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 150 + 15 * self.lvl, removable=False),
            Buff(BT.DEF, 0, 100 + 10 * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.GET_ATTACKED:
            attacker = args.get("attacker")
            if attacker.get_stats(BT.DEF) < self.owner.get_stats(BT.DEF):
                attacker.give_buff(BT.ATK, 1, d('-.1') + d('-.03') * self.lvl, count=1, count_trig={TR.AFTER_SKILL, },
                                   desc=self.name)


class HotPack(Gear):
    BASE_RARITY = R.SS
    nick = "핫팩"
    name = nick
    code = "HotPack"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ELEMENT_RES[E.ICE], 0, 25 + d('2.5') * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.ELEMENT_MIN[E.ICE], 0, 10 + 2 * self.lvl, round_=3, desc=self.name)


class SEyePatch(Gear):
    BASE_RARITY = R.SS
    nick = "찐조전장"
    name = "핏빛안대 -혈화요란-"
    code = "SEyePatch"

    def isfit(self, char: 'Character'):
        return char.id_ == 240

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, 10 + self.lvl, removable=False),
            Buff(BT.ACC, 0, 20 + 2 * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.BATTLE_CONTINUATION, 1, d('.4') + d('.05') * self.lvl, desc="혈화요란")
            self.owner.give_buff(BT.COUNTER_ATTACK, 1, d('.5') + d('.06') * self.lvl, desc="혈화요란")


class SuperHeavyComplexArmor(Gear):
    BASE_RARITY = R.SS
    nick = "변소장갑"
    name = "초중량 복합장갑"
    code = "SHCA"
    val = [(0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16),
           (0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12),]

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.DEFENDER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 200 + 50 * self.val[0][self.lvl], removable=False),
            Buff(BT.DEF, 0, 30 + 10 * self.val[1][self.lvl], removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.ROOTED, 0, 1, round_=1, desc=self.name)
            self.owner.give_buff(BT.IMMUNE_BUFF, 0, 1, data=D.BuffCond(type_=BT.FORCE_MOVE, efft=BET.DEBUFF),
                                 round_=1, desc=self.name)
            self.owner.give_buff(BT.SPD, 1, d('-.3') + d('.015') * self.lvl, round_=1, desc=self.name)


class MiniFenrir(Gear):
    BASE_RARITY = R.SS
    nick = "미니 펜리르"
    name = nick
    code = "MiniFenrir"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.ACC, 0, 5 + 4 * self.lvl, removable=False),
        )

    def passive(self, tt, args=None):
        if tt == TR.ATTACK:
            self.owner.give_buff(BT.AP, 0, d('.5') + d('.05') * self.lvl, desc="고기 먹자, 고기!")


class MiniSnowFeather(Gear):
    BASE_RARITY = R.SS
    nick = "미니 페더"
    name = "미니 스노우 페더"
    code = "MiniSnowFeather"
    
    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.DEFENDER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, 10 + 5 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.owner.give_buff(BT.MINIMIZE_DMG, 0, 9999999, count=1, count_trig={TR.GET_HIT, },
                                 overlap_type=BOT.RENEW, desc="얼어붙은 날개")


class MiniPoi(Gear):
    BASE_RARITY = R.SS
    nick = "미니 포이"
    name = nick
    code = "MiniPoi"
    
    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.ATTACKER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.CRIT, 0, 10 + self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.DEFPEN, 0, d('.18') + d('.02') * self.lvl, desc="주인님의 옷!")


class MiniFrigga(Gear):
    BASE_RARITY = R.SS
    nick = "미니 프리가"
    name = nick
    code = "MiniFrigga"

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.DEFENDER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 500 + 50 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            self.owner.give_buff(BT.TAKEDMGDEC, 1, (d('.01') * self.lvl) or d('.005'), desc="꼬옥(?) 안기")


class MiniHirume(Gear):
    BASE_RARITY = R.SS
    nick = "미니 히루메"
    name = nick
    code = "MiniHirume"

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.EVA, 0, 10 + 2 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.WAVE_START:
            desc = "가..간지럽다앗!"
            self.owner.give_buff(BT.RACON, 0, 1, desc=desc)
            self.owner.give_buff(BT.SPD, 1, d('.05') + d('.005') * self.lvl, desc=desc)


class MiniBlackWyrm(Gear):
    BASE_RARITY = R.SS
    nick = "미니 블랙 웜"
    name = nick
    code = "MiniBlackWyrm"

    def isfit(self, char: 'Character'):
        return char.type_[1] == CR.DEFENDER

    def init_buff(self):
        self.buff = BuffList(
            Buff(BT.HP, 0, 250 + 25 * self.lvl, removable=False)
        )

    def passive(self, tt, args=None):
        if tt == TR.GET_HIT:
            attacker = args.get('attacker')
            if attacker.get_stats(BT.SPD) > self.owner.get_stats(BT.SPD):
                attacker.give_buff(BT.ELEMENT_RES[E.FIRE], 0, -10 - self.lvl, round_=1, efft=BET.DEBUFF,
                                   max_stack=1, tag=f"{self.code}_ER", desc="사전 제압")
