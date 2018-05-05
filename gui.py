# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets, QtGui
import kdniao

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.createMenus()
        self.window_size_info()
        self.window_set()

    def window_set(self):
        """the parts of the window"""
        # 创建实例并设为中心部件
        main_ground = QtWidgets.QWidget()
        self.setCentralWidget(main_ground)
        # 创建网格布局
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(20)

        hint = QtWidgets.QLabel("请输入快递单号")
        btn = QtWidgets.QPushButton("查询",self)
        self.code = QtWidgets.QLineEdit(self)
        self.result = QtWidgets.QLabel()

        self.code.textChanged[str].connect(self.record)
        btn.pressed.connect(self.look_up)
        # 使用 addWidget()方法将部件加入到网格布局中。addWidget()方法的参数依次为要加入到局部的部件，行号和列号。
        grid.addWidget(hint, 0, 0)
        grid.addWidget(self.code, 1, 0)
        grid.addWidget(btn, 1, 1)
        grid.addWidget(self.result, 2, 0, 10, 1)
        # 将网格布局置于实例上
        main_ground.setLayout(grid)

    def record(self, text):
        """Record the tracking number"""
        self.log_code=text

    def look_up(self):
        """call kdniao.recognise()"""
        self.result.setText(kdniao.recognise(self.log_code))
    
    def selectAboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self, "About Qt")

    def selectAbout(self):
        QtWidgets.QMessageBox.about(self, "About", "`````")

    def createMenus(self):
        """setting of menubar and toolbar"""
        # 退出操作
        exit_action = QtWidgets.QAction(QtGui.QIcon(r"exit.jpg"), "Exit", self)
        exit_action.setStatusTip("Quit PMS")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        # about_menu
        # about
        about_action = QtWidgets.QAction(QtGui.QIcon(), "About", self)
        about_action.setStatusTip("Show information about the program")
        about_action.triggered.connect(self.selectAbout)

        # aboutQt
        aboutQt_action = QtWidgets.QAction(QtGui.QIcon(), "About Qt", self)
        aboutQt_action.setStatusTip("Show information about Qt")
        aboutQt_action.triggered.connect(self.selectAboutQt)

        # menubar
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        file.addAction(exit_action)
        about = menubar.addMenu("About")
        about.addAction(about_action)
        about.addAction(aboutQt_action)

    def window_size_info(self):
        """basic window's settings"""
        self.resize(500, 600)
        self.center()
        self.setWindowTitle('Sample')
        self.setWindowIcon(QtGui.QIcon(r'ex.ico'))
        self.setToolTip("This is a sample")
        self.statusBar().showMessage("Ready")
        # QtWidgets.QToolTip.setFont(QtGui.QFont("Times", 10)

    def center(self):
        """a method for window_size_info to put the window in the center of the screen"""
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        """confirm when click the close_button """
        reply = QtWidgets.QMessageBox.question(
            self,
            'Exit',
            'Are you sure you want to exit?',
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    my_first_app = MainWindow()
    my_first_app.show()
    sys.exit(app.exec_())

