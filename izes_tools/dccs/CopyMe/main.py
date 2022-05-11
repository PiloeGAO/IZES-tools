"""
    :package:   CopyMe
    :file:      main.py
    :brief:     File that open the UI in standalone mode.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import sys
from os import path

from PySide2 import QtWidgets, QtGui

if __package__ is None:
    print("Not executed in package.")
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    
from CopyMe.widgets.standalone_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Source: https://www.wenzhaodesign.com/techartblog/python-pyside2-simple-dark-theme
    # darktheme = QtGui.QPalette()
    # darktheme.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
    # darktheme.setColor(QtGui.QPalette.Base, QtGui.QColor(45, 45, 45))
    # darktheme.setColor(QtGui.QPalette.Background, QtGui.QColor(45, 45, 45))
    # darktheme.setColor(QtGui.QPalette.Foreground, QtGui.QColor(45, 45, 45))
    # darktheme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(222, 222, 222))
    # darktheme.setColor(QtGui.QPalette.Text, QtGui.QColor(222, 222, 222))
    # darktheme.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 45))
    # darktheme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(222, 222, 222))
    # darktheme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(222, 222, 222))
    # darktheme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(222, 222, 222))
    # darktheme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(45, 45, 45))
    # app.setPalette(darktheme)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 