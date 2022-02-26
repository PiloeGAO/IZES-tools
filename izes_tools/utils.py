'''
    :package:   izes_tools
    :file:      shelf_commands.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     List of all functions for izes_tools to be stored in the shelf.
'''
import os
import webbrowser

def open_documentation():
    """Opent the documentation inside of user browser.
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    documentation_index = os.path.join(project_root, "documentation", "build", "html", "index.html")
    webbrowser.open('file://' + documentation_index, new=2)
