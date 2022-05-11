"""
    :package:   CopyMe
    :file:      project_folder.py
    :brief:     Main class for project_folder management.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from CopyMe.core.folder import Folder

class ProjectFolder(Folder):
    def __init__(self) -> None:
        super().__init__("")
        self.__input_folder = ""
        self.__output_folder = ""

        self.project_files = []

        self.__allow_export = False
    
    @property
    def input_folder(self):
        return self.__input_folder
    
    @input_folder.setter
    def input_folder(self, path):
        if('/' in path): path = path.replace('/', os.path.sep)

        self.__input_folder = path
        self.path = path

        if(os.path.isdir(self.__input_folder)):
            self.load_project_content()
    
    @property
    def output_folder(self):
        return self.__output_folder
    
    @output_folder.setter
    def output_folder(self, path):
        if('/' in path): path = path.replace('/', os.path.sep)

        self.__output_folder = path

        if(os.path.isdir(self.__output_folder)):
            self.__allow_export = True
    
    def load_project_content(self):
        """Scan the content of the selected project and register everything.
        """
        # Scan the directory and grab everything inside of it.
        self.load_content(recursive=True)

        self.project_files = self.grab_files(recursive=True)

        print(self.get_extensions())
    
    def get_extensions(self):
        """Get all the extensions that can be found in the project.

        Returns:
            list:'str': List of extensions.
        """
        extensions_dict = {}

        for extension in [file.extension for file in self.project_files]:
            if(extension in extensions_dict.keys()):
                extensions_dict[extension] = extensions_dict[extension] + 1
                continue

            extensions_dict[extension] = 1

        return {k: v for k, v in sorted(extensions_dict.items(), key=lambda item: item[1], reverse=True)}