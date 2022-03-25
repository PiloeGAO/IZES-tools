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

   4. Select all the references and execute the :ref:`Rename namespaces for assets <maya_rename-assets>` script.

   5. Export the set dressing by selecting all the references and execute the "Export Selection" from the **SetDressTools**.

      - Please export it to **O:/shows/IZES/assets/environment/<assetName>/publishs/STD_A/v<versionNumber>/caches/STD_A_<assetName>_scene.v<versionNumber>.abc**

   6. Publishing the set dress **without the default cache geometry but with the previously exported set dressing file.**
   
   .. figure:: /images/pipeline_setdressing_assests_step0060.png
      :align: center
      :width: 700px
      :class: with-shadow

      Settings to use for publishing the set dress (same as rig)