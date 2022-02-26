****************
Mosaic Converter
****************

.. figure:: /images/houdini_modeling_mosaic-converter_node.png
   :align: right
   :width: 255px

:Category:  Modeling
:Description: Create procedural mosaics from faces.
:Version: 4.0.0
:Location: :menuselection:`IZES --> Modeling`
:File: modeling_procedural__mosaicConverter.hda
:Author: Leo Depoix (PiloeGAO)
:License: MIT

User Interface
==============
.. figure:: /images/houdini_modeling_mosaic-converter_ui.png
   :align: center
   :width: 526px

Attributes:
-----------

* Margin: Distance use as joints. [Default: 0.0125]

* Extrude Distance: Thickness of the mosaics. [Default: 0.045]

* Extrude Range Multiplier: Multiplier value use to generate non uniform thickness between mosaics. [Default: 0.8 - 1.2]

* Bevel Size: Size of the bevel. [Default: 0.005]

* Add Backfaces: Add backfaces to mosaics. [Default: Off]

* Generate UVs: Generate UVs of the extruded mosaic, warning: this is performance heavy. [Default: On]


Node Inputs
===========
- Geometry

Node Outputs
============
- Mosaic Geometry