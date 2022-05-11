"""
    :package:   CopyMe
    :file:      folder.py
    :brief:     Main class for folder management.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

from CopyMe.core.file import File

class Folder:
    def __init__(self, path) -> None:
        self.path = path
        self.sub_folders = []
        self.files = []
    
    def load_content(self, recursive=False):
        """Load the content of the directory inside of the class.

        Args:
            recursive (bool, optional): Is the operation is done on new folders found during scan. Defaults to False.
        """
        for element in os.listdir(self.path):
            element_path = os.path.join(self.path, element)

            if(os.path.isfile(element_path)):
                self.files.append(File(element_path))
                continue
            
            elif(recursive is True):
                sub_folder = Folder(element_path)
                sub_folder.load_content(recursive=True)
                self.sub_folders.append(sub_folder)
                continue
            
            print(f'Unknow element: {element}')
    
    def grab_files(self, recursive=False):
        """Get the list of all the files stored in the current folder.

        Args:
            recursive (bool, optional): Is the operation is repeated in nested folders. Defaults to False.

        Returns:
            list:`CopyMe.core.File`: List of grabbed files.
        """
        grabbed_files = self.files

        if(recursive):
            for folder in self.sub_folders:
                grabbed_files.extend(
                    folder.grab_files(recursive=True)
                )
        
        return grabbed_files