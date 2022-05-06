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

    def build_ui(self, hou_node):
        """Function to generate spare parameters on the node.

        Args:
            hou_node (class: `houNode`): The node to edit.
        """
        # Get the interface template group.
        ptg = hou_node.parmTemplateGroup()
        
        # Add Export JSON Button.
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
    
    def clear_ui(self, hou_node):
        """Delete all the spare parameters on the node.

        Args:
            hou_node (class: `houNode`): The node to edit.
        """
        # Remove sparse parameters.
        hou_node.removeSpareParms()
    
    def reset_hda(self, hou_node):
        """Utility function that reset the HDA to it's default state on saving.

        Args:
            hou_node (class: `houNode`): The node to edit.
        """
        self.clear_ui(hou_node)
        self.remove_assets(hou_node)
        self.build_ui(hou_node)

    def remove_assets(self, hou_node):
        """Function to remove all the assets generated on shot loading.

        Args:
            hou_node (class: `houNode`): The node to edit.
        """
        assets_node = hou_node.node("ASSETS")

        for node in assets_node.children():
            if(node.name() in self.processing_nodes): continue
            node.destroy()