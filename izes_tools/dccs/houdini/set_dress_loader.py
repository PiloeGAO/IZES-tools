'''
    :package:   izes_tools
    :file:      set_dress_loader.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     System to manage static set dress loading.
'''
import os

import hou

class SetDressLoader:
    asset_folder_template = "<drive>:/shows/<project>/assets/<assetType>/<asset>/publishs/<step>"

    def __init__(self) -> None:
        pass

    ########################
    # Processing Functions #
    ########################
    def import_set_dress_cache(self, hou_node):
        """This function load the list of assets from the Alembic File to the hidden list.

        Args:
            hou_node (`class` : hou.Node): the current hda node.
        """
        # Find all the informations from the attributes and store them in the root node.
        setDressNode    = hou_node.node('IMPORT_SET_DRESS').node('OUT')
        setDressGeo     = setDressNode.geometry()
        
        points          = setDressGeo.points()
        
        hou_node.parm("assets").set(len(points))
        
        for point in setDressGeo.points():
            pointID         = point.number()
            assetName       = point.stringAttribValue('assetName')
            assetInstance   = point.intAttribValue('assetInstance')
            assetType       = point.stringAttribValue('assetType')
            assetStep       = hou_node.parm("assetStep%i" % pointID).evalAsString()
            
            hou_node.parm("assetType%i" % pointID).set(assetType)
            hou_node.parm("assetName%i" % pointID).set(assetName)
            hou_node.parm("assetInstance%i" % pointID).set("%03d" % assetInstance)

            assetPublishPath = self.asset_folder_template.replace('<drive>', 'O')
            assetPublishPath = assetPublishPath.replace('<project>', 'IZES')
            assetPublishPath = assetPublishPath.replace('<assetType>', assetType)
            assetPublishPath = assetPublishPath.replace('<asset>', assetName)
            assetPublishPath = assetPublishPath.replace('<step>', assetStep)

            versions    = self.get_asset_versions(assetPublishPath)
            lastVersion = self.get_last_version(versions)
            
            hou_node.parm("assetVersion%i" % pointID).set(lastVersion)
            
            assetPublishPath = "%s/v%s/caches" % (assetPublishPath, lastVersion)
            
            fileName = self.get_version_file(assetPublishPath)
            
            if(fileName is not None):
                assetPublishPath = "%s/%s" % (assetPublishPath, fileName)
                
            hou_node.parm("assetPath%i" % pointID).set(assetPublishPath)
        
        self.load_assets(hou_node)
    
    def get_asset_versions(self, publishPath):
        """ Get the list of available versions for the current publish path.
        """
        versionList = []
        
        if(os.path.exists(publishPath)):
            for folder in os.listdir(publishPath):
                if(folder[0] == 'v'):
                    versionList.append(folder.split('v')[1])
                    
        return versionList

    def get_last_version(self, versions):
        """ Get the last version number from the version list.
        """
        lastVersion = '000'
        
        for ver in versions:
            if(int(lastVersion) < int(ver)):
                lastVersion = ver

        return lastVersion
        
    def get_version_file(self, path):
        """ Get the version from the filepath.
        """
        if(os.path.exists(path)):
            files = os.listdir(path)
            if(len(files) > 0):
                return files[0]
                
        return None
    
    def load_assets(self, hou_node):
        """ Load all the assets from the UI.
        """
        asset_subnet_node = hou_node.node("ASSETS")

        for i in range(hou_node.parm('assets').eval()):
            assetName       = hou_node.parm('assetName%i' % i).evalAsString()
            assetInstance   = hou_node.parm('assetInstance%i' % i).evalAsString()
            
            assetPath       = hou_node.parm('assetPath%i' % i).evalAsString()
            
            nodeName        = "%s_%s" % (assetName, assetInstance)
                    
            if(asset_subnet_node.node(nodeName) is None):
                assetNode   = asset_subnet_node.createNode('staticDeformer', node_name=nodeName)
                assetNode.parm("alembicFile").set(hou_node.parm('assetPath%i' % i))
                assetNode.parm("setDressGeometry").set('../../IMPORT_SET_DRESS/OUT')
                assetNode.parm("assetInstance").set(hou_node.parm('assetInstance%i' % i))
                assetNode.parm("viewportlod").set(hou_node.parm('assetDisplay%i' % i))
                assetNode.parm("viewportlod2").set(hou_node.parm('assetDisplay%i' % i))
                
        asset_subnet_node.layoutChildren()
    
    def clear_assets(self, hou_node):
        """Clear all the generated assets.

        Args:
            hou_node (`class` : hou.Node): the current hda node.
        """
        for child in hou_node.node("ASSETS").children():
            child.destroy()