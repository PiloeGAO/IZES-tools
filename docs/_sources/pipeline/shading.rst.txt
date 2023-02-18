.. _pipeline_shading-tasks:

#################
  Shading Tasks  
#################

Environment :
-------------

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Inputs
     - Outputs
   
   * - STD_A (.abc)
     - Shader (.mtlx)

Steps :
   1. Create an **Import Set Dress** node.

      .. figure:: /images/pipeline_shading_enviro_step0010.png
         :align: center
         :width: 467px
         :class: with-shadow

   2. Set the "Set Dress File" to the publish of the set dress from maya.

      .. figure:: /images/pipeline_shading_enviro_step0020.png
         :align: center
         :width: 700px
         :class: with-shadow

   3. Click on **Import Set Dress** and check if the "Assets Settings" got populated by every assets from the set dress.

      .. figure:: /images/pipeline_shading_enviro_step0030.png
         :align: center
         :width: 700px
         :class: with-shadow

         Example of the list of asset inside of "Assets Settings".

   4. Unlock the digital asset (**but never save it after otherwise you will break all the scenes !**).

   5. Click on **Load Alembic**.

      .. figure:: /images/pipeline_shading_enviro_step0050.png
         :align: center
         :width: 700px
         :class: with-shadow

         The scene is now loaded as bounding box to take advantage of the deferred loading to the Render Engine.

   6. You can now create shaders inside of the "/mat" network and assigning them to every sub-objects inside of the "Import Set Dress" node.

      A shader was already created and can be downloaded here: :download:`base_mosaic_shader.mtlx <../_downloads/base_mosaic_shader.mtlx>`.
   
      .. figure:: /images/pipeline_shading_enviro_step0060.png
         :align: center
         :width: 700px
         :class: with-shadow

   7. Deplicate the base material and rename it with following pattern: *assetName_assetInstance*

   8. Enable the MaterialX export from the Arnold Render node.
      
      - Export path: O:/shows/IZES/assets/environment/<assetName>/publishs/SHD/v<versionNumber>/caches/SHD_<assetName>_scene.v<versionNumber>.mtlx
      - Look: <assetName>

      Then you need to "Render to Disk" the node.
      
      .. figure:: /images/pipeline_shading_enviro_step0080.png
         :align: center
         :width: 700px
         :class: with-shadow

   9. Remove shaders from the objects.

      .. figure:: /images/pipeline_shading_enviro_step0090.png
         :align: center
         :width: 700px
         :class: with-shadow

   10. Add a MaterialX node and connect it to the rendering node.

      .. figure:: /images/pipeline_shading_enviro_step0100.png
         :align: center
         :width: 700px
         :class: with-shadow
   
   11. Publish the scene and **add the MaterialX file at publish**.

Characters :
------------

Steps :
   **TO-DO**