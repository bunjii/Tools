# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
import sys
import numpy as np
#os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
#os.environ['QT_API'] = 'pyqt5'

import sip
sip.setapi('QString', 2)

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
#from pyface.qt import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)
from tvtk.pyface.api import Scene

from traits.api import HasTraits, Instance, Button, on_trait_change
from traitsui.api import View, Item, HSplit, Group
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi import mlab

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QDesktopWidget,
                             QFileDialog, QApplication, QWidget, QSizePolicy, QBoxLayout,
                             QGridLayout, QLabel, QPushButton, QLineEdit, QMenu,
                             QHBoxLayout, QVBoxLayout, QMessageBox, QTabWidget)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

################################################################################
# Mayavi Part
################################################################################

class MyVisuClass(HasTraits):
    scene = Instance(MlabSceneModel, ())

    def redraw_scene(self, scene):
        mlab.clf(figure=scene.mayavi_scene)
        mlab.figure(figure=scene.mayavi_scene, bgcolor=(0.15, 0.15, 0.15))
        x, y, z, s = np.random.random((4, 100))
        mlab.points3d(x, y, z, s, figure=scene.mayavi_scene)

    @on_trait_change('scene.activated')
    def update_plot(self):
        self.redraw_scene(self.scene)

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=Scene),
                     height=250, width=300, show_label=False),
                resizable=True  # We need this to resize with the parent widget
                )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
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
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu('&File')

        self.import_action = QAction('Import data', self)
        self.import_action.setShortcut('Ctrl+O')
        self.import_action.triggered.connect(self.show_dialog)
        self.new_action = QAction('New', self)
        self.file_menu.addAction(self.import_action)
        self.file_menu.addAction(self.new_action)

        self.show()

    def show_dialog(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'select input data file', '/home', "Data file (*.dat)")

        if self.fname[0]:
            f = open(self.fname[0], 'r')
            self.setWindowTitle(self.window_title+":: "+str(self.fname[0]))

            with f:
                data = f.read()
                # print(data)
    
    def plot(self,data):
        pass


################################################################################
# MAIN
################################################################################


if __name__ == "__main__":

    app = QApplication.instance()
    # define a "complex" layout to test the behaviour
    
    # container.show()
    window = MyMainWindow()

    # Start the main event loop.
    sys.exit(app.exec_())
