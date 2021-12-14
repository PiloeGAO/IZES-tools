'''
    :package:   izes_tools
    :file:      shelf.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     Maya shelf (source: arnoldShelf.py [mtoa plugin]).
'''
import os

import maya.cmds as cmds
import maya

current_dir = os.path.dirname(os.path.realpath(__file__))

def remove_shelf():
   if cmds.shelfLayout('izes_tools', exists=True):
      cmds.deleteUI('izes_tools')

def create_shelf():
   remove_shelf()
   shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
   maya.mel.eval('global string $izes_toolsShelf;')
   maya_version = int(cmds.about(version=True))
   if maya_version < 2017:
      maya.mel.eval('$izes_toolsShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel izes_tools`;')   
   else:
      maya.mel.eval('$izes_toolsShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel -version \"2022\" izes_tools`;')

   shelfStyle = ('shelf' if maya_version >= 2016 else 'simple')

   cmds.shelfButton(
      label='Export Blendshapes',
      command='from izes_tools.dccs.maya.shelf_commands import export_blendshapes; export_blendshapes()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "massiveMultiplayer.png"),
      style='iconOnly'
   )
   
   cmds.separator(width=12,height=35, style=shelfStyle, hr=False)