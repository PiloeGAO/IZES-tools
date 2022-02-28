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

from frankenstein import RigUtils
rig_utils = RigUtils()

from ldRigNodes.space_switch_manager import SpaceSwitchManager, SpaceSwitchType

global use_SGTK
try:
    import sgtk
    use_SGTK = True
except ImportError:
    print("SGTK not loaded, skipping auto functions.")
    use_SGTK = False

if(use_SGTK):
    current_engine = sgtk.platform.current_engine()
    tk = current_engine.sgtk
    current_context = current_engine.context
    shotgun_instance = current_engine.shotgun


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

def create_props_rig():
    """Create a simple rig for a props.
    """
    if(not use_SGTK): return

    entity = current_context.entity
    task = current_context.task
    step = current_context.step
    
    asset_name = entity["name"]

    if(asset_name in cmds.ls()):
        cmds.delete(asset_name)

    if(step["name"] != "Rig"):
        raise RuntimeError("Incorrect Step.")
    
    # Find the UV task
    fields = ["id", "sg_status_list"]

    filters = [
        ['project', 'is', {'type': 'Project', 'id': current_context.project["id"]}],
        ["entity.Asset.id", "is", current_context.entity["id"]],
        ["step.Step.code", "is", "uv"]
    ]

    uv_step = shotgun_instance.find("Task", filters, fields)

    if(len(uv_step) != 1):
        raise ValueError("No UV task for asset.")

    uv_step = uv_step[0]
    if(uv_step["sg_status_list"] != "apr"):
        raise RuntimeError("Status invalid, UV must be approved to allow rigging.")
    
    # Get the last publish for the UV step.
    fields = ["id", "version_number", "published_file_type", "path_cache"]
    filters = [
        ['project', 'is', {'type': 'Project', 'id': current_context.project["id"]}],
        ["entity.Asset.id", "is", current_context.entity["id"]],
        ["task.Task.id", "is", uv_step["id"]]
    ]

    publishs = shotgun_instance.find("PublishedFile", filters, fields)

    abc_publishes = [publish for publish in publishs if publish["published_file_type"]["name"] == "Alembic Cache"]
    abc_publishes_sorted = sorted(abc_publishes, key=lambda publish: publish["version_number"], reverse=True)

    if(len(abc_publishes_sorted) == 0):
        raise RuntimeError("No ABC publish for asset.")

    last_abc_publish = abc_publishes_sorted[0]

    path_to_abc = os.path.join("O:/", "shows", last_abc_publish["path_cache"]).replace("\\", "/")

    if(os.path.isfile(path_to_abc) == False):
        raise FileNotFoundError(f"Published file not found on disk: {path_to_abc}")
    
    # Import UV ABC into the scene.
    command = f"AbcImport -mode import -debug \"{path_to_abc}\""
    mel.eval(command)

    # Creating the rig.
    if("main_module" in cmds.ls()):
        cmds.delete("main_module")

    cmds.namespace(add="main")
    cmds.namespace(set=":main")
    rig_utils.createRigModule()

    cmds.select(clear=True)
    global_con = rig_utils.createRigController(5)
    global_con.name = "SRT_global"
    cmds.parent(global_con.name, f"main:controllers_GRP")
    cmds.select(clear=True)
    local_con = rig_utils.createRigController(8)
    local_con.name = "SRT_local"
    cmds.parent(local_con.name, f"main:SRT_global")
    cmds.select(clear=True)

    cmds.parent("main:module", f"rig_GRP")

    cmds.namespace(set=":")
    namespace_list = cmds.namespaceInfo("main", ls=True)
    if(type(namespace_list) == None): raise RuntimeError()

    for obj in namespace_list:
        try: cmds.rename(obj, obj.replace(':', '_'))
        except: pass

    try: cmds.namespace(rm="main")
    except: pass

    obj_to_parent = ["|".join(obj.split("|")[:-1]) for obj in cmds.ls(dagObjects=True, type=['mesh'], long=True) if f"{asset_name}|meshes_GRP" in obj]
    for mesh in obj_to_parent:
        spaceSwitchtools = SpaceSwitchManager(nodeName=mesh)
        spaceSwitchtools.delete_space_switch() # This is not necessary but good to have to avoid strange errors.
        spaceSwitchtools.add_space("main_SRT_local", SpaceSwitchType.SRT)

    # Done !

# Animation Tools
def setupShot():
    """Setup the shot with framerate, framerange, auto import assets.
    """
    if(not use_SGTK): return

    # Getting datas from Shotgrid.use_SGTKshotgun_instance = current_engine.shotgun
    fields = ['id', 'code', 'sequence', 'sg_cut_in', 'sg_cut_out', 'sg_frames', 'assets']

    filters = [
        ['project', 'is', {'type': 'Project', 'id': current_engine.context.project["id"]}],
        ["id", "is", current_engine.context.entity["id"]]
    ]

    sg_datas = shotgun_instance.find_one("Shot", filters, fields)

    if(None in sg_datas):
        print("Invalid datas from Shotgrid, skipping.")
        return

    # Set main values for timeline setup.
    # Correct order is:
    # |-----------------------------------------------------------------------|
    # | startFrame | startAnimationFrame ======> endAnimationFrame | endFrame |
    # |-----------------------------------------------------------------------|
    preRoll             = 48
    startAnimationFrame = int(sg_datas["sg_cut_in"])
    endAnimationFrame   = int(sg_datas["sg_cut_out"])
    postRoll            = 48

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
    createBookmark(name="POSTROLL", start=(endAnimationFrame+1), stop=(endAnimationFrame+postRoll),                color=(0.67, 0.23, 0.23))

    del createBookmark

    # Setting up render settings in the scene.
    width, height = (1920, 1080)
    cmds.setAttr("defaultResolution.width", width)
    cmds.setAttr("defaultResolution.height", height)

    # Import References.