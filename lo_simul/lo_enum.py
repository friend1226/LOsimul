from enum import IntEnum, IntFlag, Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class Rarity(IntEnum):
    B = 0
    A = 1
    S = 2
    SS = 3
    SSS = 4


_CharType_desc = ("경장형", "중장형", "기동형")
_CharRole_desc = ("공격기", "방어기", "지원기")
_Element_desc = ("물리", "화염", "냉기", "전기")
_EquipType_desc = ('칩', 'OS', '보조')
_BuffEffectType_desc = {
    1: '강화 효과',
    2: '해로운 효과',
    4: '일반 효과'
}


class CharType(IntEnum):
    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.desc = _CharType_desc[obj.value]
        return obj

    LIGHT = 0
    HEAVY = 1
    FLY = 2


class CharRole(IntEnum):
    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.desc = _CharRole_desc[obj.value]
        return obj

    ATTACKER = 0
    DEFENDER = 1
    SUPPORTER = 2


class Element(IntEnum):
    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.desc = _Element_desc[obj.value]
        return obj
    
    @classmethod
    def _missing_(cls, value: object):
        return cls.PHYSICAL

    PHYSICAL = 0
    FIRE = 1
    ICE = 2
    ELEC = 3


class BuffType(StrEnum):
    def __init__(self, *args):
        try:
            self.element = Element.__getitem__(self.name.partition("_")[0])
        except KeyError:
            self.element = Element.PHYSICAL
    
    ATK = "공격력"
    DEF = "방어력"
    HP = "HP"
    ACC = "적중"
    EVA = "회피"
    CRIT = "치명타"

    SPD = "행동력"
    AP = "AP"
    CHANGE_AP = "AP 변경"
    RANGE = "사거리"
    RANGE_1SKILL = "1번 액티브 스킬 사거리"
    RANGE_2SKILL = "2번 액티브 스킬 사거리"
    SKILL_RATE = "스킬 위력"

    GIVEDMGINC = "주는 피해 증가"
    TAKEDMGINC = "받는 피해 증가"
    GIVEDMGDEC = "주는 피해 감소"
    TAKEDMGDEC = "받는 피해 감소"

    COST = "출격 비용"
    EXP = "경험치"
    BUFFLVL = "벞디벞 레벨"

    ROOTED = "이동 불가"
    MARKED = "표식"
    PROVOKED = "도발"

    DEFPEN = "방어 관통"
    ANTI_LIGHT = "대 경장 피해량"
    ANTI_HEAVY = "대 중장 피해량"
    ANTI_FLY = "대 기동 피해량"

    PHYSICAL_RES = "물리 저항"
    FIRE_RES = "화염 저향"
    ICE_RES = "냉기 저항"
    ELEC_RES = "전기 저항"
    PHYSICAL_REV = "물리 저항 반전"
    FIRE_REV = "화염 저향 반전"
    ICE_REV = "냉기 저항 반전"
    ELEC_REV = "전기 저항 반전"
    PHYSICAL_MIN = "물리 저항 최소"
    FIRE_MIN = "화염 저향 최소"
    ICE_MIN = "냉기 저항 최소"
    ELEC_MIN = "전기 저항 최소"

    ROW_PROTECT = "행 보호"
    COLUMN_PROTECT = "열 보호"
    TARGET_PROTECT = "지정 보호"
    FOLLOW_ATTACK = "지원 공격"
    COOP_ATTACK = "협동 공격"
    COUNTER_ATTACK = "반격"

    ACTIVE_RATE = "효과 발동"
    ACTIVE_RESIST = "효과 저항"

    BARRIER = "방어막"
    IGNORE_BARRIER_DMGDEC = "방어막 / 피해 감소 무시"
    BATTLE_CONTINUATION = "전투 속행"
    MINIMIZE_DMG = "피해 최소화"
    IMMUNE_DMG = "피해 무효"
    PHYSICAL_DOT_DMG = "지속 물리 피해"
    FIRE_DOT_DMG = "지속 화염 피해"
    ICE_DOT_DMG = "지속 냉기 피해"
    ELEC_DOT_DMG = "지속 전기 피해"
    INSTANT_DMG = "피해 (즉발)"
    FORCE_MOVE = "밀기 / 당기기"
    INABILLITY_SKILL = "스킬 사용 불가"
    INABILLITY_ACT = "행동 불가"

    GIMMICK = "기믹"
    RACON = "정찰"
    REMOVE_BUFF = "버프 제거"
    REMOVE_BUFF_RESIST = "버프 제거 저항"
    IMMUNE_BUFF = "버프 면역"
    IGNORE_PROTECT = "보호 무시"
    ACT_PER_TURN = "턴당 행동 횟수"

    WIDE_TAKEDMG = "광역 피해 분산"
    WIDE_GIVEDMG = "광역 피해 집중"

BT_BASE_STATS = (BuffType.HP, BuffType.ATK, BuffType.DEF, BuffType.ACC, BuffType.EVA, BuffType.CRIT)
BT_ANTI_OS = (BuffType.ANTI_LIGHT, BuffType.ANTI_HEAVY, BuffType.ANTI_FLY)
BT_ELEMENT_RES = (BuffType.PHYSICAL_RES, BuffType.FIRE_RES, BuffType.ICE_RES, BuffType.ELEC_RES)
BT_ELEMENT_REV = (BuffType.PHYSICAL_REV, BuffType.FIRE_REV, BuffType.ICE_REV, BuffType.ELEC_REV)
BT_ELEMENT_MIN = (BuffType.PHYSICAL_MIN, BuffType.FIRE_MIN, BuffType.ICE_MIN, BuffType.ELEC_MIN)
BT_DOT_DMG = (BuffType.PHYSICAL_DOT_DMG, BuffType.FIRE_DOT_DMG, BuffType.ICE_DOT_DMG, BuffType.ELEC_DOT_DMG)
BT_BASE_STATS_SET = frozenset(BT_BASE_STATS)
BT_ANTI_OS_SET = frozenset(BT_ANTI_OS)
BT_ELEMENT_RES_SET = frozenset(BT_ELEMENT_RES)
BT_ELEMENT_REV_SET = frozenset(BT_ELEMENT_REV)
BT_ELEMENT_MIN_SET = frozenset(BT_ELEMENT_MIN)
BT_DOT_DMG_SET = frozenset(BT_DOT_DMG)

BT_NOVAL = set()
for _typestr in ('ROOTED', 'MARKED', 'PROVOKED', 'ROW_PROTECT', 'COLUMN_PROTECT', 'TARGET_PROTECT',
                 'FOLLOW_ATTACK', 'COOP_ATTACK', 'IGNORE_BARRIER_DMGDEC', 'IMMUNE_DMG',
                 'INABILLITY_SKILL', 'INABILLITY_ACT', 'GIMMICK', 'RACON', 'REMOVE_BUFF', 'IMMUNE_BUFF',
                 'IGNORE_PROTECT', 'GIMMICK'):
    BT_NOVAL.add(BuffType[_typestr])
BT_NOVAL = frozenset(BT_NOVAL)

BT_CYCLABLE = {*BT_BASE_STATS_SET, *BT_ELEMENT_RES, *BT_ELEMENT_MIN}
for _typestr in ("SPD", "AP", "DEFPEN", "BARRIER", ):
    BT_CYCLABLE.add(BuffType[_typestr])
BT_CYCLABLE = frozenset(BT_CYCLABLE)


class BuffOverlapType(IntEnum):
    NORMAL = 0  # 기본
    SINGLE = 1  # 단일
    UPDATE = 2  # 갱신
    RENEW = 3  # 재생성
    INSTANCE = 4  # 즉발


class BasicData:
    passive_order = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    ally_act_order = (2, 5, 8, 1, 4, 7, 0, 3, 6)
    enemy_act_order = (0, 3, 6, 1, 4, 7, 2, 5, 8)

    act_order_idx = (6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 12, 15, 10, 13, 16, 11, 14, 17)
    act_order_revidx = ally_act_order + enemy_act_order

    keypad = (7, 8, 9, 4, 5, 6, 1, 2, 3)

    arange_all_abs = ((0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 1), (1, 2, 1), (2, 0, 1), (2, 1, 1), (2, 2, 1))
    arange_all_rel = ((-1, -1, 1), (-1, 0, 1), (-1, 1, 1), (0, -1, 1), (0, 0, 1), (0, 1, 1),
                      (1, -1, 1), (1, 0, 1), (1, 1, 1))

    prange_all_abs = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))
    prange_all_rel = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))


class Trigger(StrEnum):
    ROUND_START = "라운드 시작 시"
    ROUND_END = "라운드 종료 시"
    WAVE_START = "전투 시작 시"
    WAVE_END = "전투 종료 시"

    ATTACK = "공격 시"
    GET_ATTACKED = "공격 받을 시"
    HIT = "공격 적중 시"
    EXPECT_GET_HIT = "피격 예정 시"
    GET_HIT = "피격 시"
    EVADE = "회피 시"

    ENEMY_DEAD = "적 사망 시"
    KILL = "적 처치 시"
    DEAD = "사망 시"
    INCAPABLE = "전투 불능 시"
    ALLY_DEAD = "아군이 사망하면"
    ALLY_KILLED = "아군이 처치당하면"

    BATTLE_CONTINUED = "전투 속행 시"
    MOVE = "이동 시"
    IDLE = "대기 시"

    AFTER_SKILL = "스킬 사용 후"
    AFTER_COUNTER = "반격 후"
    AFTER_FOLLOW = "공격 지원 후"
    AFTER_COOP = "협동 공격 후"
    AFTER_HIT = "공격 적중 후"
    ACT = "행동 시"
    DUMMY = "DUMMY"


class Group(StrEnum):
    AGENCY_080 = '080팀'
    GOLDEN_WORKERS = '골든 워커즈'
    DOOM_BRINGER = '둠 브링어'
    MONGUS = '몽구스 팀'
    BATTLE_MAID = '배틀 메이드 프로젝트'
    BERMUDA = '버뮤다 팀'
    SKY_NIGHTS = '스카이 나이츠'
    STRIKERS = '스트라이커즈'
    STEEL_LINE = '스틸 라인'
    VALHALLA = '시스터즈 오브 발할라'
    CITY_GUARD = '시티가드'
    ARMORED_MAIDEN = '아머드 메이든'
    ANYWHERE = '애니웨어 시리즈'
    HORDE = '앵거 오브 호드'
    AMUSE_ATTENDANT = '어뮤즈 어텐던트'
    ORBITAL_WATCHER = '오비탈 와쳐'
    WATCHER_OF_NATURE = '와처 오브 네이쳐'
    COMPANION = '컴페니언 시리즈'
    KOUHEI = '코헤이 교단'
    PUBLIC_SERVANT = '퍼블릭 서번트'
    FAIRY = '페어리 시리즈'
    HORIZEN = '호라이즌'
    AA_CANNONIERS = 'AA 캐노니어'
    AGS = 'AGS 로보테크'
    D_ENTERTAINMENT = 'D-엔터테이먼트'
    BISMARK = '비스마르크 코퍼레이션'
    SMART_ENJOY = '스마트엔조이'

    PARASITE = '철충'
    SUMMON = '소환물'


class EquipType(IntEnum):
    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.desc = _EquipType_desc[obj.value]
        return obj

    CHIP = 0
    OS = 1
    GEAR = 2


class BuffEffectType(IntFlag):
    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.desc = _BuffEffectType_desc[obj.value]
        return obj

    BUFF = 1
    DEBUFF = 2
    NORMAL = 4


class Gimmick(StrEnum):
    PHOSPHIDE = "인화물 부착"
    PHOSPHIDE_DESC = "인화물 폭발"

    FLOOD = "침수"
    FLOOD_FIRE = "침수_화"
    FLOOD_ICE = "침수_냉"
    FLOOD_ELEC = "침수_전"

    CORROSION = "부식"
    CORROSION_SPD = "부식_행동력"
    CORROSION_DEF = "부식_방어력"
    CORROSION_DOT = "부식_지속피해"

    LABIATA = "플라즈마 제너레이터"
    EMILY = "리미터 해제"
    PEREGRINUS_FALCON = "팔콘 폼"
    PEREGRINUS_HUMAN = "휴먼 폼"
    PEREGRINUS_READY = "모드 전환 준비"

    UNDER_WATCHER_GENERATOR_B05 = "충전_1"
    UNDER_WATCHER_GENERATOR_TU2 = "충전_2"
    
    Tyrant_Challenge_1 = "포식자_1"

    GOLTARION = "불사의 장갑"
    
    FREEZE = "빙결"

    AUSGJROWJS = "면허개전"
    
    DRAGON_STANDBY = "포격 대기"
    DRAGON_BOMBARDMENT = "함대 포격 모드"


GIMMICKS = set()
for _x in dir(Gimmick):
    if _x.startswith('__') and _x.endswith('__'):
        continue
    GIMMICKS.add(_x)
GIMMICKS = frozenset(GIMMICKS)

R = Rarity
CT = CharType
CR = CharRole
E = Element
BT = BuffType
BOT = BuffOverlapType
TR = Trigger
ET = EquipType
BET = BuffEffectType
G = Gimmick

del IntEnum, IntFlag, Enum, StrEnum
