from lo_simul import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QColor, QFontMetrics, QIcon

list_split = ','
list2d_split = '/'
CH_ICON_SIZE = 128
EQ_ICON_SIZE = 64

# TODO : 도움말 다듬기 & 추가
import os
with open(os.path.join(PATH, "GUI_README.md"), 'r', encoding='utf-8') as f:
    helptxt = f.read().strip()

temphelptxt = f"""============== C O M M A N D S ==============
이 프로그램에서 게임 상태를 조정할 때 쓰이는 명령어들을 설명하는 부분입니다.

0-1. field
아군/적군을 구분할 때 사용됩니다.
0은 아군(필드), 1은 적군(필드)를 의미합니다.

0-2. pos
위치를 나타낼 때 사용됩니다. 각 필드의 위치 값은 다음과 같습니다:

0 1 2
3 4 5
6 7 8

0-3. 매개변수
다음과 같이 특정 글자로 둘러쌓인 매개변수는 각각의 뜻을 가지고 있습니다:
"매개변수"는 *그대로* 입력되어야 하는 키워드를 뜻합니다. (대부분 명령어 그 자체)
"<매개변수>"는 꼭 입력되어야 하는 매개변수를 뜻합니다.
"(매개변수)"는 입력되지 않아도 되는 매개변수를 뜻합니다.
"[매|개|변|수]"는 '|'로 구분되어있는 여러 값들 중 하나를 입력하는 매개변수를 뜻합니다.
이러한 표현은 서로 동시에 사용될 수 있습니다.

일부 명령어의 경우 키워드 매개변수(keyword arguments)(kwargs로 보통 표현됩니다)를 통해 매개변수를 입력할 수 있습니다.
이때 이 입력들은 *무조건* 명령어의 맨 끝에 위치되어야 합니다.


1. add <field> <pos> <id> (kwargs)
캐릭터를 추가합니다.

field, pos는 어느 위치에 캐릭터를 추가할지 결정합니다.
id는 추가할 캐릭터의 ID값입니다.
아군의 캐릭터의 경우 도감 번호나 이름을 입력하십시오.
적군 등의 다른 캐릭터의 경우 주어진 특정 이름을 입력하십시오.

kwargs에는 다음과 같은 이름을 허용합니다:
rarity, lvl, stat_lvl, skill_lvl, equips, link, full_link_bonus_no, affection, pledge
이 이름 순서로 id 매개변수 위치의 뒤부터 차례로 값을 입력할 수도 있습니다.
(예: "add 0 0 2 lvl=5 rarity=3" 대신 "add 0 0 2 3 5"로 입력합니다.)

rarity는 캐릭터의 등급을 뜻합니다. B부터 SS까지 0부터 3의 값으로 해당됩니다. 기본값은 그 캐릭터의 태초 등급입니다.
lvl은 캐릭터의 레벨을 뜻합니다. 1부터 100까지의 정수를 입력하십시오. 기본값은 1입니다.  
stat_lvl은 캐릭터의 스탯의 레벨을 뜻합니다. '{list_split}'으로 구분하여 6개의 0~300의 정수를 입력하십시오. 
능력의 순서는 '체공방적회치'입니다. 기본값은 0,0,0,0,0,0입니다.
skill_lvl은 캐릭터의 스킬의 레벨을 뜻합니다. '{list_split}'으로 구분하여 5개의 1~10의 정수를 입력하십시오.
기본값은 1,1,1,1,1입니다.
equips는 캐릭터가 착용할 장비를 뜻합니다. [아직 구현되지 않았습니다.]
link는 캐릭터의 링크 값을 뜻합니다. 0~500의 정수를 입력하십시오. 기본값은 0입니다.
full_link_bonus_no는 캐릭터의 풀링크보너스 값을 뜻합니다. 0~4의 정수를 입력하십시오.
입력하지 않으면 풀링크보너스를 선택하지 않은 것으로 간주합니다.
affection은 호감도를 뜻합니다. 0~200의 정수를 입력하십시오. 기본값은 0입니다.
pledge는 서약 여부를 뜻합니다. 0 또는 1을 입력하십시오. 기본값은 0입니다.
current_hp는 현재 HP를 뜻합니다. 0(기본값)을 입력할 경우 100% HP가 됩니다.


2. remove <field> <pos>
해당 위치에 있는 캐릭터를 제거합니다.


3. trigger <trigtype>
모든 캐릭터에게 트리거를 보냅니다.
캐릭터의 패시브에 달려있는 일부 조건 버프를 작동할 때 사용됩니다.
trigtype에는 다음 이름들 중 하나를 입력해야 합니다:
ROUND_START = "라운드 시작 시"
ROUND_END = "라운드 종료 시"
WAVE_START = "전투 시작 시"
WAVE_END = "전투 종료 시"
ATTACK = "공격 시"
GET_ATTACKED = "공격 받을 시"
HIT = "공격 적중 시"
GET_HIT = "피격 시"
EVADE = "회피 시"
ENEMY_DEAD = "적 사망 시"
KILL = "적 처치 시"
DEAD = "사망 시"
INCAPABLE = "전투 불능 시"
ALLY_DEAD = "아군이 사망하면"
ALLY_KILLED = "아군이 처치당하면"
BATTLE_CONTINUED = "전투 속행 시"
MOVE = "이동 시"
IDLE = "대기 시"


4. skill <field> <pos> <skill_no> <objpos>
해당 위치에 있는 캐릭터가 적 필드(또는 아군 필드)의 objpos 위치에 skill_no에 따라 행동합니다.
skill_no에는 1~4의 정수를 입력하십시오.
1 = 액티브스킬1번을 사용
2 = 액티브스킬2번을 사용
3 = 해당 위치로 이동
4 = 대기

=============================================
"""


class HelpWindow(QDialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle("도움?말")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        self.textbox = QTextBrowser(self)
        self.textbox.setAcceptRichText(True)
        self.textbox.setOpenExternalLinks(True)
        self.textbox.setFont(QFont("Malgun Gothic", 10))
        self.textbox.setMarkdown(helptxt)
        self.textbox.show()
        self.textbox.moveCursor(QTextCursor.Start)
        layout.addWidget(self.textbox)
        self.setLayout(layout)

    def show_window(self):
        super().show()


class ShowActOrder(QDialog):
    def __init__(self, parent, game: 'Game', *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle("행동 순서")
        self.setGeometry(100, 100, 500, 350)
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.textbox = QTextBrowser(self)
        self.textbox.setFontPointSize(11)
        self.textbox.insertPlainText(game.get_act_order_str().strip())
        self.textbox.show()
        self.textbox.verticalScrollBar().setValue(0)
        layout.addWidget(self.textbox)
        self.setLayout(layout)

    def show_window(self):
        super().show()


class SelectFunction(QDialog):
    def __init__(self, field, pos, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle("기능 선택")
        self.setFixedSize(300, 400)
        self.selected_button_code = 0
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        addbutton = QPushButton("캐릭터 추가")
        removebutton = QPushButton("캐릭터 제거")
        movebutton = QPushButton("캐릭터 이동")
        infobutton = QPushButton("캐릭터 정보 보기")
        cancelbutton = QPushButton("취소")
        addbutton.setIcon(QIcon(os.path.join(PATH, 'images', 'add_button.png')))
        removebutton.setIcon(QIcon(os.path.join(PATH, 'images', 'remove_button.png')))
        layout.addWidget(addbutton)
        layout.addWidget(removebutton)
        layout.addWidget(movebutton)
        layout.addWidget(infobutton)
        layout.addWidget(cancelbutton)
        if parent.game.get_char(pos, field=field):
            addbutton.setDisabled(True)
        else:
            removebutton.setDisabled(True)
            movebutton.setDisabled(True)
            infobutton.setDisabled(True)
        button_codes = {
            addbutton: 1,
            removebutton: 2,
            movebutton: 3,
            infobutton: 4,
            cancelbutton: 0,
        }
        for btn, btnc in button_codes.items():
            btn.setFixedSize(300, 80)
            btn.clicked.connect(self.clicked(btnc))
        self.setLayout(layout)

    def clicked(self, button_code):
        def foo():
            if button_code:
                self.selected_button_code = button_code
                self.accept()
            else:
                self.reject()
        return foo

    def show_window(self):
        return super().exec_()


class CreateCharacter(QDialog):
    rarity_list = ['B', 'A', 'S', 'SS', 'SSS']

    def __init__(self, field, pos, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.field = field
        self.pos = pos
        if tempchar := parent.game.get_char(pos, field=field):
            raise ValueError(f"캐릭터가 존재함 : {'적군' if field else '아군'} {pos}번 위치에 {tempchar}")
        self.setWindowTitle(f"{'적군' if field else '아군'} {pos}번 위치에 캐릭터 생성")

        def makeframe(layout, *widgets):
            frame = QFrame()
            flayout = layout()
            flayout.setContentsMargins(0, 0, 0, 0)
            for w in widgets:
                flayout.addWidget(w)
            frame.setLayout(flayout)
            return frame

        def set_avaliable_minimum_width(label):
            label.setFixedWidth(QFontMetrics(label.font()).width(label.text()))

        glayout = QGridLayout()
        self.setStyleSheet("""
        QGroupBox {
            border: 1px solid gray;
            margin-top: 0.5em;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        """)

        klasslabel = QLabel("캐릭터 : ")
        set_avaliable_minimum_width(klasslabel)
        self.klassbox = klasscombobox = QComboBox()
        klasscombobox.setEditable(True)
        klasscombobox.addItems((CharacterPools.ENEMY if field else CharacterPools.ALLY).keys())
        klassframe = makeframe(QHBoxLayout, klasslabel, klasscombobox)

        infobox = QGroupBox("정보")
        infolayout = QGridLayout()

        self.iconlabel = iconlabel = QLabel("<font color='red'>???</font>")
        iconlabel.setMinimumHeight(CH_ICON_SIZE)
        iconlabel.setAlignment(Qt.AlignCenter)

        raritylabel = QLabel("등급")
        set_avaliable_minimum_width(raritylabel)
        self.raritybox = raritycombobox = QComboBox()
        raritycombobox.setEditable(True)
        raritycombobox.lineEdit().setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        raritycombobox.lineEdit().setReadOnly(True)
        rarityframe = makeframe(QHBoxLayout, raritycombobox, raritylabel)

        levellabel = QLabel("레벨")
        set_avaliable_minimum_width(levellabel)
        self.levelbox = levelspinbox = QSpinBox()
        levelspinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        levelspinbox.setMinimum(1)
        levelspinbox.setMaximum(999)
        levelspinbox.setSingleStep(1)
        levelspinbox.setValue(levelspinbox.minimum())
        levelspinbox.setAccelerated(True)
        levelframe = makeframe(QHBoxLayout, levelspinbox, levellabel)

        rlframe = makeframe(QHBoxLayout, rarityframe, levelframe)
        rlframe.layout().setSpacing(30)

        linklabel1 = QLabel("코어 링크")
        set_avaliable_minimum_width(linklabel1)
        self.linkbox = linkspinbox = QSpinBox()
        linkspinbox.setMinimum(0)
        linkspinbox.setMaximum(500)
        linkspinbox.setSingleStep(5)
        linkspinbox.setValue(linkspinbox.minimum())
        linkspinbox.setAccelerated(True)
        linklabel2 = QLabel("%")
        set_avaliable_minimum_width(linklabel2)
        linkframe = makeframe(QVBoxLayout, makeframe(QHBoxLayout, linkspinbox, linklabel2))
        linkframe.layout().insertWidget(0, linklabel1, alignment=Qt.AlignCenter)

        flblabel = QLabel("풀링크 보너스")
        set_avaliable_minimum_width(flblabel)
        self.flbbox = flbcombobox = QComboBox()
        flbframe = makeframe(QVBoxLayout, flbcombobox)
        flbframe.layout().insertWidget(0, flblabel, alignment=Qt.AlignCenter)

        afflabel = QLabel("호감도")
        set_avaliable_minimum_width(afflabel)
        self.affectionbox = affspinbox = QSpinBox()
        affspinbox.setMinimum(0)
        affspinbox.setMaximum(200)
        affspinbox.setSingleStep(1)
        affspinbox.setValue(affspinbox.minimum())
        affspinbox.setAccelerated(True)
        affectionframe = makeframe(QVBoxLayout, affspinbox)
        affectionframe.layout().insertWidget(0, afflabel, alignment=Qt.AlignCenter)

        remainhplabel = QLabel("현재 HP 설정")
        set_avaliable_minimum_width(remainhplabel)
        self.remainhpbox = remainhpspinbox = QSpinBox()
        remainhpspinbox.setMinimum(0)
        remainhpspinbox.setSingleStep(1)
        remainhpspinbox.setValue(remainhpspinbox.minimum())
        remainhpspinbox.setAccelerated(True)
        remainhpframe = makeframe(QVBoxLayout, remainhpspinbox)
        remainhpframe.layout().insertWidget(0, remainhplabel, alignment=Qt.AlignCenter)

        self.pledgebox = pledge = QCheckBox("서약")

        infolayout.addWidget(rlframe, 0, 0, 1, 2)
        infolayout.addWidget(linkframe, 1, 0)
        infolayout.addWidget(flbframe, 1, 1)
        infolayout.addWidget(affectionframe, 2, 0)
        infolayout.addWidget(remainhpframe, 2, 1)
        infolayout.addWidget(pledge, 3, 1, alignment=Qt.AlignRight | Qt.AlignVCenter)
        infolayout.setHorizontalSpacing(20)
        infolayout.setVerticalSpacing(15)
        infolayout.setContentsMargins(15, 15, 15, 15)
        infobox.setLayout(infolayout)

        statbox = QGroupBox("스탯")
        statlayout = QVBoxLayout()
        self.statspinboxes = {i: None for i in BT.BASE_STATS}

        def setmax(box):
            def func():
                box.setValue(box.maximum())
            return func

        for st in BT.BASE_STATS:
            stlabel = QLabel(st)
            stlabel.setAlignment(Qt.AlignCenter)
            stlabel.setFixedWidth(40)
            stspinbox = QSpinBox()
            stspinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            stspinbox.setMinimum(0)
            stspinbox.setSingleStep(1)
            stspinbox.setValue(affspinbox.minimum())
            stspinbox.setAccelerated(True)
            stspinbox.setMinimumWidth(45)
            stmaxbtn = QPushButton("MAX")
            stmaxbtn.setFixedWidth(stmaxbtn.fontMetrics().width("MAX")+10)
            stmaxbtn.clicked.connect(setmax(stspinbox))
            self.statspinboxes[st] = stspinbox
            stspinbox.valueChanged.connect(self.stat_value_changed)
            statlayout.addWidget(makeframe(QHBoxLayout, stlabel, stspinbox, stmaxbtn))
        self.statlabel = QLabel("스탯 합은 레벨의 3배 이하")
        statlayout.addSpacing(15)
        statlayout.addWidget(self.statlabel)
        statlayout.setContentsMargins(15, 15, 15, 15)
        statbox.setLayout(statlayout)

        self.levelbox.valueChanged.connect(self.lvl_changed)
        self.lvl_changed()

        skillbox = QGroupBox("스킬")
        skilllayout = QVBoxLayout()
        self.skillspinboxes = {
            "액티브1스킬": None,
            "액티브2스킬": None,
            "패시브1스킬": None,
            "패시브2스킬": None,
            "패시브3스킬": None,
        }
        for sk in self.skillspinboxes.keys():
            sklabel = QLabel(sk)
            set_avaliable_minimum_width(sklabel)
            skspinbox = QSpinBox()
            skspinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            skspinbox.setMinimum(1)
            skspinbox.setMaximum(10)
            skspinbox.setSingleStep(1)
            skspinbox.setValue(skspinbox.minimum())
            skspinbox.setAccelerated(True)
            self.skillspinboxes[sk] = skspinbox
            sklvllabel = QLabel("레벨")
            set_avaliable_minimum_width(sklvllabel)
            skilllayout.addWidget(makeframe(QHBoxLayout, sklabel, skspinbox, sklvllabel))
        skilllayout.setContentsMargins(15, 15, 15, 15)
        skillbox.setLayout(skilllayout)

        equipbox = QGroupBox("장비")
        equiplayout = QVBoxLayout()
        self.equips = [None, None, None, None]
        for i in range(4):
            eqlabel = QLabel(f"장비{i+1}")
            eqklassbox = QComboBox()
            eqklassbox.setEditable(True)
            eqklassbox.setMinimumWidth(127)
            eqraritybox = QComboBox()
            eqraritybox.setMinimumWidth(45)
            eqraritybox.setEditable(True)
            eqraritybox.lineEdit().setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            eqraritybox.lineEdit().setReadOnly(True)
            eqraritylabel = QLabel("등급")
            eqlvlbox = QSpinBox()
            eqlvlbox.setMinimumWidth(35)
            eqlvlbox.setMinimum(0)
            eqlvlbox.setMaximum(10)
            eqlvlbox.setSingleStep(1)
            eqlvlbox.setValue(eqlvlbox.minimum())
            eqlvlbox.setAccelerated(True)
            eqlvlbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            eqlvllabel = QLabel("레벨")
            set_avaliable_minimum_width(eqraritylabel)
            set_avaliable_minimum_width(eqlvllabel)
            self.equips[i] = (eqlabel, eqklassbox, eqraritybox, eqlvlbox)
            eqrarityframe = makeframe(QHBoxLayout, eqraritybox, eqraritylabel)
            eqlvlframe = makeframe(QHBoxLayout, eqlvlbox, eqlvllabel)
            eqrlframe = makeframe(QHBoxLayout, eqrarityframe, eqlvlframe)
            eqtotalframe = makeframe(QVBoxLayout, eqklassbox, eqrlframe)
            eqtotalframe.layout().insertWidget(0, eqlabel, alignment=Qt.AlignCenter)
            equiplayout.addWidget(eqtotalframe)
            eqklassbox.currentTextChanged.connect(self.equip_changed(i))
        for idx in range(3):
            lineframe = QFrame()
            lineframe.setFrameShape(QFrame.HLine | QFrame.Plain)
            lineframe.setStyleSheet("color: gray;")
            equiplayout.insertWidget(2*idx+1, lineframe)
        equiplayout.setSpacing(10)
        equiplayout.setContentsMargins(15, 15, 15, 15)
        equipbox.setLayout(equiplayout)

        funcbox = QGroupBox("편의 기능")
        funclayout = QHBoxLayout()
        affection200b = QPushButton("\n호감도\n200\n")
        skillmaxb = QPushButton("\n스킬\n10레벨\n")
        equiplvlmaxb = QPushButton("\n장비\n10레벨\n")
        loadfromfileb = QPushButton("\n파일에서\n불러오기\n")
        savetofileb = QPushButton("\n파일로\n저장하기\n")

        map(lambda btn: btn.resize(btn.sizeHint()),
            [affection200b, skillmaxb, equiplvlmaxb, loadfromfileb, savetofileb])

        def affection200():
            self.affectionbox.setValue(200)

        def skillmax():
            for box in self.skillspinboxes.values():
                box.setValue(10)

        def equiplvlmax():
            for eq in self.equips:
                eq[3].setValue(10)

        affection200b.clicked.connect(affection200)
        skillmaxb.clicked.connect(skillmax)
        equiplvlmaxb.clicked.connect(equiplvlmax)
        loadfromfileb.clicked.connect(self.load_from_file)
        savetofileb.clicked.connect(self.save_to_file)

        funclayout.addWidget(makeframe(QHBoxLayout, affection200b, skillmaxb, equiplvlmaxb, loadfromfileb, savetofileb))
        funcbox.setLayout(funclayout)

        klasscombobox.currentTextChanged.connect(self.klass_changed)
        self.klass_changed()

        okbutton = QPushButton("추가")
        okbutton.clicked.connect(self.accept)
        okbutton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        cancelbutton = QPushButton("취소")
        cancelbutton.clicked.connect(self.reject)
        cancelbutton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        glayout.addWidget(iconlabel, 0, 0)
        glayout.addWidget(klassframe, 1, 0)
        glayout.addWidget(infobox, 2, 0, 2, 1)
        glayout.addWidget(statbox, 0, 1, 3, 1)
        glayout.addWidget(skillbox, 3, 1)
        glayout.addWidget(equipbox, 0, 2, 4, 2)
        glayout.addWidget(funcbox, 4, 0, 1, 2)
        glayout.addWidget(okbutton, 4, 2)
        glayout.addWidget(cancelbutton, 4, 3)
        glayout.setSpacing(15)
        self.setLayout(glayout)

    def load_from_file(self):
        fname = QFileDialog.getOpenFileName(
            self,
            '캐릭터 불러오기',
            './',
            "Json files (*.json)",
            "Json files (*.json)"
        )
        if not fname[0]:
            return
        with open(fname[0], 'r', encoding='utf-8') as f_:
            temp_ = json.load(f_)
            klass = CharacterPools.ALL_CODES[temp_["code"]]
            self.klassbox.setCurrentIndex(
                [self.klassbox.itemText(i) for i in range(self.klassbox.count())].index(klass.name))
            args = temp_.get("args")
            if args is None:
                return
            self.raritybox.setCurrentIndex(args["rarity"]-klass.get_info()["base_rarity"] if "rarity" in args else 0)
            self.levelbox.setValue(args.get("lvl", self.levelbox.minimum()))
            for idx, box in enumerate(self.statspinboxes.values()):
                box.setValue(args["stat_lvl"][idx] if "stat_lvl" in args else box.minimum())
            for idx, box in enumerate(self.skillspinboxes.values()):
                box.setValue(args["skill_lvl"][idx] if "skill_lvl" in args else box.minimum())
            if "equips" in args:
                for idx, eq in enumerate(args["equips"]):
                    eqlabel, eqklassbox, eqraritybox, eqlvlbox = self.equips[idx]
                    if eq[0] not in EquipPools.ALL_NAME:
                        eqklassbox.setCurrentIndex(0)
                        continue
                    eqklassbox.setCurrentIndex([eqklassbox.itemText(i) for i in range(eqklassbox.count())].index(eq[0]))
                    eqraritybox.setCurrentIndex(eq[1]-EquipPools.ALL_NAME[eq[0]].BASE_RARITY)
                    eqlvlbox.setValue(eq[2])
            else:
                for eq in self.equips:
                    eq[1].setCurrentIndex(0)
            self.linkbox.setValue(args.get("link", 0))
            if "full_link_bonus_no" not in args or (flbno := args["full_link_bonus_no"]) is None:
                self.flbbox.setCurrentIndex(0)
            else:
                self.flbbox.setCurrentIndex(flbno + 1)
            self.affectionbox.setValue(args.get("affection", 0))
            self.pledgebox.setChecked(args.get("pledge", False))
            self.remainhpbox.setValue(args.get("current_hp", 0))

    def save_to_file(self):
        fname = QFileDialog.getSaveFileName(
            self,
            "캐릭터 저장",
            "./",
            "Json files (*.json)",
            "Json files (*.json)"
        )
        if not fname[0]:
            QMessageBox.information(
                self,
                "오류",
                "캐릭터 저장에 실패했습니다.",
                QMessageBox.Ok
            )
            return
        res = self.generate_arguments()
        if res is None:
            pass
        data = {
            "code": res[0].code,
            "args": dict(zip(
                ("rarity", "lvl", "stat_lvl", "skill_lvl", "equips", "link",
                 "full_link_bonus_no", "affection", "pledge", "current_hp"),
                res[1])
            ),
        }
        with open(fname[0], 'w', encoding='utf-8') as f:
            json.dump(data, f)
        QMessageBox.information(
            self,
            "성공",
            f"캐릭터 저장에 성공했습니다.\n({fname[0]})",
            QMessageBox.Ok
        )

    def generate_arguments(self):
        klass = CharacterPools.ALL.get(self.klassbox.currentText())
        if klass is None:
            return None
        rarity = Rarity[self.raritybox.currentText()]
        level = self.levelbox.value()
        stat_lvl = [0, 0, 0, 0, 0, 0]
        for idx, bt in enumerate(BT.BASE_STATS):
            stat_lvl[idx] = self.statspinboxes[bt].value()
        skill_lvl = [0, 0, 0, 0, 0]
        for idx, box in enumerate(self.skillspinboxes.values()):
            skill_lvl[idx] = box.value()
        equips = []
        for eq in self.equips:
            if eq[1].currentText() == "없음":
                equips.append(None)
            else:
                equips.append((eq[1].currentText(), Rarity[eq[2].currentText()], eq[3].value()))
        link = self.linkbox.value()
        flb = self.flbbox.currentIndex()
        if flb == 0:
            flb = None
        else:
            flb -= 1
        affection = self.affectionbox.value()
        pledge = self.pledgebox.isChecked()
        currenthp = self.remainhpbox.value()
        return klass, (rarity, level, stat_lvl, skill_lvl, equips, link, flb, affection, pledge, currenthp)

    def lvl_changed(self):
        lvl = self.levelbox.value()
        for box in self.statspinboxes.values():
            box.setMaximum(lvl * 3)
        self.stat_value_changed()

    def stat_value_changed(self):
        statpoint = 0
        lvl = self.levelbox.value()
        for box in self.statspinboxes.values():
            statpoint += box.value()
        if statpoint > lvl * 3:
            self.statlabel.setStyleSheet("color: red;")
        else:
            self.statlabel.setStyleSheet("color: black;")

    def klass_changed(self):
        klass = CharacterPools.ALL.get(self.klassbox.currentText())
        if klass is None:
            return
        self.raritybox.clear()
        self.flbbox.clear()
        self.iconlabel.clear()
        klassinfo = klass.get_info()
        self.raritybox.addItems(self.rarity_list[klassinfo["base_rarity"]:klassinfo["promotion"]+1])
        self.flbbox.addItem("없음")
        if klass.code not in UNITDATA:
            for flb in klassinfo["full_link_bonuses"]:
                if flb is None:
                    continue
                self.flbbox.addItem(flb.simpl_str())
        else:
            for flb in klassinfo["full_link_bonuses"]:
                if flb is None:
                    continue
                self.flbbox.addItem(Buff(flb[0], flb[1], d(flb[2])).simpl_str())
        self.raritybox.setCurrentIndex(0)
        self.flbbox.setCurrentIndex(0)
        character_icon = klass.get_icon_filename()
        if character_icon is None or character_icon + '.png' not in os.listdir(os.path.join(PATH, 'data', 'icons')):
            self.iconlabel.setText(f"<font color='red'>{character_icon}</font>")
        else:
            self.iconlabel.setPixmap(QPixmap(os.path.join(PATH, 'data', 'icons', character_icon + '.png'))
                                     .scaledToHeight(CH_ICON_SIZE))
        equipcond = klassinfo["equip_condition"]
        for i in range(4):
            eqlabel, eqklassbox = self.equips[i][:2]
            eqlabel.setText(f"장비{i+1} ({ET.desc[equipcond[i]]})")
            eqklassbox.clear()
            eqklassbox.addItem("없음")
            eqklassbox.addItems(list(EquipPools.ALL_NAME_LIST[equipcond[i]].keys()))

    def equip_changed(self, i):
        def func():
            eqlabel, eqklassbox, eqraritybox, eqlvlbox = self.equips[i]
            eqraritybox.clear()
            eqklass = EquipPools.ALL_NAME.get(eqklassbox.currentText())
            if eqklass:
                eqraritybox.addItems(self.rarity_list[eqklass.BASE_RARITY:eqklass.PROMOTION+1])
            else:
                eqraritybox.addItem("")
            eqraritybox.setCurrentIndex(0)
        return func

    def show_window(self):
        return super().exec_()


class Trigger(QDialog):
    def __init__(self, parents, *args, **kwargs):
        super().__init__(parents, *args, **kwargs)
        self.setWindowTitle("트리거 발동")

        self.trigbox = QComboBox()
        self.trigbox.addItems(list(TRIGGERS_REV.keys()))
        self.trigbox.setFixedWidth(200)

        self.selected_characters = set()
        self.ally_pools = set()
        self.enemy_pools = set()
        self.buttons = [
            [[None, None, None],
             [None, None, None],
             [None, None, None]],
            [[None, None, None],
             [None, None, None],
             [None, None, None]]
        ]

        field = QFrame()
        flayout = QHBoxLayout()
        aff = QFrame(field)
        aff.setFrameShadow(QFrame.Sunken)
        blank = QFrame(field)
        blank.setFixedWidth(30)
        eff = QFrame(field)
        eff.setFrameShadow(QFrame.Sunken)
        flayout.addWidget(aff)
        flayout.addWidget(blank)
        flayout.addWidget(eff)
        field.setLayout(flayout)
        affg = QGridLayout(aff)
        effg = QGridLayout(eff)
        aff.setLayout(affg)
        eff.setLayout(effg)
        for i in range(3):
            for j in range(3):
                ac = self.parentWidget().game.get_char(i, j)
                ec = self.parentWidget().game.get_char(i, j, 1)
                if ac is None:
                    abtn = QPushButton(f"None")
                else:
                    abtn = QPushButton(f"{ac.name}{ac.getposxy()}")
                    abtn.setCheckable(True)
                    abtn.setAutoExclusive(False)
                    self.ally_pools.add(ac)
                    abtn.character = ac
                    abtn.clicked.connect(self.add_character(abtn))
                if ec is None:
                    ebtn = QPushButton(f"None")
                else:
                    ebtn = QPushButton(f"{ec.name}{ec.getposxy()}")
                    ebtn.setCheckable(True)
                    ebtn.setAutoExclusive(False)
                    self.enemy_pools.add(ec)
                    ebtn.character = ec
                    ebtn.clicked.connect(self.add_character(ebtn))
                affg.addWidget(abtn, i, j)
                effg.addWidget(ebtn, i, j)
                self.buttons[0][i][j] = abtn
                self.buttons[1][i][j] = ebtn

        toggles = QFrame(self)
        toggles.setFixedHeight(50)
        tlayout = QHBoxLayout()
        select_ally_button = QPushButton("모든 아군")
        select_enemy_button = QPushButton("모든 적군")
        select_all_button = QPushButton("모든 캐릭터")
        unselect_all_button = QPushButton("모두 해제")
        select_ally_button.clicked.connect(self.select_ally_button_clicked)
        select_enemy_button.clicked.connect(self.select_enemy_button_clicked)
        select_all_button.clicked.connect(self.select_all_button_clicked)
        unselect_all_button.clicked.connect(self.unselect_all_button_clicked)
        tlayout.addWidget(select_ally_button)
        tlayout.addWidget(select_enemy_button)
        tlayout.addWidget(select_all_button)
        tlayout.addWidget(unselect_all_button)
        toggles.setLayout(tlayout)

        okbutton = QPushButton("확인")
        okbutton.clicked.connect(self.okclicked)
        cancelbutton = QPushButton("취소")
        cancelbutton.clicked.connect(self.cancelclicked)
        hlayout = QHBoxLayout()
        hlayout.addWidget(okbutton)
        hlayout.addWidget(cancelbutton)
        buttons = QWidget(self)
        buttons.setFixedHeight(50)
        buttons.setLayout(hlayout)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(field)
        layout.addWidget(self.trigbox, alignment=Qt.AlignCenter)
        layout.addWidget(toggles)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def add_character(self, btn):
        def func(b):
            if b:
                self.selected_characters.add(btn.character)
            else:
                self.selected_characters.remove(btn.character)
        return func

    def select_ally_button_clicked(self):
        for i in range(3):
            for j in range(3):
                self.buttons[0][i][j].setChecked(True)
        self.selected_characters.update(self.ally_pools)

    def select_enemy_button_clicked(self):
        for i in range(3):
            for j in range(3):
                self.buttons[1][i][j].setChecked(True)
        self.selected_characters.update(self.enemy_pools)

    def select_all_button_clicked(self):
        for i in range(3):
            for j in range(3):
                self.buttons[0][i][j].setChecked(True)
                self.buttons[1][i][j].setChecked(True)
        self.selected_characters.update(self.ally_pools)
        self.selected_characters.update(self.enemy_pools)

    def unselect_all_button_clicked(self):
        for i in range(3):
            for j in range(3):
                self.buttons[0][i][j].setChecked(False)
                self.buttons[1][i][j].setChecked(False)
        self.selected_characters = set()

    def okclicked(self):
        self.accept()

    def cancelclicked(self):
        self.reject()

    def show_window(self):
        return super().exec_()


class UseSkill(QDialog):
    def __init__(self, subjc, parents, *args, **kwargs):
        super().__init__(parents, *args, **kwargs)
        self.subjc = subjc
        self.setWindowTitle(f"{self.subjc} 스킬 사용")

        self.buttons = [
            [[None, None, None],
             [None, None, None],
             [None, None, None]],
            [[None, None, None],
             [None, None, None],
             [None, None, None]]
        ]

        field = QFrame()
        flayout = QHBoxLayout()
        aff = QFrame(field)
        aff.setFrameShadow(QFrame.Sunken)
        blank = QFrame(field)
        blank.setFixedWidth(30)
        eff = QFrame(field)
        eff.setFrameShadow(QFrame.Sunken)
        flayout.addWidget(aff)
        flayout.addWidget(blank)
        flayout.addWidget(eff)
        field.setLayout(flayout)
        affg = QGridLayout(aff)
        effg = QGridLayout(eff)
        aff.setLayout(affg)
        eff.setLayout(effg)
        for i in range(3):
            for j in range(3):
                ac = self.parentWidget().game.get_char(i, j)
                ec = self.parentWidget().game.get_char(i, j, 1)
                if ac is None:
                    abtn = QPushButton(f"None")
                else:
                    abtn = QPushButton(f"{ac.name}{ac.getposxy()}")
                abtn.setCheckable(True)
                if ec is None:
                    ebtn = QPushButton(f"None")
                else:
                    ebtn = QPushButton(f"{ec.name}{ec.getposxy()}")
                ebtn.setCheckable(True)
                abtn.fpos = (0, i * 3 + j)
                ebtn.fpos = (1, i * 3 + j)
                abtn.clicked.connect(self.pos_selected(abtn))
                ebtn.clicked.connect(self.pos_selected(ebtn))
                affg.addWidget(abtn, i, j)
                effg.addWidget(ebtn, i, j)
                self.buttons[0][i][j] = abtn
                self.buttons[1][i][j] = ebtn

        self.objpos = -1
        self.objfield = -1
        self.skill_no = -1

        skillbuttons = QFrame()
        slayout = QHBoxLayout()
        ql = QLabel("스킬 : ")
        ql.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        slayout.addWidget(ql)
        sbuttons = [QPushButton(sst) for sst in ("스킬1", "스킬2", "이동", "대기")]
        for i, sbtn in enumerate(sbuttons):
            sbtn.setFixedSize(70, 50)
            sbtn.setCheckable(True)
            sbtn.clicked.connect(self.skill_selected(i))
            slayout.addWidget(sbtn)
        slayout.setAlignment(Qt.AlignCenter)
        skillbuttons.setLayout(slayout)

        okbutton = QPushButton("확인")
        okbutton.clicked.connect(self.okclicked)
        cancelbutton = QPushButton("취소")
        cancelbutton.clicked.connect(self.cancelclicked)
        hlayout = QHBoxLayout()
        hlayout.addWidget(okbutton)
        hlayout.addWidget(cancelbutton)
        buttons = QWidget(self)
        buttons.setFixedHeight(50)
        buttons.setLayout(hlayout)

        layout = QVBoxLayout()
        layout.addWidget(field)
        layout.addWidget(skillbuttons)
        layout.addWidget(buttons)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def pos_selected(self, btn):
        def func():
            self.objfield, self.objpos = btn.fpos
        return func

    def skill_selected(self, no):
        def func():
            self.skill_no = no + 1
        return func

    def okclicked(self):
        if self.objpos == -1 or self.objfield == -1:
            QMessageBox.information(
                self,
                self.parentWidget().windowTitle(),
                "스킬을 사용할 위치를 정해주세요.\n"
                "창을 나가고 싶으면 대신 '취소' 버튼을 클릭하세요."
            )
            return
        if self.skill_no == -1:
            QMessageBox.information(
                self,
                self.parentWidget().windowTitle(),
                "사용할 스킬을 정해주세요.\n"
                "창을 나가고 싶으면 대신 '취소' 버튼을 클릭하세요."
            )
            return
        self.accept()

    def cancelclicked(self):
        self.reject()

    def show_window(self):
        return super().exec_()


class CharacterInfo(QDialog):
    def __init__(self, character: 'Character', parents, *args, **kwargs):
        super().__init__(parents, *args, **kwargs)
        self.character = character
        self.setWindowTitle(f"{self.character}의 정보")
        self.setMinimumWidth(500)

        show_eqname_type = parents.SHOW_EQNAME_TYPE

        infogroupbox = QGroupBox('정보')
        statgroupbox = QGroupBox('능력치')
        equigroupbox = QGroupBox('장비')
        buffgroupbox = QGroupBox('버프')
        self.equipgroupbox = equigroupbox

        ilayout = QVBoxLayout()
        templabel = QLabel()
        templabel.setAlignment(Qt.AlignCenter)
        templabel.setMinimumHeight(81)
        character_icon = self.character.get_icon_filename()
        if character_icon is None or character_icon + '.png' not in os.listdir(os.path.join(PATH, 'data', 'icons')):
            templabel.setText(f"<font color='red'>{character_icon}</font>")
        else:
            templabel.setPixmap(QPixmap(os.path.join(PATH, 'data', 'icons', character_icon + '.png'))
                                .scaledToHeight(CH_ICON_SIZE))
        ilayout.addWidget(templabel, alignment=Qt.AlignCenter)
        templabel = QLabel(self.character.name)
        templabel.setAlignment(Qt.AlignCenter)
        ilayout.addWidget(templabel, alignment=Qt.AlignCenter)
        templabel = QLabel(self.character.get_type_str())
        templabel.setAlignment(Qt.AlignCenter)
        ilayout.addWidget(templabel, alignment=Qt.AlignCenter)
        templabel = QLabel(f"Lv. {self.character.lvl}")
        templabel.setAlignment(Qt.AlignCenter)
        ilayout.addWidget(templabel, alignment=Qt.AlignCenter)
        templabel = QLabel(f"{'적' if self.character.isenemy else '아'}군 {self.character.getposn()}번 위치")
        templabel.setAlignment(Qt.AlignCenter)
        ilayout.addWidget(templabel, alignment=Qt.AlignCenter)
        infogroupbox.setLayout(ilayout)

        slayout = QVBoxLayout()

        # 체 AP
        # 공 방
        # 적 회
        # 치 행
        # 화염저항, 냉기저항, 전기저항

        frames = [QFrame(), QFrame(), QFrame(), QFrame(), QFrame()]
        layouts = [QHBoxLayout(frames[i]) for i in range(5)]

        layouts[0].addWidget(QLabel(f"체력\n{self.character.hp}/{self.character.maxhp}"))
        layouts[0].addWidget(QLabel(f"AP\n{self.character.ap}/20"))

        stats = self.character.get_stats(*BT.BASE_STATS, BT.SPD, *BT.ELEMENT_RES)
        bstats = self.character.get_base_stats()

        atk = stats[BT.ATK].to_integral(rounding=decimal.ROUND_FLOOR)
        batk = bstats[BT.ATK].to_integral(rounding=decimal.ROUND_FLOOR)
        def_ = stats[BT.DEF].to_integral(rounding=decimal.ROUND_FLOOR)
        bdef = bstats[BT.DEF].to_integral(rounding=decimal.ROUND_FLOOR)

        layouts[1].addWidget(QLabel(f"공격력\n{atk}" +
                                    (f" ({da:+})" if (da := atk - batk) != 0 else "")))
        layouts[1].addWidget(QLabel(f"방어력\n{def_}" +
                                    (f" ({dd:+})" if (dd := def_ - bdef) != 0 else "")))

        layouts[2].addWidget(QLabel(f"적중률\n{stats[BT.ACC]}%" +
                                    (f" ({dac:+}%)" if (dac := stats[BT.ACC] - bstats[BT.ACC]) != 0 else "")))
        layouts[2].addWidget(QLabel(f"회피율\n{stats[BT.EVA]}%" +
                                    (f" ({de:+}%)" if (de := stats[BT.EVA] - bstats[BT.EVA]) != 0 else "")))

        layouts[3].addWidget(QLabel(f"치명률\n{stats[BT.CRIT]}%" +
                                    (f" ({dcr:+}%)" if (dcr := stats[BT.CRIT] - bstats[BT.CRIT]) != 0 else "")))
        layouts[3].addWidget(QLabel(f"행동력\n{stats[BT.SPD]}" +
                                    (f" ({ds:+})" if
                                     (ds := stats[BT.SPD] - self.character.get_orig_spd()) != 0 else "")))

        layouts[4].addWidget(QLabel(f"화염저항\n{stats[BT.ELEMENT_RES[1]]}%"))
        layouts[4].addWidget(QLabel(f"냉기저항\n{stats[BT.ELEMENT_RES[2]]}%"))
        layouts[4].addWidget(QLabel(f"전기저항\n{stats[BT.ELEMENT_RES[3]]}%"))

        for i in range(5):
            frames[i].setLayout(layouts[i])
            slayout.addWidget(frames[i])
        slayout.setSpacing(0)

        statgroupbox.setLayout(slayout)

        elayout = QHBoxLayout(equigroupbox)
        self.equip_frames = []
        for e in self.character.equips:
            ef = QFrame()
            ef.setMinimumHeight(100)
            ef.setFrameShape(QFrame.Panel | QFrame.Sunken)
            ef.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
            self.equip_frames.append(ef)
            elayout.addWidget(ef, stretch=1)
            efl = QVBoxLayout(ef)
            efl.setAlignment(Qt.AlignCenter)
            if e is None:
                efl.addWidget(QLabel("없음"))
            else:
                eqiconlabel = QLabel()
                equip_icon = e.get_icon_filename()
                if equip_icon is None or equip_icon + '.png' not in os.listdir(
                        os.path.join(PATH, 'data', 'icons')):
                    eqiconlabel.setText(f"<font color='red'>{equip_icon}</font>")
                else:
                    eqiconlabel.setPixmap(QPixmap(os.path.join(PATH, 'data', 'icons', equip_icon + '.png'))
                                          .scaledToWidth(EQ_ICON_SIZE))
                efl.addWidget(eqiconlabel)
                if show_eqname_type:
                    if show_eqname_type == 1:
                        efl.addWidget(QLabel(e.nick))
                    else:
                        efl.addWidget(QLabel(e.name))
                else:
                    efl.addWidget(QLabel(e.nick))
                    efl.addWidget(QLabel(f"({e.name})"))
                efl.addWidget(QLabel(f"[{list(R)[e.rarity].name}] Lv.{e.lvl}"))
            ef.setLayout(efl)
            for label in [efl.itemAt(i).widget() for i in range(efl.count())]:
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setAlignment(Qt.AlignCenter)
        equigroupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        equigroupbox.setLayout(elayout)

        blayout = QVBoxLayout(buffgroupbox)
        bltextbox = QTextBrowser()
        bltextbox.setMinimumHeight(200)
        bltextbox.setAcceptRichText(True)
        bltextbox.setFont(QFont("consolas", pointSize=9))
        bltextbox.setLineWrapMode(QTextEdit.WidgetWidth)
        buffcolors = {BET.BUFF: "green", BET.DEBUFF: "red", BET.NORMAL: "black"}
        for bl in self.character.buff_iter[1:]:
            for b in bl:
                bltextbox.setTextColor(QColor(buffcolors[b.efftype]))
                bltextbox.insertPlainText(str(b)+'\n')
        blayout.addWidget(bltextbox)
        buffgroupbox.setLayout(blayout)

        mlayout = QVBoxLayout(self)
        subframe = QFrame()
        slayout = QHBoxLayout(subframe)
        slayout.addWidget(infogroupbox)
        slayout.addWidget(statgroupbox)
        slayout.setContentsMargins(0, 0, 0, 0)
        subframe.setLayout(slayout)
        mlayout.addWidget(subframe)
        mlayout.addWidget(equigroupbox)
        mlayout.addWidget(buffgroupbox)
        self.setLayout(mlayout)

    def resizeEquipFrames(self):
        boxlayout = self.equipgroupbox.layout()
        tempfunc = lambda tp: tp[0] + tp[2]
        framewidth = (self.equipgroupbox.width() - tempfunc(self.equipgroupbox.getContentsMargins())
                      - tempfunc(boxlayout.getContentsMargins()) - boxlayout.spacing() * 3) // 4
        for ef in self.equip_frames:
            efl = ef.layout()
            tfw = framewidth - tempfunc(ef.getContentsMargins()) - tempfunc(efl.getContentsMargins())
            for i in range(efl.count()):
                eflitem = efl.itemAt(i).widget()
                text_font = eflitem.font()
                text_font.setPointSize(9)
                while QFontMetrics(text_font).width(eflitem.text()) > tfw and text_font.pointSize() > 6:
                    text_font.setPointSize(text_font.pointSize() - 1)
                eflitem.setFont(text_font)

    def resizeEvent(self, a0) -> None:
        self.resizeEquipFrames()
        return super().resizeEvent(a0)

    def show_window(self):
        super().show()


class Settings(QDialog):
    def __init__(self, parents, *args, **kwargs):
        super().__init__(parents, *args, **kwargs)
        self.setWindowTitle("설정")
        self.setMinimumSize(350, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.app = self.parentWidget().app
        self.game = self.app.game

        self.realtime_frame = QFrame()
        rtlayout = QVBoxLayout(self.realtime_frame)
        rtlayout.setAlignment(Qt.AlignTop)

        self.realtime_checkbox = QCheckBox("수치 실시간으로 계산하기")
        self.realtime_checkbox_helptexts = [
            QLabel("\"수치 비례 버프\"를 적용할 때 적용 즉시 그 수치를 계산하여 반영합니다.<br>"
                   "(고정 수치 버프로 대체/표시됩니다)"),
            QLabel("\"수치 비례 버프\"를 적용할 때 필요할 때마다 그 수치를 계산하여 반영합니다.<br>"
                   "<span style=\"color:red\"><b>[주의]</b><br>"
                   "이 게산 방식은 실제 인게임 방식과 다를 수 있으며,<br>"
                   "일부 상황에서는 비례하는 비율이 일정 수치를 넘어서면<br>"
                   "수치를 계산할 수 없거나 수치의 부호가 반전될 수 있습니다.</span>")
        ]
        for label in self.realtime_checkbox_helptexts:
            label.setWordWrap(True)
            label.setTextFormat(Qt.RichText)

        if self.game.REAL_TIME:
            self.realtime_checkbox.setChecked(True)

        self.last_label = self.realtime_checkbox_helptexts[int(self.realtime_checkbox.isChecked())]

        rtlayout.addWidget(self.realtime_checkbox)
        rtlayout.addWidget(self.last_label)
        self.realtime_frame.setLayout(rtlayout)
        self.realtime_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.show_eqname_type_frame = QFrame()
        eqlayout = QHBoxLayout(self.show_eqname_type_frame)
        self.eqnametype_combobox = QComboBox(self.show_eqname_type_frame)
        sizepolicy = self.eqnametype_combobox.sizePolicy()
        sizepolicy.setHorizontalPolicy(QSizePolicy.Expanding)
        self.eqnametype_combobox.setSizePolicy(sizepolicy)
        eqlayout.addWidget(QLabel("장비 이름 표시 방식 : "))
        eqlayout.addWidget(self.eqnametype_combobox)
        self.show_eqname_type_frame.setLayout(eqlayout)

        self.eqnametype_combobox.addItem("별명과 이름 모두 표시")
        self.eqnametype_combobox.addItem("별명만 표시")
        self.eqnametype_combobox.addItem("이름만 표시")

        self.eqnametype_combobox.setCurrentIndex(self.app.SHOW_EQNAME_TYPE)

        self.realtime_checkbox.stateChanged.connect(self.realtime_checkbox_checked)
        self.eqnametype_combobox.currentIndexChanged.connect(self.eqnametype_combobox_valuechanged)

        tiplabel = QLabel("<b>[ 변경점은 즉시 적용됩니다 ]</b>")
        tiplabel.setTextFormat(Qt.RichText)
        sizepolicy = tiplabel.sizePolicy()
        sizepolicy.setHorizontalPolicy(QSizePolicy.Expanding)
        tiplabel.setSizePolicy(sizepolicy)
        tiplabel.setAlignment(Qt.AlignHCenter)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(tiplabel)
        layout.addSpacing(10)
        layout.addWidget(self.realtime_frame)
        layout.addWidget(self.show_eqname_type_frame)
        self.setLayout(layout)

    def realtime_checkbox_checked(self):
        if self.last_label:
            layout = self.realtime_frame.layout()
            layout.removeWidget(self.last_label)
            self.last_label.setParent(None)
            self.game.REAL_TIME = self.realtime_checkbox.isChecked()
            self.last_label = self.realtime_checkbox_helptexts[int(self.realtime_checkbox.isChecked())]
            layout.addWidget(self.last_label)
            self.realtime_frame.setLayout(layout)
            self.realtime_frame.updateGeometry()
            QApplication.processEvents()
            self.adjustSize()

    def eqnametype_combobox_valuechanged(self):
        self.app.SHOW_EQNAME_TYPE = self.eqnametype_combobox.currentIndex()

    def show_window(self):
        super().show()
