# LOsimul_API

> 작성 중인 문서입니다.

## 파일 구조 :

```
LOsimul
|-- API.md
|-- README.md
|-- cases
|   |-- 312_1.json
|   |-- 312_2.json
|   |-- 312_3.json
|   |-- 312_4.json
|   |-- 312titania.json
|   |-- 58.json
|   |-- 582.json
|   |-- 58emily.json
|   `-- blank.json
|-- data
|   |-- icons
|   |   |-- TbarIcon_3P_Alexandra_N.png
|   |   |-- TbarIcon_3P_Alexandra_NS1.png
|   |   |-- TbarIcon_3P_Alexandra_NS2.png
|   |   |-- TbarIcon_3P_Alice_N.png
|   |   `-- ...
|   `-- unitdata
|-- images
|   |-- add_button.png
|   |-- exit.png
|   |-- load_button.png
|   |-- question.png
|   |-- remove_button.png
|   |-- speed_button.png
|   `-- trigger_button.png
|-- lo_gui.py
|-- lo_gui_subwindows.py
|-- runGui.py
|-- lo_simul
|   |-- __init__.py
|   |-- characters
|   |   |-- __init__.py
|   |   |-- Alice.py
|   |   |-- Cerestia.py
|   |   `-- ...
|   |-- lo_char.py
|   |-- lo_enum.py
|   |-- lo_equips.py
|   |-- lo_imports.py
|   |-- lo_mod.py
|   `-- lo_system.py
`-- splash.png
```

- `lo_simul` : 전투 시뮬레이터 프로그램
- `lo_gui*.py`, `runGui.py` : GUI 프로그램
- `data/unitdata` : 캐릭터의 스탯, 스킬 등의 데이터 파일

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

---

> ## ⚠️ 경고 ⚠️
> **보호 매커니즘, 패시브 버프 적용 순서, 데미지 계산, 효과 저항 적용** 등등  
> 많은 부분에서 인게임과 많은 차이가 날 수 있습니다.  
> 차이가 나는 케이스를 개발자한테 전달하주시면 개발자에게 큰 힘이 됩니다!

---

# lo_simul.`lo_enum`

- ## `lo_enum.Rarity`<br>`lo_enum.R`
  등급. [`enum.IntEnum`]을 상속받습니다.
  
  |Variable|Value|
  |---|:---:|
  |`R.B`|0|
  |`R.A`|1|
  |`R.S`|2|
  |`R.SS`|3|
  |`R.SSS`|4|

- ## `lo_enum.CharType`<br>`lo_enum.CT`
  유닛 유형. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`CT.LIGHT`|0|경장형|
  |`CT.HEAVY`|1|중장형|
  |`CT.FLY`|2|기동형|

- ## `lo_enum.CharRole`<br>`lo_enum.CR`
  유닛 역할. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`CR.ATTACKER`|0|공격기|
  |`CR.DEFENDER`|1|보호기|
  |`CR.SUPPORTER`|2|지원기|

- ## `lo_enum.Element`<br>`lo_enum.E`
  속성. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.
  
  |Variable|Value|Description
  |---|:---:|:---:|
  |`E.PHYSICAL`|0|물리|
  |`E.FIRE`|1|화염|
  |`E.ICE`|2|냉기|
  |`E.ELEC`|3|전기|

- ## `lo_enum.BuffType`<br>`lo_enum.BT`
  버프 타입.  
  _<주의>_ [`enum.Enum`]을 상속받지 않습니다. 문자열을 직접 사용해도 전혀 문제가 되지 않습니다.
  ```python
  ...
  char.give_buff("공격력", 1, d(".1"))
  ...
  ```
  |Variable|Value|
  |---|:---:|
  |`BT.ATK`|공격력|
  |`BT.DEF`|방어력|
  |`BT.HP`|HP|
  |`BT.ACC`|적중|
  |`BT.EVA`|회피|
  |`BT.CRIT`|치명타|
  |`BT.SPD`|행동력|
  |`BT.AP`|AP|
  |`BT.CHANGE_AP`|AP 변경|
  |`BT.RANGE`|사거리|
  |`BT.RANGE_1SKILL`|1번 액티브 스킬 사거리|
  |`BT.RANGE_2SKILL`|2번 액티브 스킬 사거리|
  |`BT.SKILL_RATE`|스킬 위력|
  |`BT.GIVEDMGINC`|주는 피해 증가|
  |`BT.TAKEDMGINC`|받는 피해 증가|
  |`BT.GIVEDMGDEC`|주는 피해 감소|
  |`BT.TAKEDMGDEC`|받는 피해 감소|
  |`BT.COST`|출격 비용|
  |`BT.EXP`|경험치|
  |`BT.BUFFLVL`|벞디벞 레벨|
  |`BT.ROOTED`|이동 불가|
  |`BT.MARKED`|표식|
  |`BT.PROVOKED`|도발|
  |`BT.DEFPEN`|방어 관통|
  |`BT.ANTI_LIGHT`|대 경장 피해량|
  |`BT.ANTI_HEAVY`|대 중장 피해량|
  |`BT.ANTI_FLY`|대 기동 피해량|
  |`BT.FIRE_RES`|화염 저향|
  |`BT.ICE_RES`|냉기 저항|
  |`BT.ELEC_RES`|전기 저항|
  |`BT.FIRE_REV`|화염 저향 반전|
  |`BT.ICE_REV`|냉기 저항 반전|
  |`BT.ELEC_REV`|전기 저항 반전|
  |`BT.FIRE_MIN`|화염 저향 최소|
  |`BT.ICE_MIN`|냉기 저항 최소|
  |`BT.ELEC_MIN`|전기 저항 최소|
  |`BT.ROW_PROTECT`|행 보호|
  |`BT.COLUMN_PROTECT`|열 보호|
  |`BT.TARGET_PROTECT`|지정 보호|
  |`BT.FOLLOW_ATTACK`|지원 공격|
  |`BT.COOP_ATTACK`|협동 공격|
  |`BT.COUNTER_ATTACK`|반격|
  |`BT.ACTIVE_RATE`|효과 발동|
  |`BT.ACTIVE_RESIST`|효과 저항|
  |`BT.BARRIER`|방어막|
  |`BT.IGNORE_BARRIER_DMGDEC`|방어막 / 피해 감소 무시|
  |`BT.BATTLE_CONTINUATION`|전투 속행|
  |`BT.MINIMIZE_DMG`|피해 최소화|
  |`BT.IMMUNE_DMG`|피해 무효|
  |`BT.DOT_DMG`|지속 피해|
  |`BT.INSTANT_DMG`|피해 (즉발)|
  |`BT.FORCE_MOVE`|밀기 / 당기기|
  |`BT.INABILLITY_SKILL`|스킬 사용 불가|
  |`BT.INABILLITY_ACT`|행동 불가|
  |`BT.GIMMICK`|기믹|
  |`BT.RACON`|정찰|
  |`BT.REMOVE_BUFF`|버프 제거|
  |`BT.REMOVE_BUFF_RESIST`|버프 제거 저항|
  |`BT.IMMUNE_BUFF`|버프 면역|
  |`BT.IGNORE_PROTECT`|보호 무시|
  |`BT.ACT_PER_TURN`|턴당 행동 횟수|
  |`BT.WIDE_TAKEDMG`|광역 피해 분산|
  |`BT.WIDE_GIVEDMG`|광역 피해 집중|
  ### `BuffType` 추가 편의 변수들 (1)
  |Variable|Value|
  |---|:---:|
  |`BT.BASE_STATS`|`(BT.HP, BT.ATK, BT.DEF, BT.ACC, BT.EVA, BT.CRIT)`|
  |`BT.BASE_STATS_SET`|`BT.BASE_STATS`의 [frozenset]|
  |`BT.ANTI_OS`|`(BT.ANTI_LIGHT, BT.ANTI_HEAVY, BT.ANTI_FLY)`|
  |`BT.ELEMENT_RES`|`("물리 저항", BT.FIRE_RES, BT.ICE_RES, BT.ELEC_RES)`|
  |`BT.ELEMENT_REV`|`("물리 저항 반전", BT.FIRE_REV, BT.ICE_REV, BT.ELEC_REV)`|
  |`BT.ELEMENT_MIN`|`("물리 저항 최소", BT.FIRE_MIN, BT.ICE_MIN, BT.ELEC_MIN)`|   
  ### `BuffType` 추가 편의 변수들 (2)
  |Variable|Description|
  |---|:---:|
  |lo_enum.`bufftypes`|**모든** [`BuffType`]을 모아놓은 튜플.|
  |lo_enum.`BT_NOVAL`|**값이 필요 없는** [`BuffType`]을 모아놓은 [frozenset].|
  |lo_enum.`BT_CYCLABLE`|**비례할 수 있는 수치**를 모아놓은 [frozenset].<br>(체공방적회치, 속성 저항, 속성 저항 하한, 행동력, AP, 방관, 방어막)|

- ## `lo_enum.BuffOverlapType`<br>`lo_enum.BOT`
  버프 적용 방식. [`enum.IntEnum`]을 상속받습니다.  
  _<주의>_ 이 클래스는 desc 속성이 없으며, Description의 문자열을 얻을 수 없습니다.
  
  |Variable|Value|Description
  |---|:---:|:---:|
  |`BOT.NORMAL`|0|기본|
  |`BOT.SINGLE`|1|단일|
  |`BOT.UPDATE`|2|갱신|
  |`BOT.RENEW`|3|재생성|
  |`BOT.INSTANCE`|4|즉발|
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
  트리거 타입 모음.  [`str`], [`enum.Enum`]을 상속받습니다.

  |Variable|Value|
  |---|:---:|
  |`TR.ROUND_START`|라운드 시작 시|
  |`TR.ROUND_END`|라운드 종료 시|
  |`TR.WAVE_START`|전투 시작 시|
  |`TR.WAVE_END`|전투 종료 시|
  |`TR.ATTACK`|공격 시|
  |`TR.GET_ATTACKED`|공격 받을 시|
  |`TR.HIT`|공격 적중 시|
  |`TR.EXPECT_GET_HIT`|피격 예정 시|
  |`TR.GET_HIT`|피격 시|
  |`TR.EVADE`|회피 시|
  |`TR.ENEMY_DEAD`|적 사망 시|
  |`TR.KILL`|적 처치 시|
  |`TR.DEAD`|사망 시|
  |`TR.INCAPABLE`|전투 불능 시|
  |`TR.ALLY_DEAD`|아군이 사망하면|
  |`TR.ALLY_KILLED`|아군이 처치당하면|
  |`TR.BATTLE_CONTINUED`|전투 속행 시|
  |`TR.MOVE`|이동 시|
  |`TR.IDLE`|대기 시|
  |`TR.AFTER_SKILL`|스킬 사용 후|
  |`TR.AFTER_COUNTER`|반격 후|
  |`TR.AFTER_FOLLOW`|공격 지원 후|
  |`TR.AFTER_COOP`|협동 공격 후|
  |`TR.AFTER_HIT`|공격 적중 후|
  |`TR.ACT`|행동 시|
  |`TR.DUMMY`|DUMMY|

- ## `lo_enum.Group`
  소속 그룹 모음. [`str`], [`enum.Enum`]을 상속받습니다.

  |Variable|Value|
  |---|:---:|
  |`Group.AGENCY_080`|080팀|
  |`Group.GOLDEN_WORKERS`|골든 워커즈|
  |`Group.DOOM_BRINGER`|둠 브링어|
  |`Group.MONGUS`|몽구스 팀|
  |`Group.BATTLE_MAID`|배틀 메이드 프로젝트|
  |`Group.BERMUDA`|버뮤다 팀|
  |`Group.SKY_NIGHTS`|스카이 나이츠|
  |`Group.STRIKERS`|스트라이커즈|
  |`Group.STEEL_LINE`|스틸 라인|
  |`Group.VALHALLA`|시스터즈 오브 발할라|
  |`Group.CITY_GUARD`|시티가드|
  |`Group.ARMORED_MAIDEN`|아머드 메이든|
  |`Group.ANYWHERE`|애니웨어 시리즈|
  |`Group.HORDE`|앵거 오브 호드|
  |`Group.AMUSE_ATTENDANT`|어뮤즈 어텐던트|
  |`Group.ORBITAL_WATCHER`|오비탈 와쳐|
  |`Group.WATCHER_OF_NATURE`|와처 오브 네이쳐|
  |`Group.COMPANION`|컴페니언 시리즈|
  |`Group.KOUHEI`|코헤이 교단|
  |`Group.PUBLIC_SERVANT`|퍼블릭 서번트|
  |`Group.FAIRY`|페어리 시리즈|
  |`Group.HORIZEN`|호라이즌|
  |`Group.AA_CANNONIERS`|AA 캐노니어|
  |`Group.AGS`|AGS 로보테크|
  |`Group.D_ENTERTAINMENT`|D-엔터테이먼트|
  |`Group.BISMARK`|비스마르크 코퍼레이션|
  |`Group.SMART_ENJOY`|스마트엔조이|
  |`Group.PARASITE`|철충|
  |`Group.SUMMON`|소환물|

- ## `lo_enum.EquipType`<br>`lo_enum.ET`
  장비 타입. [`enum.IntEnum`]을 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`ET.CHIP`|0|칩|
  |`ET.OS`|1|OS|
  |`ET.GEAR`|2|보조|

- ## `lo_enum.BuffEffectType`<br>`lo_enum.BET`
  버프 효과 종류. [`enum.IntFlag`]를 상속받습니다.  
  `desc` 속성을 통해 Description의 문자열을 얻을 수 있습니다.

  |Variable|Value|Description
  |---|:---:|:---:|
  |`BET.BUFF`|1|강화 효과|
  |`BET.DEBUFF`|2|해로운 효과|
  |`BET.NORMAL`|4|일반 효과|

- ## `lo_enum.Gimmick`<br>`lo_enum.G`
  기믹 전용 텍스트 모음. 주로 `Buff` 생성 시 `tag`나 `desc` 매개변수에 쓰입니다.  
  [`str`], [`enum.Enum`]을 상속받습니다.

  |Variable|Value|
  |---|:---:|
  |`G.PHOSPHIDE`|인화물 부착|
  |`G.PHOSPHIDE_DESC`|인화물 폭발|
  |`G.FLOOD`|침수|
  |`G.FLOOD_FIRE`|침수_화|
  |`G.FLOOD_ICE`|침수_냉|
  |`G.FLOOD_ELEC`|침수_전|
  |`G.CORROSION`|부식|
  |`G.LABIATA`|플라즈마 제너레이터|
  |`G.EMILY`|리미터 해제|
  |`G.PEREGRINUS_FALCON`|팔콘 폼|
  |`G.PEREGRINUS_HUMAN`|휴먼 폼|
  |`G.PEREGRINUS_READY`|모드 전환 준비|
  |`G.UNDER_WATCHER_GENERATOR_B05`|충전_1|
  |`G.UNDER_WATCHER_GENERATOR_TU2`|충전_2|
  |`G.Tyrant_Challenge_1`|포식자_1|
  |`G.GOLTARION`|불사의 장갑|
  |`G.FREEZE`|빙결|
  |`G.AUSGJROWJS`|면허개전|

  - ### `lo_enum.GIMMICKS`
    모든 `Gimmick` 문자열을 모아놓은 frozenset.

---

# lo_simul.`lo_system`

전투 상황과 버프(Buff)가 구현되어있는 모듈입니다.

- ## `lo_system.Game()`
게임 판을 만듭니다.  
이후 캐릭터를 배치하거나 전투를 진행햐는 등의 행동을 할 수 있습니다.

- ### `Game.round`
  현재 라운드 숫자입니다.

- ### `Game.wave`
  현재 웨이브 숫자입니다.

- ### `Game.REAL_TIME`
  비례 수치 계산 방법입니다.   
  `True` = 버프를 계산할 때 수치를 불러와서 계산함   
  `False` = 버프를 부여할 때 수치를 불러와서 계산함

- ### _@property_ `Game.stream`
  메세지를 출력할 스트림을 설정합니다. (설정 가능)  
  기본값은 `sys.stdout`입니다.

- ### _@property_ `Game.random`
  게임 내 랜덤 이벤트에 사용되는 [`random.Random`](https://docs.python.org/ko/3/library/random.html#random.Random) 객체입니다.

- ### _@property_ `Game.enemy_all_down`
  적 필드에 아무도 없는 지 알 수 있습니다.

- ### `Game.put_char` *(self, c, field=None)*
  캐릭터를 배치합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`c`|`Character`|**배치할 캐릭터 개체**<br>배치할 위치에 캐릭터가 존재하면<br>해당 캐릭터는 [`remove_char`](#gameremove_char-self-c-msgfalse)로 제거됩니다.|
    |`field`|<code>[int] &#124; None</code>|**배치할 필드**<br>`0` = 아군<br>`1` = 적군<br>`None` = `c.isenemy`값|

- ### `Game.remove_char` *(self, c, msg=False)*
  캐릭터를 제거합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`c`|`Character`|**제거할 캐릭터 개체**<br>캐릭터가 배치되어 있지 않으면<br>[`ValueError`]를 일으킵니다.|
    |`msg`|[`bool`]|`True` 설정 시<br>제거 메세지를 출력합니다.|

- ### `Game.get_char` *(self, x, y=None, field=0)*
  해당 위치에 있는 캐릭터를 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`x`, `y`|[`int`], [`int`]<br>또는<br><code>[int] &#124; Tuple[[int], [int]] &#124; Pos</code>, `None`|**얻고자 하는 캐릭터의 위치**<br>2차원 좌표나 그리드 번호, 또는 `Pos`객체.|
    |`field`|[`int`]|**원하는 캐릭터의 필드**<br>`0` = 아군<br>`1` = 적군|
  - 예시
    ```python
    p = Pos(2, 1)
    assert g.get_char(2, 1) \        # x = 2     , y = 1
           == g.get_char((2, 1)) \   # x = (2, 1), y = None
           == g.get_char(7) \        # x = 7     , y = None
           == g.get_char(p)          # x = p     , y = None
    ```

- ### `Game.get_chars` *(self, aoe=None, field=0)*
  해당 위치에 있는 캐릭터들을 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`aoe`|<code>Iterable[[tuple][[int], [int]] &#124; [int] &#124; Pos]</code>|**얻고자 하는 범위 리스트**<br>각 요소는[`get_char`](#gameget_char-self-x-ynone-field0)의 인자로<br>사용될 수 있어야 합니다.|
    |`field`|[`int`]|**범위의 필드**<br>`0` = 아군<br>`1` = 적군|

  - |Return type|Description|
    |---|---|
    |<code>[dict][[tuple][[int], [int]], Character]</code>|(2차원 좌표, 캐릭터 개체)로 매핑된 딕셔너리입니다.|

- ### `Game.put_from_file` *(self, filename, field)*
  배치 정보가 저장된 파일을 불러와 저장합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`filename`|[`str`]|**배치 정보가 저장된 파일 경로**<br>JSON 파일이어야 합니다.<br>파일 구조는 표 아래를 참고하십시오.|
    |`field`|[`int`]|**배치하는 필드**<br>`0` = 아군<br>`1` = 적군|
  - `filename` 경로의 JSON 데이터 구조는 다음과 같아야 합니다.  
    ```json
    [
      { 0번 자리 데이터 },
      {},  // 1번 자리에는 캐릭터가 없음
      { 2번 자리 데이터 },
      // ...
      { 8번 자리 데이터 }
    ]
    ```
    각 자리의 데이터 구조는 다음과 같습니다.    
     ```json
     {
       "code": "3P_Labiata",  // 캐릭터 코드
       "args": {
         "rarity": 3,  // 등급; B~SS => 0~3, 생략 시 태생 등급
         "lvl": 96,  // 레벨; 1 이상의 정수, 생략 시 1
         "stat_lvl": [0, 100, 0, 20, 0, 50],  // 체공방적회치 스탯 포인트; 각 0 이상의 정수, 생략 시 ALL 0
         "skill_lvl": [10, 10, 10, 10, 10],  // 액티브 및 패시브 스킬 레벨; 각 1~10, 생략 시 ALL 1
         "equips": [  // 장비들
           ["공칩", 3, 10],  // 장비 이름, 등급(0~4), 레벨(0~10)
                             // 장비 이름은 lo_equips.py에서 원하는 장비의 nick 속성를 입력하십시오.
           null,  // 장비 미착용
           ...,
           ...
         ],  // (생략 시 ALL null)
         "link": 500,  //링크; 0 이상의 정수, 생략 시 0
         "full_link_bonus_no": 0,  // 풀링크 보너스; 인게임 내 리스트 순서대로 0~4 / null 또는 생략 시 선택 안 함
         "affection": 100,  // 호감도; 0 이상의 정수, 생략 시 0
         "pledge": false,  // 서약 여부; false/true, 생략 시 false
         "current_hp": 0  // 초기 HP 설정; 0 이상의 정수, 생략 또는 0 이하 시 최대치
       }
     }
     ```
     `LOsimul/cases` 폴더에 예시 JSON 파일들을 첨부하였으니 참고하시기 바랍니다.   
     >`58.json` = 메인5-8  
     `582.json` = 메인5-8ex  
     `58emily.json` = <a href="https://arca.live/b/lastorigin/36585033">이 공략글</a>의 에밀리 세팅  
     `312_n.json` = 메인3-1ex `n`웨이브  
     `312titania.json` = <a href="https://arca.live/b/lastorigin/43503283">이 공략글</a>의 티타니아 세팅

- ### `Game.trigger` *(self, trigtype=Trigger.DUMMY, ally_pos=None, enemy_pos=None, args=None)*
  ***트리거***를 발동합니다.    
  ***트리거***를 통해 조건부로 발동하는 패시브 버프들(예: 공격 시, 피격 시, 라운드 시작 시 등)을 발동할 수 있습니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`trigtype`|[`str`]([`Trigger`](#lo_enumtriggerbrlo_enumtr))|**트리거 타입**|
    |`ally_pos`, `enemy_pos`|<code>Iterable[[int] &#124; [tuple][[int], [int]] &#124; Pos]</code>|**트리거 순서**<br>순서대로 트리거 할 위치 배열.<br>`None`(기본값)은 `(0, 1, 2, ..., 8)`입니다.|
    |`args`|`Any`|트리거에 추가로 필요한 데이터.|
  - `ally_pos`, `enemy_pos`의 정확한 기본값은 <code>[lo_enum.BasicData](#lo_enumbasicdata).passive_order</code>에 저장되어 있습니다.
  - 적군 진영에 아무도 없고 <code>[Trigger].DUMMY</code>를 트리거하면 자동으로 웨이브를 종료합니다.([`Game.wave_end()`](#gamewave_startbrgamewave_endbrgameround_startbrgameround_end))   
  - 아군이 먼저 트리거됩니다. 즉, 트리거 순서는 `ally_pos`, `enemy_pos` 순입니다.

- ### `Game.get_targets` *(self, aoe, ignore_protect=False, field=0)*
  공격 범위를 입력받고 피격당하는 캐릭터들을 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`aoe`|<code>Iterable[[tuple][[int], [int]] &#124; [int] &#124; Pos]</code>|**공격 범위**<br>[`get_chars`](#gameget_chars-self-aoenone-field0)의 `aoe` 매개변수와 동일합니다.|
    |`ignore_protect`|[`bool`]|**트리거 순서**<br>순서대로 트리거 할 위치 배열.<br>`None`(기본값)은 `(0, 1, 2, ..., 8)`입니다.|
  
  - |Return type|Description|
    |---|---|
    |<code>[dict][[tuple]\[[int], [int]], [tuple]\[[str] &#124; None, Character]]</code>|각 2차원 좌표마다 보호 타입(`str`)과 실제 피격되는 캐릭터(`Character`)가 매핑된 딕셔너리입니다.<br>보호 타입이 `None`이면 보호를 받지 않았다는 뜻입니다.|

- ### `Game.use_skill` *(self, subjc, skill_no, objpos=None)*
  캐릭터의 행동을 지휘합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`subjc`|`Character`|**공격 캐릭터**<br>행동하는 캐릭터 개체입니다.|
    |`skill_no`|[`int`]|**행동 타입**<br>`1` = 액티브 1스킬<br>`2` = 액티브 2스킬<br>`3` = 이동<br>`4` = 대기|
    |`objpos`|<code>[int] &#124; [tuple][[int], [int]] &#124; Pos</code>|**목표 좌표**<br>대상 지정이 아닌 스킬 또는 대기이면 이 매개변수는 비워뇌도 됩니다.|
  - 만약 해당 스킬이 착탄 스킬이라면, 해당 스킬은 저장되었다가,   
    정해진 턴 이후 [`Game.round_end()`](#gamewave_startbrgamewave_endbrgameround_startbrgameround_end) 호출 시 <code>[Trigger].ROUND_END</code> 트리거 이전에 발동됩니다. 

- ### `Game.give_buff(...)`
  캐릭터에게 버프를 부여합니다.
  - |Parameter|Type|Default Value|Description|
    |---|---|---|---|
    |`target`|`Character`|*없음*|**버프를 받는 캐릭터**|
    |`type_`|[`str`]\([`BuffType`])|*없음*|**버프 타입**|
    |`opr`|[`int`]\(`0` or `1`)|*없음*|**버프 계산 타입**<br>`0` = 덧셈 / `1` = 곱셈|
    |`value`|<code>[int] &#124; [decimal.Decimal]</code>|*없음*|**버프 수치**|
    |`round_`|[`int`]|`sys.maxsize`|**지속 라운드**|
    |`count`|[`int`]|`sys.maxsize`|**횟수 제한**|
    |`count_trig`|<code>[set][[str] 또는 [Trigger]]</code>|`None`|**횟수 차감 트리거**<br>횟수(`count`)를 차감할 [`Trigger`]들의 집합입니다.|
    |`efft`|[`BuffEffectType`]|`BET.NORMAL`|**버프 효과 타입**<br>이로운(`BET.BUFF`), 해로운(`BET.DEBUFF`), 일반(`BET.NORMAL`)|
    |`max_stack`|[`int`]|`0`|**최대 중첩 수**<br>최대 중첩 수를 설정하려면 꼭 `tag` 매개변수도 설정해야 합니다.<br>`0` = 제한 없음|
    |`removable`|[`bool`]|`True`|**해제 가능 여부**<br>`False`로 설정하면 이 버프는 해제 버프로 해제할 수 없습니다.<br>이 버프를 해제하려면 `Character.remove_buff`를 사용해야 합니다.|
    |`tag`|[`str`]|`None`|**버프 태그**<br>특별한 버프를 구별할 아무 문자열입니다.|
    |`data`|`Datas`|`None`|**버프의 추가 데이터**<br>버프 적용에 필요한 추가적인 데이터입니다.|
    |`proportion`|<code>[tuple][Character, [BuffType]]</code>|`None`|**버프 비례 데이터**<br>버프가 어느 캐릭터의 어느 수치에 비례하는지를 입력합니다.|
    |`force`|[`bool`]|`False`|**강제 적용 여부**<br>`True`로 설정하면 효과 저항 등에 영향을 받지 않고 적용됩니다. (`chance`는 적용됨)|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|`100`|**적용 확률**<br>버프가 적용될 확률을 백분율로 입력합니다.|
    |`made_by`|`Character`|`None`|**버프를 발현한 캐릭터**<br>`None`이면 이 함수를 호출한 프레임의 `self`값을 얻어옵니다. (없으면 `None`)|
    |`do_print`|[`bool`]|`True`|**버프 적용 메세지 출력 여부**|

  - |Return type|Description|
    |---|---|
    |`Buff`|추가된 버프의 `Buff` 객체를 반환합니다.|
    |`None`|(버프 적용 실패 시)|

- ### `Game.wave_start()`<br>`Game.wave_end()`<br>`Game.round_start()`<br>`Game.round_end()`
  전투/라운드 시작/종료
  - 각각 <code>[TR].WAVE_START</code>, <code>[TR].WAVE_END</code>, <code>[TR].ROUND_START</code>, <code>[TR].ROUND_START</code> 트리거를 발동합니다.
  - 필드에 아/적군 아무도 없으면 발동되지 않습니다.
  > #### 주의
  > <code>[TR].ROUND_START</code> 트리거는 [`Game.round`](#gameround)가 증가되기 전에 발동됩니다.  
  > 예를 들어, <U>**3**</U>라운드를 시작하면서 <code>[TR].ROUND_START</code>가 트리거될 때 [`Game.round`](#gameround) 값은 <U>**2**</U>입니다.

- ### `Game.get_act_order` *(self, skill_uses=None)*<br>`Game.get_act_order_str` *(self, skill_uses=None)*
  캐릭터의 행동 순서를 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_uses`|<code>[dict][Character, Sequence[[int]]]</code>|**예약된 스킬 사용 데이터**<br>캐릭터마다 사용할 스킬을 모아놓은 딕셔너리입니다.<br>(예: `[1, 1, 2]` = 1번, 1번, 2번 스킬 예약)|

  - |Function|Return type|Description|
    |---|---|---|
    |`get_act_order`|<code>[list][[tuple][Character, [decimal.Decimal], [decimal.Decimal], [int]]]</code>|각 캐릭터의 AP, 행동력, 위치가 포함된 리스트를 반환합니다.<br>(오름차순).|
    |`get_act_order_str`|[`str`]|위 결과를 텍스트로 변환하여 반환합니다. 위치는 키패드 번호 배치를 따릅니다. (<code>[lo_enum.BasicData](#lo_enumbasicdata).keypad</code>)|
