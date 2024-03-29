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
      command='from izes_tools.dccs.maya.asset_tools import createAssetStructure; createAssetStructure()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "BuildAssetStructure2.png"),
      style='iconOnly'
   )
   
   cmds.shelfButton(
      label='Build Props Rig',
      command='from izes_tools.dccs.maya.asset_tools import create_props_rig; create_props_rig()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "AutoBonesGen6.png"),
      style='iconOnly'
   )
   
   cmds.shelfButton(
      label='Upgrade SetDressing to Rigs',
      command='from izes_tools.dccs.maya.asset_tools import upgrade_setdressing; upgrade_setdressing()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "Convert3.png"),
      style='iconOnly'
   )
   
   cmds.shelfButton(
      label='Rename namespaces for assets',
      command='from izes_tools.dccs.maya.asset_tools import rename_assets; rename_assets()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "RenameAssets6.png"),
      style='iconOnly'
   )

   cmds.separator(width=12,height=35, style=shelfStyle, hr=False)

   # Animation Tools.
   cmds.shelfButton(
      label='Setup Shot',
      command='from izes_tools.dccs.maya.animation_tools import setupShot; setupShot()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "ShotSetup4.png"),
      style='iconOnly'
   )

   cmds.shelfButton(
      label='Attach Backpack to Joy',
      command='from izes_tools.dccs.maya.animation_tools import attach_backpack_to_joy; attach_backpack_to_joy()',
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

   cmds.separator(width=12,height=35, style=shelfStyle, hr=False)

   # Data Management Tools.
   cmds.shelfButton(
      label='Export Selection To Publish',
      command='from izes_tools.dccs.maya.data_management import export_character_animation2; export_character_animation2()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "ExportToAnimation7.png"),
      style='iconOnly'
   )

   cmds.shelfButton(
      label='Export Set Dressing To Publish',
      command='from izes_tools.dccs.maya.data_management import export_setdressing; export_setdressing()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "ExportToAnimation7.png"),
      style='iconOnly'
   )

   cmds.shelfButton(
      label='Pack Scene',
      command='from izes_tools.dccs.maya.data_management import pack_scene; pack_scene()',
      sourceType='python',
      annotation='',
      image=os.path.join(current_dir, "icons", "ShotSetup4.png"),
      style='iconOnly'
   )