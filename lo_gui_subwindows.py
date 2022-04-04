from lo_simul import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QTextCursor

list_split = ','
list2d_split = '/'

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


class SelectCharacter(QDialog):
    args = {
        'field': ('아군', '적군'),
        'pos': ('0', '1', '2', '3', '4', '5', '6', '7', '8'),
        'id': tuple(),
        'rarity': ('B', 'A', 'S', 'SS'),
        'lvl': tuple(),
        'stat_lvl': tuple(),
        'skill_lvl': tuple(),
        'link': tuple(),
        'full_link_bonus_no': ('없음', '0', '1', '2', '3', '4'),
        'affection': tuple(),
        'pledge': ('서약 안 함', '서약함'),
        'current_hp': tuple()
    }

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle("캐릭터 생성")
        self.selectors = {a: QComboBox() for a in self.args}
        for a in self.args:
            self.selectors[a].addItems(list(map(str, self.args[a])))

        scroll_area = QScrollArea(self)

        self.selectors['equips'] = [None, None, None, None]
        self.selectors['field'].currentTextChanged.connect(self.update_character_list)
        self.update_character_list()
        self.selectors['id'].currentTextChanged.connect(self.update_equip_form_and_rarity)
        self.selectors['id'].setCurrentIndex(0)
        self.update_equip_form_and_rarity()

        lvspin = self.selectors['lvl'] = QSpinBox()
        lvspin.setMinimum(1)
        lvspin.setMaximum(1000)
        lvspin.setSingleStep(1)
        lvspin.setValue(lvspin.minimum())
        lvspin.setAccelerated(True)
        stspin = self.selectors['stat_lvl'] = [QSpinBox() for _ in range(6)]
        for s in stspin:
            s.setMinimum(0)
            s.setMaximum(360)
            s.setSingleStep(1)
            s.setValue(s.minimum())
            s.setAccelerated(True)
        skspin = self.selectors['skill_lvl'] = [QSpinBox() for _ in range(5)]
        for s in skspin:
            s.setMinimum(1)
            s.setMaximum(10)
            s.setSingleStep(1)
            s.setValue(s.minimum())
            s.setAccelerated(True)
        lkspin = self.selectors['link'] = QSpinBox()
        lkspin.setMinimum(0)
        lkspin.setMaximum(500)
        lkspin.setSingleStep(1)
        lkspin.setValue(lkspin.minimum())
        lkspin.setAccelerated(True)
        afspin = self.selectors['affection'] = QSpinBox()
        afspin.setMinimum(0)
        afspin.setMaximum(200)
        afspin.setSingleStep(1)
        afspin.setValue(afspin.minimum())
        afspin.setAccelerated(True)
        chspin = self.selectors['current_hp'] = QSpinBox()
        chspin.setMinimum(0)
        chspin.setSingleStep(1)
        chspin.setValue(chspin.minimum())
        chspin.setAccelerated(True)

        scroll_widget = QWidget(scroll_area)
        glayout = QGridLayout()
        self.scroll_glayout = glayout
        def ql(s_):
            q = QLabel(s_)
            q.setFixedWidth(150)
            q.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            return q

        posframe = QFrame()
        poslayout = QHBoxLayout(posframe)
        poslayout.setContentsMargins(0, 0, 0, 0)
        poslayout.addWidget(self.selectors['field'])
        poslayout.addWidget(self.selectors['pos'])
        posqlabel = QLabel("번 그리드")
        posqlabel.setFixedWidth(60)
        posqlabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        poslayout.addWidget(posqlabel)
        posframe.setLayout(poslayout)

        statdoc = ['체럭', '공격력', '방어력', '적중', '회피', '치명률']
        glayout.addWidget(ql("위치 = "), 0, 0)
        glayout.addWidget(posframe, 0, 1)
        glayout.addWidget(ql("ID = "), 1, 0)
        glayout.addWidget(self.selectors['id'], 1, 1)
        glayout.addWidget(ql("희귀도 = "), 2, 0)
        glayout.addWidget(self.selectors['rarity'], 2, 1)
        glayout.addWidget(ql("레벨 = "), 3, 0)
        glayout.addWidget(self.selectors['lvl'], 3, 1)
        for i in range(6):
            glayout.addWidget(ql(f"{statdoc[i]} 스탯 레벨 = "), 4+i, 0)
            glayout.addWidget(self.selectors['stat_lvl'][i], 4+i, 1)
        for i in range(5):
            glayout.addWidget(ql(f"스킬 {i}번 레벨 = "), 10+i, 0)
            glayout.addWidget(self.selectors['skill_lvl'][i], 10+i, 1)
        glayout.addWidget(ql("장비1 = "), 15, 0)
        glayout.addWidget(self.selectors['equips'][0], 15, 1)
        glayout.addWidget(ql("장비2 = "), 16, 0)
        glayout.addWidget(self.selectors['equips'][1], 16, 1)
        glayout.addWidget(ql("장비3 = "), 17, 0)
        glayout.addWidget(self.selectors['equips'][2], 17, 1)
        glayout.addWidget(ql("장비4 = "), 18, 0)
        glayout.addWidget(self.selectors['equips'][3], 18, 1)
        glayout.addWidget(ql("링크 = "), 19, 0)
        glayout.addWidget(self.selectors['link'], 19, 1)
        glayout.addWidget(ql("풀링크보너스 = "), 20, 0)
        glayout.addWidget(self.selectors['full_link_bonus_no'], 20, 1)
        glayout.addWidget(ql("호감도 = "), 21, 0)
        glayout.addWidget(self.selectors['affection'], 21, 1)
        glayout.addWidget(ql("서약 여부 = "), 22, 0)
        glayout.addWidget(self.selectors['pledge'], 22, 1)
        glayout.addWidget(ql("현재 HP (100%이면 0) = "), 23, 0)
        glayout.addWidget(self.selectors['current_hp'], 23, 1)
        scroll_widget.setLayout(glayout)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(450)

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
        layout.addWidget(scroll_area)
        layout.addWidget(buttons)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def gen_equip_frame(self, eqtype: int):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        available_equips = EquipPools.ALL_NAME_LIST[eqtype]
        names = frame.names = QComboBox(frame)
        names.setMinimumWidth(130)
        names.addItem("없음")
        names.addItems(list(available_equips.keys()))
        rarity = frame.rarity = QComboBox(frame)
        rarity.setFixedWidth(50)
        rarity.addItems(['B', 'A', 'S', 'SS', 'SSS'])
        lvl = frame.lvl = QComboBox(frame)
        lvl.setFixedWidth(50)
        lvl.addItems(list(map(str, range(11))))
        layout.addWidget(names)
        layout.addWidget(rarity)
        layout.addWidget(lvl)
        frame.setLayout(layout)
        names.currentTextChanged.connect(lambda: self.update_equip_rarity(names))
        return frame

    def update_character_list(self):
        isenemy = self.selectors['field'].currentText()
        if isenemy == '아군':
            characters = list(CharacterPools.ALLY.keys())
        else:
            characters = list(CharacterPools.ENEMY.keys())
        self.selectors['id'].clear()
        self.selectors['id'].addItems(characters)
        self.selectors['id'].setCurrentIndex(0)

    def update_equip_form_and_rarity(self):
        if (nowch := self.selectors['id'].currentText()) == '':
            return
        char_class = CharacterPools.ALL[nowch].get_info()
        base_rarity, equip_conditions = char_class[-2], char_class[-3]
        self.selectors['rarity'].clear()
        self.selectors['rarity'].addItem("없음")
        self.selectors['rarity'].addItems(R.desc[base_rarity:-1])
        for i in range(len(equip_conditions)):
            initiating = self.selectors['equips'][i] is None
            if not initiating:
                self.scroll_glayout.removeWidget(self.selectors['equips'][i])
                self.selectors['equips'][i].deleteLater()
            self.selectors['equips'][i] = self.gen_equip_frame(equip_conditions[i])
            if not initiating:
                self.scroll_glayout.addWidget(self.selectors['equips'][i], 15+i, 1)

    def update_equip_rarity(self, comb: QComboBox):
        combtxt = comb.currentText()
        if combtxt == "없음":
            return
        eq_class = EquipPools.ALL_NAME[combtxt]
        rarity = comb.parent().rarity
        rarity.clear()
        rarity.addItems(R.desc[eq_class.BASE_RARITY:-1])

    def okclicked(self):
        self.accept()

    def cancelclicked(self):
        self.reject()

    def show_window(self):
        return super().exec_()


class RemoveCharacter(QDialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle("캐릭터 제거")

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
                if ec is None:
                    ebtn = QPushButton(f"None")
                else:
                    ebtn = QPushButton(f"{ec.name}{ec.getposxy()}")
                abtn.character = ac
                ebtn.character = ec
                abtn.clicked.connect(self.make_func(abtn))
                ebtn.clicked.connect(self.make_func(ebtn))
                affg.addWidget(abtn, i, j)
                effg.addWidget(ebtn, i, j)

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

        self.selected_character = None
        self.selected_character_label = QLabel('선택된 캐릭터 = None')
        self.selected_character_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(field)
        layout.addWidget(self.selected_character_label)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def make_func(self, btn):
        def do():
            self.selected_character = btn.character
            if self.selected_character is None:
                self.selected_character_label.setText('선택된 캐릭터 = None')
            else:
                self.selected_character_label.setText(
                    f"선택된 캐릭터 = "
                    f"{self.selected_character.name}{self.selected_character.getposxy()}"
                )
        return do

    def okclicked(self):
        if self.selected_character is None:
            QMessageBox.information(
                self,
                self.parentWidget().windowTitle(),
                "캐릭터를 무조건 선택해야 합니다.\n"
                "창을 나가고 싶으면 대신 '취소' 버튼을 클릭하세요."
            )
        else:
            self.accept()

    def cancelclicked(self):
        self.reject()

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
        if self.objpos == -1:
            QMessageBox.information(
                self,
                self.parentWidget().windowTitle(),
                "스킬을 사용할 위치를 정해주세요.\n"
                "창을 나가고 싶으면 대신 '취소' 버튼을 클릭하세요."
            )
        if self.objfield == -1:
            QMessageBox.information(
                self,
                self.parentWidget().windowTitle(),
                "스킬을 사용할 위치를 정해주세요.\n"
                "창을 나가고 싶으면 대신 '취소' 버튼을 클릭하세요."
            )
        if self.skill_no == -1:
            QMessageBox.information(
                self,
                self.parentWidget().windowTitle(),
                "사용할 스킬을 정해주세요.\n"
                "창을 나가고 싶으면 대신 '취소' 버튼을 클릭하세요."
            )
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

        infogroupbox = QGroupBox('정보')
        statgroupbox = QGroupBox('능력치')
        equigroupbox = QGroupBox('장비')
        buffgroupbox = QGroupBox('버프')

        ilayout = QVBoxLayout()
        templabel = QLabel()
        templabel.setAlignment(Qt.AlignCenter)
        character_icon = self.character.get_icon_filename()
        if character_icon is None or character_icon + '.png' not in os.listdir(os.path.join(PATH, 'data', 'icons')):
            templabel.setText(str(character_icon))
        else:
            templabel.setPixmap(QPixmap(os.path.join(PATH, 'data', 'icons', character_icon + '.png')))
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

        stats = self.character.get_stats()
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
        layouts[3].addWidget(QLabel(f"행동력\n{self.character.get_spd()}" +
                                    (f" ({ds:+})" if
                                     (ds := self.character.get_spd() - self.character.get_orig_spd()) != 0 else "")))

        reses = self.character.get_res()

        layouts[4].addWidget(QLabel(f"화염저항\n{reses[0]}%"))
        layouts[4].addWidget(QLabel(f"냉기저항\n{reses[1]}%"))
        layouts[4].addWidget(QLabel(f"전기저항\n{reses[2]}%"))

        for i in range(5):
            frames[i].setLayout(layouts[i])
            slayout.addWidget(frames[i])
        slayout.setSpacing(0)

        statgroupbox.setLayout(slayout)

        elayout = QHBoxLayout(equigroupbox)
        equips = []
        for e in self.character.equips:
            ef = QFrame()
            ef.setMinimumHeight(100)
            ef.setFrameShape(QFrame.Panel | QFrame.Sunken)
            equips.append(ef)
            efl = QVBoxLayout(ef)
            efl.setAlignment(Qt.AlignCenter)
            if e is None:
                efl.addWidget(QLabel("없음"))
            else:
                efl.addWidget(QLabel(e.nick))
                efl.addWidget(QLabel(f"({e.name})"))
                efl.addWidget(QLabel(f"[{R.desc[e.rarity]}] Lv.{e.lvl}"))
                efl.children()
            for i in range(efl.count()):
                efl.itemAt(i).setAlignment(Qt.AlignCenter)
            ef.setLayout(efl)
        for ef in equips:
            elayout.addWidget(ef)
        equigroupbox.setLayout(elayout)

        blayout = QVBoxLayout(buffgroupbox)
        bltextbox = QTextBrowser()
        bltextbox.setMinimumHeight(200)
        bltextbox.setAcceptRichText(True)
        bltextbox.setFont(QFont("consolas", pointSize=7))
        bltextbox.setLineWrapMode(QTextEdit.WidgetWidth)
        allbufflist = sum(self.character.buff_iter[1:], BuffList())
        bltextbox.setText(str(allbufflist))
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

    def show_window(self):
        super().show()
