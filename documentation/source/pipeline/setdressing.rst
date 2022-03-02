.. _pipeline_setdressing-tasks:

######################
  Set Dressing Tasks  
######################

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Inputs
     - Outputs
   
   * - Rigs (.ma)
     - Set Dress (.ma)

Steps :
   1. Open the Environment in the *setDressing* state.

   2. Open the "Shotgun Load", and import all the rigs from props as **reference**.

   3. To place assets, move the "main_SRT_local", **not the reference**.

   4. Publishing the set dress **without** the cache geometry.
   
   .. figure:: /images/pipeline_rigging_props_step0030.png
      :align: center
      :width: 700px
      :class: with-shadow

      Settings to use for publishing the set dress (same as rig)