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

        # Add environment parameter.
        environment = ["-----[Select]-----"]
        environment.extend(self.find_subdirectories("O:/shows/IZES/assets/environment"))
        production_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "environment",
            "Environment",
            environment,
            script_callback="hou.phm().importer.update_environment_versions_menu(kwargs['node'])",
            script_callback_language=hou.scriptLanguage.Python,
            join_with_next=True,
        ))

        # Add environmentVersions parameter.
        production_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "environmentVersions",
            "Shading Version",
            ["-----[Select]-----"],
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
        ))
        
        # Add animated version parameter.
        versions_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "setDressAnimatedVersions",
            "Animated SetDress",
            ["-----[Select]-----"],
        ))
        
        # Add animated version parameter.
        versions_settings_folder.addParmTemplate(hou.MenuParmTemplate(
            "setDressStaticVersions",
            "Static SetDress",
            ["-----[Select]-----"],
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

        for version_name in ["characterVersions", "setDressAnimatedVersions", "setDressStaticVersions"]:
            self.update_menu_list(hou_node, version_name, versions, reset_index=True)
            if(len(versions) > 0): hou_node.parm(version_name).set(1)

    def update_environment_versions_menu(self, hou_node) -> None:
        """Update the content of the environment shading versions dropdown.

        Args:
            hou_node (class: `hou.Node`): The node to edit.
        """
        environment = self.get_parm_value(hou_node, "environment")

        if(environment is "-----[Select]-----"): return
        
        versions = self.find_subdirectories(os.path.join("O:", "shows", "IZES", "assets", "environment", environment, "publishs", "SHD"))
        versions = [version for version in versions if version[0] == "v"]
        versions.reverse()

        self.update_menu_list(hou_node, "environmentVersions", versions, reset_index=True)
        if(len(versions) > 0): hou_node.parm("environmentVersions").set(1)

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

        environment = self.get_parm_value(hou_node, "environment")
        environment_shading_version = self.get_parm_value(hou_node, "environmentVersions")

        characters_version = self.get_parm_value(hou_node, "characterVersions")
        animated_setdress_version = self.get_parm_value(hou_node, "setDressAnimatedVersions")
        static_setdress_version = self.get_parm_value(hou_node, "setDressStaticVersions")

        all_settings = (
            sequence,
            shot,
            environment,
            environment_shading_version,
            characters_version,
            animated_setdress_version,
            static_setdress_version
        )

        if("-----[Select]-----" in all_settings):
            print("Can't open shot, due to invalid selection.")
            return
        
        print(all_settings, sep="\n")

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
            hou_node (`class` : hou.Node): HDA node.
            parm_name (str) : Name of the parameter.
        Returns:
            str: Value of the parameter.
        """
        value = hou_node.parm(parm_name).evalAsString()
        
        if("[select]" in value): return None
        return value

    def find_subdirectories(self, path) -> str:
        """Get the name of the folders for the given path.

        Args:
            path (str): Path to a directory.

        Returns:
            list: `str`: Name of the directories.
        """
        return [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder)) and folder[0] != "_"]