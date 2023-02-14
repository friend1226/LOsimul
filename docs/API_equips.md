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

[Equip]: #lo_equipsequip
[`Equip`]: #lo_equipsequip
[Chip]: #lo_equipschip
[`Chip`]: #lo_equipschip
[OS]: #lo_equipsos
[`OS`]: #lo_equipsos
[Gear]: #lo_equipsgear
[`Gear`]: #lo_equipsgear

# lo_simul.`lo_equips`

장비의 베이스 클래스 및 각 장비들의 클래스가 구현되어있는 모듈입니다.

---

## `lo_equips.EquipPools`
모든 [`Equip`] 서브 클래스를 관리하기 위한 클래스입니다.

- |Attribute|Type|Description|
  |---|---|---|
  |`EquipPools.CHIP_NAME`<br>`EquipPools.OS_NAME`<br>`EquipPools.GEAR_NAME`|<code>[dict]\[[str], Type\[[Chip]]]</code><br><code>[dict]\[[str], Type\[[OS]]]</code><br><code>[dict]\[[str], Type\[[Gear]]]</code>|`Equip.nick`을 키로 가지는 딕셔너리입니다.<br>각각 칩, OS, 보조장비 장비 클래스를 가지고 있습니다.|
  |`EquipPools.ALL_NAME`|<code>[dict]\[[str], Type\[[Equip]]]</code>|`Equip.nick`을 키로 가지는 딕셔너리입니다.<br>모든 장비 클래스를 가지고 있습니다.|
  |`EquipPools.ALL_NAME_LIST`|<code>[list]\[[dict]\[[str], Type\[[Equip]]]]</code>|`[EquipPools.CHIP_NAME, EquipPools.OS_NAME, EquipPools.GEAR_NAME]`와 같습니다.|
  |`EquipPools.ALL_CODE`|<code>[dict]\[[str], Type\[[Equip]]]</code>|`Equip.code`를 키로 가지는 딕셔너리입니다.<br>모든 장비 클래스를 가지고 있습니다.|

---

## `lo_equips.Equip`
모든 장비의 기반이 되는 클래스입니다.  
**주의:** 새로운 장비를 만들 때 이 클래스를 직접 상속하면 안 됩니다!  
만들고자 하는 장비 타입에 따라 [`Chip`], [`OS`], [`Gear`] 중에서 골라 상속하십시오.

새로운 장비를 만들 때, 다음과 같이 클래스 변수를 정의해둬야 합니다.

- ### 필수로 입력해야 하는 변수들
  |Variable|Type|Description|
  |---|---|---|
  |`nick`|[`str`]|장비 **별명**|
  |`name`|[`str`]|장비 **이름**|
  |`code`|[`str`]|장비 **코드**|
  |`BASE_RARITY`|[`Rarity`]|장비 **최저 등급**|
  |`PROMOTION`|[`Rarity`]|장비 **최고 등급**|

- ### `Equip` *(rarity=-1, lvl=0, owner=None)*
  - |Parameter|Type|Description|
    |---|---|---|
    |`rarity`|<code>[int] &#124; [Rarity]</code>|장비 등급|
    |`lvl`|[`int`]|장비 레벨|
    |`owner`|[`Character`]|장비 소유자<br>이후 설정 가능합니다.|

- ### `Equip.EQUIP_TYPE`
  장비 타입(칩, OS, 보조장비)을 나타냅니다.
  - Type: [`EquipType`]

- ### `Equip.nick`
  장비 별명입니다.
  - Type: [`str`]

- ### `Equip.name`
  장비 이름입니다.
  - Type: [`str`]

- ### `Equip.code`
  장비 코드입니다.
  - Type: [`str`]

- ### `Equip.BASE_RARITY`
  장비 태생 등급입니다.
  - Type: [`Rarity`]

- ### `Equip.PROMOTION`
  장비의 존재하는 최대 등급입니다.
  - Type: [`Rarity`]

- ### `Equip.rarity`
  장비 등급입니다.
  - Type: [`Rarity`]

- ### `Equip.owner`
  장비를 장착하고 있는 캐릭터입니다.
  - Type: <code>[Character] &#24; None</code>

- ### `Equip.lvl`
  장비 레벨입니다.
  - Type: [`int`]

- ### `Equip.buff`
  장비 기본 스탯입니다.
  - Type: [`BuffList`]

- ### `Equip.isfit` *(char)*
  해당 캐릭터가 착용할 수 있는 지를 나타냅니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`char`|[`Character`]|장착해주고 싶은 캐릭터|
  
  - |Return type|Description|
    |---|---|
    |[`bool`]|장착 가능 여부|

- ### `Equip.get_icon_filename()`
  장비 아이콘 파일 이름을 반환합니다.
  
  - |Return type|Description|
    |---|---|
    |[`str`]|아이콘 파일 이름|

- ### `Equip.init_buff()`
  장비 스탯 버프를 설정합니다.  
  이 함수는 [`Equip`] 객체 생성 시 호출됩니다.

- ### `Equip.passive` *(tt, args=None)*
  장비의 조건부 버프들을 트리거합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|

--

## `lo_equips.Chip`
## `lo_equips.OS`
## `lo_equips.Gear`
`EQUIP_TYPE`이 미리 정해진 클래스입니다.  
새로운 장비를 만들 때 이 클래스를 상속하십시오.
