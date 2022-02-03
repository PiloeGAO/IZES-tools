'''
    :package:   izes_tools
    :file:      shelf_commands.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     List of all functions for izes_tools to be stored in the shelf.
'''
import os

from maya import cmds
import maya.mel as mel

global use_SGTK
try:
    import sgtk
    use_SGTK = True
except ImportError:
    print("SGTK not loaded, skipping auto functions.")
    use_SGTK = False

if(use_SGTK):
    current_engine = sgtk.platform.current_engine()
    current_context = current_engine.context

# Assets Tools

def createAssetStructure():
    """Create object base structure.
    Get object's name if sgtk is used.
    """
    object_name = "AssetName"

    if(use_SGTK):
        object_name = current_context.entity["name"]

    cmds.createNode("transform", name=object_name)
    cmds.createNode("transform", name="meshes_GRP", parent=object_name)
    cmds.createNode("transform", name="HI_GRP", parent="meshes_GRP")
    cmds.createNode("transform", name="MI_GRP", parent="meshes_GRP")
    cmds.createNode("transform", name="LO_GRP", parent="meshes_GRP")
    cmds.createNode("transform", name="Technical_GRP", parent="meshes_GRP")
    cmds.createNode("transform", name="Mosaic_Baked", parent="Technical_GRP")
    cmds.createNode("transform", name="Mosaic", parent="Technical_GRP")
    cmds.createNode("transform", name="rig_GRP", parent=object_name)
    cmds.createNode("transform", name="bones_GRP", parent=object_name)

def export_blendshapes():
    """Export blendshapes to a selected directory.
    """
    outputDirectory = cmds.fileDialog2(fileFilter="All Files (*.*)", fileMode=3, dialogStyle=1)[0]

    selection = cmds.ls(sl=True)

    for item in selection:
        cmds.select(clear=True)
        cmds.select(item)
        
        mel_cmd = 'AbcExport -j "-frameRange 1 1 -writeVisibility -dataFormat ogawa -root {} -file {}"'.format(item, outputDirectory + "/" + item.replace("|", "") + ".abc")
        mel.eval(mel_cmd)

# Animation Tools
def setupShot():
    """Setup the shot with framerate, framerange, auto import assets.
    """
    # Set main values for timeline setup.
    # Correct order is:
    # |-----------------------------------------------------------------------|
    # | startFrame | startAnimationFrame ======> endAnimationFrame | endFrame |
    # |-----------------------------------------------------------------------|
    preRoll             = 48
    startAnimationFrame = 1000
    endAnimationFrame   = 1240
    postRoll            = 0

    if(use_SGTK):
        # TODO: Get framerange from fields.
        startAnimationFrame = 1000
        endAnimationFrame   = 1240

    # Set timeline datas.
    cmds.currentUnit( time='%sfps' % int(24)) # WARNING: Framerate must be setup before timeline !

    cmds.playbackOptions(animationStartTime=(startAnimationFrame-preRoll), minTime=startAnimationFrame,
                        animationEndTime=(endAnimationFrame+postRoll),      maxTime=endAnimationFrame,
                        playbackSpeed=1.0)

    # Create timeline bookmarks (for visual feedback).
    # "timeSliderBookmark.mll" need to be loaded first.
    cmds.loadPlugin("timeSliderBookmark.mll", quiet=True)
    from maya.plugin.timeSliderBookmark.timeSliderBookmark import createBookmark

    createBookmark(name="PREROLL",  start=(startAnimationFrame-preRoll),            stop=(startAnimationFrame-1), color=(0.67, 0.23, 0.23))
    createBookmark(name="ANIM",     start=startAnimationFrame,   stop=endAnimationFrame,       color=(0.28, 0.69, 0.48))
    # createBookmark(name="POSTROLL", start=(endAnimationFrame+1), stop=(endAnimationFrame+postRoll),                color=(0.67, 0.23, 0.23))

    del createBookmark

    # Setting up render settings in the scene.
    width, height = (1920, 1080)
    cmds.setAttr("defaultResolution.width", width)
    cmds.setAttr("defaultResolution.height", height)

    if(use_SGTK):
        # TODO: Import reference from the breakdwon.
        pass