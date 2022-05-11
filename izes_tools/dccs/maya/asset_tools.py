'''
    :package:   izes_tools
    :file:      asset_tools.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     List of all functions for the asset management and editing.
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

def upgrade_setdressing():
    """Upgrade the selected reference to use the Rig task instead of the UV task.
    """
    selection = cmds.ls(sl=True)

    not_updatable = 0

    for sel in selection:
        # Get the asset datas from previous ref.
        reference_path_raw = cmds.referenceQuery(sel, filename=True)
        if("{" in reference_path_raw): reference_path = reference_path_raw.split("{")[0]
        else: reference_path = reference_path_raw
        
        # Get all the nodes from the original ref.
        sub_nodes = cmds.referenceQuery(sel, nodes=True)

        if(sub_nodes == None):
            print(f"Failed to get the reference node {sel}")
            continue
        
        # Get the object matrix of the original ref.
        ref_object_matrix = cmds.xform(f"|{sub_nodes[0]}", m=True, q=True)
        if(ref_object_matrix == [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]):
            print(f"Failed to get the position {sel}")
            not_updatable += 1
            continue
        
        # Get SGTK fields.
        ref_fields = tk.templates["asset_alembic_cache"].get_fields(reference_path)
        
        # Find the Rig task
        fields = ["id", "sg_status_list"]

        filters = [
            ['project', 'is', {'type': 'Project', 'id': current_context.project["id"]}],
            ["entity.Asset.code", "is", ref_fields["Asset"]],
            ["step.Step.code", "is", "Rig"]
        ]

        rig_step = shotgun_instance.find("Task", filters, fields)
        
        if(len(rig_step) == 0):
            print(f"No rig task for asset: {ref_fields['Asset']}")
            not_updatable += 1
            continue
        
        rig_step = rig_step[0]
        if(rig_step["sg_status_list"] != "apr"):
            print(f"Skipping Asset {ref_fields['Asset']} because task not approved.")
            not_updatable += 1
            continue
        
        # Get the last publish for the Rig step.
        fields = ["id", "version_number", "name", "published_file_type", "path_cache"]
        filters = [
            ['project', 'is', {'type': 'Project', 'id': current_context.project["id"]}],
            ["entity.Asset.code", "is", ref_fields["Asset"]],
            ["task.Task.id", "is", rig_step["id"]]
        ]

        publishs = shotgun_instance.find("PublishedFile", filters, fields)
        
        ma_publishes = [publish for publish in publishs if publish["published_file_type"]["name"] == "Maya Scene"]
        ma_publishes_sorted = sorted(ma_publishes, key=lambda publish: publish["version_number"], reverse=True)

        if(len(ma_publishes_sorted) == 0):
            print(f"No Rig publish for {ref_fields['Asset']}")
            not_updatable += 1
            continue
        
        last_ma_publish = ma_publishes_sorted[0]

        path_to_ma = os.path.join("O:/", "shows", last_ma_publish["path_cache"]).replace("\\", "/")

        if(os.path.isfile(path_to_ma) == False):
            print(f"Published file not found on disk: {path_to_ma}")
            not_updatable += 1
            continue
            
        # Import reference for current selection.
        rig_reference_import_path = cmds.file(path_to_ma, r=True, ns=f"{ref_fields['Asset']}_{last_ma_publish['name']}")
        rig_reference_namespace = cmds.referenceQuery(rig_reference_import_path, namespace=True)

        # Move the rig object.
        cmds.xform(f"{rig_reference_namespace}:main_SRT_local", matrix=ref_object_matrix)
        
        # Remove old reference.
        cmds.file(reference_path_raw, removeReference=True)

    # Print stats.
    print(f"{len(selection) - not_updatable}/{len(selection)}")

def rename_assets():
    """ Rename the selection to set the asset name and the instance number in the namespace.
    """
    already_fixed = []

    for sel in cmds.ls(sl=True):
        rig_path = cmds.referenceQuery(sel, filename=True)
        asset_name = rig_path.split("/")[5]
        
        instance_number = 1
        new_name = f"{asset_name}_{str(instance_number).zfill(3)}"
        
        while new_name in already_fixed:
            instance_number += 1
            new_name = f"{asset_name}_{str(instance_number).zfill(3)}"
        
        already_fixed.append(new_name)
        
        current_namespace = f":{sel.split(':')[0]}"

        print(f"Working on {current_namespace}")

        if(cmds.namespace(exists=new_name)):
            # This is needed in case of existing namespace.
            cmds.namespace(rename=[current_namespace, "temp"])
            current_namespace = "temp"

        cmds.namespace(rename=[current_namespace, new_name])
    
    print("DONE")