from enum import IntEnum


class Rarity(IntEnum):
    B = 0
    A = 1
    S = 2
    SS = 3
    SSS = 4


class CharType:
    LIGHT = 0
    HEAVY = 1
    FLY = 2
    desc = ["경장형", "중장형", "기동형"]


class CharRole:
    ATTACKER = 0
    DEFENDER = 1
    SUPPORTER = 2
    desc = ["공격기", "방어기", "지원기"]


class Element:
    PHYSICAL = 0
    FIRE = 1
    ICE = 2
    ELEC = 3
    desc = ["물리", "화염", "냉기", "전기"]


class BuffType:
    ATK = "공격력"
    DEF = "방어력"
    HP = "HP"
    ACC = "적중"
    EVA = "회피"
    CRIT = "치명타"
    STATS = (HP, ATK, DEF, ACC, EVA, CRIT)
    STATS_SET = set(STATS)
    
    SPD = "행동력"
    AP = "AP"
    RANGE = "사거리"
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
    ANTI_OS = ["대 경장 피해량", "대 중장 피해량", "대 기동 피해량"]
    ELEMENT_RES = ["물리 저항?", "화염 저항", "냉기 저항", "전기 저항"]
    ELEMENT_REV = ["물리 저항 반전?", "화염 저항 반전", "냉기 저항 반전", "전기 저항 반전"]
    ELEMENT_MIN = ["물리 저항 최소?", "화염 저항 최소", "냉기 저항 최소", "전기 저항 최소"]
    
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
    DOT_DMG = "지속 피해"
    INSTANT_DMG = "피해 (즉발)"
    FORCE_MOVE = "밀기 / 당기기"
    INABILLITY_SKILL = "스킬 사용 불가"
    INABILLITY_ACT = "행동 불가"
    
    GIMMICK = "기믹"
    RACON = "정찰"
    REMOVE_BUFF = "버프 제거"
    REMOVE_BUFF_RESIST = "버프 제거 저항"
    IMMUNE_BUFF = "버프 면역"

    WIDE_TAKEDMG = "광역 피해 분산"
    WIDE_GIVEDMG = "광역 피해 집중"


bufftypes = []
for x in dir(BuffType):
    if x.startswith('__') and x.endswith('__'):
        continue
    temp = getattr(BuffType, x)
    if isinstance(temp, list):
        bufftypes.extend(temp)
    elif isinstance(temp, str):
        bufftypes.append(temp)
    elif temp is None:
        continue
    del x, temp
BuffType.ANIT_OS_SET = set(BuffType.ANTI_OS)

BT_NOVAL = set()
for typestr in ('ROOTED', 'MARKED', 'PROVOKED', 'ROW_PROTECT', 'COLUMN_PROTECT', 'TARGET_PROTECT',
                'FOLLOW_ATTACK', 'COOP_ATTACK', 'IGNORE_BARRIER_DMGDEC', 'MINIMIZE_DMG', 'IMMUNE_DMG',
                'INABILLITY_SKILL', 'INABILLITY_ACT', 'GIMMICK', 'RACON', 'REMOVE_BUFF', 'IMMUNE_BUFF'):
    BT_NOVAL.add(getattr(BuffType, typestr))

BT_CYCLABLE = {*BuffType.STATS_SET, *BuffType.ELEMENT_RES, *BuffType.ELEMENT_MIN}
for typestr in ("SPD", "AP", "DEFPEN", "BARRIER", ):
    BT_CYCLABLE.add(getattr(BuffType, typestr))


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


class Trigger:
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
    ACT = "행동 시"
    DUMMY = "DUMMY"


TRIGGERS = []
TRIGGERS_REV = dict()
for x in dir(Trigger):
    if x.startswith('__') and x.endswith('__'):
        continue
    if x == "DUMMY":
        continue
    TRIGGERS.append(x)
    TRIGGERS_REV[getattr(Trigger, x)] = x
    del x


class Group:
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
    SMART_ENJOY = "스마트엔조이"
    
    PARASITE = '철충'
    SUMMON = '소환물'


class EquipType:
    CHIP = 0
    OS = 1
    GEAR = 2
    desc = ['칩', 'OS', '보조']


class BuffEffectType:
    BUFF = 0
    DEBUFF = 1
    NORMAL = 2
    desc = ['강화 효과', '해로운 효과', '일반 효과']


class Gimmick:
    PHOSPHIDE = "인화물 부착"
    PHOSPHIDE_DESC = "인화물 폭발"

    FLOOD = "침수"
    FLOOD_FIRE = "침수_화"
    FLOOD_ICE = "침수_냉"
    FLOOD_ELEC = "침수_전"

    CORROSION = "부식"

    LABIATA = "플라즈마 제너레이터"
    EMILY = "리미터 해제"
    PEREGRINUS_FALCON = "팔콘 폼"
    PEREGRINUS_HUMAN = "휴먼 폼"
    PEREGRINUS_READY = "모드 전환 준비"

    UNDER_WATCHER_GENERATOR_B05 = "충전_1"
    UNDER_WATCHER_GENERATOR_TU2 = "충전_2"
    
    Tyrant_Challenge_1 = "포식자_1"

    GOLTARION = "불사의 장갑"


GIMMICKS = set()
for x in dir(Gimmick):
    if x.startswith('__') and x.endswith('__'):
        continue
    GIMMICKS.add(x)
    del x

R = Rarity
CT = CharType
CR = CharRole
E = Element
BT = BuffType
TR = Trigger
ET = EquipType
BET = BuffEffectType
G = Gimmick

del IntEnum
