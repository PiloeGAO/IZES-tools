'''
    :package:   izes_tools
    :file:      data_management.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     System to manage data inside of the toolset.
'''
import os

import hou

class ShotImporter:
    processing_nodes = ["MTLX_DATABASE"]

    def __init__(self) -> None:
        pass

    def build_ui(self, hou_node) -> None:
        """Function to generate spare parameters on the node.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        # Get the interface template group.
        ptg = hou_node.parmTemplateGroup()
        
        # Add a folder to store the parameters for production.
        production_settings_folder = hou.FolderParmTemplate(
            "productionSettings",
            "Production Settings",
            folder_type=hou.folderType.Simple
        )

        # Add sequence parameter.
        sequences = ["-----[Select]-----"]
        sequences.extend(self.find_subdirectories("O:/shows/IZES/sequences"))
        production_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "sequences",
            "Sequences",
            sequences,
            script_callback="hou.phm().importer.update_shots_menu(kwargs['node'])",
            script_callback_language=hou.scriptLanguage.Python,
            join_with_next=True,
        ))

        # Add shot parameter.
        production_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "shots",
            "Shots",
            ["-----[Select]-----"],
            script_callback="hou.phm().importer.update_versions_menu(kwargs['node'])",
            script_callback_language=hou.scriptLanguage.Python,
        ))

        # Add production_settings_folder to template group.
        ptg.addParmTemplate(production_settings_folder)

        # Add a folder to store the parameters for versions.
        versions_settings_folder = hou.FolderParmTemplate(
            "versionsSettings",
            "Versions Settings",
            folder_type=hou.folderType.Simple
        )
        
        # Add characters version parameter.
        versions_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "characterVersions",
            "Characters",
            ["-----[Select]-----"],
            script_callback="hou.phm().importer.create_characters_nodes(kwargs['node'])",
            script_callback_language=hou.scriptLanguage.Python,
        ))
        
        # Add animated version parameter.
        versions_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "setDressExtendVersions",
            "Extended Props",
            ["-----[Select]-----"],
            script_callback="hou.phm().importer.create_props_nodes(kwargs['node'])",
            script_callback_language=hou.scriptLanguage.Python,
        ))
        
        # Add animated version parameter.
        versions_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "setDressVersions",
            "SetDress",
            ["-----[Select]-----"],
            script_callback="hou.phm().importer.create_setdress_nodes(kwargs['node'])",
            script_callback_language=hou.scriptLanguage.Python,
        ))

        # Add versions_settings_folder to template group.
        ptg.addParmTemplate(versions_settings_folder)

        # Add Import content Button.
        ptg.addParmTemplate(
            hou.ButtonParmTemplate(
                "importAssets",
                "Import Assets",
                script_callback="hou.phm().importer.import_assets(kwargs['node'])",
                script_callback_language=hou.scriptLanguage.Python
            )
        )

        # Add Clear content Button.
        ptg.addParmTemplate(
            hou.ButtonParmTemplate(
                "clearAssets",
                "Clear Assets",
                script_callback="hou.phm().importer.remove_assets(kwargs['node'])",
                script_callback_language=hou.scriptLanguage.Python
            )
        )

        # Update the node interface.
        hou_node.setParmTemplateGroup(ptg)
    
    def update_shots_menu(self, hou_node) -> None:
        """Update the content of the shots dropdown.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        sequence = self.get_parm_value(hou_node, "sequences")

        if(sequence is "-----[Select]-----"): return
        
        shots = self.find_subdirectories(os.path.join("O:", "shows", "IZES", "sequences", sequence))
        self.update_menu_list(hou_node, "shots", shots, reset_index=True)
        self.update_menu_list(hou_node, "versions", [], reset_index=True)
    
    def update_versions_menu(self, hou_node) -> None:
        """Update the content of the versions dropdown.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        sequence = self.get_parm_value(hou_node, "sequences")
        shot = self.get_parm_value(hou_node, "shots")

        if("-----[Select]-----" in [sequence, shot]): return
        
        versions = self.find_subdirectories(os.path.join("O:", "shows", "IZES", "sequences", sequence, shot, "publishs", "ANM"))
        versions = [version for version in versions if version[0] == "v"]
        versions.reverse()

        for version_name in ["characterVersions", "setDressExtendVersions", "setDressVersions"]:
            self.update_menu_list(hou_node, version_name, versions, reset_index=True)
            if(len(versions) > 0): hou_node.parm(version_name).set(1)

    def clear_ui(self, hou_node) -> None:
        """Delete all the spare parameters on the node.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        # Remove sparse parameters.
        hou_node.removeSpareParms()
    
    def reset_hda(self, hou_node) -> None:
        """Utility function that reset the HDA to it's default state on saving.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        self.clear_ui(hou_node)
        self.remove_assets(hou_node)
        self.remove_materialx(hou_node)
        self.build_ui(hou_node)

    def import_assets(self, hou_node) -> None:
        """Function to import all the assets generated on shot loading.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        sequence = self.get_parm_value(hou_node, "sequences")
        shot = self.get_parm_value(hou_node, "shots")

        characters_version = self.get_parm_value(hou_node, "characterVersions")
        props_version = self.get_parm_value(hou_node, "setDressExtendVersions")
        setdress_version = self.get_parm_value(hou_node, "setDressVersions")

        all_settings = (
            sequence,
            shot,
            characters_version,
            props_version,
            setdress_version
        )

        if("-----[Select]-----" in all_settings):
            print("Can't open shot, due to invalid selection.")
            return
        
        # Clean the node before generating the whole content.
        self.remove_assets(hou_node)
        self.remove_materialx(hou_node)
    
        # Import characters.
        self.create_characters_nodes(hou_node)

        # Import props.
        self.create_props_nodes(hou_node)

        # Import setdressing (static objects).
        self.create_setdress_nodes(hou_node)

    def create_characters_nodes(self, hou_node) -> None:
        """Get all the files for the characters and create the nodes.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        # Clear the previous characters nodes generated.
        self.remove_characters_nodes(hou_node)

        # Find the data to properly find the files.
        sequence = self.get_parm_value(hou_node, "sequences")
        shot = self.get_parm_value(hou_node, "shots")
        version = self.get_parm_value(hou_node, "characterVersions")

        # Get files to import.
        export_directory = os.path.join("O:", "shows", "IZES", "sequences", sequence, shot, "publishs", "ANM", version, "caches")
        files = [file for file in os.listdir(export_directory) if os.path.isfile(os.path.join(export_directory, file)) and ".abc" in file]

        deformers = [file for file in files if "deformer" in file]

        # Build objects.
        assets_node = hou_node.node("ASSETS")
        materials_node = assets_node.node("MTLX_DATABASE")
        for character in deformers:
            character_datas = character.split(".")[0]
            character_name = character_datas.split("_")[3]
            character_instance = f'{character_name}_{character_datas.split("_")[-1]}'

            # Create the actual geometry node.
            character_node = assets_node.createNode("geo", node_name=character_instance)
            abc_node = character_node.createNode("alembic", node_name="IN_CACHES")
            abc_node.parm("fileName").set(os.path.join(export_directory, character))

            self.add_asset_category(character_node, category_name="Character")

            # Create the materialx node and assign it.
            path_to_shading = os.path.join("O:\\", "shows", "IZES", "assets", "Character", character_name, "publishs", "SHD")
            last_version = [directory for directory in self.find_subdirectories(path_to_shading) if directory[0] == "v"][-1]
            materialx_path = os.path.join(path_to_shading, last_version, "caches", f'SHD_{character_name}.{last_version}.mtlx')

            material_node = materials_node.createNode("materialx", node_name=f'{character_instance}_mtlx')
            material_node.parm("selection").set("*")
            material_node.parm("filename").set(materialx_path)
            material_node.parm("look").set("default")
            character_node.parm("ar_operator_graph").set(character_node.relativePathTo(material_node))

            self.add_asset_category(material_node, category_name="Character")

    def remove_characters_nodes(self, hou_node) -> None:
        """Remove all the character generated nodes.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        self.remove_nodes_from_category(hou_node, category_name="Character")

    def create_props_nodes(self, hou_node) -> None:
        """Get all the files for the props and create the nodes.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        # Clear the previous props nodes generated.
        self.remove_props_nodes(hou_node)

        # Find the data to properly find the files.
        sequence = self.get_parm_value(hou_node, "sequences")
        shot = self.get_parm_value(hou_node, "shots")
        version = self.get_parm_value(hou_node, "setDressExtendVersions")

        # Get files to import.
        export_directory = os.path.join("O:\\", "shows", "IZES", "sequences", sequence, shot, "publishs", "ANM", version, "caches", "set_dressing")
        files = [file for file in self.recursive_file_search(export_directory)
            if not "deformer" in file and not "staticObjects" in file and ".abc" in file
        ]

        # Build objects.
        assets_node = hou_node.node("ASSETS")
        materials_node = assets_node.node("MTLX_DATABASE")
        for prop_file in files:
            # Getter prop datas (Name, Type...).
            prop = os.path.basename(prop_file)
            parent_setdress = "_".join(os.path.dirname(prop_file).split(os.sep)[-1].split("_")[:-1]) \
                if os.path.dirname(prop_file).split(os.sep)[-1] != "set_dressing" else ""

            prop_datas = prop.split(".")[0]

            prop_name = []
            prop_name.extend(prop_datas.split("_"))
            del prop_name[0:3]
            del prop_name[-1]
            prop_name = "_".join(prop_name)

            prop_type = self.get_asset_type(prop_name)

            prop_instance = f'{prop_name}_{prop_datas.split("_")[-1]}'
            prop_node = assets_node.createNode("propsDeformer", node_name=prop_instance)
            
            # Setup the deformer node.
            prop_node.parm("assetType").set(prop_type)
            prop_node.parm("assetName").set(prop_name)
            prop_node.parm("version").set(self.get_last_publish_version(prop_name, "MDL"))
            prop_node.parm("deformedCache").set(prop_file)

            if(not os.path.isfile(prop_node.node("save_cache").parm("filename").evalAsString())):
                # Compute the ABC only when not present on disk.
                prop_node.node("save_cache").parm("execute").pressButton()

            self.add_asset_category(prop_node, category_name="Prop")

            # Setup the material.
            if(parent_setdress != ""):
                path_to_shading = os.path.join("O:\\", "shows", "IZES", "assets", "environment", parent_setdress, "publishs", "SHD")
                last_version = [directory for directory in self.find_subdirectories(path_to_shading) if directory[0] == "v"]

                if(len(last_version) >= 1):
                    last_version = last_version[-1]
                    materialx_path = os.path.join(path_to_shading, last_version, f'{prop_instance}.mtlx')

                    material_node = materials_node.createNode("materialx", node_name=f'{prop_instance}_mtlx')
                    material_node.parm("selection").set("*")
                    material_node.parm("filename").set(materialx_path)
                    material_node.parm("look").set("default")
                    prop_node.parm("ar_operator_graph").set(prop_node.relativePathTo(material_node))

                    self.add_asset_category(material_node, category_name="Prop")

    def remove_props_nodes(self, hou_node) -> None:
        """Remove all the props generated nodes.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        self.remove_nodes_from_category(hou_node, category_name="Prop")

    def create_setdress_nodes(self, hou_node) -> None:
        """Get all the files for the setdressing and create the nodes.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        # Clear the previous props nodes generated.
        self.remove_setdress_nodes(hou_node)

        # Find the data to properly find the files.
        sequence = self.get_parm_value(hou_node, "sequences")
        shot = self.get_parm_value(hou_node, "shots")
        version = self.get_parm_value(hou_node, "setDressVersions")

        # Get files to import.
        export_directory = os.path.join("O:\\", "shows", "IZES", "sequences", sequence, shot, "publishs", "ANM", version, "caches", "set_dressing")

        # Build objects.
        assets_node = hou_node.node("ASSETS")
        materials_node = assets_node.node("MTLX_DATABASE")

        for set_dress in self.find_subdirectories(export_directory):
            set_dress_name = "_".join(set_dress.split("_")[:-1])
            static_file = os.path.join(export_directory, set_dress, f'ANM_{sequence}_{shot}_staticObjects.{version}.abc')
            
            set_dress_node = assets_node.createNode("setDressing", node_name=set_dress)
            set_dress_node.parm("cacheFile").set(static_file)
            set_dress_node.parm("importButton").pressButton()

            self.add_asset_category(set_dress_node, category_name="SetDressing")

            # Managing materialx import.
            path_to_shading = os.path.join("O:\\", "shows", "IZES", "assets", "environment", set_dress_name, "publishs", "SHD")
            last_version = [directory for directory in self.find_subdirectories(path_to_shading) if directory[0] == "v"]

            if(len(last_version) >= 1):
                last_version = last_version[-1]

                for asset_node in set_dress_node.node("ASSETS").children():
                    assets_name = asset_node.name()

                    materialx_path = os.path.join(path_to_shading, last_version, f'{assets_name}.mtlx')

                    material_node = materials_node.createNode("materialx", node_name=f'{assets_name}_mtlx')
                    material_node.parm("selection").set("*")
                    material_node.parm("filename").set(materialx_path)
                    material_node.parm("look").set("default")
                    asset_node.parm("ar_operator_graph").set(asset_node.relativePathTo(material_node))

                    self.add_asset_category(material_node, category_name="SetDressing")
            
    def remove_setdress_nodes(self, hou_node) -> None:
        """Remove all the setdressing generated nodes.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        self.remove_nodes_from_category(hou_node, category_name="SetDressing")

    def remove_assets(self, hou_node) -> None:
        """Function to remove all the assets generated on shot loading.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        assets_node = hou_node.node("ASSETS")

        for node in assets_node.children():
            if(node.name() in self.processing_nodes): continue
            node.destroy()
    
    def remove_materialx(self, hou_node) -> None:
        """Function to remove all the materialx generated on shot loading.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        materialx_node = hou_node.node("ASSETS").node("MTLX_DATABASE")

        for node in materialx_node.children():
            if(node.name() in self.processing_nodes): continue
            node.destroy()
    
    def add_asset_category(self, hou_node, category_name="") -> None:
        """Add a spare parameter to the node and set the category name.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
            category_name (str, optional): Name of the category tag to create. Defaults to "".
        """
        if(not "assetCategory" in self.get_parm_names(hou_node)):
            # Get the interface template group.
            ptg = hou_node.parmTemplateGroup()

            # Add category field.
            ptg.addParmTemplate(
                hou.StringParmTemplate (
                    "assetCategory",
                    "Category",
                    1,
                    is_hidden=True,
                )
            )

            # Update the node interface.
            hou_node.setParmTemplateGroup(ptg)

        hou_node.parm("assetCategory").set(category_name)

    def remove_nodes_from_category(self, hou_node, category_name=""):
        """Remove all the nodes with the given category tag.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
            category_name (str, optional): Name of the category tag to find. Defaults to "".
        """
        for node in hou_node.children():
            if("assetCategory" in self.get_parm_names(node)):
                if(node.parm("assetCategory").evalAsString() == category_name):
                    node.destroy()
                    continue

            self.remove_nodes_from_category(node, category_name=category_name)

    def update_menu_list(self, hou_node, menu_name, items, reset_index=False) -> None:
        """Update menu parameter list inside of the HDA interface.
        Args:
            hou_node (`class` : hou.Node): HDA node.
            menu_name (str): The name of the menu parm.
            items (list): Items to update.
        """
        # Get the interface template group.
        ptg = hou_node.parmTemplateGroup()

        # Find the menu from name.
        menu = ptg.find(menu_name)

        # Check if the menu exist.
        if(menu is None):
            return
        
        menu_list = []
        menu_list.extend(items)

        # Update menu items.
        menu_list.insert(0, "-----[Select]-----")

        menu.setMenuItems(menu_list)
        menu.setMenuLabels(menu_list)

        # Replace the menu instance with the new one.
        ptg.replace(menu_name, menu)
        hou_node.setParmTemplateGroup(ptg)

        # Reset index.
        if(reset_index):
            hou_node.parm(menu_name).set(0)

    def get_parm_value(self, hou_node, parm_name) -> str:
        """ Update the selected sequence.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
            parm_name (str) : Name of the parameter.
        Returns:
            str: Value of the parameter.
        """
        if(not parm_name in self.get_parm_names(hou_node)):
            raise RuntimeError(f'Parameter "{parm_name}" don\'t exist on "{hou_node}"')
            return None

        value = hou_node.parm(parm_name).evalAsString()
        
        if("[select]" in value): return None
        return value

    def get_parm_names(self, hou_node) -> list:
        """Return a list of parm names for the node. 

        Args:
            hou_node (class: `hou.Node`): The node to edit.

        Returns:
            list: List of parm name.
        """
        return [parm.name() for parm in hou_node.parms()]

    def get_asset_type(self, name):
        """Get the type of an asset from his name.

        Args:
            name (str): Name fo the asset.

        Returns:
            str: Type of the asset.
        """
        for types_folder in self.find_subdirectories("O:\\shows\\IZES\\assets"):
            for asset_folder in  self.find_subdirectories(os.path.join("O:\\shows\\IZES\\assets", types_folder)):
                if(asset_folder == name):
                    return types_folder
        
        return None

    def get_last_publish_version(self, name, task_type):
        """Functio to get the last publish version for a given task.

        Args:
            name (str): Name fo the asset.

        Returns:
            int: Version number.
        """
        version = 1

        cache_directory = os.path.join(
            "O:\\",
            "shows",
            "IZES",
            "assets",
            self.get_asset_type(name),
            name,
            "publishs",
            task_type
        )

        last_version_dir = [folder for folder in os.listdir(cache_directory)
            if os.path.isdir(os.path.join(cache_directory, folder)) and folder[0] == "v"
        ]

        if(len(last_version_dir) != 0): version = int(last_version_dir[-1][1:])

        return version

    def find_subdirectories(self, path) -> str:
        """Get the name of the folders for the given path.

        Args:
            path (str): Path to a directory.

        Returns:
            list: `str`: Name of the directories.
        """
        return [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder)) and folder[0] != "_"]
    
    def recursive_file_search(self, path):
        """Find all the files in a directory and it's subdirectories.

        Args:
            path (str): Path to a directory.

        Returns:
            list: `str`: File's paths.
        """
        files = []

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if(os.path.isfile(item_path)):
                files.append(item_path)
                continue

            files.extend(self.recursive_file_search(item_path))

        return files