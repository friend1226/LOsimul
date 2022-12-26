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
[Pos]: ./API_imports.md#lo_importspos
[`Pos`]: ./API_imports.md#lo_importspos

[`Game`]: #lo_systemgame
[`Buff`]: #lo_systembuff
[Buff]: #lo_systembuff
[`BuffList`]: #lo_systembufflist
[`BuffSUM`]: #lo_systembuffsum

[`Buff.issatisfy`]: #buffissatisfy-type_none-efftnone-tagnone-funcnone-id_none-val_signnone-oprnone-chance100-kwargs

# lo_simul.`lo_system`

게임 판과 버프(Buff)가 구현되어있는 모듈입니다.

---

## `lo_system.Game` *()*
게임 판을 담당하는 클래스입니다.  
캐릭터 배치/제거나 스킬 발동, 라운드/웨이브 진행을 할 수 있습니다.  
초기화시 인자를 받지 않습니다.

```python
from lo_simul.lo_system import Game

g = Game()
```

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

- ### `Game.put_char` *(c, field=None)*
  캐릭터를 배치합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`c`|`Character`|**배치할 캐릭터 개체**<br>배치할 위치에 캐릭터가 존재하면<br>해당 캐릭터는 [`remove_char`](#gameremove_char-c-msgfalse)로 제거됩니다.|
    |`field`|<code>[int] &#124; None</code>|**배치할 필드**<br>`0` = 아군<br>`1` = 적군<br>`None` = `c.isenemy`값|

- ### `Game.remove_char` *(c, msg=False)*
  캐릭터를 제거합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`c`|`Character`|**제거할 캐릭터 개체**<br>캐릭터가 배치되어 있지 않으면<br>[`ValueError`]를 일으킵니다.|
    |`msg`|[`bool`]|`True` 설정 시<br>제거 메세지를 출력합니다.|

- ### `Game.get_char` *(x, y=None, field=0)*
  해당 위치에 있는 캐릭터를 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`x`, `y`|[`int`], [`int`]<br>또는<br><code>[int] &#124; [tuple][[int], [int]] &#124; [Pos]</code>, `None`|**얻고자 하는 캐릭터의 위치**<br>2차원 좌표나 그리드 번호, 또는 [`Pos`]객체.|
    |`field`|[`int`]|**원하는 캐릭터의 필드**<br>`0` = 아군<br>`1` = 적군|
  - 예시
    ```python
    ...
    p = Pos(2, 1)
    assert g.get_char(2, 1) \        # x = 2     , y = 1
           == g.get_char((2, 1)) \   # x = (2, 1), y = None
           == g.get_char(7) \        # x = 7     , y = None
           == g.get_char(p)          # x = p     , y = None
    ...
    ```

- ### `Game.get_chars` *(aoe=None, field=0)*
  해당 위치에 있는 캐릭터들을 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`aoe`|<code>Iterable[[tuple][[int], [int]] &#124; [int] &#124; [Pos]]</code>|**얻고자 하는 범위 리스트**<br>각 요소는[`get_char`](#gameget_char-x-ynone-field0)의 인자로<br>사용될 수 있어야 합니다.|
    |`field`|[`int`]|**범위의 필드**<br>`0` = 아군<br>`1` = 적군|

  - |Return type|Description|
    |---|---|
    |<code>[dict][[tuple][[int], [int]], Character]</code>|(2차원 좌표, 캐릭터 개체)로 매핑된 딕셔너리입니다.|

- ### `Game.put_from_file` *(filename, field)*
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

- ### `Game.trigger` *(trigtype=Trigger.DUMMY, ally_pos=None, enemy_pos=None, args=None)*
  ***트리거***를 발동합니다.    
  ***트리거***를 통해 조건부로 발동하는 패시브 버프들(예: 공격 시, 피격 시, 라운드 시작 시 등)을 발동할 수 있습니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`trigtype`|[`Trigger`]|**트리거 타입**|
    |`ally_pos`, `enemy_pos`|<code>Iterable[[int] &#124; [tuple][[int], [int]] &#124; [Pos]]</code>|**트리거 순서**<br>순서대로 트리거 할 위치 배열.<br>`None`(기본값)은 `(0, 1, 2, ..., 8)`입니다.|
    |`args`|`Any`|트리거에 추가로 필요한 데이터.|
  - `ally_pos`, `enemy_pos`의 정확한 기본값은 <code>[lo_enum.BasicData](#lo_enumbasicdata).passive_order</code>에 저장되어 있습니다.
  - 적군 진영에 아무도 없고 <code>[Trigger].DUMMY</code>를 트리거하면 자동으로 웨이브를 종료합니다.([`Game.wave_end()`](#gamewave_startbrgamewave_endbrgameround_startbrgameround_end))   
  - 아군이 먼저 트리거됩니다. 즉, 트리거 순서는 `ally_pos`, `enemy_pos` 순입니다.

- ### `Game.get_targets` *(aoe, ignore_protect=False, field=0)*
  공격 범위를 입력받고 피격당하는 캐릭터들을 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`aoe`|<code>Iterable[[tuple][[int], [int]] &#124; [int] &#124; [Pos]]</code>|**공격 범위**<br>[`get_chars`](#gameget_chars-aoenone-field0)의 `aoe` 매개변수와 동일합니다.|
    |`ignore_protect`|[`bool`]|**트리거 순서**<br>순서대로 트리거 할 위치 배열.<br>`None`(기본값)은 `(0, 1, 2, ..., 8)`입니다.|
  
  - |Return type|Description|
    |---|---|
    |<code>[dict][[tuple]\[[int], [int]], [tuple]\[[str] &#124; None, Character]]</code>|각 2차원 좌표마다 보호 타입(`str`)과 실제 피격되는 캐릭터(`Character`)가 매핑된 딕셔너리입니다.<br>보호 타입이 `None`이면 보호를 받지 않았다는 뜻입니다.|

- ### `Game.use_skill` *(subjc, skill_no, objpos=None)*
  캐릭터의 행동을 지휘합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`subjc`|`Character`|**공격 캐릭터**<br>행동하는 캐릭터 개체입니다.|
    |`skill_no`|[`int`]|**행동 타입**<br>`1` = 액티브 1스킬<br>`2` = 액티브 2스킬<br>`3` = 이동<br>`4` = 대기|
    |`objpos`|<code>[int] &#124; [tuple][[int], [int]] &#124; [Pos]</code>|**목표 좌표**<br>대상 지정이 아닌 스킬 또는 대기이면 이 매개변수는 비워뇌도 됩니다.|
  - 만약 해당 스킬이 착탄 스킬이라면, 해당 스킬은 저장되었다가,   
    정해진 턴 이후 [`Game.round_end()`](#gamewave_startbrgamewave_endbrgameround_startbrgameround_end) 호출 시 <code>[Trigger].ROUND_END</code> 트리거 이전에 발동됩니다. 

- ### `Game.give_buff(...)`
  캐릭터에게 버프를 부여합니다.
  - Parameter는 [`Buff`] 생성 시와 비슷하지만, 약간 다르거나 추가/삭제된 요소가 있습니다.
    
    |Parameter|Type|Default Value|Description|
    |---|---|---|---|
    |`target`|`Character`|*필수 입력*|**버프를 받는 캐릭터**|
    |`type_`|[`str`]\([`BuffType`])|*필수 입력*|**버프 타입**|
    |`opr`|[`int`]\(`0` or `1`)|*필수 입력*|**버프 계산 타입**<br>`0` = 덧셈 / `1` = 곱셈|
    |`value`|<code>[int] &#124; [decimal.Decimal]</code>|*필수 입력*|**버프 수치**|
    |`round_`|[`int`]|`sys.maxsize`|**지속 라운드**|
    |`count`|[`int`]|`sys.maxsize`|**횟수 제한**|
    |`count_trig`|<code>[set][[str] 또는 [Trigger]]</code>|`None`|**횟수 차감 트리거**<br>횟수(`count`)를 차감할 [`Trigger`]들의 집합입니다.|
    |`efft`|[`BuffEffectType`]|`BET.NORMAL`|**버프 효과 타입**<br>이로운(`BET.BUFF`), 해로운(`BET.DEBUFF`), 일반(`BET.NORMAL`)|
    |`max_stack`|[`int`]|`0`|**최대 중첩 수**<br>최대 중첩 수를 설정하려면 꼭 `tag` 매개변수도 설정해야 합니다.<br>`0` = 제한 없음|
    |`removable`|[`bool`]|`True`|**해제 가능 여부**<br>`False`로 설정하면 이 버프는 해제 버프로 해제할 수 없습니다.<br>이 버프를 해제하려면 `Character.remove_buff`를 사용해야 합니다.|
    |`tag`|[`str`]|`None`|**버프 태그**<br>특별한 버프를 구별할 문자열입니다.<br>**이 문자열은 `desc`와 다르며, [`Gimmick`](./API_enum.md#lo_enumgimmicklo_enumg)이 아닌 이상 보여지지 않습니다.**|
    |`data`|`Datas`|`None`|**버프의 추가 데이터**<br>버프 적용에 필요한 추가적인 데이터입니다.|
    |`proportion`|<code>[tuple][Character, [BuffType]]</code>|`None`|**버프 비례 데이터**<br>버프가 어느 캐릭터의 어느 수치에 비례하는지를 입력합니다.|
    |`desc`|[`str`]|`None`|**버프 표시 문자열**<br>텍스트 출력 시 다른 버프와 구별할 문자열입니다. (표시용)|
    |`overlap_type`|[`BuffOverlapType`]|`None`|**버프 적용 타입**<br>버프가 적용되는 타입을 설정합니다. ([`BuffOverlapType`] 참고)|
    |`force`|[`bool`]|`False`|**강제 적용 여부**<br>`True`로 설정하면 효과 저항 등에 영향을 받지 않고 적용됩니다. (`chance`는 적용됨)|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|`100`|**적용 확률**<br>버프가 적용될 확률을 백분율로 입력합니다.|
    |`made_by`|`Character`|`None`|**버프를 발현한 캐릭터**<br>`None`이면 이 함수를 호출한 프레임의 `self`값을 얻어옵니다. (없으면 `None`)|
    |`do_print`|[`bool`]|`True`|**버프 로그 여부**<br>`True`로 설정하면 적용/제거될 때 기록을 남기지 않습니다.|

  - |Return type|Description|
    |---|---|
    |`Buff`|추가된 버프의 `Buff` 객체를 반환합니다.|
    |`None`|(버프 적용 실패 시)|

- ### `Game.wave_start` *()*<br>`Game.wave_end` *()*<br>`Game.round_start` *()*<br>`Game.round_end` *()*
  전투/라운드 시작/종료
  - 각각 <code>[TR].WAVE_START</code>, <code>[TR].WAVE_END</code>, <code>[TR].ROUND_START</code>, <code>[TR].ROUND_START</code> 트리거를 발동합니다.
  - 필드에 아/적군 아무도 없으면 발동되지 않습니다.
  > #### 주의
  > <code>[TR].ROUND_START</code> 트리거는 [`Game.round`](#gameround)가 증가되기 전에 발동됩니다.  
  > 예를 들어, <U>**3**</U>라운드를 시작하면서 <code>[TR].ROUND_START</code>가 트리거될 때 [`Game.round`](#gameround) 값은 <U>**2**</U>입니다.

- ### `Game.get_act_order` *(skill_uses=None)*<br>`Game.get_act_order_str` *(skill_uses=None)*
  캐릭터의 행동 순서를 반환합니다.
  - |Parameter|Type|Description|
    |---|---|---|
    |`skill_uses`|<code>[dict][Character, Sequence[[int]]]</code>|**예약된 스킬 사용 데이터**<br>캐릭터마다 사용할 스킬을 모아놓은 딕셔너리입니다.<br>(예: `[1, 1, 2]` = 1번, 1번, 2번 스킬 예약)|

  - |Function|Return type|Description|
    |---|---|---|
    |`get_act_order`|<code>[list][[tuple][Character, [decimal.Decimal], [decimal.Decimal], [int]]]</code>|각 캐릭터의 AP, 행동력, 위치가 포함된 리스트를 반환합니다.<br>(오름차순).|
    |`get_act_order_str`|[`str`]|위 결과를 텍스트로 변환하여 반환합니다. 위치는 키패드 번호 배치를 따릅니다. (<code>[lo_enum.BasicData](#lo_enumbasicdata).keypad</code>)|

- ### `Game.process_move` *()*
  예약된 캐릭터 행동 task를 처리합니다.  
  [`Game`]객체가 트리거될 때마다 호출됩니다.

---

## `lo_system.Buff`
버프를 담당하는 클래스입니다.

- ### `Buff` *(type_, opr, value, round_=MAX, count=MAX, count_trig=None, efft=BET.NORMAL, max_stack=0, removable=True, tag=None, data=None, proportion=None, desc=None, owner=None, made_by=None, game=None, do_print=True)*
  - |Parameter|Type|Default Value|Description|
    |---|---|---|---|
    |`type_`|[`str`]\([`BuffType`])|*필수 입력*|**버프 타입**|
    |`opr`|[`int`]\(`0` or `1`)|*필수 입력*|**버프 계산 타입**<br>`0` = 덧셈 / `1` = 곱셈|
    |`value`|<code>[int] &#124; [decimal.Decimal]</code>|*필수 입력*|**버프 수치**|
    |`round_`|[`int`]|`sys.maxsize`|**지속 라운드**|
    |`count`|[`int`]|`sys.maxsize`|**횟수 제한**|
    |`count_trig`|<code>[set][[str] 또는 [Trigger]]</code>|`set()`|**횟수 차감 트리거**<br>횟수(`count`)를 차감할 [`Trigger`]들의 집합입니다.|
    |`efft`|[`BuffEffectType`]|`BET.NORMAL`|**버프 효과 타입**<br>이로운(`BET.BUFF`), 해로운(`BET.DEBUFF`), 일반(`BET.NORMAL`)|
    |`max_stack`|[`int`]|`0`|**최대 중첩 수**<br>최대 중첩 수를 설정하려면 꼭 `tag` 매개변수도 설정해야 합니다.<br>`0` = 제한 없음|
    |`removable`|[`bool`]|`True`|**해제 가능 여부**<br>`False`로 설정하면 이 버프는 해제 버프로 해제할 수 없습니다.<br>이 버프를 해제하려면 `Character.remove_buff`를 사용해야 합니다.|
    |`tag`|[`str`]|`None`|**버프 태그**<br>특별한 버프를 구별할 문자열입니다.<br>**이 문자열은 `desc`와 다르며, [`Gimmick`](./API_enum.md#lo_enumgimmicklo_enumg)이 아닌 이상 보여지지 않습니다.**|
    |`data`|`Datas`|`None`|**버프의 추가 데이터**<br>버프 적용에 필요한 추가적인 데이터입니다.|
    |`proportion`|<code>[tuple][Character, [BuffType]]</code>|`None`|**버프 비례 데이터**<br>버프가 어느 캐릭터의 어느 수치에 비례하는지를 입력합니다.|
    |`desc`|[`str`]|`None`|**버프 표시 문자열**<br>텍스트 출력 시 다른 버프와 구별할 문자열입니다. (표시용)|
    |`owner`|`Character`|`None`|**버프 소유자**|
    |`made_by`|`Character`|`None`|**버프를 발현한 캐릭터**|
    |`game`|[`Game`]|`None`|**버프가 존재하는 Game 객체**|
    |`do_print`|[`bool`]|`True`|**버프 로그 여부**<br>`True`로 설정하면 적용/제거될 때 기록을 남기지 않습니다.|

    위 파라메터들의 이름들은 만들어진 [`Buff`] 객체의 속성으로 접근할 수 있습니다.  
    (`type_`, `round_`, `efft` 제외: 각각 `type`, `round`, `efftype`로 접근할 수 있습니다.)
    ```python
    b = Buff(BT.MINIMIZE_DMG, 0, 9999999, round_=9, efft=BET.BUFF)
    assert b.type == BT.MINIMIZE_DMG \
           and b.round == 9 \
           and b.efftype == BET.BUFF \
           and b.opr == 0
    ```

  - #### `type_`에 따른 `opr`, `value` 입력 방법
    - 기본적으로, 합연산이면 `opr`값은 0, `value`에는 적용하고자 하는 값을 입력하고,  
      곱연산이면 `opr`값은 1, `value`에는 적용하고자 하는 %수치를 100으로 나눈 값을 입력합니다.
      ```python
      import decimal
      d = decimal.Decimal

      Buff(BT.ATK, 1, d('.2'))  # 공격력 +20%
      Buff(BT.EVA, 0, 20)  # 회피 +20%
      ```
    - 적중, 회피, 치명률 중감의 경우 %증가로 표시되더라도 실제로는 합연산으로 적용되므로  
      위의 예시처럼 입력하십시오.
    - [`lo_enum.BT_NOVAL`](./API_enum.md#bufftype-추가-편의-변수들)에 속하는 `type`의 경우 아무 값으로 설정해도 됩니다만, `opr=0, value=1`을 추천합니다.
    - **효과 저항, 효과 발동, 버프 해제 저항, 속성 저항 관련** 버프들에 대해서는  
      `value` 값을 %수치 그대로 입력하십시오.  
      (단, 속성 저항에 곱연산을 적용하려는 경우는 예외입니다.)
      ```python
      Buff(BT.FIRE_RES, 0, 20)  # 화염 저항 +20% (80% => 100%)
      Buff(BT.FIRE_RES, 1, d('.2'))  # 화염 저항 수치를 1.2배로 올림 (80% => 96%)
      ```
    - **효과 저항, 버프 해제 저항** 버프의 경우 실제로 버프 적용 계산에 사용될 때 2가지로 사용됩니다:
      1. 버프 적용을 판정하는 경우 (예: 효과 저항)
      2. 기본 적용 확률을 조정하는 경우 (예: 효과 저항 감소)
      a 방식으로 적용하고 싶은 경우 `opr`값을 1, b 방식으로 적용하고 싶은 경우 0으로 입력하십시오.

      ```python
      # https://arca.live/b/lastorigin/48033013 (아카라이브 효과학개론 글) 2. (c)번 참고
      from lo_simul import *
      
      g = Game()
      ally = DummyAlly(g, 4)
      enemy = DummyEnemy(g, 4)
      g.put_char(ally)
      g.put_char(enemy)

      ally.give_buff(BT.ACTIVE_RATE, 0, -20, do_print=False)
      enemy.give_buff(BT.ACTIVE_RESIST, 1, 25, do_print=False)
      enemy.give_buff(BT.ACTIVE_RESIST, 1, -36, do_print=False)
      
      g.give_buff(enemy, BT.GIMMICK, 0, 1, efft=BET.DEBUFF, chance=50, made_by=ally)
      # [brs] <더미(적군)_A> - 버프 추가 실패 (확률) : [기믹 (99+라운드, 99+횟수) {해로운 효과}] (80.00% 확률)
      # [brs] <더미(적군)_A> - 버프 추가 실패 (저항) : [기믹 (99+라운드, 99+횟수) {해로운 효과}] (21.50% 확률)
      # [bad] <더미(적군)_A> - 버프 추가됨: [기믹 (99+라운드, 99+횟수) {해로운 효과}] (17.20% 확률)
      ```

      - **버프 해제 저항**은 *(인게임에서 이 버프타입이 구현된 것은 **강화 해제 저항** 뿐입니다)*  
        인게임에서는 합연산밖에 존재하지 않지만, 만일 곱연산(독립시행)으로 구현하고 싶은 분들을 위해  
        효과 저항 버프처럼 작동하게 구현해놨으니 참고하시기 바랍니다.  
        즉, 인게임 구현을 위해서는 **버프 해제 저항 버프타입은 `opr`값을 무조건 0으로 입력하셔야 합니다.**

  - 만약 `proportion`의 [`BuffType`]이 [`lo_enum.BT_CYCLABLE`](./API_enum.md#bufftype-추가-편의-변수들)에 포함되지 않는다면 [`ValueError`]를 일으킵니다.

- ### _@property_ `Buff.id`
  [`Buff`]의 고유 ID를 반환합니다. *(양수)*  
  같은 [`Buff`] 클래스로 만들어진 서로 다른 [`Buff`] 객체는 ID 값 또한 서로 달라야 합니다.

- ### `Buff.random`
  랜덤 판정에 사용되는 함수입니다.
  1. `owner`가 정해졌다면 `owner.random`과 동일합니다.
  2. 대신 `game`이 정해졌다면 `game.random.uniform`을 사용합니다.
  3. 둘 모두 안 정해졌다면 `random` 모듈의 `random.uniform`을 사용합니다.

  파라메터 및 리턴에 관해서는 `Character.random`을 참고하십시오.

- ### `Buff.expired`
  버프 만료 여부입니다. (기본값 `False`)  
  이 값은 라운드 지속 시간 종료, 횟수 모두 차감 등과 **관련이 없는 독립적인 값**이며  
  이 값이 `True`면 `TR.DUMMY` 트리거 시 제거됩니다.  

  <code>[BT].INSTANT_DMG</code> 버프이거나 [`Game.give_buff`](#gamegive_buff)에서 `overlap_type` 값을 <code>[BOT].INSTANCE</code>로 설정 시 이 값이 `True`로 설정됩니다.

- ### `Buff.calc` *(v, extra_rate=None)*
  버프가 해당 수치에 적용된 값을 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`v`|<code>[int] &#124; [decimal.Decimal]</code>|계산할 수치|
    |`extra_rate`|<code>[int] &#124; [decimal.Decimal]</code>|버프 수치를 조정할 비율 값<br>기본값은 `decimal.Decimal(1)`입니다.|

  - |Return type|Description|
    |---|---|
    |[`decimal.Decimal`]|계산된 값|

  - Examples
    ```python
    print(Buff(BT.ATK, 1, d('.3')).calc(10))  # 13
    print(Buff(BT.ATK, 1, d('.3')).calc(10, extra_rate=d('.5')))  # 11.5
    print(Buff(BT.ACC, 0, 50).calc(40, extra_rate=d('.1')))  # 45
    ```

- ### `Buff.trigger` *(tt, args=None)*
  버프에 트리거를 발동합니다.  
  후술할 `BuffList.update`에서 이 함수를 호출합니다.  
  `Buff.base_passive`와 `Buff.passive`를 호출하며, 인자들을 그대로 입력합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|

- ### `Buff.base_passive` *(tt, args=None)*
  트리거 발동시 기본으로 동작시킬 코드들입니다.

- ### `Buff.passive` *(tt, args=None)*
  여기에 추가로 트리거 발동시 동작시킬 코드를 작성하십시오.

- ### `Buff.issatisfy` *(type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None, chance=100, **kwargs)*
  이 버프가 주어지는 조건을 만족하는 지를 반환하는 함수입니다.  
  특정 조건을 만족하는 버프 검색/삭제 시 이 함수를 통해 판단합니다.  
    
  모든 매개변수들은 기본값으로 `None`이 주어지며, 해당 조건을 검사하지 않고 **패스**하게 됩니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`type_`|[`BuffType`] 또는 <code>[Collection][[BuffType]]</code>|**버프 타입**<br>Collection으로 모아서 여러 타입들로 검사할 수 있습니다.|
    |`efft`|[`BuffEffectType`]|**버프 효과 타입**|
    |`tag`|[`str`]|**버프 태그**<br>동등이 아닌 포함 여부로 판정합니다. (`str.startswith`)|
    |`func`|<code>[Callable](https://docs.python.org/ko/3.10/library/typing.html#callable)\[\[[Buff]\], [bool]\]</code>|**버프 판정 함수**<br>Buff 객체를 받아 boolean 값을 반환해야 합니다.<br>여기 나열된 매개변수들로 부족하다면 직접 판정 함수를 만들어 입력하십시오.|
    |`id_`|[`int`] 또는 <code>[Collection][[int]]</code>|**버프 ID**<br>Collection으로 모아서 여러 ID들로 검사할 수 있습니다.|
    |`val_sign`|`-1`, `0`, `1` 중 하나|**버프 수치 부호**|
    |`opr`|`0`, `1` 중 하나|**버프 연산 타입**|
    |`chance`|<code>[int] &#124; [decimal.Decimal]</code>|**버프 판정 확률**|
  
  - |Return type|Description|
    |---|---|
    |[`bool`]|판정 결과 (`True`가 만족입니다.)|

- ### 일부 타입들과의 상호작용
  - 숫자(<code>[int] &#124; [decimal.Decimal]</code>)를 곱하면 `value` 속성에 적용됩니다.
    
    ```python
    b1 = Buff(BT.ATK, 1, d('.25'))
    b2 = Buff(BT.ATK, 1, d('.1'))

    print(b1 == (b2 * d('2.5')))  # True
    ```
    제자리 연산을 수행할 경우 (`*=`) 결과값은 새로운 [`Buff`] 객체를 만들지 않고 자기 자신을 반환합니다.
  
  - [`Buff`]간 동등 여부는 `Buff.attrs`에 있는 속성들의 값이 모두 같아야 합니다.  
    (`type`, `opr`, `value`, `round`, `count`, `count_triggers`, `efftype`, `max_stack`, `removable`, `tag`, `data`, `desc`, `owner`)  
    
    > **주의**  
    > 이 조건은 불시에 변경될 수 있습니다.

---

## `lo_system.BuffList`
[`Buff`]를 관리하는 리스트 클래스입니다.

- ### `BuffList` *(\*buffs)*
  - |Parameter|Type|Description|
    |---|---|---|
    |`buffs`|[`Buff`]|버프들.<br>만약 리스트 등 컨테이너를 입력하고 싶다면 언패킹해야 합니다.|

- ### `BuffList.buffs`
  실제 버프들이 저장되는 [`collections.deque`](https://docs.python.org/ko/3.10/library/collections.html#collections.deque)타입의 속성입니다.

- ### `BuffList.show_str` *()*
  버프들을 문자열로 바꿔서 한 줄씩 붙여 만든 문자열을 반환합니다.

- ### *@property* `BuffList.count`
  버프 개수입니다.  `len(BuffList)`, `len(BuffList.buffs)`와 동일합니다.

- ### `BuffList.append` *(buff)*
  `BuffList.buffs.append`와 동일하나, `None`값은 추가하지 않습니다.

- ### `BuffList.appendleft` *(buff)*
  `BuffList.buffs.appendleft`와 동일하나, `None`값은 추가하지 않습니다.

- ### `BuffList.pop` *()*
  `BuffList.buffs.pop`와 동일합니다.

- ### `BuffList.popleft` *()*
  `BuffList.buffs.pop`와 동일합니다.

- ### `BuffList.union` *(other)*
  다른 [`BuffList`]의 버프들을 자신의 리스트로 들여옵니다.  
  > **<주의>**  
  > `other`는 빈 리스트가 되고, 새로운 객체가 아닌 원래의 자신을 반환합니다.  
  >  ```python
  >  def union(self, other: 'BuffList'):
  >    while other:
  >        self.append(other.popleft())
  >    return self
  >  ```

- ### `BuffList.update` *(tt=TR.DUMMY, args=None, except_condition=None)*
  버프들을 트리거하고, 라운드 지속 시간을 초과하거나 횟수가 모두 차감된 버프들을 제거합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`tt`|[`Trigger`]|트리거 타입|
    |`args`|`Any`|트리거에 뒤따라오는 추가 데이터들|
    |`except_condition`|<code>[Callable]\[\[[Buff]], [bool]]</code>|트리거하지 않을 버프를 판정하는 함수|
  
  - |Return type|Description|
    |---|---|
    |[`BuffList`]|제거된 버프 리스트|

- ### `BuffList.find` *(type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None, **kwargs)*
  조건에 맞는 버프를 검색하여 새 [`BuffList`]로 반환합니다.  
  [`Buff.issatisfy`]에 있는 파라메터 이름과 동일한 파라메터는 그 부분에 있는 설명을 참고하십시오.
  
  - |Return type|Description|
    |---|---|
    |[`BuffList`]|조건을 만족하는 버프 리스트|

- ### `BuffList.remove` *(type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None, limit=MAX, force=False)*
  조건에 맞는 버프를 검색하여 제거합니다.  
  [`Buff.issatisfy`]에 있는 파라메터 이름과 동일한 파라메터는 그 부분에 있는 설명을 참고하십시오.

  - 추가 파라메터들  
    |Parameter|Type|Description|
    |---|---|---|
    |`limit`|[`int`]|제거 횟수 제한<br>기본 값은 `sys.maxsize`입니다.|
    |`force`|[`bool`]|`True` 설정시 `Buff.removable`이 `False`인 버프도 제거합니다.|
  
  - |Return type|Description|
    |---|---|
    |[`BuffList`]|제거된 버프 리스트|

- ### `BuffList.get_sum` *(mul=False)*
  버프를 합하여 계산할 수 있는 [`BuffSUM`] 객체를 반환합니다.  

  `mul` 파라메터에 관해서는 [`BuffSUM`]의 초기화 함수 설명을 참고하십시오.

- ### 일부 타입들과의 상호작용
  - 다른 [`BuffList`] 객체와 더할 수 있습니다.  
    제자리 연산이 아니라면 새로운 [`BuffList`] 객체를 반환하고, 제자리 연산이라면 자기 자신을 반환합니다.  
    오른쪽 피연산자인 [`BuffList`] 객체 안의 [`Buff`]들은 [`BuffList.union`](#bufflistunion-other)과 달리 없어지지 않지만, [`Buff`] 객체를 그대로 가져옵니다.

  - 숫자(<code>[int] &#124; [decimal.Decimal]</code>)를 곱하면 안의 모든 [`Buff`] 객체에 대해 연산을 수행합니다.  
    새로운 [`BuffList`] 객체를 반환하고, 안에 있는 [`Buff`] 객체들도 새로 생성하여 추가합니다.  
    만약 제자리 연산이라면, 자기 자신을 반환하고, 안에 있는 [`Buff`] 객체들도 제자리 연산됩니다.

---

## `lo_system.BuffSUM`
버프 통합 계산에 사용되는 클래스입니다.  

안에는 모든 [`BuffType`]에 대해 합연산 수치와 곱연산 수치를 지니는 딕셔너리가 포함되어 있습니다.  
기본 값은 `[d(0), d(1)]`이고, 1번째 요소가 합연산 수치, 2번째 요소가 곱연산 수치입니다.  
[`Buff`]와 달리, 곱연산 수치에 1이 추가로 더해져 있는데, 이는 이후 후술할 다른 [`BuffSUM`]과 합치거나 곱할 때의 계산을 용이하게 하기 위해서입니다.

- ### `BuffSUM` *(buffs, mul=False)*
  - |Parameter|Type|Description|
    |---|---|---|
    |`buffs`|[`BuffList`]|통합할 버프 리스트|
    |`mul`|[`bool`]|`False`(기본값) 설정시 곱연산 수치들은 합연산됩니다.<br>`True` 설정시 곱연산 수치들은 곱연산됩니다.|

    ```
    Example) 20% + 30%
    mul=False => 50% (1 + 0.2 + 0.3)
    mul=True  => 56% (1.2 * 1.3)
    ```

- ### `BuffSUM.calc` *(t, v=1, switch_order=False, extra_rate=None)*
  버프가 해당 수치에 적용된 값을 반환합니다.

  - |Parameter|Type|Description|
    |---|---|---|
    |`t`|[`BuffType`]|계산할 버프 타입|
    |`v`|<code>[int] &#124; [decimal.Decimal]</code>|계산할 수치|
    |`switch_order`|[`bool`]|기본값(`False`) 설정시 곱연산 후 합연산,<br>`True` 설정시 합연산 후 곱연산합니다.|
    |`extra_rate`|<code>[int] &#124; [decimal.Decimal]</code>|버프 수치를 조정할 비율 값<br>기본값은 `decimal.Decimal(1)`입니다.<br>**주의: 합연산 수치에는 반영되지 않습니다.**|

  - |Return type|Description|
    |---|---|
    |[`decimal.Decimal`]|계산된 값|

  - Examples
    ```python
    bs = BuffList(
        Buff(BT.ATK, 1, d('.2')),
        Buff(BT.ATK, 1, d('.3')),
        Buff(BT.ATK, 0, 30),
        Buff(BT.ACC, 0, 40)
    ).get_sum()
    
    print(bs.calc(BT.ATK, 100))
    # 180; 100 * 1.5 + 30
    print(bs.calc(BT.ATK, 100, switch_order=True))
    # 195; (100 + 30) * 1.5
    print(bs.calc(BT.ACC, 10))
    # 50 ; 10 + 40
    ```

- ### 일부 타입들과의 상호작용
  - 다른 [`BuffSUM`] 객체와 더하거나 곱할 수 있습니다.  
    더하거나 곱한 후의 [`BuffSUM`] 객체는 새로 생성한 객체입니다.

    더할 시 합연산/곱연산 수치들끼리 더합니다.  
    곱할 시 오른쪽 피연산자인 [`BuffSUM`] 객체의 곱연산 수치를 자기 자신의 수치에 반영한 후, 합연산 수치를 반영합니다.  

    예를 들어, 어떤 버프 수치가 `(10, 1.1)`인 객체와 같은 버프 수치가 `(5, 1.5)`인 객체가 있으면:
    - 서로 더하면 `(15, 1.6)`인 객체가 됩니다.
    - 서로 곱하면 `(20, 1.65)`인 객체가 됩니다. (합연산 수치 = `10 * 1.5 + 5 = 20`)
  
  - 숫자(<code>[int] &#124; [decimal.Decimal]</code>)를 곱하면 합연산 및 곱연산 수치에 곱합니다.