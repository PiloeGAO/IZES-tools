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
import maya.mel as mel

from setDressTools import SetDressTools

def export_setdressing(auto_output_path=True, use_selection=True):
    cmds.loadPlugin('AbcExport2')

    # Find the range of the shot.
    frame_range = (
        int(cmds.playbackOptions(query=True, animationStartTime=True)),
        int(cmds.playbackOptions(query=True, animationEndTime=True))
    )

    if(auto_output_path):
        # Get shot datas from path.
        scene_path = cmds.file(q=True, sn=True)
        sequence = scene_path.split("/")[4]
        shot = scene_path.split("/")[5]
        version = scene_path.split(".")[-2]
        version_number = int(version.replace("v", ""))

        output_path = os.path.join(
            "O:\\shows",
            "IZES",
            "sequences",
            sequence,
            shot,
            "publishs",
            "ANM",
            version,
            "caches"
        )

        output_path = output_path.replace("\\", "/")

    else:
        output_path = cmds.fileDialog2(fileMode=2, caption="Export Animated Set Dress")
        output_path = output_path[0]

        sequence = output_path.split("/")[4]
        shot = output_path.split("/")[5]
        version_number = int(output_path.split("/")[-1].replace("v", ""))
    
    objects_filter = []
    if(use_selection and len(cmds.ls(sl=True)) > 0):
        objects_filter = [object.split("|")[1] for object in cmds.ls(sl=True, long=True) if len(object.split("|")) == 2]
        print(f'Selected objects: {" - ".join(objects_filter)}')

    exporter = ShotExporter(output_path, frame_range, sequence, shot, version_number, objects_filter=objects_filter)

class ShotExporter:
    def __init__(self, output_path, frame_range, sequence, shot, version_number, objects_filter=[])->None:
        self.__output_path = output_path
        self.__frame_range = frame_range
        self.__sequence = sequence
        self.__shot = shot
        self.__version_number = version_number

        self.__objects_filter = objects_filter

        # Export Characters.
        self.export_characters()

        # Export Cameras.
        self.export_cameras()

        # Process the background
        self.__setdress_objects = self.find_objects_by_keyword_in_path("/assets/environment/")
        self.__setdress_objects = self.find_objects_by_keyword_in_path("/assets/Environment/")
        self.__setdress_objects.extend(self.find_objects_by_keyword_in_path("/assets/Prop/"))
        self.__setdress_objects.extend(self.find_objects_by_keyword_in_path("/assets/Props-Nature/"))
        
        self.__processed_setdress_objects = self.process_objects()

        full_animated_objects = [object_data["name"] for object_data in self.__processed_setdress_objects if object_data["animated"]]
        full_static_objects = [object_data["name"] for object_data in self.__processed_setdress_objects if not object_data["animated"]]

        full_objects = []
        full_objects.extend(full_animated_objects)
        full_objects.extend(full_static_objects)

        set_dress_names = set([object.split(":")[0] for object in full_objects if object.count(":") > 1])

        for set_dress_name in set_dress_names:
            # Exporting animated objects.
            print(f"Exporting animated setdress assets for {set_dress_name}.")
            animated_objects = [object for object in full_animated_objects if set_dress_name in object]
            self.export_deformed_to_disk(animated_objects, set_dress=True, set_dress_name=set_dress_name)

            # Exporting static objects.
            print(f"Exporting static setdress assets for {set_dress_name}.")
            static_objects = [object for object in full_static_objects if set_dress_name in object]
            output_path = f'{self.__output_path}/set_dressing/{set_dress_name}/ANM_{self.__sequence}_{self.__shot}_staticObjects.v{str(self.__version_number).zfill(3)}.abc'
            self.create_output_directory(output_path)
            sdt = SetDressTools()
            sdt.export(1001, 1001, output_path, objects=static_objects)
        
        print(f"Exporting animated objects not in  the set dress.")
        extend_pieces = [object for object in full_objects if object.split(":")[0] not in set_dress_names]
        self.export_deformed_to_disk(extend_pieces, set_dress=True, set_dress_name="")
        

    def process_objects(self):
        """This function inspect every objects to check if they need to be exported as transforms or as meshs.

        Returns:
            dict: List of objects with the corresponding namespace and the tag for animation.
        """
        obj_datas = []

        for obj in self.__setdress_objects:
            obj_namespace = ":".join(obj.split(":")[:-1])
            
            # Parse datas.
            datas = {
                "name" : obj,
                "obj_namespace" : obj_namespace,
                "animated": False
            }

            if(not cmds.objExists(f'{obj_namespace}:main_SRT_local')
            or not cmds.objExists(f'{obj_namespace}:main_SRT_global')):
                print(f'Invalid rig for: {obj_namespace}')
                continue

            # Get the list of the sub-controllers.
            controllers_to_check = ["main_SRT_global", "main_SRT_local"]
            controllers_extended = cmds.listRelatives(f'{obj_namespace}:main_SRT_local', children=True, allDescendents=True, type="transform")
            
            if(controllers_extended != None):
                controllers_extended = [obj.split(":")[-1] for obj in controllers_extended if "_CON" in obj]
                controllers_to_check.extend(controllers_extended)
            
            # Check if controllers for keys.
            for controller in controllers_to_check:
                keyframes = cmds.keyframe(f'{obj_namespace}:{controller}', time=self.__frame_range, query=True)

                if(keyframes != None):
                    # print(f'Object {controller} is keyed!')
                    datas["animated"] = True
                    break
            
            # Otherwise, check for rest pose on sub-controllers.
            if(datas["animated"] is False and controllers_extended != None):
                for sub_controller in controllers_extended:
                    if(cmds.getAttr(f'{obj_namespace}:{sub_controller}.matrix') != \
                    [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]):
                        # print(f'{sub_controller} moved.')
                        datas["animated"] = True
                        break
            
            obj_datas.append(datas)
        
        return obj_datas
    
    def export_characters(self):
        """Export every characters of the scene.
        """
        print("Exporting Characters: ")

        objects = self.find_objects_by_keyword_in_path("/assets/Character/")

        for i, character in enumerate(objects):
            asset = character.split(":")[character.count(":")-1]
            instance = character.split(":")[0].split("_")[-1]

            output_path = f'{self.__output_path}/ANM_{self.__sequence}_{self.__shot}_{asset}.v{str(self.__version_number).zfill(3)}.abc'
            self.create_output_directory(output_path)

            all_objs = cmds.listRelatives(character, allDescendents=True, fullPath=True, path=True, type="shape")
            to_export_objs = [
                obj.replace(f"|{obj.split('|')[-1]}", "") for obj in all_objs
                if not "rig_GRP" in obj
                and not "bones_GRP" in obj
                and not "blendShapes" in obj
            ]

            roots = "-root " + " -root ".join(to_export_objs)

            command = f'AbcExport2 -j "-frameRange {self.__frame_range[0]} {self.__frame_range[1]} -stripNamespaces -uvWrite -worldSpace -dataFormat ogawa {roots} -file {output_path}";'
            print(f"Exporting `{asset}`: {i+1}/{len(objects)}")
            mel.eval(command)

    def export_cameras(self):
        """Export every cameras of the scene.
        """
        camera_rigs = self.find_objects_by_keyword_in_path("/assets/Camera/")
        
        for i, rig in enumerate(camera_rigs):
            namespace = rig.split(":")[0]

            output_path = f'{self.__output_path}/ANM_{self.__sequence}_{self.__shot}_{namespace}.v{str(self.__version_number).zfill(3)}.abc'
            self.create_output_directory(output_path)

            to_export_camera = f"-root {namespace}:main_persp"

            command = f'AbcExport -j "-frameRange {self.__frame_range[0]} {self.__frame_range[1]} -stripNamespaces -uvWrite -worldSpace -dataFormat ogawa {to_export_camera} -file {output_path}";'
            print(f"Exporting `{rig}`: {i+1}/{len(camera_rigs)}")
            mel.eval(command)

    def export_deformed_to_disk(self, objects, set_dress=False, set_dress_name=""):
        """Utility function to export on disk deformed assets.

        Args:
            objects (list): List of objects root.
        """
        for i, elem in enumerate(objects):
            asset = elem.split(":")[elem.count(":")-1]
            instance = elem.split(":")[0].split("_")[-1]

            if(set_dress):
                if(set_dress_name == ""):
                    output_path = f'{self.__output_path}/set_dressing/ANM_{self.__sequence}_{self.__shot}_{asset}.v{str(self.__version_number).zfill(3)}.abc'
                else:
                    output_path = f'{self.__output_path}/set_dressing/{set_dress_name}/ANM_{self.__sequence}_{self.__shot}_{asset}.v{str(self.__version_number).zfill(3)}.abc'
            else:
                output_path = f'{self.__output_path}/ANM_{self.__sequence}_{self.__shot}_{asset}.v{str(self.__version_number).zfill(3)}.abc'
            
            self.create_output_directory(output_path)

            command = f'AbcExport2 -j "-frameRange {self.__frame_range[0]} {self.__frame_range[1]} -stripNamespaces -uvWrite -worldSpace -dataFormat ogawa -root |{elem} -file {output_path}";'
            print(f"Exporting `{asset}`: {i+1}/{len(objects)}")
            mel.eval(command)
    
    def find_objects_by_keyword_in_path(self, keyword):
        """Find every references with a keyword in their path.

        Args:
            keyword (str): Part to find in the path

        Returns:
            list: List of objects.
        """
        objects = []
        
        for ref in cmds.ls(references=True):
            reference_path = cmds.referenceQuery(ref, filename=True)
            
            if(not keyword in reference_path):
                continue
            
            nodes = cmds.referenceQuery(ref, nodes=True, showDagPath=True)
            if(len(nodes) > 0):
                if(self.__objects_filter != []):
                    if(nodes[0] in self.__objects_filter):
                        objects.append(nodes[0])
                else:
                    objects.append(nodes[0])
        
        return objects
    
    def create_output_directory(self, path):
        if(os.path.isdir(os.path.dirname(path)) == False):
            os.makedirs(os.path.dirname(path))
        
        return

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
        print(f"Exporting {asset} > {i+1}/{len(cmds.ls(sl=True))}")
        mel.eval(command)

    print("Export DONE")

def export_character_animation2():
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

        all_objs = cmds.listRelatives(elem, allDescendents=True, fullPath=True, path=True, type="shape")
        to_export_objs = [
            obj.replace(f"|{obj.split('|')[-1]}", "") for obj in all_objs
            if not "rig_GRP" in obj
            and not "bones_GRP" in obj
            and not "blendShapes" in obj
        ]

        roots = "-root " + " -root ".join(to_export_objs)

        command = f'AbcExport2 -j "-frameRange {in_frame} {out_frame} -stripNamespaces -uvWrite -worldSpace -dataFormat ogawa {roots} -file {output_path}";'
        # print(command)
        print(f"Exporting {asset} > {i+1}/{len(cmds.ls(sl=True))}")
        mel.eval(command)

    print("Export DONE")

def find_objects_by_keyword_in_path(keyword):
    """Find every references with a keyword in their path.

    Args:
        keyword (str): Part to find in the path

    Returns:
        list: List of objects.
    """
    objects = []
    
    for ref in cmds.ls(references=True):
        reference_path = cmds.referenceQuery(ref, filename=True)
        
        if(not keyword in reference_path):
            continue
        
        nodes = cmds.referenceQuery(ref, nodes=True, showDagPath=True)
        if(len(nodes) > 0):
            objects.append(nodes[0])
    
    return objects

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