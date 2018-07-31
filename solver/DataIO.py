"""
# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
"""
import datetime
import os.path
import solver.StrData
import solver.Node
import solver.classElement

# ****** DATA INPUT ******

def ReadInput(filename, _nodes, _elements, _materials,
              _secs, _constraints, _loads):

    dataIn = open(filename, 'r')
    lines = dataIn.readlines()
    dataIn.close()

    for i in range(len(lines)):
        items = []
        # continue with comment lines
        if lines[i].startswith('#'):
            continue
        # node id, x, y
        elif lines[i].startswith('n') or lines[i].startswith('N'):
            items = lines[i].split(',')
            _nodes.append_node(int(items[1]), float(items[2]), float(items[3]))
        # element id, n1, n2, material type, section type
        elif lines[i].startswith('elem'):
            items = lines[i].split(',')
            _elements.appendElement( \
            int(items[1]), int(items[2]), int(items[3]), int(items[4]), int(items[5]))
        # material id, name, e-module
        elif lines[i].startswith('mat'):
            items = lines[i].split(',')
            _materials.appendMaterial(int(items[1]), str(items[2].strip()), float(items[3]))
        # section id, area, moment of inertia
        elif lines[i].startswith('sec'):
            items = lines[i].split(',')
            _secs.appendSection(int(items[1]), float(items[2]), float(items[3]))
        # constraint id, node id, condition x, condition y
        elif lines[i].startswith('constr'):
            items = lines[i].split(',')
            _constraints.appendConstraint( \
            int(items[1]), int(items[2]), int(items[3]), int(items[4]))
        # load id, node id, load x, load y
        elif lines[i].startswith('load'):
            items = lines[i].split(',')
            _loads.appendLoad(int(items[1]), int(items[2]), float(items[3]), float(items[4]))

        else: continue

def ReadInput(filename, _strData):
# def ReadInput(filename, _nodes, _elements, _materials, _secs, _constraints, _loads):
    dataIn = open(filename, 'r')
    lines = dataIn.readlines()
    dataIn.close()

    for i in range(len(lines)):
        items = []
        if lines[i].startswith('#'):
            continue
        # node id, x, y
        elif lines[i].startswith('n') or lines[i].startswith('N'):
            items = lines[i].split(',')
            _nodes.append_node(int(items[1]), float(items[2]), float(items[3]))
        # element id, n1, n2, material type, section type
        elif lines[i].startswith('elem'):
            items = lines[i].split(',')
            _elements.appendElement( \
            int(items[1]), int(items[2]), int(items[3]), int(items[4]), int(items[5]))
        # material id, name, e-module
        elif lines[i].startswith('mat'):
            items = lines[i].split(',')
            _materials.appendMaterial(int(items[1]), str(items[2].strip()), float(items[3]))
        # section id, area, moment of inertia
        elif lines[i].startswith('sec'):
            items = lines[i].split(',')
            _secs.appendSection(int(items[1]), float(items[2]), float(items[3]))
        # constraint id, node id, condition x, condition y
        elif lines[i].startswith('constr'):
            items = lines[i].split(',')
            _constraints.appendConstraint( \
            int(items[1]), int(items[2]), int(items[3]), int(items[4]))
        # load id, node id, load x, load y
        elif lines[i].startswith('load'):
            items = lines[i].split(',')
            _loads.appendLoad(int(items[1]), int(items[2]), float(items[3]), float(items[4]))

        else: continue

def readInput2dR(filename, _nodes, _elements, _materials,
                 _secs, _constraints, _loads):

    dataIn = open(filename, 'r')
    lines = dataIn.readlines()
    dataIn.close()

    # Input Nodes
    for i in range(len(lines)):

        items = []

        if(lines[i].startswith('node')):        # node id, x, y
            items = lines[i].split(',')
            _nodes.appendNode(int(items[1]),float(items[2]),float(items[3]))
        elif(lines[i].startswith('elem')):      # element id, n1, n2, material type, section type
            items = lines[i].split(',')
            _elements.appendElement(int(items[1]), int(items[2]), int(items[3]), int(items[4]), int(items[5]))
        elif(lines[i].startswith('mat')):       # material id, name, e-module
            items = lines[i].split(',')
            _materials.appendMaterial(int(items[1]), str(items[2].strip()), float(items[3]))
        elif(lines[i].startswith('sec')):       # section id, area, moment of inertia
            items = lines[i].split(',')
            _secs.appendSection(int(items[1]), float(items[2]), float(items[3]))
        elif(lines[i].startswith('constr')):    # constraint id, node id, condition x, condition y
            items = lines[i].split(',')
            _constraints.appendConstraint(int(items[1]), int(items[2]), int(items[3]), int(items[4]))
            _constraints.appendConstraint2dR(int(items[1]),int(items[5]), float(items[6]))
        elif(lines[i].startswith('load')):      # load id, node id, load x, load y
            items = lines[i].split(',')
            _loads.appendLoad2dR(int(items[1]), int(items[2]), float(items[3]), float(items[4]), float(items[5]))
            
        else: continue
        
def readInput3dTruss(filename, _nodes, _elements, _materials, 
              _secs, _constraints, _loads):
    
    dataIn = open(filename, 'r' )
    lines = dataIn.readlines()
    dataIn.close()

    
    # Input Nodes 
    for i in range(len(lines)):
        
        items=[]
        
        if(lines[i].startswith('node')):        # node id, x, y, z
            items = lines[i].split(',')
            _nodes.appendNode3d(int(items[1]),float(items[2]),float(items[3]), float(items[4]))
        elif(lines[i].startswith('elem')):      # element id, n1, n2, material type, section type
            items = lines[i].split(',')
            _elements.appendElement(int(items[1]), int(items[2]), int(items[3]), int(items[4]), int(items[5]))
        elif(lines[i].startswith('mat')):       # material id, name, e-module
            items = lines[i].split(',')
            _materials.appendMaterial(int(items[1]), str(items[2].strip()), float(items[3]))
        elif(lines[i].startswith('sec')):       # section id, area, moment of inertia
            items = lines[i].split(',')
            _secs.appendSection(int(items[1]), float(items[2]), float(items[3]))
        elif(lines[i].startswith('constr')):    # constraint id, node id, condition x, condition y, condition z
            items = lines[i].split(',')
            _constraints.appendConstraint3d(int(items[1]), int(items[2]), int(items[3]), int(items[4]), int(items[5]))
        elif(lines[i].startswith('load')):      # load id, node id, load x, load y, load z
            items = lines[i].split(',')
            _loads.appendLoad3d(int(items[1]), int(items[2]), float(items[3]), float(items[4]), float(items[5]))
            
        else: continue

def summaryInputData(filename, _nodes, _elements, _materials,
                     _sectionTypes, _constraints, _loads):
    
    # header -- date and filename
    filenameAbs = os.path.abspath(filename)
    outputName = 'input_'+filename
    f = open(outputName, 'w')
    
    f.write('# --- HEADER ---\n')
    f.write('\n')
    f.write('# ANALYSIS DATE: ' + str(datetime.datetime.now()))
    f.write('\n')
    f.write('# INPUT SOURCE: ' + filenameAbs + '\n')
    f.write('# NUMBER OF NODES: ' + str(len(_nodes.nodes)) +'\n')
    f.write('# NUMBER OF ELEMENTS: ' + str(len(_elements.elements)) +'\n')
    f.write('# NUMBER OF FIXED NODES: ' + str(len(_constraints.constraints)) +'\n') 
    f.write('# NUMBER OF LOADED NODES: ' + str(len(_loads.loads)) +'\n')
    f.write('\n')
    
    # node info
    f.write('# --- NODE ---\n')
    f.write('#        ID,          X,          Y')
    f.write(_nodes.outputNodesInfo())
    f.write('\n\n')

    # element info
    f.write('# --- ELEMENT ---\n')
    f.write('#        ID,    N1,    N2, MATID, SECID,     LENGTH,        SIN,        COS, LOC. STIFF')
    f.write(_elements.outputElemsInfo())
    f.write('\n\n')
    
    # material
    f.write('# --- MATERIAL ---\n')
    f.write('#        ID,  NAME,          E')
    f.write(_materials.outputMaterialsInfo())
    f.write('\n\n')  
    
    # section types
    f.write('# --- SECTION ---\n')
    f.write('#        ID,       AREA, MOM. INERT')
    f.write(_sectionTypes.outputSectionsInfo())
    f.write('\n\n')
   
    # constraintsStansted
    f.write('# --- CONSTRAINTS (0:FREE, 1:FIXED) ---\n')
    f.write('#        ID,   NID,     X,     Y')
    f.write(_constraints.outputConstraintsInfo())
    f.write('\n\n')
    
    # loads
    f.write('# --- LOADS ---\n')
    f.write('#        ID,   NID,          X,          Y')
    f.write(_loads.outputLoadsInfo())
    f.write('\n\n')
    
    # end of the input data
    f.write('<END OF INPUT DATA> ' + str(datetime.datetime.now()))
    
    f.close()

def summaryInputData2dR(filename, _nodes, _elements, _materials, 
              _sectionTypes, _constraints, _loads):
    
    # header -- date and filename
    filenameAbs = os.path.abspath(filename)
    outputName = 'input_'+filename
    f = open(outputName, 'w')
    
    f.write('--- header ---\n')
    f.write('\n')
    f.write('analysis date: ' + str(datetime.datetime.now()))
    f.write('\n')
    f.write('input source: ' + filenameAbs + '\n')
    f.write('number of nodes: ' + str(len(_nodes.nodes)) +'\n')
    f.write('number of elements: ' + str(len(_elements.elements)) +'\n')
    f.write('number of fixed nodes: ' + str(len(_constraints.constraints)) +'\n') 
    f.write('number of loaded nodes: ' + str(len(_loads.loads)) +'\n')
    f.write('\n')
    
    # node info
    f.write('--- node info ---\n')
    f.write('node id, x, y')
    f.write(_nodes.outputNodesInfo())
    f.write('\n\n')

    # element info
    f.write('--- element info ---\n')
    f.write('element id, n1, n2, material type, section type, length, sin, cos, local stiffness')
    f.write(_elements.outputElemsInfo())
    f.write('\n\n')
    
    # material
    f.write('--- material info ---\n')
    f.write('material id, name, e-module')
    f.write(_materials.outputMaterialsInfo())
    f.write('\n\n')  
    
    # section types
    f.write('--- section types ---\n')
    f.write('section id, area, moment of inertia')
    f.write(_sectionTypes.outputSectionsInfo())
    f.write('\n\n')
   
    # constraints
    f.write('--- constraints (0:free, 1:fixed) ---\n')
    f.write('constraint id, node id, condition x, condition y')
    f.write(_constraints.outputConstraintsInfo())
    f.write('\n\n')
    
    # loads
    f.write('--- loads ---\n')
    f.write('load id, node id, load x, load y')
    f.write(_loads.outputLoadsInfo2dR())
    f.write('\n\n')
    
    # end of the input data
    f.write('<end of the input data> ' + str(datetime.datetime.now()))
    
    f.close()
    

def summaryInputData3dTruss(filename, _nodes, _elements, _materials, 
              _sectionTypes, _constraints, _loads):
    
    # header -- date and filename
    filenameAbs = os.path.abspath(filename)
    outputName = 'input_'+filename
    f = open(outputName, 'w')
    
    f.write('--- header ---\n')
    f.write('\n')
    f.write('analysis date: ' + str(datetime.datetime.now()))
    f.write('\n')
    f.write('input source: ' + filenameAbs + '\n')
    f.write('number of nodes: ' + str(len(_nodes.nodes)) +'\n')
    f.write('number of elements: ' + str(len(_elements.elements)) +'\n')
    f.write('number of fixed nodes: ' + str(len(_constraints.constraints)) +'\n') 
    f.write('number of loaded nodes: ' + str(len(_loads.loads)) +'\n')
    f.write('\n')
    
    # node info
    f.write('--- node info ---\n')
    f.write('node id, x, y, z ')
    f.write(_nodes.outputNodesInfo3dTruss())
    f.write('\n\n')

    # element info
    f.write('--- element info ---\n')
    f.write('element id, n1, n2, material type, section type, length, sin, cos, local stiffness')
    f.write(_elements.outputElemsInfo())
    f.write('\n\n')
    
    # material
    f.write('--- material info ---\n')
    f.write('material id, name, e-module')
    f.write(_materials.outputMaterialsInfo())
    f.write('\n\n')  
    
    # section types
    f.write('--- section types ---\n')
    f.write('section id, area, moment of inertia')
    f.write(_sectionTypes.outputSectionsInfo())
    f.write('\n\n')
   
    # constraints
    f.write('--- constraints (0:free, 1:fixed) ---\n')
    f.write('constraint id, node id, condition x, condition y, condition z')
    f.write(_constraints.outputConstraintsInfo3dTruss())
    f.write('\n\n')
    
    # loads
    f.write('--- loads ---\n')
    f.write('load id, node id, load x, load y, load z')
    f.write(_loads.outputLoadsInfo3dTruss())
    f.write('\n\n')

    # end of the input data
    f.write('<end of the input data> ' + str(datetime.datetime.now()))

    f.close()
    
# ****** DATA OUTPUT ******  
def resultTruss2d(filename, _nodes, _elements):

    filenameAbs = os.path.abspath(filename)
    outputName = 'result_'+filename
    f = open(outputName, 'w')

    # header -- date and filename
    f.write('# --- HEADER ---\n')
    f.write('# \n')
    f.write('# analysis date: ' + str(datetime.datetime.now()))
    f.write('# \n')
    f.write('# input source: ' + filenameAbs + '\n\n')

    # node deformations
    f.write('# --- NODE ---\n')
    f.write('#        ID,       DEFX,       DEFY')
    f.write(_nodes.outputNodesResult())
    f.write('\n\n')

    # element forces, stresses and strain
    f.write('# --- ELEMENT ---\n')
    f.write('#        ID,   N. FORCE,  N. STRESS,  N. STRAIN')
    f.write(_elements.outputElemsResult())
    f.write('\n\n')

    # end of the input data
    f.write('<END OF RESULT> ' + str(datetime.datetime.now()))

    f.close()
    
def resultTruss3d(filename, _nodes, _elements):
    
    filenameAbs = os.path.abspath(filename)
    outputName = 'result_'+filename
    f = open(outputName, 'w')
    
    # header -- date and filename
    f.write('--- header ---\n')
    f.write('\n')
    f.write('analysis date: ' + str(datetime.datetime.now()))
    f.write('\n')
    f.write('input source: ' + filenameAbs + '\n\n')
    
    # node deformations
    f.write('--- node info ---\n')
    f.write('node id, def_x, def_y, def_z ')
    f.write(_nodes.outputNodesResult3dTruss())
    f.write('\n\n')
    
    # element forces, stresses and strain
    f.write('--- element info ---\n')
    f.write('element id, normal force, normal stress, strain')
    f.write(_elements.outputElemsResult())
    f.write('\n\n')

    
    f.close()
    