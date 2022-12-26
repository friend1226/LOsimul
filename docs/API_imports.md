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

## `lo_system.lo_imports`
내장 모듈들을 불러오고, 커스텀 클래스 및 함수들이 정의된 모듈입니다.

---

## `lo_imports.Pos`
2차원 좌표를 다루는 클래스입니다.

- ### `Pos` *(x, y=None, grid=(3, 3))*
  - |Parameter|Type|Description|
    |---|---|---|
    |`x`, `y`|[`int`], [`int`]<br>또는<br><code>[int] &#124; [str] &#124; [tuple]\[[int], [int]] &#124; [Pos]</code>|좌표값|
