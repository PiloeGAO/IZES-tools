.. _houdini_set-alembic-path:

****************
Set Alembic Path
****************

.. figure:: /images/houdini_export_set-alembic-path_node.png
   :align: right
   :width: 255px

:Category:  Export
:Description: Set the path attribute to the geometry.
:Version: 1.0.0
:Location: :menuselection:`IZES --> Pipeline`
:File: export_utils__set_alembic_path.hda
:Author: Leo Depoix (PiloeGAO)
:License: MIT

User Interface
==============
.. figure:: /images/houdini_export_set-alembic-path_ui.png
   :align: center
   :width: 526px

Attributes:
-----------

* Technical Type: Set the geometry inside of the sub-group.
    * Mosaic [Default]
    * Mosaic Baked

* Asset name: Name of the Asset (Can be get from shotgrid by clicking on the button "Get Attributes From SG") [Default: ]

* Object Name: Name of the geometry (usefull when multiple geometries need to be in the same group but with different name) [Default: obj]

IO
--
.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Inputs
     - Outputs
   
   * - Geometry
     - Geometry