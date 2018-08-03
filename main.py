import os
import sys

import numpy as np
from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QAction, QApplication, QBoxLayout, QDesktopWidget,
                             QFileDialog, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QMenu, QMessageBox,
                             QPushButton, QSizePolicy, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QPlainTextEdit , qApp)
from traits.api import Button, HasTraits, Instance, on_trait_change
from traitsui.api import Group, HSplit, Item, View
from tvtk.pyface.api import Scene

import sip
sip.setapi('QString', 2)
from solver.classConstraint import Constraints
from solver.classElement import Elements
from solver.classLoad import Loads
from solver.classMaterial import Materials
from solver.classSection import Sections
from solver.classSolve import (createLoadVector2d, createStiffnessMatrix2d,
                               obtainDefVector, obtainInverseMatrix,
                               obtainNormalForceStressStrain)
from solver.Condition import Conditions
from solver.DataIO import ReadInput, resultTruss2d, summaryInputData, WriteInputData2
from solver.Node import Nodes
from solver.StrData import StructuralData

################################################################################
# Mayavi Part
################################################################################

class MyVisuClass(HasTraits):

    scene = Instance(MlabSceneModel, ())
    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=Scene),
                     height=250, width=300, show_label=False),
                resizable=True )  # We need this to resize with the parent widget
               
    def redraw_scene(self):
        mlab.clf(figure=self.scene.mayavi_scene)
        mlab.figure(figure=self.scene.mayavi_scene, bgcolor=(0.15, 0.15, 0.15))

    def plot_model_geometry(self, _strdata):
        mlab.clf(figure=self.scene.mayavi_scene) 
        # mlab.axes(x_axis_visibility=True, y_axis_visibility=True, z_axis_visibility=True)
        
        # node
        nodes = _strdata.Nodes.nodes
        num_node = len(nodes)
        xlist = []
        ylist = []
        zlist = []
        for i in range(len(nodes)):
            xlist.append(nodes[i].x)
            ylist.append(nodes[i].y)
            # zlist.append(nodes[i].z)
        x = np.array(xlist)
        y = np.array(ylist)
        z = np.zeros(num_node) # zero element for 2d analysis

        mlab.points3d(x,y,z,figure=self.scene.mayavi_scene, resolution=64, scale_factor=0.2)

        # elem
        elems = _strdata.Elems.elements
        num_elem = len(elems)

        for i in range(num_elem):
            n1 = elems[i].n1
            n2 = elems[i].n2
            self.LinePlot(n1, n2, _strdata.Nodes)
        
        # loads
        loads = _strdata.Loads.loads
        num_loads = len(loads)
        for i in range(num_loads):
            self.show_load_vec(loads[i], _strdata)

        # global axes
        mlab.orientation_axes(figure=self.scene.mayavi_scene, opacity=1.0, line_width=1.0)  

    
    def show_load_vec(self, _load, _strdata):
        # loads
        nd = _strdata.Nodes.findNodeById(_load.nodeId)
        maxVecLength = _strdata.Loads.maxLength 
        # node X = nd.x
        # node Y = nd.y
        # node Z = 0
        if _load.loadX != 0:
            
            pass

    @on_trait_change('scene.activated')
    def update_plot(self):
        self.redraw_scene()
    
    def reset_view_xy(self):
        mlab.view(0,0)

    @staticmethod
    def LinePlot(_sid, _eid, _nodes):
        spt = _nodes.findNodeById(_sid)
        ept = _nodes.findNodeById(_eid)
        mlab.plot3d([spt.x, ept.x],[spt.y,ept.y],[0.0,0.0])

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
        self.gridlayout = QGridLayout(self.container)

        self.setCentralWidget(self.container)
        self.setWindowTitle(self.window_title)
        self.resize(1200, 800)

        # left area
        # left area tab
        tabs = QTabWidget()
        tabs.setFixedWidth(580)
        tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab1 = QPlainTextEdit(tabs)
        # tab1.setText("HW \n HW")
        self.tab1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab2 = QWidget()
        tabs.addTab(self.tab1, "INPUT")
        tabs.addTab(self.tab2, "OUTPUT")
        
        # right area
        self.mayavi_widget = MayaviQWidget()

        # register right/left area to gridlayout
        self.gridlayout.addWidget(tabs, 0, 0)
        self.gridlayout.addWidget(self.mayavi_widget, 0, 1)

        # menubar
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')
        edit_menu = menubar.addMenu('&Edit')
        view_menu = menubar.addMenu('&View')
        solve_menu = menubar.addMenu('&Solve')

        # "file" actions
        ## import data
        import_action = QAction('Import data', self)
        import_action.setShortcut('Ctrl+O')
        import_action.triggered.connect(self.show_open_dialog)

        ## save input data
        save_action  = QAction('Save input file', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        close_action = QAction('&Close', self)
        close_action.setShortcut('Alt+F4')
        close_action.triggered.connect(self.close)

        # "view" actions
        view_xy_action = QAction('&XY plane', self)
        view_xy_action.setShortcut('Ctrl+1')
        view_xy_action.triggered.connect(self.mayavi_widget.visualization.reset_view_xy)

        # "solve" actions
        # solve

        # register actions to menu
        file_menu.addAction(import_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)

        edit_menu.addAction(import_action)
        
        view_menu.addAction(view_xy_action)
        solve_menu.addAction(close_action)
        
        self.show()

    def save_file(self):
        print("save_file")
        pass

    def show_open_dialog(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'select input data file', '/home', "Data file (*.dat)")
        
        if not self.fname[0]:
            pass

        f = open(self.fname[0], 'r')
        self.setWindowTitle(self.window_title+" :: "+str(self.fname[0]))
        
        data.ResetStrData()
        ReadInput(f.readlines(), data)
        f.close()

        self.mayavi_widget.visualization.plot_model_geometry(data)  

        filepath = self.fname[0]
        tab1txt = WriteInputData2(data)
        self.write_input_text(tab1txt)
    
    def write_input_text(self, _txt):
        font = QtGui.QFont()
        font.setStyleHint(QFont().Monospace)
        font.setFamily("Monospace")
        self.tab1.setFont(font)
        self.tab1.setPlainText(_txt)

################################################################################
# STRUCTURAL MODEL
################################################################################

# ****** VARIABLES ******
def SetStrData():

    nds = Nodes()
    elms = Elements()
    mts = Materials()
    secs = Sections()
    consts = Constraints()
    lds = Loads()
    conds = Conditions()

    str_data = StructuralData(nds, elms, mts, secs, consts, lds, conds)

    return str_data

################################################################################
# MAIN
################################################################################


if __name__ == "__main__":

    app = QApplication.instance()    
    window = MyMainWindow()
    data = SetStrData()
    sys.exit(app.exec_())
