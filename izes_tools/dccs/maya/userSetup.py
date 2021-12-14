'''
    :package:   izes_tools
    :file:      userSetup.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     Autodesk Maya user setup script.
'''
from maya import cmds

def init_plugin():
    print("Loading IZES-Tools")

    # Loading the UI.
    from izes_tools.dccs.maya import shelf
    shelf.create_shelf()

# Delay execution on UI startup
cmds.evalDeferred(init_plugin)