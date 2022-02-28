############
  Modeling  
############

List of all custom tools for modeling.

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