# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'standalone_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from CopyMe.widgets.main_widget import MainWidget


class Ui_StandaloneWindow(object):
    def setupUi(self, StandaloneWindow):
        if not StandaloneWindow.objectName():
            StandaloneWindow.setObjectName(u"StandaloneWindow")
        StandaloneWindow.resize(800, 600)
        self.mainWidget = MainWidget(StandaloneWindow)
        self.mainWidget.setObjectName(u"mainWidget")
        StandaloneWindow.setCentralWidget(self.mainWidget)

        self.retranslateUi(StandaloneWindow)

        QMetaObject.connectSlotsByName(StandaloneWindow)
    # setupUi

    def retranslateUi(self, StandaloneWindow):
        StandaloneWindow.setWindowTitle(QCoreApplication.translate("StandaloneWindow", u"CopyMe", None))
    # retranslateUi

