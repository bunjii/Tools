import os
import sys
from datetime import datetime

import numpy as np
import math

from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QTextCursor
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
from solver.DataIO import ReadInput, resultTruss2d, summaryInputData, WriteInputData2, Write_OutputData
from solver.Node import Nodes, Node
from solver.StrData import StructuralData
from solver.solve_2d_truss import solve_2d_truss

################################################################################
# Mayavi Part
################################################################################

class MyVisuClass(HasTraits):

    # def __init__(self):

    scene = Instance(MlabSceneModel, ())
    # the layout of the dialog created
    """
    view = View(Item('scene', editor=SceneEditor(scene_class=Scene),
                    height=250, width=300, show_label=False),
                resizable=True )  # We need this to resize with the parent widget
    """
    view = View(Item('scene', editor=SceneEditor(),
                    height=250, width=300, show_label=False),
                resizable=True)

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
            if n2.x - n1.x ==0:
                if n2.y-n1.y > 0:
                    angle = 90
                else:
                    angle = 270
            else:
                    angle = math.degrees(math.atan((n2.y-n1.y)/(n2.x-n1.x)))

            window.elemText.append(mlab.text3d(
                x, y, 0, "E"+str(elems[i].id), figure=self.scene.mayavi_scene, 
                scale=0.08, color=(1, 1, 1), orientation=(0,0,angle)))
        self.scene.disable_render = False
        # elem text
        
        # loads
        load_scale_factor = 0.2
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

            window.loadText.append(mlab.text3d(
                x, y, 0, ""+str(loads[i].vecLength), figure=self.scene.mayavi_scene,
                scale=0.08, color=(1, 1, 1), orientation=(0, 0, 0)))
        x = np.array(xlist)
        y = np.array(ylist)
        u = np.array(ulist)
        v = np.array(vlist)
        window.loadvecs = mlab.quiver3d(x, y, zlist, u, v, wlist, 
                                        scale_factor=load_scale_factor, mode='2darrow', line_width =3.0)

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
        self.gridlayout = QGridLayout(self.container)
        self.setCentralWidget(self.container)
        self.setWindowTitle(self.window_title)
        self.statusBar().showMessage("READY")
        self.resize(1200, 800)

        # left area
        # left area tab
        
        tabs = QTabWidget()
        tabs.setFixedWidth(580)
        tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tabs2 = QTabWidget()
        tabs2.setFixedWidth(580)
        tabs2.setFixedHeight(180)
        tabs2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vtabbox = QVBoxLayout()
        vtabbox.addWidget(tabs)
        self.tab1 = QPlainTextEdit(tabs)
        self.tab1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab2 = QPlainTextEdit(tabs)
        self.tab2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab3 = QPlainTextEdit(tabs2)
        tabs.addTab(self.tab1, "INPUT")
        tabs.addTab(self.tab2, "OUTPUT")
        tabs2.addTab(self.tab3, "CONSOLE")
        vtabbox.addWidget(tabs2)

        # right area
        self.mayavi_widget = MayaviQWidget()

        # register right/left area to gridlayout
        # self.gridlayout.addWidget(tabs, 0, 0)
        self.gridlayout.addLayout(vtabbox, 0, 0)
        self.gridlayout.addWidget(self.mayavi_widget, 0, 1)

        # menubar
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')
        edit_menu = menubar.addMenu('&Edit')
        view_menu = menubar.addMenu('&View')
        solve_menu = menubar.addMenu('&Solve')

        # "file" actions
        ## import data
        import_action = QAction('Open input file', self)
        import_action.setShortcut('Ctrl+O')
        import_action.triggered.connect(self.open_file_dialog)

        ## save input data
        save_action  = QAction('Save input file', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        close_action = QAction('&Close', self)
        close_action.setShortcut('Alt+F4')
        close_action.triggered.connect(self.close)

        # "edit" actions
        show_pipeline_action = QAction('&Show pipeline', self)
        show_pipeline_action.setShortcut('Alt+P')
        show_pipeline_action.triggered.connect(self.mayavi_widget.visualization.showpip)

        # "view" actions
        view_xy_action = QAction('&XY plane', self)
        view_xy_action.setShortcut('Ctrl+1')
        view_xy_action.triggered.connect(self.mayavi_widget.visualization.reset_view_xy)

        view_nodeid_action = QAction('&Toggle node ID', self)
        view_nodeid_action.setShortcut('Alt+N')
        view_nodeid_action.triggered.connect(self.mayavi_widget.visualization.toggle_nid)

        view_elemid_action = QAction('&Toggle element ID', self)
        view_elemid_action.setShortcut('Alt+M')
        view_elemid_action.triggered.connect(self.mayavi_widget.visualization.toggle_eid)

        view_load_action = QAction('&Toggle loads', self)
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
        self.render_text(self.tab3, "Solve Executed: " + dts + "\n")
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
        self.tab3.insertPlainText("Reset Datafile: " + str(datetime.now()) + "\n")
        # need to retrieve data from tab1
        # ReadInput(lines, data)
        # 
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText("Read Input tab: " + str(datetime.now()) + "\n")
        # reset mayavi window
        self.mayavi_widget.visualization.plot_model_geometry(data)
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText("Redrew Graphics: " + str(datetime.now()) + "\n")
        # 
        # solve 
        solve_2d_truss.truss2d(data, self.filename)
        dtf = str(datetime.now())  # .strftime('%Y/%m/%d %H:%M:%S')
        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText("Solve Finished: " + dtf + "\n")
        # write output to screen
        tab2txt = Write_OutputData(data, self.filename)
        self.render_text(self.tab2, tab2txt)
        # write output to file
        outfilename = 'RES_'+ os.path.basename(self.filename)
        f = open(outfilename, 'w')
        f.write(tab2txt)
        f.close()

        self.tab3.moveCursor(QTextCursor.MoveOperation(11))
        self.tab3.insertPlainText(
            "Wrote Output: " + str(datetime.now()) + "\n")

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
