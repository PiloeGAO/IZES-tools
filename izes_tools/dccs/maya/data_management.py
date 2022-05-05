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


def export_character_animation():
    """Export selection to animation publish directory.
    """
    # Ask for Version.
    version = cmds.promptDialog(
        title='Export Animation',
        message='Enter Version:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )

    if version != 'OK':
        print("Export aborded.")
        return

    version_number = str(cmds.promptDialog(query=True, text=True))

    # Get shot datas from path.
    scene_path = cmds.file(q=True, sn=True)
    sequence = scene_path.split("/")[4]
    shot = scene_path.split("/")[5]

    in_frame = int(cmds.playbackOptions(query=True, animationStartTime=True))
    out_frame = int(cmds.playbackOptions(query=True, animationEndTime=True))

    # Export each elements.
    for i, elem in enumerate(cmds.ls(sl=True)):
        asset = elem.split(":")[0]
        instance = elem.split(":")[0].split("_")[-1]
        
        output_path = os.path.join(
            "O:\\shows",
            "IZES",
            "sequences",
            sequence,
            shot,
            "publishs",
            "ANM",
            f"v{version_number.zfill(3)}",
            "caches",
            f"ANM_{sequence}_{shot}_{asset}.v{version_number.zfill(3)}.abc"    
        )
        
        output_dir = os.path.dirname(output_path)
        
        if(os.path.isdir(output_dir) == False):
            os.makedirs(output_dir)
        
        # Export ABC
        output_path = output_path.replace("\\", "/")
        command = f'AbcExport2 -j "-frameRange {in_frame} {out_frame} -stripNamespaces -uvWrite -worldSpace -dataFormat ogawa -root |{elem} -file {output_path}";'
        # print(command)
        print(f"Exporting {i+1}/{len(cmds.ls(sl=True))}")
        mel.eval(command)

    print("Export DONE")

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