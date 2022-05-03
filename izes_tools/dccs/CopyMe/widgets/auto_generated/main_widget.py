# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(1280, 720)
        self.verticalLayout = QVBoxLayout(MainWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.inputFolderLayout = QHBoxLayout()
        self.inputFolderLayout.setObjectName(u"inputFolderLayout")
        self.inputFolderLabel = QLabel(MainWidget)
        self.inputFolderLabel.setObjectName(u"inputFolderLabel")

        self.inputFolderLayout.addWidget(self.inputFolderLabel)

        self.inputFolderPathLineEdit = QLineEdit(MainWidget)
        self.inputFolderPathLineEdit.setObjectName(u"inputFolderPathLineEdit")
        self.inputFolderPathLineEdit.setReadOnly(True)

        self.inputFolderLayout.addWidget(self.inputFolderPathLineEdit)

        self.inputFolderBrowseButton = QPushButton(MainWidget)
        self.inputFolderBrowseButton.setObjectName(u"inputFolderBrowseButton")

        self.inputFolderLayout.addWidget(self.inputFolderBrowseButton)


        self.verticalLayout.addLayout(self.inputFolderLayout)

        self.exclusionLayout = QVBoxLayout()
        self.exclusionLayout.setObjectName(u"exclusionLayout")
        self.exclusionLayout.setContentsMargins(-1, 10, -1, -1)
        self.extensionsTable = QTableView(MainWidget)
        self.extensionsTable.setObjectName(u"extensionsTable")

        self.exclusionLayout.addWidget(self.extensionsTable)

        self.exclusionFolderLayout = QHBoxLayout()
        self.exclusionFolderLayout.setObjectName(u"exclusionFolderLayout")
        self.exclusionFolderLabel = QLabel(MainWidget)
        self.exclusionFolderLabel.setObjectName(u"exclusionFolderLabel")

        self.exclusionFolderLayout.addWidget(self.exclusionFolderLabel)

        self.exclusionFolderNameLineEdit = QLineEdit(MainWidget)
        self.exclusionFolderNameLineEdit.setObjectName(u"exclusionFolderNameLineEdit")

        self.exclusionFolderLayout.addWidget(self.exclusionFolderNameLineEdit)


        self.exclusionLayout.addLayout(self.exclusionFolderLayout)


        self.verticalLayout.addLayout(self.exclusionLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.outputFolderLayout = QHBoxLayout()
        self.outputFolderLayout.setObjectName(u"outputFolderLayout")
        self.outputFolderLabel = QLabel(MainWidget)
        self.outputFolderLabel.setObjectName(u"outputFolderLabel")

        self.outputFolderLayout.addWidget(self.outputFolderLabel)

        self.outputFolderPathLineEdit = QLineEdit(MainWidget)
        self.outputFolderPathLineEdit.setObjectName(u"outputFolderPathLineEdit")

        self.outputFolderLayout.addWidget(self.outputFolderPathLineEdit)

        self.outputFolderBrowseButton = QPushButton(MainWidget)
        self.outputFolderBrowseButton.setObjectName(u"outputFolderBrowseButton")

        self.outputFolderLayout.addWidget(self.outputFolderBrowseButton)


        self.verticalLayout.addLayout(self.outputFolderLayout)

        self.exportLine = QFrame(MainWidget)
        self.exportLine.setObjectName(u"exportLine")
        self.exportLine.setFrameShape(QFrame.HLine)
        self.exportLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.exportLine)

        self.exportLayout = QHBoxLayout()
        self.exportLayout.setObjectName(u"exportLayout")
        self.exportProgressBar = QProgressBar(MainWidget)
        self.exportProgressBar.setObjectName(u"exportProgressBar")

        self.exportLayout.addWidget(self.exportProgressBar)

        self.exportButton = QPushButton(MainWidget)
        self.exportButton.setObjectName(u"exportButton")

        self.exportLayout.addWidget(self.exportButton)


        self.verticalLayout.addLayout(self.exportLayout)


        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Form", None))
        self.inputFolderLabel.setText(QCoreApplication.translate("MainWidget", u"Project Folder:", None))
        self.inputFolderBrowseButton.setText(QCoreApplication.translate("MainWidget", u"Browse", None))
        self.exclusionFolderLabel.setText(QCoreApplication.translate("MainWidget", u"Exclusion Filter (need to be separated with \",\"):", None))
        self.outputFolderLabel.setText(QCoreApplication.translate("MainWidget", u"Output path:", None))
        self.outputFolderBrowseButton.setText(QCoreApplication.translate("MainWidget", u"Browse", None))
        self.exportButton.setText(QCoreApplication.translate("MainWidget", u"Export", None))
    # retranslateUi

