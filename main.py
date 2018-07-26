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

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
                             QFileDialog, QApplication, QWidget, QSizePolicy,
                             QGridLayout, QLabel, QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot


################################################################################
# Mayavi Part
################################################################################
class MyVisuClass(HasTraits):
    scene1 = Instance(MlabSceneModel, ())
    scene2 = Instance(MlabSceneModel, ())

    button1 = Button('Redraw')
    button2 = Button('Redraw')

    def __init__(self):
        HasTraits.__init__(self)
        self.test_points3d(self.scene1)
        self.redraw_scene(self.scene2)

    @on_trait_change('button1')
    def redraw_scene1(self):
        self.test_points3d(self.scene1)

    @on_trait_change('button2')
    def redraw_scene2(self):
        self.redraw_scene(self.scene2)

    def redraw_scene(self, scene):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.
        mlab.clf(figure=scene.mayavi_scene)
        mlab.figure(figure=scene.mayavi_scene, bgcolor=(0.9,0.9,0.9))
        # mlab.figure(bgcolor=(1,1,1))
        x, y, z, s = np.random.random((4, 100))
        mlab.points3d(x, y, z, s, figure=scene.mayavi_scene)

    def test_points3d(self, scene):
        mlab.clf(figure=scene.mayavi_scene)
        mlab.figure(figure=scene.mayavi_scene, bgcolor=(0.9,0.9,0.9))

        t = np.linspace(0, 4 * np.pi, 20)
        cos = np.cos
        sin = np.sin

        x = sin(2 * t)
        y = cos(t)
        z = cos(2 * t)
        s = 2 + sin(t)

        mlab.points3d(x, y, z, s, colormap="copper", scale_factor=.25,
                      figure=scene.mayavi_scene)

    def plot_node(self, scene, nodes):
        # under development
        return

    # The layout of the dialog created
    view = View(HSplit(
                  Group(
                       Item('scene1',
                            editor=SceneEditor(), height=250,
                            width=300),
                       'button1',
                       show_labels=False,
                  ),
                  Group(
                       Item('scene2',
                            editor=SceneEditor(scene_class=Scene), height=250,
                            width=300, show_label=False),
                       'button2',
                       show_labels=False,
                  ),
                ),
                resizable=True,
                )

################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
################################################################################
class MayaviQWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.visualization = MyVisuClass()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

################################################################################
# UI
################################################################################

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        container = QWidget()
        layout = QGridLayout(container)

        self.setWindowTitle('Structural Tools Ver.0.1')
        self.setCentralWidget(container)
        self.statusBar()

        # put some stuff around mayavi
        for i in range(2):
            for j in range(2):
                if (i == 0) and (j == 1):
                    continue
                elif (i == 0) and (j == 0):

                    self.textbox1 = QLineEdit(self)
                    self.textbox1.setReadOnly(True)
                    self.textbox1.move(20, 80)
                    self.textbox1.resize(300,20)

                    continue

                # qwidget_test01 = QWidget() ###
                label = QLabel(container)
                label.setText("Your QWidget at (%d, %d)" % (i, j))
                label.setAlignment(QtCore.Qt.AlignHCenter |
                                   QtCore.Qt.AlignVCenter)
                label.minimumWidth = 320
                # label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

                layout.addWidget(label, i, j)

        layout.addWidget(MayaviQWidget(container), 0, 1)

        # menubar

        open_file = QAction('Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('opening new file...')
        open_file.triggered.connect(self.show_dialog)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file)

        self.show()

    def show_dialog(self):

        fname = QFileDialog.getOpenFileName(self, 'select input data file', '/home', "Data file (*.dat)")
        # osname = os.name
        # cwd = os.getcwd()

        # inputfilename = "input01.dat"
        # if osname == 'nt':  # in case of Windows
        #     path = cwd+"\\"+inputfilename
        # else:  # Mac, Linux
        #     path = cwd+"/"+inputfilename

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textbox1.setText(str(fname[0]))
                # print(data)


################################################################################
# MAIN
################################################################################
if __name__ == '__main__':

    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app = QApplication.instance()

    window = MyMainWindow()
    # Start the main event loop.
    app.exec_()
