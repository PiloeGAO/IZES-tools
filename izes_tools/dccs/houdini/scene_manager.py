import hou

OBJ_NET = hou.node("/obj")

def build_scene_from_outs():
    """Build the scene from a selection of multiple null object
    """
    selection = hou.selectedNodes()
    if(len(selection) == 0):
        hou.ui.displayMessage("Please select at least 1 node!")
        return

    for node in selection:
        if(node.type().name() == "null" and "OUT_" in node.name()):
            obj_node = OBJ_NET.createNode("geo", node.name().replace("OUT_", ""))
            obj_node.moveToGoodPosition()
            
            merge_node = obj_node.createNode("object_merge", node.name().replace("OUT", "IN"))
            merge_node.setParms(
                {
                    "objpath1":node.path()
                }
            )
            
            out_node = obj_node.createNode("null", "OUT_modeling")
            out_node.setInput(0, merge_node)
            
            obj_node.layoutChildren()

    hou.ui.displayMessage("Building DONE.")