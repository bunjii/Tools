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
                             QGridLayout, QLabel, QPushButton, QLineEdit, 
                             QHBoxLayout, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

################################################################################
# Mayavi Part
################################################################################

class MyVisuClass(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        self.scene.mlab.test_points3d()

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
# MAIN
################################################################################

if __name__ == "__main__":
    app = QApplication.instance()
    container = QWidget()
    container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
    # define a "complex" layout to test the behaviour
    layout = QGridLayout(container)

    label = QtWidgets.QLabel(container)
    label.setText("Your QWidget aiueo kakikukeko at (%d, %d)" % (0, 0))
    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    layout.addWidget(label, 0, 0)

    mayavi_widget = MayaviQWidget(container)

    layout.addWidget(mayavi_widget, 0, 1)
    # container.show()
    window = QMainWindow()
    window.setCentralWidget(container)
    window.show()

    # Start the main event loop.
    sys.exit(app.exec_())
