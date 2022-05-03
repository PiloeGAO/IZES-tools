"""
    :package:   CopyMe
    :file:      main_widget.py
    :brief:     Maion widget for CopyMe.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
from PySide2 import QtWidgets

from CopyMe.core.project_folder import ProjectFolder

from CopyMe.widgets.auto_generated.main_widget import Ui_MainWidget

class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__()

        self.__project_folder = ProjectFolder()

        self.setupUi(self)

        self.setup_interactions()
    
    def setup_interactions(self):
        """Setup all interactions for the main widget.
        """
        self.inputFolderBrowseButton.clicked.connect(self.load_input_folder)
        self.outputFolderBrowseButton.clicked.connect(self.load_output_folder)

    def load_input_folder(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        dialog.setReadOnly(True)

        if (dialog.exec_()):
            directories = dialog.selectedFiles()
        
        if(directories == []):
            print("Select a directory please !")
        
        input_directory = directories[0]
        self.inputFolderPathLineEdit.setText(input_directory)
        self.__project_folder.input_folder = input_directory
    
    def load_output_folder(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        dialog.setReadOnly(True)

        if (dialog.exec_()):
            directories = dialog.selectedFiles()
        
        if(directories == []):
            print("Select a directory please !")
        
        output_directory = directories[0]
        self.outputFolderPathLineEdit.setText(output_directory)
        self.__project_folder.output_folder = output_directory