# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
import sys
import numpy as np

import sip
sip.setapi('QString', 2)

from tvtk.pyface.api import Scene

from traits.api import HasTraits, Instance, Button, on_trait_change
from traitsui.api import View, Item, HSplit, Group
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi import mlab

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QDesktopWidget, qApp,
                             QFileDialog, QApplication, QWidget, QSizePolicy, QBoxLayout,
                             QGridLayout, QLabel, QPushButton, QLineEdit, QMenu,
                             QHBoxLayout, QVBoxLayout, QMessageBox, QTabWidget)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

from solver.classConstraint import Constraints
from solver.classElement import Elements
from solver.classMaterial import Materials
from solver.classSection import Sections
from solver.classLoad import Loads
from solver.classSolve import createStiffnessMatrix2d
from solver.classSolve import createLoadVector2d
from solver.classSolve import obtainInverseMatrix
from solver.classSolve import obtainDefVector
from solver.classSolve import obtainNormalForceStressStrain
from solver.Node import Nodes
from solver.DataIO import ReadInput, summaryInputData, resultTruss2d
from solver.StrData import StructuralData

################################################################################
# Mayavi Part
################################################################################

class MyVisuClass(HasTraits):

    scene = Instance(MlabSceneModel, ())

    def redraw_scene(self):
        mlab.clf(figure=self.scene.mayavi_scene)
        mlab.figure(figure=self.scene.mayavi_scene, bgcolor=(0.15, 0.15, 0.15))
        x, y, z, s = np.random.random((4, 100))
        mlab.points3d(x, y, z, s, figure=self.scene.mayavi_scene)

    def update(self):
        # print("update executed")
        mlab.clf()  # Clear the figure
        t = np.linspace(0, 20, 200)
        mlab.plot3d(np.sin(t), np.cos(t), 0.1*t, t, figure=self.scene.mayavi_scene)

    @on_trait_change('scene.activated')
    def update_plot(self):
        # self.redraw_scene(self.scene)
        self.redraw_scene()

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=Scene),
                     height=250, width=300, show_label=False),
                resizable=True  # We need this to resize with the parent widget
               )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
################################################################################
class MayaviQWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        mayavi_layout = QtWidgets.QVBoxLayout(self)
        mayavi_layout.setContentsMargins(0, 0, 0, 0)
        mayavi_layout.setSpacing(0)
        self.visualization = MyVisuClass()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        mayavi_layout.addWidget(self.ui)
        self.ui.setParent(self)

################################################################################
# UI
################################################################################

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.window_title = "Structural Tools V.0.1"
        self.container = QWidget()
        self.layout = QGridLayout(self.container)

        self.setCentralWidget(self.container)
        self.setWindowTitle(self.window_title)
        self.resize(1200, 800)

        # left area
        self.leftarea = QWidget(self.container)
        self.leftarea.setFixedSize(400, 800)

        # right area
        self.mayavi_widget = MayaviQWidget(self.container)

        # register to layout
        self.layout.addWidget(self.leftarea, 0, 0)
        self.layout.addWidget(self.mayavi_widget, 0, 1)

        # menubar
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('&File')
        edit_menu = menubar.addMenu('&Edit')
        solve_menu = menubar.addMenu('&Solve')

        import_action = QAction('Import data', self)
        import_action.setShortcut('Ctrl+O')
        import_action.triggered.connect(self.show_dialog)

        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(import_action)
        file_menu.addAction(exit_action)
        edit_menu.addAction(import_action)
        solve_menu.addAction(exit_action)
        
        self.show()

    def show_dialog(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'select input data file', '/home', "Data file (*.dat)")

        if self.fname[0]:
            f = open(self.fname[0], 'r')
            self.setWindowTitle(self.window_title+":: "+str(self.fname[0]))

            with f:
                data = f.read()
                # ReadInput
                self.mayavi_widget.visualization.update()

                # print(data)
    
    def plot(self,data):
        pass

################################################################################
# STRUCTURAL MODEL
################################################################################

# ****** VARIABLES ******

ns = Nodes()
elms = Elements()
mts = Materials()
secs = Sections()
consts = Constraints()
lds = Loads()

str_data = StructuralData(ns, elms, mts, secs, consts, lds)


################################################################################
# MAIN
################################################################################


if __name__ == "__main__":

    app = QApplication.instance()    
    window = MyMainWindow()

    sys.exit(app.exec_())
