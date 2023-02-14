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

---

> <font size=+3 color="red">**경고**</font>  
> **보호 매커니즘, 패시브 버프 적용 순서, 데미지 계산, 효과 저항 적용** 등등  
> 많은 부분에서 인게임과 <font color="red">**다소 차이가 날 수 있습니다.**</font>  
> 차이가 나는 케이스를 개발자한테 전달하주시면 개발자에게 큰 힘이 됩니다!

---

[lo_enum.py](./API_enum.md)

[lo_system.py](./API_system.md)

[lo_char.py](./API_char.md)

[lo_equips.py](./API_equips.md)

[lo_imports.py](./API_imports.md)
