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
[EquipType]: ./API_enum.md#lo_enumequiptypelo_enumet
[`Rarity`]: ./API_enum.md#lo_enumraritylo_enumr
[Rarity]: ./API_enum.md#lo_enumraritylo_enumr

[`Game`]: ./API_system.md#lo_systemgame
[`Buff`]: ./API_system.md#lo_systembuff
[Buff]: ./API_system.md#lo_systembuff
[`BuffList`]: ./API_system.md#lo_systembufflist

[Character]: #lo_charcharacter
[`Character`]: #lo_charcharacter
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
  - Type: <code>[tuple]\[[tuple]\[MappingProxyType | None]]]</code>

