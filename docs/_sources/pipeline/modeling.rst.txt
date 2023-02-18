.. _pipeline_modeling-tasks:

##################
  Modeling Tasks  
##################

All scenes part of the Modelings Steps need to have the proper hierarchy (please see :ref:`this page <maya_modeling_tools>` automated tools).

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Inputs
     - Outputs
   
   * - 
     - Modeling (.ma, .abc)

.. _pipeline_modeling-tasks_modeling:

Modeling
--------

In this task state, the artist must create the asset normaly like any realistic object.

.. figure:: /images/pipeline_modeling_modeling_example.png
   :align: center
   :width: 700px
   :class: with-shadow
   :alt: Image of a correctly modeled book.

   Exemple of a correctly modeled book.

.. _pipeline_modeling-tasks_retopo:

Retopo
------

The next step of the process is to convert the modeling to mosaics.

To do that, the previously published ABC from Modeling need to be imported inside of Houdini.

.. figure:: /images/pipeline_modeling_retopo_example.png
   :align: center
   :width: 700px
   :class: with-shadow
   :alt: Image of a usual nodegraph for retopology inside of houdini.

   Simple graph for converting a book to mosaics.

Steps:
   1. Importing the ABC inside of Houdini.
      Also you need to unpack and convert the mesh to allow editing.

   2. Make the graph to generate :ref:`mosaics <houdini_modeling_tools>` (Don't forget to use the *normal* node to set them on *Points* instead of *Vertices*).

   3. Don't forget to use the :ref:`Set Alembic Path <houdini_set-alembic-path>` node after doing modeling to keep the groups on export.

   .. figure:: /images/pipeline_modeling_retopo_set-alembic-path_ui.png
      :align: center
      :width: 487px
      :class: with-shadow
      :alt: Example of setup of the *set alembic path* node.

      Example of a setup to set the path inside of an alembic.

   4. Use the :ref:`Alembic To Publish <houdini_alembic-to-publish>` node to save the alembic in the appropriate publish directory (everything is setup by using SGTK).


.. _pipeline_modeling-tasks_uv:

UV
--

**This step is really important because the** :ref:`rigging <pipeline_rigging-tasks>` **departement need a structured hierarchy for automation.**

Steps:
   1. Create the structure by using the script provided [:ref:`this page <maya_build-asset-structure>`].
   2. Import the previous steps:

      * The modeling need to be stored in the *MI_GRP*.

      * The retopolo need to be stored in the folowing directories:

         * Mosaic_Baked --> For the actual pieces.
         * Mosaic --> Joints, important for shading.

   3. **REMOVE ALL THE NAMESPACES FROM THE SCENE.**