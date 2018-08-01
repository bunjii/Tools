import os
from cx_Freeze import setup, Executable
import cx_Freeze.hooks
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack
# import scipy
import matplotlib

# scipy_path = os.path.dirname(scipy.__file__) 
#use this if you are also using scipy in your application
"""
build_exe_options = {"packages": ["pyface.ui.qt4", "tvtk.vtk_module", 
                    "tvtk.pyface.ui.wx", "matplotlib.backends.backend_qt4",
                    'pygments.lexers', 'tvtk.pyface.ui.qt4',
                    'pyface.qt', 'pyface.qt.QtGui', 'pyface.qt.QtCore', 
                    'numpy','matplotlib','mayavi'],
                     "include_files": [(str(scipy_path), "scipy"), #for scipy
                    (matplotlib.get_data_path(), "mpl-data"),],
                     "includes":['PyQt4.QtCore','PyQt4.QtGui','mayavi','PyQt4'],
                     'excludes':'Tkinter',
                    "namespace_packages": ['mayavi']
                    }
"""

build_exe_options = {"packages": ["pyface.ui.qt4", "tvtk.vtk_module", 
                    "tvtk.pyface.ui.wx", "matplotlib.backends.backend_qt4",
                    'pygments.lexers', 'tvtk.pyface.ui.qt4',
                    'pyface.qt', 'pyface.qt.QtGui', 'pyface.qt.QtCore', 
                    'numpy','matplotlib','mayavi'],
                     "include_files": [(matplotlib.get_data_path(), "mpl-data")],
                     "includes":['PyQt5.QtCore','PyQt5.QtGui','mayavi','PyQt5'],
                     'excludes':'Tkinter',
                    "namespace_packages": ['mayavi']
                    }

executables = [
    Executable('main.py', targetName="main.exe",base = 'Win32GUI',)
]

setup(name='main',
      version='1.0',
      description='',
      options = {"build_exe": build_exe_options},
      executables=executables,
      )