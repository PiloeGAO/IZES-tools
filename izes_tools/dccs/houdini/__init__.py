import hou

def fix_AO():
    matContext = hou.node("mat")

    for arnoldShader in matContext.children():
        occlusionNode = arnoldShader.node("ambient_occlusion2")
        occlusionNode.parm("far_clip").set(1)