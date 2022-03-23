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
|   |-- code.py
|   |-- icons
|   |   |-- TbarIcon_.png
|   |   |-- TbarIcon_3P_Alexandra_N.png
|   |   |-- TbarIcon_3P_Alexandra_NS1.png
|   |   |-- TbarIcon_3P_Alexandra_NS2.png
|   |   |-- TbarIcon_3P_Alice_N.png
|   |   |-- ...
|   |   |-- TbarIcon_SU_HoloTiger_N.png
|   |   |-- TbarIcon_SU_HoloTiger_NS1.png
|   |   |-- TbarIcon_SU_RabbitBarrier_N.png
|   |   `-- TbarIcon_SU_TrenchBomb_N.png
|   |-- icons.py
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
|-- lo_simul
|   |-- __init__.py
|   |-- lo_char_base.py
|   |-- lo_chars
|   |   |-- __init__.py
|   |   |-- characters
|   |   |   |-- __init__.py
|   |   |   |-- characters_ally.py
|   |   |   `-- characters_enemy.py
|   |   `-- pool.py
|   |-- lo_enum.py
|   |-- lo_equips.py
|   |-- lo_imports.py
|   |-- lo_mod.py
|   `-- lo_system.py
|-- runGui.py
`-- splash.png
```

- `lo_simul` : 전투 시뮬레이터 프로그램
- `lo_gui*.py`, `runGui.py` : GUI 프로그램
- `data/unitdata` : 캐릭터의 스탯, 스킬 등의 데이터 파일

---

(여러 쓰이는 용어들 입력)

---

# lo_simul.`lo_system`

전투 상황과 버프(Buff)가 구현되어있는 모듈입니다.

- ## lo_system.`Game()`
게임 판을 만듭니다.  
이후 캐릭터를 배치하거나 전투를 진행햐는 등의 행동을 할 수 있습니다.
- ### _@property_ Game.`stream`
  - 메세지를 출력할 스트림을 설정합니다.
  - 기본값은 `sys.stdout`입니다.
- ### Game.`put_char(self, c, field=None) -> None`
  - 캐릭터를 배치합니다.
  - `c`에 캐릭터, `field`에 필드 번호를 입력합니다.   
    아군 진영에 배치하려면 `0`, 적군 진영에 배치하려면 `1`을 입력합니다.    
    `field`가 `None`이면, `c.isenemy`로 결정합니다.
  - 만약 `c`의 위치에 다른 캐릭터가 있다면, 그 캐릭터는 `Game.remove_char`를 통해 없어집니다.
- ### Game.`remove_char(self, c, msg=False) -> None`
  - 캐릭터를 제거합니다.
  - 만약 `c`가 전장에 배치되지 않았으면, `ValueError`를 일으킵니다.
  - `msg`가 `True`면, 캐릭터가 전장에서 제거된다는 메세지를 출력합니다.
- ### Game.`get_char(self, x, y=None, field=0) -> Character`
  - 해당 위치에 있는 캐릭터를 반환합니다.
  - `x`, `y`에 위치 정보, `field`에 필드 번호를 입력합니다.
  - 위치를 전달하는 방법은 다음과 같습니다.
    - `x`, `y`에 각각 행 번호`(0~2)`, 열 번호`(0~2)`를 입력합니다.
    - `x`에 그리드 번호`(0~8)`나 `(행, 열)`로 이루어진 튜플을 입력합니다.
    - `x`에 `Pos`객체를 입력합니다.
- ### Game.`get_chars(self, aoe=None, field=0) -> {(int_x, int_y): Character, ...}`
  - 해당 위치에 있는 캐릭터들을 반환합니다.
  - `aoe`는 각 요소가 `그리드_번호(int)`, `(행, 열)`, `Pos`중 하나인 배열이여야 하며,   
    `field`에는 필드 번호를 입력합니다.
  - 반환값으로는 `(행, 열): Character` 형태의 딕셔너리가 주어집니다.
- ### Game.`put_from_file(self, filename, field) ->  None`
  - 배치 정보가 저장된 파일을 불러와 저장합니다.
  - `filename`에는 해당 파일 경로를 입력합니다.    
    `field`에는 필드 번호를 입력합니다.
  - 파일 내용은 JSON으로 parse할 수 있는 텍스트여야 합니다. (GUI_README.md 내용 옮기기)
- ### Game.`trigger(self, trigtype=Trigger.DUMMY, ally_pos=None, enemy_pos=None) -> None`
  - "트리거"를 발동합니다.    
    "트리거"를 통해 캐릭터들의 조건부 스킬(예: 공격 시, 피격 시, 라운드 시작 시 등)들을 발동할 수 있습니다.
  - `trigtype`에 트리거 타입, `ally_pos`와 `enemy_pos`에 각각 아군/적군의 트리거 적용 순서를 입력합니다.    
    `trigtype`에 들어갈 값들은 `lo_simul.lo_enum.Trigger`를 참고하세요.    
    `ally_pos`와 `enemy_pos`는 각 요소가 `그리드_번호(int)`, `(행, 열)`, `Pos`중 하나인 배열입니다.   
    생략하면 미리 정의된 순서로 정해집니다. (`lo_simul.lo_enum.BasicData.passive_order`)
  - 적군 진영에 아무도 없고 `Trigger.DUMMY`를 트리거하면 자동으로 웨이브를 종료합니다.(`Game.wave_end()`)   
    트리거 순서는 `ally_pos`, `enemy_pos` 순입니다.
- ### Game.`get_targets(self, aoe, ignore_protect=False, field=0) -> {(int_x, int_y): (str, Character), ...}`
  - 해당 `field`로 범위가 `aoe`인 공격이 들어왔을 때    
    실제로 피격당하는 캐릭터들을 반환합니다.
  - `aoe`는 `Game.get_chars`의 `aoe`에 들어갈 수 있는 값이어야 합니다.    
    `ignore_protect`가 `True`이면 보호 무시가 적용됩니다. `field`에는 필드 번호를 입력합니다.
  - 반환값으로, `(행, 열): (보호 타입, Character)` 형태의 딕셔너리가 주어집니다.   
    `보호 타입`은 `None`, `BuffType.ROW_PROTECT`, `BuffType.COLUMN_PROTECT`, `BuffType.TARGET_PROTECT` 중 하나입니다.
- ### Game.`use_skill(self, subjc, skill_no, objpos, catkr=None, follow=None, coop=None, impact=0) ->  None`
  - 캐릭터의 행동을 지휘합니다.
  - `subjc`에 행동할 캐릭터, `skill_no`에 스킬 번호, `objpos`에 대상 위치를
  (`그리드_번호(int)`, `(행, 열)`, `Pos` 중 하나로) 입력합니다.    
    `skill_no`는 1~4 중 하나입니다.
    > `1` = 액티브 1스킬  
      `2` = 액티브 2스킬  
      `3` = 이동  
      `4` = 대기
    
    `catkr`, `follow`, `coop`, `impact`는 임의로 입력하지 않는 것을 권장합니다.
    > `catkr`이 `None`이 아니면, 이 캐릭터는 반격한다는 뜻입니다.  
      `follow`가 `None`이 아니면, 이 캐릭터는 지원공격한다는 뜻입니다.   
      `coop`가 `None`이 아니면, 이 캐릭터는 협동공격한다는 뜻입니다.   
      `impact`가 `0`이 아니면, 이 공격은 착탄 공격이라는 뜻입니다.
  - 만약 해당 스킬이 착탄 스킬이라면, 해당 스킬은 저장되었다가,   
    정해진 턴 이후 `Game.round_end()` 호출 시 `ROUND_END` 트리거 이전에 발동됩니다. 