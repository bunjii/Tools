#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout,\
    QSizePolicy

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = QWidget()

    button1 = QPushButton('1')
    button2 = QPushButton('2')
    
    # 自動伸縮を設定
    button1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    button2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    
    layout = QHBoxLayout()
    layout.addWidget(button1)
    layout.addWidget(button2)
    window.setLayout(layout)
    
    window.show()
    sys.exit(app.exec_())