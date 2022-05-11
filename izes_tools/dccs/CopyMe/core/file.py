"""
    :package:   CopyMe
    :file:      file.py
    :brief:     Main class for file management.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os

class File:
    def __init__(self, path) -> None:
        self.path = path
        
        self.name = os.path.basename(path)
        self.extension = os.path.splitext(self.name)[1]

        self.__file_stat = os.stat(path)

        self.mode = self.__file_stat.st_mode
        self.size = self.__file_stat.st_size #in bytes