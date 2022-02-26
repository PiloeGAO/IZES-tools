*****************
Transfert Texture
*****************

.. figure:: /images/houdini_modeling_transfert-texture_node.png
   :align: right
   :width: 255px

:Category:  Modeling
:Description: Copy textures from HP to mosaics (as attributes on primitives).
:Version: 1.0.0
:Location: :menuselection:`IZES --> Modeling`
:File: modeling_procedural__transfertTexture.hda
:Author: Leo Depoix (PiloeGAO)
:License: MIT

User Interface
==============
.. figure:: /images/houdini_modeling_transfert-texture_ui.png
   :align: center
   :width: 526px

Attributes:
-----------

* Diffuse Path: Path to the diffuse texture, create a `diffuse_color` attribute on primitives. [Default: ]

* Roughness Path: Path to the roughness texture, create a `roughness_color` attribute on primitives. [Default: ]

* Dirt Path: Path to the dirt texture, create a `dirt_color` attribute on primitives. [Default: ]

Node Inputs
===========
- LowPoly Geometry
- HighPoly Geometry

Node Outputs
============
- Geometry with attributes