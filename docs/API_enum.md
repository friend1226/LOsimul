[`enum.Enum`]: https://docs.python.org/ko/3/library/enum.html#enum.Enum
[`enum.IntEnum`]: https://docs.python.org/ko/3/library/enum.html#enum.IntEnum
[`enum.IntFlag`]: https://docs.python.org/ko/3/library/enum.html#enum.IntFlag
[int]: https://docs.python.org/ko/3/library/functions.html#int
[`int`]: https://docs.python.org/ko/3/library/functions.html#int
[str]: https://docs.python.org/ko/3/library/stdtypes.html#str
[`str`]: https://docs.python.org/ko/3/library/stdtypes.html#str
[`bool`]: https://docs.python.org/ko/3/library/functions.html#bool
[list]: https://docs.python.org/ko/3/library/stdtypes.html#list
[set]: https://docs.python.org/ko/3/library/stdtypes.html#set
[tuple]: https://docs.python.org/ko/3/library/stdtypes.html#tuple
[dict]: https://docs.python.org/ko/3/library/stdtypes.html#dict
[frozenset]: https://docs.python.org/ko/3/library/stdtypes.html#frozenset
[decimal.Decimal]: https://docs.python.org/ko/3/library/decimal.html#decimal.Decimal
[`decimal.Decimal`]: https://docs.python.org/ko/3/library/decimal.html#decimal.Decimal
[`ValueError`]: https://docs.python.org/ko/3/library/exceptions.html#ValueError

[`BuffType`]: #lo_enumbufftypelo_enumbt
[BuffType]: #lo_enumbufftypelo_enumbt
[`BuffEffectType`]: #lo_enumbuffeffecttypelo_enumbet
[BuffEffectType]: #lo_enumbuffeffecttypelo_enumbet
[`Trigger`]: #lo_enumtriggerlo_enumtr
[Trigger]: #lo_enumtriggerlo_enumtr
[TR]: #lo_enumtriggerlo_enumtr

# lo_simul.`lo_enum`

- ## `lo_enum.Rarity`<br>`lo_enum.R`
  등급. [`enum.IntEnum`]을 상속받습니다.
  
  |Variable|Value|
  |---|:---:|
  |`R.B`|`0`|
  |`R.A`|`1`|
  |`R.S`|`2`|
  |`R.SS`|`3`|
  |`R.SSS`|`4`|

- ## `lo_enum.CharType`<br>`lo_enum.CT`
  유닛 유형. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`CT.LIGHT`|`0`|경장형|
  |`CT.HEAVY`|`1`|중장형|
  |`CT.FLY`|`2`|기동형|

- ## `lo_enum.CharRole`<br>`lo_enum.CR`
  유닛 역할. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`CR.ATTACKER`|`0`|공격기|
  |`CR.DEFENDER`|`1`|보호기|
  |`CR.SUPPORTER`|`2`|지원기|

- ## `lo_enum.Element`<br>`lo_enum.E`
  속성. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.
  
  |Variable|Value|Description
  |---|:---:|:---:|
  |`E.PHYSICAL`|`0`|물리|
  |`E.FIRE`|`1`|화염|
  |`E.ICE`|`2`|냉기|
  |`E.ELEC`|`3`|전기|

- ## `lo_enum.BuffType`<br>`lo_enum.BT`
  버프 타입. [`str`], [`enum.Enum`]을 상속받습니다.   
  |Variable|Value|
  |---|:---:|
  |`BT.ATK`|`"공격력"`|
  |`BT.DEF`|`"방어력"`|
  |`BT.HP`|`"HP"`|
  |`BT.ACC`|`"적중"`|
  |`BT.EVA`|`"회피"`|
  |`BT.CRIT`|`"치명타"`|
  |`BT.SPD`|`"행동력"`|
  |`BT.AP`|`"AP"`|
  |`BT.CHANGE_AP`|`"AP 변경"`|
  |`BT.RANGE`|`"사거리"`|
  |`BT.RANGE_1SKILL`|`"1번 액티브 스킬 사거리"`|
  |`BT.RANGE_2SKILL`|`"2번 액티브 스킬 사거리"`|
  |`BT.SKILL_RATE`|`"스킬 위력"`|
  |`BT.GIVEDMGINC`|`"주는 피해 증가"`|
  |`BT.TAKEDMGINC`|`"받는 피해 증가"`|
  |`BT.GIVEDMGDEC`|`"주는 피해 감소"`|
  |`BT.TAKEDMGDEC`|`"받는 피해 감소"`|
  |`BT.COST`|`"출격 비용"`|
  |`BT.EXP`|`"경험치"`|
  |`BT.BUFFLVL`|`"벞디벞 레벨"`|
  |`BT.ROOTED`|`"이동 불가"`|
  |`BT.MARKED`|`"표식"`|
  |`BT.PROVOKED`|`"도발"`|
  |`BT.DEFPEN`|`"방어 관통"`|
  |`BT.ANTI_LIGHT`|`"대 경장 피해량"`|
  |`BT.ANTI_HEAVY`|`"대 중장 피해량"`|
  |`BT.ANTI_FLY`|`"대 기동 피해량"`|
  |`BT.FIRE_RES`|`"화염 저향"`|
  |`BT.ICE_RES`|`"냉기 저항"`|
  |`BT.ELEC_RES`|`"전기 저항"`|
  |`BT.FIRE_REV`|`"화염 저향 반전"`|
  |`BT.ICE_REV`|`"냉기 저항 반전"`|
  |`BT.ELEC_REV`|`"전기 저항 반전"`|
  |`BT.FIRE_MIN`|`"화염 저향 최소"`|
  |`BT.ICE_MIN`|`"냉기 저항 최소"`|
  |`BT.ELEC_MIN`|`"전기 저항 최소"`|
  |`BT.ROW_PROTECT`|`"행 보호"`|
  |`BT.COLUMN_PROTECT`|`"열 보호"`|
  |`BT.TARGET_PROTECT`|`"지정 보호"`|
  |`BT.FOLLOW_ATTACK`|`"지원 공격"`|
  |`BT.COOP_ATTACK`|`"협동 공격"`|
  |`BT.COUNTER_ATTACK`|`"반격"`|
  |`BT.ACTIVE_RATE`|`"효과 발동"`|
  |`BT.ACTIVE_RESIST`|`"효과 저항"`|
  |`BT.BARRIER`|`"방어막"`|
  |`BT.IGNORE_BARRIER_DMGDEC`|`"방어막 / 피해 감소 무시"`|
  |`BT.BATTLE_CONTINUATION`|`"전투 속행"`|
  |`BT.MINIMIZE_DMG`|`"피해 최소화"`|
  |`BT.IMMUNE_DMG`|`"피해 무효"`|
  |`BT.PHYSICAL_DOT_DMG`|`"지속 물리 피해"`|
  |`BT.FIRE_DOT_DMG`|`"지속 화염 피해"`|
  |`BT.ICE_DOT_DMG`|`"지속 냉기 피해"`|
  |`BT.ELEC_DOT_DMG`|`"지속 전기 피해"`|
  |`BT.INSTANT_DMG`|`"피해 (즉발)"`|
  |`BT.FORCE_MOVE`|`"밀기 / 당기기"`|
  |`BT.INABILLITY_SKILL`|`"스킬 사용 불가"`|
  |`BT.INABILLITY_ACT`|`"행동 불가"`|
  |`BT.GIMMICK`|`"기믹"`|
  |`BT.RACON`|`"정찰"`|
  |`BT.REMOVE_BUFF`|`"버프 제거"`|
  |`BT.REMOVE_BUFF_RESIST`|`"버프 제거 저항"`|
  |`BT.IMMUNE_BUFF`|`"버프 면역"`|
  |`BT.IGNORE_PROTECT`|`"보호 무시"`|
  |`BT.ACT_PER_TURN`|`"턴당 행동 횟수"`|
  |`BT.WIDE_TAKEDMG`|`"광역 피해 분산"`|
  |`BT.WIDE_GIVEDMG`|`"광역 피해 집중"`|
  ### `BuffType` 추가 편의 변수들
  |Variable|Value|
  |---|:---:|
  |lo_enum.`BUFFTYPES`|**모든** [`BuffType`]을 모아놓은 튜플.|
  |lo_enum.`BT_BASE_STATS`|`(BT.HP, BT.ATK, BT.DEF, BT.ACC, BT.EVA, BT.CRIT)`|
  |lo_enum.`BT_ANTI_OS`|`(BT.ANTI_LIGHT, BT.ANTI_HEAVY, BT.ANTI_FLY)`|
  |lo_enum.`BT_ELEMENT_RES`|`("물리 저항", BT.FIRE_RES, BT.ICE_RES, BT.ELEC_RES)`|
  |lo_enum.`BT_ELEMENT_REV`|`("물리 저항 반전", BT.FIRE_REV, BT.ICE_REV, BT.ELEC_REV)`|
  |lo_enum.`BT_ELEMENT_MIN`|`("물리 저항 최소", BT.FIRE_MIN, BT.ICE_MIN, BT.ELEC_MIN)`|
  |lo_enum.`BT_DOT_DMG`|`(BT.PHYSICAL_DOT_DMG, BT.FIRE_DOT_DMG, BT.ICE_DOT_DMG, BT.ELEC_DOT_DMG)`|
  |lo_enum.`BT_NOVAL`|**값이 필요 없는** [`BuffType`]을 모아놓은 [frozenset].|
  |lo_enum.`BT_CYCLABLE`|**비례할 수 있는 수치**를 모아놓은 [frozenset].<br>(체공방적회치, 속성 저항, 속성 저항 하한, 행동력, AP, 방관, 방어막)|

  `BT_BASE_STATS`, `BT_ANTI_OS`, `BT_ELEMENT_RES`, `BT_ELEMENT_REV`, `BT_ELEMENT_MIN`, `BT_DOT_DMG`는   
  각각의 [frozenset] 버전인 `BT_BASE_STATS_SET`, `BT_ANTI_OS_SET`, `BT_ELEMENT_RES_SET`, `BT_ELEMENT_REV_SET`, `BT_ELEMENT_MIN_SET`, `BT_DOT_DMG_SET`가 있습니다.

- ## `lo_enum.BuffOverlapType`<br>`lo_enum.BOT`
  버프 적용 방식. [`enum.IntEnum`]을 상속받습니다.  
  _<주의>_ 이 클래스는 desc 속성이 없으며, Description의 문자열을 얻을 수 없습니다.
  
  |Variable|Value|Description
  |---|:---:|:---:|
  |`BOT.NORMAL`|`0`|기본|
  |`BOT.SINGLE`|`1`|단일|
  |`BOT.UPDATE`|`2`|갱신|
  |`BOT.RENEW`|`3`|재생성|
  |`BOT.INSTANCE`|`4`|즉발|
  
  각 방식의 차이들은 [멸망 전의 전술 교본](https://lo.swaytwig.com)을 참고해 주십시오.

- ## `lo_enum.BasicData`
  |Variable|Description|
  |---|:---:|
  |`BasicData.passive_order`|패시브 발동 순서<br>(키패드 789456123)|
  |`BasicData.ally_act_order`|아군 행동 순서<br>(키패드 963852741)|
  |`BasicData.enemy_act_order`|적군 행동 순서<br>(키패드 147258369)|
  |`BasicData.act_order_idx`|위치-순서 매핑된 튜플|
  |`BasicData.act_order_revidx`|순서-위치 매핑된 튜플<br>(`ally_act_order` + `enemy_act_order`)|
  |`BasicData.keypad`|키패드 배치 튜플 `(7, 8, 9, 4, 5, 6, 1, 2, 3)`|
  |`BasicData.arange_all_abs`|액티브 스킬 전체 고정 범위 데이터|
  |`BasicData.arange_all_rel`|액티브 스킬 전체 비고정 범위 데이터|
  |`BasicData.prange_all_abs`|패시브 스킬 전체 고정 범위 데이터|
  |`BasicData.prange_all_rel`|패시브 스킬 전체 비고정 범위 데이터|

- ## `lo_enum.Trigger`<br>`lo_enum.TR` 
  트리거 타입 모음. [`str`], [`enum.Enum`]을 상속받습니다.

  |Variable|Value|
  |---|:---:|
  |`TR.ROUND_START`|`"라운드 시작 시"`|
  |`TR.ROUND_END`|`"라운드 종료 시"`|
  |`TR.WAVE_START`|`"전투 시작 시"`|
  |`TR.WAVE_END`|`"전투 종료 시"`|
  |`TR.ATTACK`|`"공격 시"`|
  |`TR.GET_ATTACKED`|`"공격 받을 시"`|
  |`TR.HIT`|`"공격 적중 시"`|
  |`TR.EXPECT_GET_HIT`|`"피격 예정 시"`|
  |`TR.GET_HIT`|`"피격 시"`|
  |`TR.EVADE`|`"회피 시"`|
  |`TR.ENEMY_DEAD`|`"적 사망 시"`|
  |`TR.KILL`|`"적 처치 시"`|
  |`TR.DEAD`|`"사망 시"`|
  |`TR.INCAPABLE`|`"전투 불능 시"`|
  |`TR.ALLY_DEAD`|`"아군이 사망하면"`|
  |`TR.ALLY_KILLED`|`"아군이 처치당하면"`|
  |`TR.BATTLE_CONTINUED`|`"전투 속행 시"`|
  |`TR.MOVE`|`"이동 시"`|
  |`TR.IDLE`|`"대기 시"`|
  |`TR.AFTER_SKILL`|`"스킬 사용 후"`|
  |`TR.AFTER_COUNTER`|`"반격 후"`|
  |`TR.AFTER_FOLLOW`|`"공격 지원 후"`|
  |`TR.AFTER_COOP`|`"협동 공격 후"`|
  |`TR.AFTER_HIT`|`"공격 적중 후"`|
  |`TR.ACT`|`"행동 시"`|
  |`TR.DUMMY`|`"DUMMY"`|

- ## `lo_enum.Group`
  소속 그룹 모음. [`str`], [`enum.Enum`]을 상속받습니다.

  |Variable|Value|
  |---|:---:|
  |`Group.AGENCY_080`|`"080팀"`|
  |`Group.GOLDEN_WORKERS`|`"골든 워커즈"`|
  |`Group.DOOM_BRINGER`|`"둠 브링어"`|
  |`Group.MONGUS`|`"몽구스 팀"`|
  |`Group.BATTLE_MAID`|`"배틀 메이드 프로젝트"`|
  |`Group.BERMUDA`|`"버뮤다 팀"`|
  |`Group.SKY_NIGHTS`|`"스카이 나이츠"`|
  |`Group.STRIKERS`|`"스트라이커즈"`|
  |`Group.STEEL_LINE`|`"스틸 라인"`|
  |`Group.VALHALLA`|`"시스터즈 오브 발할라"`|
  |`Group.CITY_GUARD`|`"시티가드"`|
  |`Group.ARMORED_MAIDEN`|`"아머드 메이든"`|
  |`Group.ANYWHERE`|`"애니웨어 시리즈"`|
  |`Group.HORDE`|`"앵거 오브 호드"`|
  |`Group.AMUSE_ATTENDANT`|`"어뮤즈 어텐던트"`|
  |`Group.ORBITAL_WATCHER`|`"오비탈 와쳐"`|
  |`Group.WATCHER_OF_NATURE`|`"와처 오브 네이쳐"`|
  |`Group.COMPANION`|`"컴페니언 시리즈"`|
  |`Group.KOUHEI`|`"코헤이 교단"`|
  |`Group.PUBLIC_SERVANT`|`"퍼블릭 서번트"`|
  |`Group.FAIRY`|`"페어리 시리즈"`|
  |`Group.HORIZEN`|`"호라이즌"`|
  |`Group.AA_CANNONIERS`|`"AA 캐노니어"`|
  |`Group.AGS`|`"AGS 로보테크"`|
  |`Group.D_ENTERTAINMENT`|`"D-엔터테이먼트"`|
  |`Group.BISMARK`|`"비스마르크 코퍼레이션"`|
  |`Group.SMART_ENJOY`|`"스마트엔조이"`|
  |`Group.PARASITE`|`"철충"`|
  |`Group.SUMMON`|`"소환물"`|

- ## `lo_enum.EquipType`<br>`lo_enum.ET`
  장비 타입. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`ET.CHIP`|`0`|칩|
  |`ET.OS`|`1`|OS|
  |`ET.GEAR`|`2`|보조|

- ## `lo_enum.BuffEffectType`<br>`lo_enum.BET`
  버프 효과 종류. [`enum.IntFlag`]를 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`BET.BUFF`|`1`|강화 효과|
  |`BET.DEBUFF`|`2`|해로운 효과|
  |`BET.NORMAL`|`4`|일반 효과|

- ## `lo_enum.Gimmick`<br>`lo_enum.G`
  기믹 전용 텍스트 모음. 주로 `Buff` 생성 시 `tag`나 `desc` 매개변수에 쓰입니다.  
  [`str`], [`enum.Enum`]을 상속받습니다.

  |Variable|Value|Note|
  |---|:---:|:---:|
  |`G.PHOSPHIDE`|`"인화물 부착"`|
  |`G.PHOSPHIDE_DESC`|`"인화물 폭발"`|
  |`G.FLOOD`|`"침수"`|<sup>[1]</sup>
  |`G.FLOOD_FIRE`|`"침수_화"`|<sup>[2]</sup>
  |`G.FLOOD_ICE`|`"침수_냉"`|<sup>[2]</sup>
  |`G.FLOOD_ELEC`|`"침수_전"`|<sup>[2]</sup>
  |`G.CORROSION`|`"부식"`|<sup>[1]</sup>
  |`G.CORROSION_SPD`|`"부식_행동력"`|<sup>[2]</sup>
  |`G.CORROSION_DEF`|`"부식_방어력"`|<sup>[2]</sup>
  |`G.CORROSION_DOT`|`"부식_지속피해"`|<sup>[2]</sup>
  |`G.LABIATA`|`"플라즈마 제너레이터"`|
  |`G.EMILY`|`"리미터 해제"`|
  |`G.PEREGRINUS_FALCON`|`"팔콘 폼"`|
  |`G.PEREGRINUS_HUMAN`|`"휴먼 폼"`|
  |`G.PEREGRINUS_READY`|`"모드 전환 준비"`|
  |`G.UNDER_WATCHER_GENERATOR_B05`|`"충전_1"`|
  |`G.UNDER_WATCHER_GENERATOR_TU2`|`"충전_2"`|
  |`G.Tyrant_Challenge_1`|`"포식자_1"`|
  |`G.GOLTARION`|`"불사의 장갑"`|
  |`G.FREEZE`|`"빙결"`|
  |`G.AUSGJROWJS`|`"면허개전"`|

  [1]: #footnote1
  [2]: #footnote2
  <sup><b id="footnote1">1</b></sup> (보통) 검색 태그로 사용  
  <sup><b id="footnote2">2</b></sup> (보통) 실제 태그로 사용

  - ### `lo_enum.GIMMICKS`
    모든 `Gimmick` 문자열을 모아놓은 [frozenset].
