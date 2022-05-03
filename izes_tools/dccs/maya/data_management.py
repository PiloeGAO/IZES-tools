'''
    :package:   izes_tools
    :file:      data_management.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     System to handle packing of production scene to a directory.
'''
import os
import shutil

from maya import cmds

def pack_scene():
    """This function start a packing routine to move all the references to a target directory
    """
    output_directory = cmds.fileDialog2(fileFilter="All Files (*.*)", fileMode=3, dialogStyle=1)[0]

    filepath = cmds.file(q=True, sn=True)
    maya_scene_name = os.path.basename(filepath)
    
    # Save maya file to the target directory.
    cmds.file(rename=os.path.join(output_directory, maya_scene_name))
    cmds.file(save=True, type="mayaAscii")

    # Build the folder that will store assets.
    assets_dir_path = os.path.join(output_directory, "assets")
    os.makedirs(assets_dir_path, exist_ok=True)

    for ref in cmds.ls(references=True):
        # Copy every references to asset's folder.
        print(f'Editing: {ref}')

        reference_path = cmds.referenceQuery(ref, filename=True) # This get the path from the reference.
        reference_file_name = os.path.basename(reference_path)

        shutil.copy(reference_path, assets_dir_path)
        new_path = os.path.join(assets_dir_path, reference_file_name)

        cmds.file(new_path, loadReference=ref) # This retarget the reference.