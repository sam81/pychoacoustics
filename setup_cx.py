from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
                 'excludes': ['tkinter',
                              'PyQt5.QtQml',
                              'PyQt5.QtBluetooth',
                              'PyQt5.QtQuickWidgets',
                              'PyQt5.QtSensors',
                              'PyQt5.QtSerialPort',
                              'PyQt5.QtSql'
                              ]}


import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('pychoacoustics\\__main__.py',
               base=base,
               target_name = 'pychoacoustics',
               icon='icons/point-right.ico')
]

setup(name='pychoacoustics',
    version="0.6.5",
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
