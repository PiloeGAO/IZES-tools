.. _maya_modeling_tools:

############
  Modeling  
############

List of all custom tools for modeling.

.. _maya_build-asset-structure:

Build Asset Structure
---------------------

.. figure:: /images/maya_asset-structure_icon.png
   :align: left
   :width: 32px

This tool build the correct group struture for an asset:

* *Asset Name*
    * meshes_GRP
        * HI_GRP
        * MI_GRP
        * LO_GRP
        * Technical_GRP
            * Mosaic_Baked
            * Mosaic
    * rig_GRP
    * bones_GRP

.. _maya_props-auto-rig-tool:

Props Auto Rig Tool
-------------------

.. figure:: /images/maya_porps-auto-rig_icon.png
   :align: left
   :width: 32px

This tool generate rigs for props (needed for the set dressing).

Usage
=====

1. Open the *Rig* task for the *Asset*.
2. Click on the button.
    The script will automaticly load the UV step and create the rig.
    Note: The UV step need to be set to *approved* to allow the rigging.
3. Publish the rig as usual.

.. _maya_upgrade-setdressing:

Props Auto Rig Tool
-------------------

.. figure:: /images/maya_upgrade-setdressing_icon.png
   :align: left
   :width: 32px

This tool upgrade the selected references from UV Task to Rig Task by keeping the transforms.

*All objects need to be at the root of the scene (nothing in groups).*

Usage
=====

1. Select all the references you want to convert (objects with the blue icon in the outliner).
2. Click on the button.
3. Check the console for failed imports.
