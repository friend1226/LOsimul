import sys
from lo_simul import *
import lo_gui_subwindows
import traceback
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEventLoop, QCoreApplication, QObject, pyqtSignal, QEvent
from PyQt5.QtGui import QTextCursor, QFont, QColor, QIcon


class Stream(QObject):
    sig = pyqtSignal(object, object)

    def __init__(self, *args):
        super().__init__(*args)
        self.stdout_write = sys.stdout.write
        self.stderr_write = sys.stderr.write
        sys.stdout.write = self.write
        sys.stderr.write = lambda x: self.write(x, "red")

    def write(self, s, color="black"):
        self.sig.emit(s, color)

    def __del__(self):
        sys.stdout = self.stdout_write
        sys.stderr = self.stderr_write


class MyApp(QWidget):
    kv_split = '='
    list_split = lo_gui_subwindows.list_split
    list2d_split = lo_gui_subwindows.list2d_split

    def closeEvent(self, event):
        self.deleteLater()

    def __init__(self, *args):
        super().__init__(*args)

        self.game = lo_system.Game()

        self.commands = {
            'add': self.add_,
            'remove': self.remove_,
            'exit': self.exit_,
            'trigger': self.trigger,
            'skill': self.skill,
            'help': self.help_,
            'test': self.test_
        }

        vbox = QVBoxLayout()

        field = QFrame()
        flayout = QHBoxLayout()
        flayout.setContentsMargins(0, 0, 0, 0)
        self.aff = QFrame(field)
        self.aff.setFrameShadow(QFrame.Panel | QFrame.Sunken)
        self.blank = QFrame(field)
        self.blank.setFixedWidth(30)
        self.eff = QFrame(field)
        self.eff.setFrameShadow(QFrame.Panel | QFrame.Sunken)
        flayout.addWidget(self.aff)
        flayout.addWidget(self.blank)
        flayout.addWidget(self.eff)
        field.setLayout(flayout)

        self.ally_field_layout = QGridLayout(self.aff)
        self.enemy_field_layout = QGridLayout(self.eff)
        
        def get_qlabel():
            r = QLabel()
            r.setMinimumSize(70, 50)
            r.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            r.setWordWrap(True)
            r.font().setPointSize(12)
            return r
        self.field_labels = lo_imports.np.array([
            [[get_qlabel(), get_qlabel(), get_qlabel()],
             [get_qlabel(), get_qlabel(), get_qlabel()],
             [get_qlabel(), get_qlabel(), get_qlabel()]],
            [[get_qlabel(), get_qlabel(), get_qlabel()],
             [get_qlabel(), get_qlabel(), get_qlabel()],
             [get_qlabel(), get_qlabel(), get_qlabel()]],
        ])
        self.update_field_labels()
        for i in range(3):
            for j in range(3):
                afl = self.field_labels[0, i, j]
                efl = self.field_labels[1, i, j]
                afl.fpos = (0, i * 3 + j)
                efl.fpos = (1, i * 3 + j)
                afl.installEventFilter(self)
                efl.installEventFilter(self)
                self.ally_field_layout.addWidget(afl, i, j)
                self.enemy_field_layout.addWidget(efl, i, j)

        self.log = QTextBrowser(self)
        self.log.setAcceptRichText(True)
        self.log.setFont(QFont("consolas", pointSize=8))
        self.log.setLineWrapMode(QTextEdit.WidgetWidth)
        self.outputs = QTextBrowser(self)
        self.outputs.setAcceptRichText(True)
        self.log.setFontPointSize(10)
        self.outputs.setLineWrapMode(QTextEdit.WidgetWidth)

        self.stream = Stream()
        self.stream.sig.connect(self.logging)

        self.commandbox = QLineEdit(self)
        self.commandbox.returnPressed.connect(self.get_command)

        self.buttons = QFrame()
        blayout = QHBoxLayout()
        blayout.setContentsMargins(0, 0, 0, 0)
        self.buttons.setFixedHeight(40)

        char_add_button = QPushButton(self.buttons)
        char_add_button.setIcon(QIcon(os.path.join(PATH, 'images', 'add_button.png')))
        char_add_button.clicked.connect(self.char_add_clicked)
        char_remove_button = QPushButton(self.buttons)
        char_remove_button.setIcon(QIcon(os.path.join(PATH, 'images', 'remove_button.png')))
        char_remove_button.clicked.connect(self.char_remove_clicked)
        trigger_button = QPushButton(self.buttons)
        trigger_button.setIcon(QIcon(os.path.join(PATH, 'images', 'trigger_button.png')))
        trigger_button.clicked.connect(self.trigger_clicked)
        speed_button = QPushButton(self.buttons)
        speed_button.setIcon(QIcon(os.path.join(PATH, 'images', 'speed_button.png')))
        speed_button.clicked.connect(self.show_act_order)

        blayout.addWidget(char_add_button)
        blayout.addWidget(char_remove_button)
        blayout.addWidget(trigger_button)
        blayout.addWidget(speed_button)
        self.buttons.setLayout(blayout)

        vbox.addWidget(field)
        vbox.addWidget(self.log)
        vbox.addWidget(self.buttons)
        vbox.addWidget(self.outputs)
        vbox.addWidget(self.commandbox)
        self.setLayout(vbox)

        # print('='*25)
        # self.setWindowTitle('LO simulator v.0b')
        # screen = QApplication.primaryScreen()
        # print(f"Screen : {screen.name()}")
        # size = screen.size()
        # print(f"Size : {size.width()} x {size.height()}")
        # rect = screen.availableGeometry()
        # print(f"Available : {rect.width()} x {rect.height()}")
        # print('='*25)

    def load_from_json(self, field):
        """
        json file form :
        [
            {
                "code": "Character.code",
                "args": {
                    ...
                }
            },
            ... (8 times more)
        ]
        :return:
        """
        fname = QFileDialog.getOpenFileName(
            self,
            '캐릭터 배치 불러오기',
            './',
            "Json files (*.json)",
            "Json files (*.json)"
        )
        if fname[0]:
            self.game.put_from_file(fname[0], field)
            self.update_field_labels()
            self.print(f"[Info] 파일 '{fname[0]}'로부터 불러오기 성공!")

    def eventFilter(self, source: 'QObject', ev: 'QEvent') -> bool:
        if ev.type() == QEvent.MouseButtonRelease and isinstance(source, QLabel):
            self.char_labels_clicked(source, ev.button() == Qt.LeftButton)
        return super().eventFilter(source, ev)

    def char_labels_clicked(self, label: QLabel, leftclick: bool):
        p = label.fpos
        target = self.game.get_char(p[1], field=p[0])
        if target is None:
            return
        if leftclick:
            if self.game.enemy_all_down:
                return
            win = lo_gui_subwindows.UseSkill(target, self)
            res = win.show_window()
            if not res:
                return
            subjfield, subjcpos = p
            skill_no = win.skill_no
            objpos = win.objpos
            objfield = win.objfield
            self.run_command('skill', list(map(str, (subjfield, subjcpos, skill_no, objpos))))
        else:
            win = lo_gui_subwindows.CharacterInfo(target, self)
            win.show_window()

    def show_act_order(self):
        win = lo_gui_subwindows.ShowActOrder(self, self.game)
        win.show_window()

    def update_field_labels(self):
        for x in range(2):
            for i in range(3):
                for j in range(3):
                    c = self.game.get_char(i, j, x)
                    self.field_labels[x, i, j].setText(
                        f"{c}\n" + ('--- / ---' if c is None else f'{c.hp}/{c.maxhp}')
                    )

    def print(self, s):
        self.outputs.moveCursor(QTextCursor.End)
        self.outputs.insertPlainText(str(s)+'\n')
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def logging(self, s, color):
        self.log.moveCursor(QTextCursor.End)
        self.log.setTextColor(QColor(color))
        self.log.insertPlainText(s)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def char_add_clicked(self):
        win = lo_gui_subwindows.SelectCharacter(self)
        res = win.show_window()
        if not res:
            return
        ws = win.selectors
        sub = {
            '아군': '0',
            '적군': '1',
            'B': '0',
            'A': '1',
            'S': '2',
            'SS': '3',
            '없음': 'None',
            '서약함': '1',
            '서약 안 함': '0'
        }
        cmd = [sub[ws['field'].currentText()],
               ws['pos'].currentText(),
               ws['id'].currentText()]
        for k in win.args:
            if k == 'field' or k == 'pos' or k == 'id':
                continue
            if isinstance(ws[k], list):
                templ = []
                for x in ws[k]:
                    if isinstance(x, QComboBox):
                        temps = x.currentText()
                        if not temps.isnumeric():
                            temps = sub[temps]
                    elif isinstance(x, QSpinBox):
                        temps = str(x.value())
                    else:
                        continue
                    templ.append(temps)
                temp = self.list_split.join(templ)
            elif isinstance(ws[k], QComboBox):
                temp = ws[k].currentText()
                if not temp.isnumeric() and temp not in lo_chars.CharacterPools.ALL:
                    temp = sub[temp]
            elif isinstance(ws[k], QSpinBox):
                temp = str(ws[k].value())
            else:
                continue
            cmd.append(k+'='+temp)
        eql = []
        for frm in ws['equips']:
            name = frm.names.currentText()
            if name == "없음":
                eql.append('None')
            else:
                eql.append(self.list_split.join([name, frm.rarity.currentText(), frm.lvl.currentText()]))
        cmd.append('equips='+self.list2d_split.join(eql))
        self.run_command('add', cmd)

    def char_remove_clicked(self):
        win = lo_gui_subwindows.RemoveCharacter(self)
        res = win.show_window()
        if not res:
            return
        target = win.selected_character
        self.run_command('remove', ['1' if target.isenemy else '0', str(target.getposn())])

    def trigger_clicked(self):
        win = lo_gui_subwindows.Trigger(self)
        res = win.show_window()
        if not res:
            return
        trig = lo_enum.TRIGGERS_REV[win.trigbox.currentText()]
        targets = win.selected_characters
        allys, enemys = [], []
        for t in targets:
            if t.isenemy:
                enemys.append(t.getposn())
            else:
                allys.append(t.getposn())
        self.run_command('trigger', [trig, sorted(allys), sorted(enemys)])

    def help_(self, *args):
        win = lo_gui_subwindows.HelpWindow(self)
        win.show_window()

    def test_(self, *args):
        print(self.game.get_act_order_str().strip())

    def add_(self, field, pos, id_, *args):
        if field != '-1' and field != '0' and field != '1':
            return f"[Error] field는 -1, 0, 1 중 하나여야 합니다. (현재{field=})"
        field = int(field)
        if id_.isnumeric():
            id_ = int(id_)
        char_class = lo_chars.CharacterPools.ALL.get(id_)
        if char_class is None:
            return f"[Error] ID가 {id_}인 캐릭터가 없습니다."
        pos = lo_imports.Pos(pos)
        pargs_t = []
        kwargs = dict()
        argname = {'rarity', 'lvl', 'stat_lvl', 'skill_lvl', 'equips', 'link',
                   'full_link_bonus_no', 'affection', 'pledge', 'current_hp'}
        kwstart = False
        for idx in range(len(args)):
            temp = args[idx]
            if len(kv := temp.split(self.kv_split)) > 1:
                if kv[0] not in argname:
                    return f"[Error] 매개변수 이름이 잘못되었습니다. : {kv[0]}"
                kwstart = True
                if kwargs.get(kv[0]):
                    return f"[Error] 매개변수 이름이 중복되었습니다. : {kv[0]}"
                kwargs[kv[0]] = kv[1]
            elif kwstart:
                return f"[Error] 키워드 인자(keyword argument) 뒤에 " \
                       f"인자(positional argument)가 있어서는 안 됩니다."
            else:
                pargs_t.append(temp)
        pargs = []

        def conv(eqp):
            if eqp == "None":
                return None
            eql = eqp.split(self.list_split)
            return eql[0].replace('_', ' '), getattr(lo_enum.R, eql[1]), int(eql[2])
        for a in pargs_t:
            if a == 'None':
                pargs.append(None)
            elif len(temp := a.split(self.list2d_split)) > 1:
                pargs.append(list(map(conv, temp)))
            elif len(temp := a.split(self.list_split)) > 1:
                pargs.append(list(map(int, temp)))
            else:
                pargs.append(int(a))
        for k in kwargs:
            if kwargs[k] == 'None':
                kwargs[k] = None
            elif len(temp := kwargs[k].split(self.list2d_split)) > 1:
                kwargs[k] = list(map(conv, temp))
            elif len(temp := kwargs[k].split(self.list_split)) > 1:
                kwargs[k] = list(map(int, temp))
            else:
                kwargs[k] = int(kwargs[k])
        newchar: lo_chars.Character = char_class(self.game, pos, *pargs, **kwargs)
        newchar.isenemy = [False, True, newchar.isenemy][field]
        self.game.put_char(newchar)
        return f"[Info] {newchar}가 생성되었습니다. (위치 {newchar.getpos()})"

    def remove_(self, field, pos, *args):
        if field != '-1' and field != '0' and field != '1':
            return f"[Error] field는 -1, 0, 1 중 하나여야 합니다. (현재 = {field})"
        field = int(field)
        if c := self.game.get_char(lo_imports.Pos(pos), field=field):
            self.game.remove_char(c)
            return f"[Info] {c}가 제거되었습니다."
        else:
            return f"[Error] 해당 위치에 캐릭터가 없습니다."

    def trigger(self, trig, *args):
        try:
            tt = getattr(lo_enum.Trigger, trig)
        except AttributeError:
            self.print(f"[Error] 잘못된 트리거 타입입니다. : {trig}")
        else:
            self.game.trigger(tt, *args)
            return f"[Info] <{tt}> 트리거 완료."

    def skill(self, field, pos, skill_no, objpos, *args):
        if field != '-1' and field != '0' and field != '1':
            return f"[Error] field는 -1, 0, 1 중 하나여야 합니다. (주어진 값 = {field})"
        field = int(field)
        if not (skill_no.isnumeric() and 0 < int(skill_no) < 5):
            return f"[Error] skill_no는 1~4의 정수 중 하나여야 합니다. (주어진 값 = {field})"
        skill_no = int(skill_no)
        subjc = self.game.get_char(lo_imports.Pos(pos), field=field)
        self.game.use_skill(
            subjc=subjc,
            skill_no=skill_no,
            objpos=lo_imports.Pos(objpos)
        )
        return f"[Info] 스킬 사용 완료. " \
               f"({subjc}(이)가 {objpos}번 위치에 {skill_no}번 스킬 사용)"

    def exit_(self, *args):
        QCoreApplication.instance().quit()

    def get_command(self):
        commands = self.commandbox.text().strip().split(' ')
        cmd, args = commands[0], commands[1:]
        self.run_command(cmd, args)

    def run_command(self, cmd, args):
        try:
            if cmd == "eval":
                self.print(eval(' '.join(args)))
            else:
                return_str = self.commands[cmd](*args)
                if cmd != "help" and cmd != "test":
                    self.print(return_str)
            self.update_field_labels()
            self.commandbox.setText("")
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)


class MyWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)

        wg = MyApp()
        self.setCentralWidget(wg)

        def load_ally():
            wg.load_from_json(0)

        def load_enemy():
            wg.load_from_json(1)

        load_ally_file_action = QAction(QIcon(os.path.join(PATH, 'images', 'load_button.png')), '아군 불러오기...', self)
        load_ally_file_action.setStatusTip('파일로부터 아군 캐릭터의 배치 정보를 불러옵니다. (현재 정보는 초기화됨)')

        load_ally_file_action.triggered.connect(load_ally)
        load_enemy_file_action = QAction(QIcon(os.path.join(PATH, 'images', 'load_button.png')), '적 불러오기...', self)
        load_enemy_file_action.setStatusTip('파일로부터 적의 배치 정보를 불러옵니다. (현재 정보는 초기화됨)')
        load_enemy_file_action.triggered.connect(load_enemy)

        def wave_start():
            wg.game.wave_start()
            wg.print("[Info] 전투 시작.")

        def wave_end():
            wg.game.wave_end()
            wg.print("[Info] 전투 종료.")

        def round_start():
            wg.game.round_start()
            wg.print("[Info] 라운드 시작.")

        def round_end():
            wg.game.round_end()
            wg.print("[Info] 라운드 시작.")

        def next_round():
            wg.game.go_next_round()
            wg.print("[Info] 다음 라운드 진행.")

        wave_start_action = QAction(QIcon(), '전투 시작', self)
        wave_start_action.setStatusTip('전투를 시작합니다. (전투 시작 트리거 실행 + 라운드 시작)')
        wave_start_action.triggered.connect(wave_start)
        wave_end_action = QAction(QIcon(), '전투 종료', self)
        wave_end_action.setStatusTip('전투를 종료합니다. (전투 종료 트리거 실행)')
        wave_end_action.triggered.connect(wave_end)
        round_start_action = QAction(QIcon(), '라운드 시작', self)
        round_start_action.setStatusTip('라운드를 시작합니다. (라운드 시작 트리거 실행, 라운드 수 증가)')
        round_start_action.triggered.connect(round_start)
        round_end_action = QAction(QIcon(), '라운드 종료', self)
        round_end_action.setStatusTip('라운드를 종료합니다. (라운드 종료 트리거 실행)')
        round_end_action.triggered.connect(round_end)
        next_round_action = QAction(QIcon(), '다음 라운드', self)
        next_round_action.setStatusTip('다음 라운드를 시작합니다. (라운드 종료 + 라운드 시작)')
        next_round_action.triggered.connect(next_round)

        exit_action = QAction(QIcon(os.path.join(PATH, 'images', 'exit.png')), '종료', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('프로그램을 종료합니다.')
        exit_action.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        filemenu = menubar.addMenu('&File')
        filemenu.addAction(load_ally_file_action)
        filemenu.addAction(load_enemy_file_action)
        filemenu.addSeparator()
        filemenu.addAction(exit_action)

        trigmenu = menubar.addMenu('&Trigger')
        trigmenu.addAction(wave_start_action)
        trigmenu.addAction(wave_end_action)
        trigmenu.addAction(round_start_action)
        trigmenu.addAction(round_end_action)
        trigmenu.addAction(next_round_action)

        helpmenu = menubar.addMenu('&Help')
        helpaction = QAction(QIcon(os.path.join(PATH, 'images', 'question.png')), '도움말', self)
        helpaction.setStatusTip("도움!")
        helpaction.triggered.connect(wg.help_)
        helpmenu.addAction(helpaction)

        self.setWindowTitle("LO simulator v.0b")
        self.setGeometry(50, 50, 600, 700)
        self.setMinimumWidth(600)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())