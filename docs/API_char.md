[`enum.Enum`]: https://docs.python.org/ko/3/library/enum.html#enum.Enum
[`enum.IntEnum`]: https://docs.python.org/ko/3/library/enum.html#enum.IntEnum
[`enum.IntFlag`]: https://docs.python.org/ko/3/library/enum.html#enum.IntFlag
[int]: https://docs.python.org/ko/3/library/functions.html#int
[`int`]: https://docs.python.org/ko/3/library/functions.html#int
[str]: https://docs.python.org/ko/3/library/stdtypes.html#str
[`str`]: https://docs.python.org/ko/3/library/stdtypes.html#str
[bool]: https://docs.python.org/ko/3/library/functions.html#bool
[`bool`]: https://docs.python.org/ko/3/library/functions.html#bool
[list]: https://docs.python.org/ko/3/library/stdtypes.html#list
[set]: https://docs.python.org/ko/3/library/stdtypes.html#set
[tuple]: https://docs.python.org/ko/3/library/stdtypes.html#tuple
[dict]: https://docs.python.org/ko/3/library/stdtypes.html#dict
[frozenset]: https://docs.python.org/ko/3/library/stdtypes.html#frozenset
[decimal.Decimal]: https://docs.python.org/ko/3/library/decimal.html#decimal.Decimal
[`decimal.Decimal`]: https://docs.python.org/ko/3/library/decimal.html#decimal.Decimal
[`ValueError`]: https://docs.python.org/ko/3/library/exceptions.html#ValueError
[Collection]: https://docs.python.org/ko/3/library/collections.abc.html#collections.abc.Collection
[Sequence]: https://docs.python.org/ko/3.10/library/collections.abc.html#collections.abc.Sequence
[Callable]: https://docs.python.org/ko/3.10/library/typing.html#callable
[`MappingProxyType`]: https://docs.python.org/ko/3.10/library/types.html#types.MappingProxyType
[MappingProxyType]: https://docs.python.org/ko/3.10/library/types.html#types.MappingProxyType

[`BuffType`]: ./API_enum.md#lo_enumbufftypelo_enumbt
[BuffType]: ./API_enum.md#lo_enumbufftypelo_enumbt
[BT]: ./API_enum.md#lo_enumbufftypelo_enumbt
[`BuffOverlapType`]: ./API_enum.md#lo_enumbuffoverlaptypelo_enumbot
[BOT]: ./API_enum.md#lo_enumbuffoverlaptypelo_enumbot
[`BuffEffectType`]: ./API_enum.md#lo_enumbuffeffecttypelo_enumbet
[BuffEffectType]: ./API_enum.md#lo_enumbuffeffecttypelo_enumbet
[`Trigger`]: ./API_enum.md#lo_enumtriggerlo_enumtr
[Trigger]: ./API_enum.md#lo_enumtriggerlo_enumtr
[TR]: ./API_enum.md#lo_enumtriggerlo_enumtr
[CharType]: ./API_enum.md#lo_enumchartypelo_enumct
[CharRole]: ./API_enum.md#lo_enumcharrolelo_enumcr
[`EquipType`]: ./API_enum.md#lo_enumequiptypelo_enumet
[EquipType]: ./API_enum.md#lo_enumequiptypelo_enumet
[`Rarity`]: ./API_enum.md#lo_enumraritylo_enumr
[Rarity]: ./API_enum.md#lo_enumraritylo_enumr
[`Element`]: ./API_enum.md#lo_enumelementlo_enume
[Element]: ./API_enum.md#lo_enumelementlo_enume

[`Game`]: ./API_system.md#lo_systemgame
[`Buff`]: ./API_system.md#lo_systembuff
[Buff]: ./API_system.md#lo_systembuff
[`BuffList`]: ./API_system.md#lo_systembufflist

[Character]: ./API_char.md#lo_charcharacter
[`Character`]: ./API_char.md#lo_charcharacter
[Pos]: ./API_imports.md#lo_importspos
[`Pos`]: ./API_imports.md#lo_importspos

[Equip]: ./API_equips.md#lo_equipsequip

# lo_simul.`lo_char`

캐릭터 클래스가 구현되어있는 모듈입니다.

---

## `lo_char.CharacterPools`<br>`lo_char.CP`
모든 [`Character`] 서브 클래스를 관리하기 위한 클래스입니다.

- |Attribute|Type|Description|
  |---|---|---|
  |`CharacterPools.ALL_CODES`|<code>[dict]\[[str], Type\[[Character]]]</code>|`Character.code`을 키로 가지는 딕셔너리입니다.|
  |`CharacterPools.ALL`|<code>[dict]\[[str] &#124; [int], Type\[[Character]]]</code>|`Character.name`, 클래스 이름, 또는 캐릭터 도감 번호를 키로 가지는 딕셔너리입니다.|
  |`CharacterPools.ALLY`|<code>[dict]\[[str], Type\[[Character]]]</code>|`Character.name`을 키로 가지는 딕셔너리입니다. (`Character.isenemy`가 `False`인 값만)|
  |`CharacterPools.ENEMY`|<code>[dict]\[[str], Type\[[Character]]]</code>|`Character.name`을 키로 가지는 딕셔너리입니다. (`Character.isenemy`가 `True`인 값만)|

### `CharacterPools.get` *(s)*
캐릭터의 코드, 이름, 도감 번호, 또는 클래스 이름으로 캐릭터 클래스를 찾아주는 함수입니다.

- |Parameter|Type|Description|
  |---|---|---|
  |`s`|<code>[str] &#124; [int]</code>|찾고 싶은 캐릭터의 코드, 이름, 도감 번호, 또는 클래스 이름<br>(예: `"3P_Labiata"`, `"라비아타"`, `"Labiata"`, `2`)|

- |Return type|Description|
  |---|---|
  |[`Character`]|
  |`None`|해당 캐릭터를 찾을 수 없으면 `None`을 반환합니다.|

---

## `lo_char.Character`
모든 캐릭터의 기반이 되는 클래스입니다.  
새로운 캐릭터를 만들기 위해서는 이 클래스를 상속하십시오.

새로운 캐릭터를 만들 때, 다음과 같이 클래스 변수를 정의해둬야 합니다.

- ### 필수로 입력해야 하는 변수들
  |Variable|Type|Description|
  |---|---|---|
  |`name`|[`str`]|**캐릭터 이름**|
  |`code`|[`str`]|**캐릭터 코드**|
  |`isenemy`|[`bool`]|**적 유닛 여부**|

- ### 조건부 필수로 입력해야 하는 변수들
  만약 기존 캐릭터 데이터를 받아오고 싶다면 `_id` 변수를 해당 캐릭터 **도감 번호**로 정의하십시오.  
  만약 자신만의 캐릭터를 만들고 싶다면, 다음과 같은 변수들을 추가로 정의해둬야 합니다.
  |Variable|Type|Description|
  |---|---|---|
  |`stats`|<code>[tuple]\[[tuple]\[[str], ...]] &#124; None]</code>|**캐릭터 주요 스탯**<br>후술할 문단을 참조하십시오.|
  |`skills`|<code>[tuple]\[[tuple]\[[dict] &#124; None, ...], [tuple]\[[dict] &#124; None, ...], None]</code>|**캐릭터 스킬 데이터**<br>후술할 문단을 참조하십시오.|
  |`type_`|<code>[tuple]\[[CharType], [CharRole]]</code>|**캐릭터 타입**<br>경장/중장/기동형 공격/방어/지원기|
  |`isags`|[`bool`]|**AGS 여부**<br>[`int`]로도 정의할 수 있습니다. (`0` 또는 `1`)
  |`link_bonus`|[`BuffList`]|**100%당 링크 보너스**<br>링크 수치 100%당 부여할 버프 리스트|
  |`full_link_bonuses`|<code>[list]\[[Buff]]</code>|**풀링크 보너스 리스트**<br>풀링크시 부여할 수 있는 버프 리스트<br>**주의:** [`BuffList`] 객체가 아닙니다.|
  |`equip_condition`|<code>[tuple][[EquipType], [EquipType], [EquipType], [EquipType]]</code>|**풀링크 보너스 리스트**|
  |`base_rarity`|[`Rarity`]|**캐릭터 태생 등급**|
  |`promotion`|[`Rarity`]|**최대 승급 가능 등급**|

- ### `Character` *(game, pos, rarity=None, lvl=1, stat_lvl=None, skill_lvl=None, equips=None, link=0, full_link_bonus_no=None, affection=0, pledge=False, current_hp=0)*
  - |Parameter|Type|Default Value|Description|
    |---|---|:---:|---|
    |`game`|[`Game`]|*없음*|캐릭터가 포함된 **게임 객체**|
    |`pos`|<code>[int] &#124; [str] &#124; [tuple]\[[int], [int]] &#124; [Pos]</code>|*없음*|캐릭터 **위치**|
    |`rarity`|<code>[int] &#124; [Rarity]</code>|`base_rarity` 값|캐릭터 **등급**|
    |`lvl`|[`int`]|`1`|캐릭터 레벨|
    |`statlvl`|<code>[Sequence]\[[int]]</code>|`[0, 0, 0, 0, 0, 0]`|캐릭터 **스탯 레벨**<br>순서대로 체력, 공격력, 방어력, 적중, 회피, 치명타입니다.|
    |`skill_lvl`|<code>[Sequence]\[[int]]</code>|`[1, 1, 1, 1, 1]`|캐릭터 **스킬 레벨**<br>순서대로 액티브1스킬, 액티브2스킬, 패시브1스킬, 패시브2스킬, 패시브3스킬|
    |`equips`|<code>[Sequence]\[[Equip] &#124; None]</code>|`[None, None, None, None]`|캐릭터 **장비**<br>장비의 `owner` 속성 값이 자동으로 캐릭터 객체가 됩니다.|
    |`link`|[`int`]|`0`|캐릭터 **링크 수치**|
    |`full_link_bonus_no`|<code>[int] &#124; None</code>|`None`|캐릭터 **풀링크 보너스 번호**<br>인게임에서 표시되는 풀링크 보너스 리스트 순서대로 0번부터 번호가 매겨집니다.<br>(`None`값은 선택 안 함을 뜻합니다.)|
    |`affection`|[`int`]|`0`|캐릭터 **호감도**|
    |`pledge`|[`bool`]|`False`|캐릭터 **서약 여부**|
    |`current_hp`|[`int`]|`0`|캐릭터 **체력 수치**<br>현재 체력이 100%가 아닌 경우 입력하십시오.|

- ### `Character.name`
  캐릭터 이름
  - Type: [`str`]

- ### `Character.code`
  캐릭터의 고유 코드 이름
  - Type: [`str`]

- ### `Character.group`
  캐릭터가 속한 그룹  
  (철충은 `Group.PARASITE`로 통일합니다.)
  - Type: [`Group`]

- ### `Character.isenemy`
  캐릭터의 적 소속 여부
  - Type: [`bool`]

- ### `Character.type_`
  캐릭터 타입
  - Type: <code>[tuple]\[[CharType], [CharRole]]</code>

- ### `Character.isags`
  캐릭터 AGS 여부
  - Type: [`bool`]

- ### `Character.equip_condition`
  캐릭터의 장비 슬롯
  - Type: <code>[tuple]\[[EquipType], [EquipType], [EquipType], [EquipType]]</code>

- ### `Character.game`
  캐릭터가 포함된 게임
  - Type: [`Game`]

- ### `Character.pos`
  캐릭터 위치
  - Type: [`Pos`]

- ### `Character.rarity`
  캐릭터 등급
  - Type: [`Rarity`]

- ### `Character.lvl`
  캐릭터 레벨
  - Type: [`int`]

- ### `Character.statlvl`
  캐릭터 스탯 레벨
  - Type: <code>[list]\[[int]]</code>

- ### `Character.skillvl`
  캐릭터 스킬 레벨
  - Type: <code>[list]\[[int]]</code>

- ### `Character.equips`
  캐릭터가 착용한 장비
  - Type: <code>[list]\[[Equip] &#124; None]</code>

- ### `Character.link`
  캐릭터의 링크 수치
  - Type: [`int`]

- ### `Character.flinkbNO`
  캐릭터의 풀링크 보너스 번호
  - Type: [`int`]

- ### `Character.affection`
  캐릭터 호감도 수치
  - Type: [`int`]

- ### `Character.pledge`
  캐릭터 서약 여부
  - Type: [`bool`]

- ### `Character.link_bonus`
  캐릭터의 링크 보너스 버프
  - Type: [`BuffList`]

- ### `Character.full_link_bonuses`
  캐릭터의 풀링크 보너스 리스트
  - Type: <code>[list]\[[Buff]]</code>

- ### `Character.stats`
  캐릭터의 스탯 데이터
  - Type: <code>[tuple]\[[tuple]\[[str] &#124; None, ...], ...]</code>
    + 4개의 튜플로 이루어진 튜플이며, 각각 B, A, S, SS 등급에서의 스탯 데이터를 가집니다.
    + 각 등급에서의 스텟 데이터 튜플은 다음과 같습니다:  
      ```
      (hp_lv1, hp_per_lv, 
       atk_lv1, atk_per_lv, 
       def_lv1, def_per_lv1, 
       speed, critical, accuracy, evation, 
       fire_res, ice_res, elec_res)
      ```

- ### `Character.skills`
  캐릭터의 스킬 데이터
  - Type: <code>[tuple]\[[tuple]\[[MappingProxyType] &#124; None, ...], ...]</code>  
    (<code>[list]\[[list]\[[dict] &#124; None]]</code>의 수정 불가능 버전)

- ### `Character.base_rarity`
  캐릭터의 태생 등급
  - Type: [`Rarity`]
  
- ### `Character.promotion`
  캐릭터의 가능한 최고 승급 등급
  - Type: [`Rarity`]
  
- ### `Character.is_custom`
  사용자 설정 캐릭터 여부를 나타냅니다.
  - Type: [`bool`]

- ### `Character.maxhp`
  캐릭터의 최대 체력을 의미합니다.
  - Type: <code>[int] | [decimal.Decimal]</code>

- ### *@property* `Character.hp_rate`
  캐릭터의 체력 비율 값입니다.
  - Type: <code>[decimal.Decimal]</code>
  - 일반적으로 0 이상 1 이하의 값입니다.

- ### `Character.has_impact_skill`
  캐릭터가 착탄 액티브 스킬을 가지고 있는지를 알려줍니다.  
  (폼체인지 액티브 스킬에 착탄 스킬이 있는 경우 포함)
  - Type: [`bool`]

- ### `Character.get_type_str()`
  캐릭터의 타입과 역할군을 문자열로 반환합니다.  
  (예: `"경장형 공격기"`)
  - Type: [`str`]

- ### `Character.getpos()`<br>`Character.getposx()`<br>`Character.getposy()`<br>`Character.getposxy()`<br>`Character.getposn()`
  캐릭터의 위치 정보를 가져옵니다.  

  |Method|Return Type|Description|
  |---|---|---|
  |`Character.getpos()`|[`Pos`]|[`Pos`] 객체를 반환합니다.|
  |`Character.getposx()`|[`int`]|행 번호를 반환합니다. (0, 1, 2)|
  |`Character.getposy()`|[`int`]|열 번호를 반환합니다. (0, 1, 2)|
  |`Character.getposxy()`|<code>[tuple]\[[int], [int]]</code>|행/열 번호를 튜플로 반환합니다.|
  |`Character.getposn()`|[`int`]|그리드 번호를 반환합니다. (x*3 + y)|

- ### `Character.get_absolute_y()`
  [`Character.getposy()`]: #charactergetposcharactergetposxcharactergetposycharactergetposxycharactergetposn
  캐릭터의 절대적 열 번호를 반환합니다.  
  아군은 [`Character.getposy()`]와 같으며, 적군은 [`Character.getposy()`]에 3을 더한 값과 같습니다.

- ### `Character.measure` *(c)*
  다른 캐릭터와의 열 거리를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`c`|[`Character`]|거리를 잴 캐릭터|
  
  - |Return type|Description|
    |---|---|
    |[`int`]|캐릭터와의 거리<br>무조건 0 또는 양의 정수입니다.|
  
- ### `Character.attackable` *(c, skill_no)*
  다른 캐릭터가 액티브 스킬의 사정거리 안에 있는지 알려줍니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`c`|[`Character`]|목표 캐릭터|
    |`skill_no`|[`int`]|스킬 번호 (1, 2, 6, 7 중 하나)|
  
  - |Return type|Description|
    |---|---|
    |[`bool`]|액티브 스킬 사용 가능 여부|
  
- ### `Character.collocated` *()*
  캐릭터가 게임에 배치되어 있는지 알려줍니다.
  
  - |Return type|Description|
    |---|---|
    |[`bool`]|배치 여부|

- ### `Character.isformchanged` *()*
  캐릭터의 폼체인지 여부를 알려줍니다.  
  > <font size=+2 color="orange">**주의**</font>   
  > 폼체인지가 있는 캐릭터를 커스텀 및 직접 제작하는 경우  
  > 이 함수를 덮어쓰기 해야합니다.

- ### `Character.skill_idx_convert` *(skill_idx)*
  [`Game.use_skill`](./API_system.md#gameuse_skill-subjc-skill_no-objposnone)에서 폼체인지 상태일 때 기본 스킬 번호를 폼체인지 스킬 번호로 바꿔주는 함수입니다.  
  > <font size=+2 color="orange">**주의**</font>    
  > 폼체인지가 있는 캐릭터를 커스텀 및 직접 제작하는 경우  
  > 이 함수를 덮어쓰기 해야합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_idx`|[`int`]|스킬 번호|
  
  - |Return type|Description|
    |---|---|
    |[`int`]|변경된 스킬 번호|

- ### `Character.get_skill` *(skill_idx, apply_formchange=True)*
  스킬 데이터를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_idx`|[`int`]|스킬 번호|
    |`apply_formchange`|[`bool`]|폼체인지로 인한 스킬 변경을 허용할 1지를 정합니다.|
  
  - |Return type|Description|
    |---|---|
    |<code>[tuple]\[[int], [MappingProxyType] &#124; [dict] &#124; None]</code>|변경된 스킬 번호와 스킬 데이터|

- ### `Charcter.baseBuffs`<br>`Charcter.statBuffs`<br>`Charcter.antiOSBuffs`<br>`Charcter.dmgTakeIncBuffs`<br>`Charcter.dmgTakeDecBuffs`<br>`Charcter.dmgGiveIncBuffs`<br>`Charcter.dmgGiveDecBuffs`<br>`Charcter.specialBuffs`<br>`Charcter.proportionBuffs`
  캐릭터의 버프를 관리하는 버프 리스트들입니다.  

  |Attribute|Description|
  |:---:|---|
  |`Character.baseBuffs`|링크 보너스, 풀링크 보너스, 장비 스탯 증감 수치를 저장하는 리스트|
  |`Character.statBuffs`|체력, 공격력, 방어력, 적중, 회피, 치명타 증감 버프를 저장하는 리스트|
  |`Character.antiOSBuffs`|대타입 버프를 저장하는 리스트|
  |`Character.dmgTakeIncBuffs`|받는 피해 증가 버프를 저장하는 리스트|
  |`Character.dmgTakeDecBuffs`|받는 피해 감소 버프를 저장하는 리스트|
  |`Character.dmgGiveIncBuffs`|주는 피해 증가 버프를 저장하는 리스트|
  |`Character.dmgGiveDecBuffs`|주는 피해 감소 버프를 저장하는 리스트|
  |`Character.proportionBuffs`|특정 수치 비례 정보를 가진 버프를 저장하는 리스트|
  |`Character.specialBuffs`|이외의 모든 버프를 (행동력, 표식 등) 저장하는 리스트|

  - Type: [`BuffList`]

- ### `Character.buff_iter`
  위 버프 리스트들을 모아놓은 튜플입니다.  
  ```python
  self.buff_iter = (self.baseBuffs, self.statBuffs, self.proportionBuffs, self.antiOSBuffs,
                    self.dmgTakeIncBuffs, self.dmgTakeDecBuffs, selfdmgGiveIncBuffs, self.dmgGiveDecBuffs,
                    self.specialBuffs)
  ```
  - Type: <code>[tuple]\[[BuffList]]</code>

- ### `Character.get_orig_hp()`<br>`Character.get_orig_atk()`<br>`Character.get_orig_def()`<br>`Character.get_orig_acc()`<br>`Character.get_orig_eva()`<br>`Character.get_orig_crit()`<br>`Character.get_orig_spd()`<br>`Character.get_orig_res()`
  각각 체력, 공격력, 방어력, 적중, 회피, 치명타, 행동력, 속성 저항 수치를 반환하는 함수입니다.  
  이 수치는 <u>*스탯 레벨만 적용된 수치*</u>입니다.

  - |Return type|Description|
    |---|---|
    |[`decimal.Decimal`]|계산된 수치|
    |<code>[tuple]\[[decimal.Decimal], [decimal.Decimal], [decimal.Decimal]]</code>|속성 저항의 경우 `(화염, 냉기, 전기)` 저항 수치로 반환합니다.|
  
- ### `Character.get_orig_stat_funcs`
  위 get_orig 함수들을 [`BuffType`]으로 매핑한 딕셔너리입니다.  
  ```python
  self.get_orig_stat_funcs = {
      BT.HP: self.get_orig_hp,
      BT.ATK: self.get_orig_atk,
      BT.DEF: self.get_orig_def,
      BT.ACC: self.get_orig_acc,
      BT.EVA: self.get_orig_eva,
      BT.CRIT: self.get_orig_crit,
      BT.SPD: self.get_orig_spd,
  }
  ```
  - Type: <code>[dict]\[[BuffType], [Callable]\[\[], [decimal.Decimal] &#124; [tuple]\[[decimal.Decimal], [decimal.Decimal], [decimal.Decimal]]]]</code>
  
- ### `Character.get_orig_stats()`
  체력, 공격력, 방어력, 적중, 회피, 치명타 수치를 딕셔너리로 반환하는 함수입니다.  
  이 수치는 <u>*스탯 레벨만 적용된 수치*</u>입니다.

  - |Return type|Description|
    |---|---|
    |<code>[dict]\[[BuffType], [decimal.Decimal]]</code>|계산된 수치|

- ### `Character.get_base_stats()`
  체력, 공격력, 방어력, 적중, 회피, 치명타 수치를 딕셔너리로 반환하는 함수입니다.  
  이 수치는 <u>*스탯 레벨, 장비 스탯 수치, 링크 보너스가 적용된 수치*</u>입니다.

  - |Return type|Description|
    |---|---|
    |<code>[dict]\[[BuffType], [decimal.Decimal]]</code>|계산된 수치|

- ### `Character.get_stats` *(\*bufftypes)*
  캐릭터의 (기본 스탯 말고도) 원하는 스탯 수치를 [`BuffType`]으로 입력하면 반환하는 함수입니다.  
  (물론 <u>*스탯 레벨, 장비 스탯 수치, 링크 보너스, 전투 중 얻은 버프까지 **모두** 적용된 수치*</u>입니다.)

  - |Parameter|Type|Description|
    |---|---|---|
    |`*bufftypes`|[`BuffType`]|원하는 스탯의 [`BuffType`] 버전|

  - |Return type|Description|
    |---|---|
    |<code>[decimal.Decimal]</code>|계산된 수치 (단일 입력의 경우)|
    |<code>[Sequence]\[[decimal.Decimal]]</code>|일부 스탯 수치는 여러 값을 반환합니다.<br>아래 문단을 참고하십시오.|
    |<code>[dict]\[[BuffType], [decimal.Decimal] &#124; [Sequence]\[[decimal.Decimal]]]</code>|다중 입력의 경우 각 [`BuffType`]을 키로 가지는 딕셔러리를 반환합니다.|
    
    + ### 여러 값을 반환하는 스탯 수치들
      + #### 주는/받는 피해 증가/감소
        HP% 비례 여부와 공격 속성(element)에 따른 2중 리스트를 반환합니다.  
        HP% 비례 여부에 대해서는 [`Datas.DmgInfo`](./API_imports.md#datasdmginfo)의 `hp_type` 어트리뷰트를 참고하십시오.  
      + #### 효과 저항
        효과 저항 확률들의 리스트를 반환합니다. (퍼센트 수치)
      + #### 전투속행
        전투속행 수치들의 리스트를 반환합니다.  
        고정 수치는 음수, 퍼센트 수치는 양수입니다.

- ### `Character.calculate_cycled_buff()`
  순환 관계에 있는 수치 비례 버프들을 찾아내 그 수치들을 계산합니다.
  > <font size=+1 color="green">**참고**</font>  
  > 이 함수는 수치 비례 버프 계산 시 실시간으로 수치를 계산하는 경우에  
  > ([`Game.REAL_TIME`](./API_system.md#gamereal_time) 값이 `True`일때) 동작합니다.

  - |Return type|Description|
    |---|---|
    |[`BuffList`]|비례 수치 계산 중 임시로 생성한 버프들입니다.<br><font color="red">**원하는 작업을 한 이후에 꼭 [`Character.remove_buff`](#characterremove_buff-type_none-efftnone-tagnone-funcnone-id_none-val_signnone-oprnone-limitmax-forcefalse-logtrue-kwargs)으로 이 버프들을 제거해야 합니다.**</font><br>(제거하지 않을 시 중복 적용 등 오류가 일어날 수 있습니다.)|

- ### `Character.get_res_dmgrate` *(element)*
  속성 공격시 적용되는 데미지 비율을 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`element`|<code>[int] &#124; [Element]</code>|속성 타입|
  
  - |Return type|Description|
    |---|---|
    |<code>[int] &#124; [decimal.Decimal]</code>|해당 속성 공격의 데미지 비율|

- ### `Character.get_aoe` *(targ_pos, skill_no)*
  공격 범위 및 스킬 광역 계수, 또는 패시브 범위를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`targ_pos`|<code>[int] &#124; [str] &#124; [tuple]\[[int], [int]] &#124; [Pos]</code>|스킬의 목표 좌표<br>스킬의 범위가 절대 좌표인 경우 이 값은 무시됩니다.<br>상대 좌표를 가진 패시브 스킬의 경우 [`self.pos`](#characterpos)를 입력하세요.|
    |`skill_no`|[`int`]|스킬 번호 (1~10)|
  
  - |Return type|Description|
    |---|---|
    |<code>[list]\[[tuple]\[[int], [int]]]</code>|패시브의 경우 `(x좌표, y좌표)`|
    |<code>[list]\[[tuple]\[[int], [int], [int] &#124; [decimal.Decimal]]]</code>|액티브의 경우 `(x좌표, y좌표, 광역계수)`|
  
- ### `Character.get_skill_atk_rate` *(skill_no=None, value=None)*
  액티브 스킬의 공격 계수를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_no`|[`int`]|스킬 번호 (1, 2, 6, 7)|
    |`value`|<code>[int] &#124; [decimal.Decimal]</code>|스킬 데이터 이외의 다른 수를 사용하고 싶은 경우 입력하세요.|
  
  - |Return type|Description|
    |---|---|
    |<code>[int] &#124; [decimal.Decimal]</code>|계산된 공격 계수 수치|

- ### `Character.get_skill_buff_value` *(skill_no)* 
  스킬에 달려있는 버프 수치들을 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_no`|[`int`]|스킬 번호 (1~10)|
  
  - |Return type|Description|
    |---|---|
    |<code>[list]\[[int] &#124; [decimal.Decimal]]</code>|계산된 버프 수치들|

- ### `Character.get_skill_range` *(skill_no)*
  액티브 스킬 사거리 수치를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_no`|[`int`]|스킬 번호 (1, 2, 6, 7)|
  
  - |Return type|Description|
    |---|---|
    |<code>[int] &#124; [decimal.Decimal]</code>|계산된 사거리 수치|

- ### `Character.get_skill_cost` *(skill_no)*
  액티브 스킬 코스트를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_no`|[`int`]|스킬 번호 (1, 2, 6, 7)|
  
  - |Return type|Description|
    |---|---|
    |<code>[int] &#124; [decimal.Decimal]</code>|코스트|

- ### `Character.get_skill_element` *(skill_no)*
  액티브 스킬의 속성 타입을 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_no`|[`int`]|스킬 번호 (1, 2, 6, 7)|
  
  - |Return type|Description|
    |---|---|
    |[`Element`]|속성 타입|

- ### `Character.judge_hit` *(obj, acc_bonus=0)*
  다른 캐릭터에 대한 적중 및 치명타 판정 후 결과를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`obj`|[`Character`]|목표 캐릭터|
    |`acc_bonus`|<code>[int] &#124; [decimal.Decimal]</code>|적중 보너스<br>스탯/버프 계산 이후 적용됩니다.|
  
  - |Return type|Description|
    |---|---|
    |[`decimal.Decimal`]|다음 3가지 중 하나입니다.<br>- `0` = 회피함<br>- `1` = 적중, 치명타 X<br>-`1.5` = 적중, 치명타 O|

- ### `Character.judge_active` *(chance=100)*
  스킬 발동 판정 결과를 반환합니다.  
  (버프에 달린 적용 확률과는 다릅니다!)

  - |Parameter|Type|Description|
    |---|---|---|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|기본 스킬 발동 확률의 %수치<br>대부분의 스킬 발동 확률은 100%입니다. (기본값)|
  
  - |Return type|Description|
    |---|---|
    |<code>[tuple]\[[bool], [int] &#124; [decimal.Decimal]]</code>|`True`가 발동 성공입니다.<br>뒤의 값은 발동 확률을 의미합니다.|

- ### `Character.judge_resist_buff` *(buff, chance=100)*
  버프 적용 판정 결과를 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`buff`|[`Buff`]|적용되는 버프|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|기본 버프 **적용** 확률의 %수치 (기본값 100)|
  
  - |Return type|Description|
    |---|---|
    |<code>[tuple]\[[bool], [int] &#124; [decimal.Decimal]]</code>|`False`가 적용 성공입니다.<br>뒤의 값은 버프 적용 확률을 의미합니다.|

- ### `Character.calc_damage` *(obj, rate, element=Element.PHYSICAL, wr=0)*
  대상에게 공격시 가해질 데미지를 계산합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`obj`|[`Character`]|공격 대상 캐릭터|
    |`rate`|<code>[tuple]\[[int] &#124; [decimal.Decimal], [int] &#124; [decimal.Decimal], [int] &#124; [decimal.Decimal]]</code>|다음 세 개의 값을 순서대로 가진 튜플입니다:<br>1. 스킬 계수<br>2. 치명 여부 (`1` 또는 `1.5`)<br>3. 범위 스킬 계수|
    |`element`|[`Element`]|공격 속성|
    |`wr`|<code>[int] &#124; [decimal.Decimal]</code>|광역 피해 분산/집중에 쓰이는 비율<br>(`((피격 캐릭터 수) - 1) / ((공격 범위 칸 개수) - 1)`과 같습니다.|
  
  - |Return type|Description|
    |---|---|
    |<code>[tuple]\[[int] &#124; [decimal.Decimal], [int]]</code>|데미지와 버프 ID입니다.<br>버프 ID는 적용된 피해 최소화의 버프 ID이며, 피해 최소화가 적용되지 않았으면 `0`입니다.|

- ### `Character.give_damage` *(dmg, minimize_buff_id=0, direct=False, ignore_barrier=False)*
  캐릭터에게 데미지를 입힙니다.  
  *소숫점 아래는 버림합니다.*

  - |Parameter|Type|Description|
    |---|---|---|
    |`dmg`|<code>[int] &#124; [decimal.Decimal]</code>|데미지 수치|
    |`minimize_buff_id`|[`int`]|데미지에 적용된 피해 최소화 버프 ID. 없으면 `0`.<br>함수 호출 시, 해당 버프의 횟수를 1 차감합니다.|
    |`direct`|[`bool`]|`True` 설정시 피해 최소화, 피해 무효, 방어막 등을 무시합니다.<br>(위 `minimize_buff_id`로 인한 횟수 차감은 무시됩니다.)|
    |`ignore_barrier`|[`bool`]|`True` 설정시 방어막을 무시합니다.|
  
  - |Return type|Description|
    |---|---|
    |<code>[int] &#124; [decimal.Decimal]</code>|실제로 들어간 데미지|
    |`-1`|방어막으로 방어됨|
    |`-2`|피해 무효됨|

- ### `Character.give_buff(...)`
  캐릭터에게 버프를 부여합니다.  
  파라메터는 [`Game.give_buff`](./API_system.md#gamegive_buff)에서 `target`를 제외하면 동일합니다.

- ### `Character.find_buff` *(type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None)*
  캐릭터에 적용된 버프들을 검색하여 제거합니다.  
  [`BuffList.find`](./API_system.md#bufflistfind-type_none-efftnone-tagnone-funcnone-id_none-val_signnone-oprnone-kwargs)에 동일한 이름으로 존재하는 파라메터는 해당 설명을 참고하십시오.
  
  - |Return type|Description|
    |---|---|
    |[`BuffList`]|조건을 만족하는 버프 리스트|

- ### `Character.remove_buff` *(type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None, limit=MAX, force=False, log=True, \*\*kwargs)*
  캐릭터에 적용된 버프들을 검색하여 제거합니다.  
  [`BuffList.remove`](./API_system.md#bufflistremove-type_none-efftnone-tagnone-funcnone-id_none-val_signnone-oprnone-limitmax-forcefalse)에 동일한 이름으로 존재하는 파라메터는 해당 설명을 참고하십시오.

  - 추가 파라메터들  
    |Parameter|Type|Description|
    |---|---|---|
    |`log`|[`bool`]|버프 제거 로그 출력 여부|
  
  - |Return type|Description|
    |---|---|
    |[`BuffList`]|제거된 버프 리스트|

- ### `Character.buff_update` *(tt=Trigger.DUMMY, args=None)*
  적용된 버프들을 트리거하고, 라운드 지속 시간을 초과하거나 횟수가 모두 차감된 버프들을 제거합니다.  
  ()

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|
  
  - |Return type|Description|
    |---|---|
    |[`BuffList`]|제거된 버프 리스트|

- ### `Character.dead_judge_process` *(hit_value=None, damage_value=None, attacker=None, attacker_skill_no=None, attacker_follow=None)*
  캐릭터가 데미지를 입은 후 피격 및 사망 관련 판정을 하는 함수입니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`hit_value`|[`int`]|적중 판정 값<br>`0`, `1`, `1.5` 중 하나입니다.<br>입력하지 않을 시 피격/회피 트리거를 발동하지 않습니다.|
    |`damage_value`|[`int`]|입은 데미지<br>입력하지 않을 시 피격/회피 트리거를 발동하지 않습니다.|
    |`attacker`|[`Character`]|이 캐릭터에게 공격한 캐릭터|
    |`attacker_skill_no`|[`int`]|이 캐릭터에게 공격한 캐릭터가 사용한 스킬 번호 (1, 2, 6, 7)|
    |`attacker_follow`|[`int`]|이 캐릭터에게 공격한 캐릭터와 협동 공격한 캐릭터 (<code>[BuffType].FOLLOW_ATTACK</code>)|

- ### `Character.trigger` *(trigtype=TR.DUMMY, args=None, print_msg=False)*
  캐릭터를 트리거합니다.  
  이 함수를 호출함으로서 조건부로 발동되는 패시브들을 발동할 수 있습니다.  
  
  패시브 발동 순서는 다음과 같습니다:
  1. 장비 조건부 버프 트리거들 (`Equip.passive`)
  1. 버프 업데이트 ([`Character.buff_update`](#characterbuff_update-tttriggerdummy-argsnone))
  2. 패시브 이전에 발동할 트리거들 ([`Character.base_passive_before`](#characterbase_passive_before))
  3. 패시브 스킬 (1, 2, 3 순) ([`Character.passive`](#characterpassive-trigtype-argsnone))
  4. 패시브 이후에 발동할 트리거들 ([`Character.base_passive_after`](#characterbase_passive_after))
  5. 추가로 발동할 커스텀 패시브 (`Character.extra_passive`)  

  모든 함수는 `trigtype`, `args`를 인자로 받습니다.  

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|
    |`print_msg`|`bool`|로그 출력 여부 (기본값 `False`)|

- ### `Character.give_ap` *(val)*
  캐릭터에게 AP를 줍니다.  
  AP를 준 결과가 20 초과일 경우 20, 0 미만일 경우 0으로 만듭니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`val`|<code>[int] &#124; [decimal.Decimal]</code>|추가할 AP 값|

- ### `Character.active` *(skill_no, targets, atk_rate, aoe_len)*
  캐릭터의 액티브 스킬을 발동합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_no`|[`int`]|스킬 번호 (1, 2, 6, 7)|
    |`targets`|<code>[dict]\[[Character], [int] &#124; [decimal.Decimal]]</code>|타겟 및 적중 정보<br>캐릭터와 적중 계수(0, 1, 1.5)를 매핑한 딕셔너리입니다.|
    |`atk_rate`|<code>[dict]\[[Character], [tuple]\[[int] &#124; [decimal.Decimal], [int] &#124; [decimal.Decimal]]]</code>|스킬 및 범위 계수 정보<br>캐릭터와 스킬 및 범위 계수를 매핑한 딕셔너리입니다.|
    |`aoe_len`|[`int`]|적용된 스킬 범위의 넓이|
  
  - |Return type|Description|
    |---|---|
    |<code>[dict]\[[Character], [tuple]\[[int] &#124; [decimal.Decimal], [int]]]</code>|각 캐릭터당 [`Character.calc_damage`](#charactercalc_damage-obj-rate-elementelementphysical-wr0)의 결과값|

- ### `Character._active1(...)`<br>`Character._active2(...)`<br>`Character._factive1(...)`<br>`Character._factive2(...)`<br>
  [`Character.active`](#characteractive-skill_no-targets-atk_rate-aoe_len)로부터 호출될, 실제 작동하는 액티브 함수들입니다.  
  순서대로 액티브 1스킬, 액티브 2스킬, 폼체인지 액티브 1스킬, 폼체인지 액티브 2스킬입니다.  

  이 함수는 어느정도 템플릿을 가지고 있습니다.  
  공격받는 캐릭터와 적중 여부 등이 주어지면, 조건에 따라 버프를 부여하고, 최종적으로 데미지를 계산한 후 그 딕셔너리를 반환합니다.  
  또는, 버프만 부여하는 스킬이라면 빈 딕셔너리를 반환할 수도 있습니다.  
  (즉, 대부분의 스킬 구현 시, 아래 예시 코드의 `(*)`줄은 고정이라고 할 수 있습니다.)

  예시; 레아(`3P_Rhea`)의 액티브 1스킬 함수 코드
  ```python
  def _active1(self,
               targets: Dict['Character', NUM_T],
               atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
               bv: Sequence[NUM_T],
               wr: NUM_T,
               element: int):
      desc = "기능 오류"
      bv1 = bv[0]*3/5
      for t in targets:
          if targets[t] > 0:
              t.give_buff(BT.FIRE_RES, 0, bv[0], round_=2, efft=BET.DEBUFF, max_stack=1,
                          tag=G.FLOOD_FIRE)
              t.give_buff(BT.ICE_RES, 0, -bv[0], round_=2, efft=BET.DEBUFF, max_stack=1,
                          tag=G.FLOOD_ICE)
              t.give_buff(BT.ELEC_RES, 0, -bv[0], round_=2, efft=BET.DEBUFF, max_stack=1,
                          tag=G.FLOOD_ELEC)
              if t.find_buff(tag=G.CORROSION):
                  t.give_buff(BT.TAKEDMGINC, 1, bv1 / 100, overlap_type=BOT.INSTANCE, data=D.DmgInfo(element=E.ELEC), desc="급속 부식")
              if targets[t] > 1:
                  t.give_buff(BT.ACC, 0, -bv1, round_=2, efft=BET.DEBUFF, max_stack=1, tag="Rhea_A1_ACC", desc=desc)
                  t.give_buff(BT.EVA, 0, -bv1, round_=2, efft=BET.DEBUFF, max_stack=1, tag="Rhea_A1_EVA", desc=desc)
      return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}  # (*)
  ```

  - |Parameter|Type|Description|
    |---|---|---|
    |`targets`|<code>[dict]\[[Character], [int] &#124; [decimal.Decimal]]</code>|타겟 및 적중 정보<br>캐릭터와 적중 계수(0, 1, 1.5)를 매핑한 딕셔너리입니다.|
    |`atk_rate`|<code>[dict]\[[Character], [tuple]\[[int] &#124; [decimal.Decimal], [int] &#124; [decimal.Decimal]]]</code>|스킬 및 범위 계수 정보<br>캐릭터와 스킬 및 범위 계수를 매핑한 딕셔너리입니다.|
    |`bv`|<code>[Sequence]\[[int] &#124; [decimal.Decimal]]</code>|해당 스킬 함수에서 사용될 버프 수치|
    |`wr`|<code>[int] &#124; [decimal.Decimal]</code>|광역 비율 (광역 피해 분산/집중에 사용)|
    |`element`|<code>[int] &#124; [Element]</code>|공격 속성|
  
  - |Return type|Description|
    |---|---|
    |<code>[dict]\[[Character], [tuple]\[[int] &#124; [decimal.Decimal], [int]]]</code>|각 캐릭터당 [`Character.calc_damage`](#charactercalc_damage-obj-rate-elementelementphysical-wr0)의 결과값|

- ### `Character.get_active_chance` *(skill_idx)*
  해당 액티브 스킬의 버프 발동 확률을 반환합니다.  
  기본적으로 모든 스킬에 대해 100을 반환하도록 설정되어 있습니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_idx`|[`int`]|스킬 번호 (0, 1, 5, 6)|
  
  - |Return type|Description|
    |---|---|
    |<code>[int] &#124; [decimal.Decimal]</code>|발동 확률의 백분율 수치|

- ### `Character.passive` *(trigtype, args=None)*
  캐릭터의 패시브 스킬을 발동합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`trigtype`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|

- ### `Character.get_passive_targets` *(aoe, enemy=False)*
  패시브에서 스킬 범위에 해당되는 캐릭터들을 반환하는 함수입니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`aoe`|<code>[list]\[[tuple]\[[int], [int]] &#124; [int] &#124; [Pos]]</code>|좌표를 담은 리스트|
    |`enemy`|[`bool`]|가져올 캐릭터의 아군/적군 여부|
  
  - |Return type|Description|
    |---|---|
    |<code>[list]\[[Character]]</code>|범위에 해당되는 캐릭터들|

- ### `Character._passive1(...)`<br>`Character._passive2(...)`<br>`Character._passive3(...)`<br>`Character._fpassive1(...)`<br>`Character._fpassive2(...)`<br>`Character._fpassive3(...)`
  [`Character.passive`](#characterpassive-trigtype-argsnone)로부터 호출될, 실제 작동하는 패시브 함수들입니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|

- ### `Character.base_passive_before` *(tt, args=None)*<br>`Character.base_passive_after` *(tt, args=None)*
  패시브 트리거 이전/이후 작동되어야 할 함수입니다.  
  기본적인 시스템 흐름 일부가 작성되어 있으므로, 이 함수를 커스터마이징한다면 꼭 `super`를 통해 기존 함수를 호출해야 합니다.

  - #### `Character.base_passive_before`
    사망 시 전투속행을 발동합니다.
  
  - #### `Character.base_passive_after`
    라운드 시작 시 AP를 받습니다.  
    전투 불능 시, 전장에서 제거됩니다.  
    대기 시, `보속의 마리아`의 강제 대기 버프를 제거합니다.  
    웨이브 종료 시, 정찰 버프를 제외한 모든 버프를 제거하고, AP를 초기화합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|

- ### `Character.extra_passive` *(tt, args=None)*
  추가로 패시브를 발동시키고 싶은 작업이 있다면 이 함수를 오버라이딩 하십시오.

- ### `Character.move` *(pos, force_moved=False)*
  캐릭터를 이동합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`pos`|<code>[tuple]\[[int], [int]] &#124; [int] &#124; [Pos]</code>|이동할 좌표|
    |`force_moved`|[`bool`]|버프 등으로 인한 강제 이동 여부|
  
  - |Return type|Description|
    |---|---|
    |[`bool`]|이동 성공 여부|

- ### `Character.idle()`
  캐릭터가 대기합니다.
