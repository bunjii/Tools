# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

# inherited class


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.show()

    def init_ui(self):
        self.setWindowTitle('My Title')
        self.setGeometry(100,100,600,480)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # self.statusBar()

        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')

        close_act = QAction('Close', self)
        close_act.setShortcut('Ctrl+Q')
        filemenu.addAction(close_act)
        # self.showFullScreen()
        self.setGeometry(300,300,1200,960)
        self.setWindowTitle('Structural Tools Ver.0.5')


        button1 = QPushButton('SOLVE')
        button2 = QPushButton('OPEN FILE')
        button3 = QPushButton('SAVE FILE')
        button4 = QPushButton('EXIT PROG')

        # slot
        button4.clicked.connect(app.quit)

        layout1 = QHBoxLayout()
        layout1.addWidget(button1)
        layout2 = QVBoxLayout()
        layout2.addWidget(button2)
        layout2.addWidget(button3)
        layout1.addLayout(layout2)
        layout1.addWidget(button4)

        central = QWidget()
        central.setLayout(layout1)
        self.setCentralWidget(central) #.setLayout(layout1)

        self.show()

app = QApplication(sys.argv)
#window = MyWidget()
window = MyMainWindow()

# window.show()

sys.exit(app.exec())