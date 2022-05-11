"""
    :package:   PickMe
    :file:      standalone_window.py
    :brief:     Standalone window for the tool (usefull for devevelopment).
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets

from CopyMe.widgets.auto_generated.standalone_window import Ui_StandaloneWindow

class MainWindow(QtWidgets.QMainWindow, Ui_StandaloneWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)