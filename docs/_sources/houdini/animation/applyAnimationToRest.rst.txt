.. _houdini_apply-animation-to-rest:

***********************
Apply Animation To Rest
***********************

.. figure:: /images/houdini_animation_apply-animation-to-rest_node.png
   :align: right
   :width: 255px

:Category:  Animation
:Description: Deform a rest mesh from a animation cache.
:Version: 1.0.0
:Location: :menuselection:`IZES --> Deformer`
:File: animation_deformer__applyAnimationToRest.hda
:Author: Leo Depoix (PiloeGAO)
:License: MIT

User Interface
==============
.. figure:: /images/houdini_animation_apply-animation-to-rest_ui.png
   :align: center
   :width: 526px

Attributes:
-----------

* Blur Iterations: Number of iteration to apply on the blur to smooth animation [Default: 500]

IO
--
.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Inputs
     - Outputs
   
   * - Rest Geometry
     - Geometry
   
   * - Animated Geometry
     - 