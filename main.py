import math
import os
import sys
from datetime import datetime

import numpy as np
from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtWidgets import (QAction, QApplication, QBoxLayout, QDesktopWidget,
                             QFileDialog, QGridLayout, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QMenu, QMessageBox,
                             QPlainTextEdit, QPushButton, QSizePolicy,
                             QSplitter, QTabWidget, QTextEdit, QVBoxLayout,
                             QWidget, qApp, QRadioButton, QButtonGroup)
from traits.api import Button, HasTraits, Instance, on_trait_change
from traitsui.api import Group, HSplit, Item, View
from tvtk.pyface.api import Scene

import sip
from solver.classConstraint import Constraints
from solver.classElement import Elements
from solver.classLoad import Loads
from solver.classMaterial import Materials
from solver.classSection import Sections
from solver.classSolve import (createLoadVector2d, createStiffnessMatrix2d,
                               obtainDefVector, obtainInverseMatrix,
                               obtainNormalForceStressStrain)
from solver.Condition import Conditions
from solver.DataIO import (ReadInput, Write_OutputData, WriteInputData2,
                           resultTruss2d, summaryInputData)
from solver.Node import Node, Nodes
from solver.solve_2d_truss import solve_2d_truss
from solver.StrData import StructuralData

sip.setapi('QString', 2)

################################################################################
# Mayavi Part
################################################################################

class MyVisuClass(HasTraits):

    # def __init__(self):

    scene = Instance(MlabSceneModel, ())
    # the layout of the dialog created
    
    view = View(Item('scene', editor=SceneEditor(scene_class=Scene),
                    height=250, width=300, show_label=False),
                resizable=True ) 
    """
    view = View(Item('scene', editor=SceneEditor(),
                    height=250, width=300, show_label=False),
                resizable=True)
    """
    def redraw_scene(self):
        mlab.clf(figure=self.scene.mayavi_scene)
        mlab.figure(figure=self.scene.mayavi_scene, bgcolor=(0.15, 0.15, 0.15))

    def plot_model_geometry(self, _strdata):
        mlab.clf(figure=self.scene.mayavi_scene) 

        # node
        nodes = _strdata.Nodes.nodes
        num_node = len(nodes)
        xlist = []
        ylist = []
        zlist = []
        nidList = []
        for i in range(len(nodes)):
            xlist.append(nodes[i].x)
            ylist.append(nodes[i].y)
            # zlist.append(nodes[i].z)
            nidList.append(str(nodes[i].id))
        x = np.array(xlist)
        y = np.array(ylist)
        z = np.zeros(num_node) # zero element for 2d analysis

        window.pts = mlab.points3d(x,y,z,figure=self.scene.mayavi_scene, 
                            resolution=16, scale_factor=0.07)
        
        self.scene.disable_render = True

        for i in range(len(nodes)):
            x = xlist[i]
            y = ylist[i]
            window.nodeText.append(mlab.text3d(
                x, y, 0, "N"+nidList[i], figure=self.scene.mayavi_scene, 
                scale=0.08, color=(1, 1, 1)))
        
        elems = _strdata.Elems.elements
        num_elem = len(elems)
        for i in range(num_elem):
            n1id = elems[i].n1
            n2id = elems[i].n2
            self.LinePlot(n1id, n2id, _strdata.Nodes)

            n1 = _strdata.Nodes.findNodeById(n1id)
            n2 = _strdata.Nodes.findNodeById(n2id)
            midpt = Node.getMidPointCoordinates(n1,n2)
            
            x = midpt[0]
            y = midpt[1]

            angle = 0.0

            window.elemText.append(mlab.text3d(
                x, y, 0, "E"+str(elems[i].id), figure=self.scene.mayavi_scene, 
                scale=0.08, color=(1, 1, 1), orientation=(0,0,angle)))
        self.scene.disable_render = False
        # elem text
        
        # loads
        load_scale_factor = 0.2
        color_load = (135/256,206/256,250/256)
        loads = _strdata.Loads.loads
        num_loads = len(loads)
        xlist = []
        ylist = []
        zlist = np.zeros(num_loads)
        ulist = []
        vlist = []
        wlist = np.zeros(num_loads)
        for i in range(num_loads):
            n = _strdata.Nodes.findNodeById(loads[i].nodeId)
            lx = loads[i].loadX
            ly = loads[i].loadY
            x = n.x - lx * load_scale_factor
            y = n.y - ly * load_scale_factor
            xlist.append(x)
            ylist.append(y)
            ulist.append(lx)
            vlist.append(ly)

            window.loadText.append(mlab.text3d(x, y, 0, str(loads[i].vecLength), 
                                               figure=self.scene.mayavi_scene,
                                               scale=0.08, 
                                               color=color_load, 
                                               orientation=(0, 0, 0)))
        x = np.array(xlist)
        y = np.array(ylist)
        u = np.array(ulist)
        v = np.array(vlist)
        window.loadvecs = mlab.quiver3d(x, y, zlist, u, v, wlist, 
                                        scale_factor=load_scale_factor, 
                                        mode='2darrow', 
                                        line_width =2.0,
                                        color=color_load)

        # global axes
        mlab.orientation_axes(figure=self.scene.mayavi_scene, opacity=1.0, line_width=1.0)  

    def show_load_vec(self, _load, _strdata):
        # loads
        pass

    @on_trait_change('scene.activated')
    def update_plot(self):
        self.redraw_scene()
    
    def reset_view_xy(self):
        mlab.view(0,0)

    def showpip(self):
        mlab.show_pipeline()
    
    def toggle_nid(self):
        if window.tgl_nid == False:
            window.tgl_nid = True
            #window.pts.visible = True
            for i in range(len(window.nodeText)):
                window.nodeText[i].visible = True
        else:
            window.tgl_nid = False
            #window.pts.visible = False
            for i in range(len(window.nodeText)):
                window.nodeText[i].visible = False

    def toggle_eid(self):
        if window.tgl_eid == False:
            window.tgl_eid = True
            for i in range(len(window.elemText)):
                window.elemText[i].visible = True
        else:
            window.tgl_eid = False
            for i in range(len(window.elemText)):
                window.elemText[i].visible = False
    
    def toggle_load(self):
        if window.tgl_lval == False:
            window.tgl_lval = True
            window.loadvecs.visible = True
            for i in range(len(window.loadText)):
                window.loadText[i].visible = True
        else:
            window.tgl_lval = False
            window.loadvecs.visible = False
            for i in range(len(window.loadText)):
                window.loadText[i].visible = False

    @staticmethod
    def LinePlot(_sid, _eid, _nodes):
        spt = _nodes.findNodeById(_sid)
        ept = _nodes.findNodeById(_eid)
        mlab.plot3d([spt.x, ept.x], [spt.y, ept.y], [0.0, 0.0], 
                                 line_width=1.0, opacity=0.8, tube_radius=None)

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

class OutputWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        radio1 = QRadioButton('Disp.')
        radio2 = QRadioButton('Stress')

        push1 = QPushButton('Show/Hide')

        self.group = QButtonGroup()
        self.group.addButton(radio1, 1)
        self.group.addButton(radio2, 2)
        # self.group.addButton(push1,3)
        # radio1.toggle()

        # self.tab1 = QPlainTextEdit(self)
        # self.tab1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #button = QPushButton('Check')
        #button.clicked.connect(self.buttonClicked)

        layout = QVBoxLayout()
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.addWidget(push1)
        # layout.addWidget(self.tab1)

        self.setLayout(layout)

    #def buttonClicked(self):
    #    print('Radio: %d' % self.group.checkedId())

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tgl_nid = True
        self.tgl_eid = True
        self.tgl_lval = True
        self.pts = []
        self.nodeText = []
        self.elemText = []
        self.loadText = []
        self.filename = ""

        self.window_title = "Structural Tools V.0.1"
        self.container = QWidget()
        
        self.setCentralWidget(self.container)
        self.mylayout = QHBoxLayout(self.container)
        self.setWindowTitle(self.window_title)
        self.statusBar().showMessage("READY")
        self.resize(1200, 800)

        # left area

        # left upper: tabholder 1
        tabholder1 = QTabWidget(self)
        tabholder1.setMinimumWidth(500)
        tabholder1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        # left lower: tabholder 2
        tabholder2 = QTabWidget(self)
        tabholder2.setMinimumSize(500,180)
        tabholder2.setMaximumHeight(300)
        tabholder2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #
        #
        # tab1 < tabholder 1
        self.tab1 = QPlainTextEdit(tabholder1)
        self.tab1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # tab2 < tabholder 1
        self.tab2 = QPlainTextEdit(tabholder1)
        self.tab2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # tab2b < tabholder 1
        self.tab2b = OutputWidget(self)

        # tab3 < tabholder 2
        self.tab3 = QPlainTextEdit(tabholder2)
        
        tabholder1.addTab(self.tab1, "INPUT")
        tabholder1.addTab(self.tab2, "OUTPUT")
        tabholder1.addTab(self.tab2b, "DISPLAY")
        
        tabholder2.addTab(self.tab3, "CONSOLE")

        # right area
        self.mayavi_widget = MayaviQWidget()
        
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(tabholder1)
        splitter2.addWidget(tabholder2)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(splitter2)
        splitter1.addWidget(self.mayavi_widget)

        self.mylayout.addWidget(splitter1)

        # self.setLayout(self.mylayout)

        # menubar
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')
        edit_menu = menubar.addMenu('&Edit')
        view_menu = menubar.addMenu('&View')
        solve_menu = menubar.addMenu('&Solve')

        # "file" actions
        ## import data
        import_action = QAction('Open Input File', self)
        import_action.setShortcut('Ctrl+O')
        import_action.triggered.connect(self.open_file_dialog)

        ## save input data
        save_action  = QAction('Save Input File', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        close_action = QAction('&Close', self)
        close_action.setShortcut('Alt+F4')
        close_action.triggered.connect(self.close)

        # "edit" actions
        show_pipeline_action = QAction('&Show Pipeline', self)
        show_pipeline_action.setShortcut('Alt+P')
        show_pipeline_action.triggered.connect(self.mayavi_widget.visualization.showpip)

        # "view" actions
        view_xy_action = QAction('&XY Plane', self)
        view_xy_action.setShortcut('Ctrl+1')
        view_xy_action.triggered.connect(self.mayavi_widget.visualization.reset_view_xy)

        view_nodeid_action = QAction('&Toggle Node ID', self)
        view_nodeid_action.setShortcut('Alt+N')
        view_nodeid_action.triggered.connect(self.mayavi_widget.visualization.toggle_nid)

        view_elemid_action = QAction('&Toggle Element ID', self)
        view_elemid_action.setShortcut('Alt+M')
        view_elemid_action.triggered.connect(self.mayavi_widget.visualization.toggle_eid)

        view_load_action = QAction('&Toggle Loads', self)
        view_load_action.setShortcut('Alt+L')
        view_load_action.triggered.connect(self.mayavi_widget.visualization.toggle_load)

        # "solve" actions
        solve_action = QAction('&Solve', self)
        solve_action.setShortcut('F5')
        solve_action.triggered.connect(self.Solve)

        # register actions to menu
        ## file
        file_menu.addAction(import_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        ## edit
        edit_menu.addAction(show_pipeline_action)
        ## view
        view_menu.addAction(view_xy_action)
        view_menu.addAction(view_nodeid_action)
        view_menu.addAction(view_elemid_action)
        view_menu.addAction(view_load_action)
        ## solve
        solve_menu.addAction(solve_action)
        
        self.show()

    def Solve(self):
        # record start time
        dts = str(datetime.now())  # .strftime('%Y/%m/%d %H:%M:%S')
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.render_text(self.tab3, dts + ": Solve command executed \n")
        # save tab1 to input file
        self.save_file()
        # reset data file

        f = open(self.filename, 'r')
        self.setWindowTitle(self.window_title+" :: "+str(self.filename))

        data.ResetStrData()
        ReadInput(f.readlines(), data)
        f.close()
        #
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText(str(datetime.now()) + ": Data file reset and Input file read \n")
        # need to retrieve data from tab1
        # reset mayavi window
        self.mayavi_widget.visualization.plot_model_geometry(data)
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText(str(datetime.now()) + ": Graphics redrawn \n")
        # 
        # solve 
        solve_2d_truss.truss2d(data, self.filename)
        dtf = str(datetime.now())  # .strftime('%Y/%m/%d %H:%M:%S')
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText(dtf + ": Solve finished\n")
        # write output to screen
        tab2txt = Write_OutputData(data, self.filename)
        self.render_text(self.tab2, tab2txt)
        # self.render_text(self.tab2b.tab1, tab2txt)

        # write output to file
        outfilename = 'RES_'+ os.path.basename(self.filename)
        f = open(outfilename, 'w')
        f.write(tab2txt)
        f.close()

        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText(
            str(datetime.now()) + ": Output file written \n")

        self.statusBar().showMessage('READY')

    def save_file(self):
        # retrieve what's written in the text tab
        lines = self.tab1.toPlainText()
        # write down to a file (overwrite caution?)
        if not self.fname: 
            ### doesn't work here at the moment.
            print("file destination not specified")
            pass
        else:
            ### else is also unstable.
            f = open(self.fname[0],'w')
            f.write(lines)
            f.close()
            self.statusBar().showMessage('SAVED')

    def open_file_dialog(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'select input data file', '/home', "Data file (*.dat)")
        
        if not self.fname[0]:
            return

        # print(self.fname[0])
        self.filename = self.fname[0]
        f = open(self.fname[0], 'r')
        self.setWindowTitle(self.window_title+" :: "+str(self.fname[0]))
    
        data.ResetStrData()
        ReadInput(f.readlines(), data)
        f.close()

        self.mayavi_widget.visualization.plot_model_geometry(data)  

        filepath = self.fname[0]
        tab1txt = WriteInputData2(data)
        self.render_text(self.tab1, tab1txt)

    def render_text(self, _widget, _txt):
        if os.name == 'nt': # windows
            font = QtGui.QFont("Monospace")
            font.setStyleHint(QFont().Monospace)
        else:
            font = QtGui.QFont("courier")

        _widget.setFont(font)
        _widget.setPlainText(_txt)
        self.statusBar().showMessage('READ')

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
