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
[EquipType]: ./API_enum.md#lo_enumequiptypelo_enumet
[`Rarity`]: ./API_enum.md#lo_enumraritylo_enumr
[Rarity]: ./API_enum.md#lo_enumraritylo_enumr
[Element]: ./API_enum.md#lo_enumelementlo_enume
[`Element`]: ./API_enum.md#lo_enumelementlo_enume

[`Game`]: ./API_system.md#lo_systemgame
[`Buff`]: ./API_system.md#lo_systembuff
[Buff]: ./API_system.md#lo_systembuff
[`BuffList`]: ./API_system.md#lo_systembufflist

[Character]: ./API_char.md#lo_charcharacter
[`Character`]: ./API_char.md#lo_charcharacter
[Pos]: ./API_imports.md#lo_importspos
[`Pos`]: ./API_imports.md#lo_importspos

[Equip]: ./API_equips.md#lo_equipsequip

## `lo_system.lo_imports`
내장 모듈들을 불러오고, 커스텀 클래스 및 함수들이 정의된 모듈입니다.

---

## `lo_imports.Pos`
2차원 좌표를 다루는 클래스입니다.

- ### `Pos` *(x, y=None, grid=(3, 3))*
  - |Parameter|Type|Description|
    |---|---|---|
    |`x`, `y`|[`int`], [`int`]<br>또는<br><code>[int] &#124; [str] &#124; [tuple]\[[int], [int]] &#124; [Pos]</code>, `None`|좌표값|
    |`grid`|<code>[tuple]\[[int], [int]]</code>|좌표를 담는 그리드 크기<br>좌표값은 그리드를 벗어나서는 안됩니다.|
  
  - 이 객체는 다른 [`Pos`] 객체나 길이가 2인 튜플과 더하기 연산을 할 수 있습니다.  
    만약 더한 결과가 그리드를 벗어나면 `None`이 됩니다.  
    그리드는 왼쪽에 있는 [`Pos`] 객체를 따릅니다.
  
  - 이 객체는 다른 [`Pos`] 객체나 튜플, 정수와 같은지 비교할 수 있습니다. (`==`)  
    튜플과 비교할 때 길이가 2여야 하며, 비교 대상은 `(x값, y값)`이어야 합니다.  
    정수와 비교할 때 그리드 번호 (`x * grid[0] + y`)와 비교하게 됩니다.  
    이외의 객체와의 비교는 `NotImplemented`를 반환합니다.

- ### `Pos.x()`
  x좌표 값 (행 번호)를 반환합니다.

- |Return type|Description|
  |---|---|
  |[`int`]|

- ### `Pos.y()`
  y좌표 값 (열 번호)를 반환합니다.

- |Return type|Description|
  |---|---|
  |[`int`]|

- ### `Pos.xy()`
  x좌표와 y좌표 값 (행/열 번호)를 반환합니다.

- |Return type|Description|
  |---|---|
  |[tuple]\[[int], [int]]|

- ### `Pos.n()`
  그리드 번호를 반환합니다.

- |Return type|Description|
  |---|---|
  |[`int`]|`x * grid[0] + y`와 동일합니다.|

---

## `lo_imports.Datas`
버프의 추가 정보들을 담을 때 사용되는 클래스를 모아놓은 클래스입니다.  
모두 [`NamedTuple`](#https://docs.python.org/ko/3/library/typing.html#typing.NamedTuple)을 상속받습니다.  
Alias로 `lo_imports.D`로 접근할 수도 있습니다.

- ### `Datas.TargetProtect`
  지정 보호 버프 (`BuffType.TARGET_PROTECT`)의 추가 정보를 저장합니다.

  - |Attribute|Type|Description|
    |---|---|---|
    |`target`|[`Character`]|지정 보호 시전자|

- ### `Datas.Provoked`
  도발 버프 (`BuffType.PROVOKED`)의 추가 정보를 저장합니다.

  - |Attribute|Type|Description|
    |---|---|---|
    |`target`|[`Character`]|도발 시전자|

- ### `Datas.FollowAttack`
  지원 공격 버프 (`BuffType.FOLLOW_ATTACK`)의 추가 정보를 저장합니다.

  - |Attribute|Type|Description|
    |---|---|---|
    |`attacker`|[`Character`]|지원 공격 시전자|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|지원 공격 발동 확률|

- ### `Datas.CoopAttack`
  협동 공격 버프 (`BuffType.COOP_ATTACK`)의 추가 정보를 저장합니다.

  - |Attribute|Type|Description|
    |---|---|---|
    |`attacker`|[`Character`]|협동 공격 시전자|
    |`skill_no`|[`int`]|협동 공격할 스킬 번호|

- ### `Datas.BuffCond`
  버프 조건 정보를 저장합니다.  
  버프 제거 버프(`BuffType.REMOVE_BUFF`), 버프 면역 버프(`BuffType.IMMUNE_BUFF`), 조건부 버프 등에 사용됩니다.

  - |Attribute|Type|Description|
    |---|---|---|
    |`type_`|<code>[BuffType] &#124; Iterable\[[BuffType]]</code>|[`BuffType`] 또는 [`BuffType`]로 이루어진 Iterable 객체<br>([`set`]을 추천합니다)|
    |`efft`|[`BuffEffectType`]|버프 효과 타입<br>다중 입력이 가능합니다. (예: <code>BET.BUFF &#124; BET.DEBUFF</code>)|
    |`tag`|[`str`]|태그|
    |`func`|<code>[Callable](https://docs.python.org/ko/3.10/library/typing.html#callable)\[\[[Buff]\], [bool]\]</code>|판정 함수|
    |`id_`|<code>[int] &#124; Iterable\[[int]]</code>|버프 ID|
    |`val_sign`|`-1`, `0`, `1` 중 하나|버프 수치 부호|
    |`limit`|[`int`]|제거 횟수 제한 *(버프 제거에 사용)*<br>기본 값은 `sys.maxsize`입니다.|
    |`force`|[`bool`]|강제 제거 여부 *(버프 제거에 사용)*|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|버프 판정 확률 *(버프 검색에 사용)*|

- ### `Datas.DmgInfo`
  피해 관련 추가 정보를 저장합니다.  
  `BuffType.TAKEDMGINC`, `BuffType.TAKEDMGDEC`, `BuffType.GIVEDMGINC`, `BuffType.GIVEDMGDEC`, `BuffType.INSTANT_DMG`, `BuffType.DOT_DMG`에 사용됩니다.

  - |Attribute|Type|Description|
    |---|---|---|
    |`subject`|[`Character`]|공격력% 피해 시 기반 공격력이 되는 캐릭터|
    |`hp_type`|[`int`]|HP% 비례 여부<br>- `0`: 비례하지 않음 (기본값)<br>- `1`: 자신의 HP%가 높을수록<br>- `2`: 대상의 HP%가 높을수록<br>- `3`: 자신의 HP%가 낮을수록<br>- `4`: 대상의 HP%가 낮을수록|
    |`element`|<code>[int] &#124; [Element]</code>|피해 속성<br>[`int`]를 입력하면 자동으로 [`Element`]로 변환됩니다.|

- ### `Datas.BattleLogInfo`
  게임 로그에 사용

  - |Attribute|Type|Description|
    |---|---|---|
    |`event`|<code>[str] &#124; [Trigger]</code>|대충 이벤트|
    |`desc`|[`str`]|대충 설명|
    |`random_status`|[`tuple`]|`random.getstate()`|


