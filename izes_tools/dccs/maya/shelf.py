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

global use_studiolib
try:
   import studiolibrary
   use_studiolib = True
except ImportError:
   use_studiolib = False

current_dir = os.path.dirname(os.path.realpath(__file__))

def remove_shelf():
   if cmds.shelfLayout('IZES_Tools', exists=True):
      cmds.deleteUI('IZES_Tools')

def create_shelf():
   remove_shelf()
   shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
   maya.mel.eval('global string $izes_toolsShelf;')
   maya_version = int(cmds.about(version=True))
   if maya_version < 2017:
      maya.mel.eval('$izes_toolsShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel IZES_Tools`;')   
   else:
      maya.mel.eval('$izes_toolsShelf = `shelfLayout -cellWidth 32 -cellHeight 32 -p $gShelfTopLevel -version \"2022\" IZES_Tools`;')

   shelfStyle = ('shelf' if maya_version >= 2016 else 'simple')

   # Asset Tools.
   cmds.shelfButton(
      label='Build Asset Structure',
      command='from izes_tools.dccs.maya.shelf_commands import createAssetStructure; createAssetStructure()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "BuildAssetStructure2.png"),
      style='iconOnly'
   )
   
   cmds.shelfButton(
      label='Build Props Rig',
      command='from izes_tools.dccs.maya.shelf_commands import create_props_rig; create_props_rig()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "AutoBonesGen6.png"),
      style='iconOnly'
   )
   
   cmds.shelfButton(
      label='Upgrade SetDressing to Rigs',
      command='from izes_tools.dccs.maya.shelf_commands import upgrade_setdressing; upgrade_setdressing()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "Convert3.png"),
      style='iconOnly'
   )
   
   cmds.shelfButton(
      label='Rename namespaces for assets',
      command='from izes_tools.dccs.maya.shelf_commands import rename_assets; rename_assets()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "Convert3.png"),
      style='iconOnly'
   )

   cmds.separator(width=12,height=35, style=shelfStyle, hr=False)

   # Animation Tools.
   cmds.shelfButton(
      label='Setup Shot',
      command='from izes_tools.dccs.maya.shelf_commands import setupShot; setupShot()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "ShotSetup4.png"),
      style='iconOnly'
   )

   cmds.shelfButton(
      label='Attach Backpack to Joy',
      command='from izes_tools.dccs.maya.shelf_commands import attach_backpack_to_joy; attach_backpack_to_joy()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "AttachBackpackToJoy5.png"),
      style='iconOnly'
   )

   if(use_studiolib):
      cmds.shelfButton(
         label='Studio Library',
         command='import studiolibrary; studiolibrary.main()',
         sourceType='python',
         annotation='',
         image=os.path.join(current_dir, "icons", "studiolib_icon.png"),
         style='iconOnly'
      )