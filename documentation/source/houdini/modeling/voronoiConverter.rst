*****************
Voronoi Converter
*****************

.. figure:: /images/houdini_modeling_voronoi-converter_node.png
   :align: right
   :width: 255px

:Category:  Modeling
:Description: Create voronoi faces for a geometry.
:Version: 3.0.0
:Location: :menuselection:`IZES --> Modeling`
:File: modeling_procedural__voronoiConverter.hda
:Author: Leo Depoix (PiloeGAO)
:License: MIT

User Interface
==============
.. figure:: /images/houdini_modeling_voronoi-converter_ui.png
   :align: center
   :width: 526px

Attributes:
-----------

* Total Count: Number of faces to generate. [Default: 1000]

* Scatter Relax: Iteration step between points used to build the voronoi, use `0` to have non uniform faces. [Default: 0]

* Use Curvature: Use object curvature to scater more voronoi faces on area with high angles. [Default: On]

* Multiplier: Intensify the curvature influence. [Default: 500]

Node Inputs
===========
- Geometry To Convert

Node Outputs
============
- Voronoid Geometry