import sys, os
from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5.QtGui import QPixmap


def main():
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap(os.path.join(getattr(sys, '_MEIPASS', os.path.abspath('.')), 'splash.png')))
    splash.show()
    splash.showMessage("Loading Modules...")
    app.processEvents()
    import lo_gui
    splash.showMessage("Initiating Window...")
    app.processEvents()
    ex = lo_gui.MyWindow()
    ex.show()
    splash.finish(ex)
    sys.exit(app.exec_())


main()
