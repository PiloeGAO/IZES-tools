'''
    :package:   izes_tools
    :file:      animation_tools.py
    :author:    ldepoix
    :version:   0.0.2
    :brief:     List of all functions for the animation tools.
'''
import os

from maya import cmds
import maya.mel as mel

from ldRigNodes.space_switch_manager import SpaceSwitchManager, SpaceSwitchType

def attach_backpack_to_joy():
    if(len(cmds.ls(sl=True)) != 2):
        print("Please select Backpack reference and the Joy.")
        return

    backpack_namespace = cmds.ls(sl=True)[0][:-2]
    joy_namespace = cmds.ls(sl=True)[1][:-2]

    print(f"Attaching {backpack_namespace} to {joy_namespace}")

    if(cmds.getAttr(f"{backpack_namespace}:main_SRT_global.translate") != cmds.getAttr(f"{joy_namespace}:main_SRT_local_CON.translate")):
        print("Backpack and joy not aligned, skipping.")
        return

    # Aligning Backpack to correct orient.
    cmds.setAttr(f"{backpack_namespace}:main_SRT_global.rotateY",
        (cmds.getAttr(f"{joy_namespace}:main_SRT_local_CON.rotateY") + 180.0))

    # Connect every controllers to targets (config created from a production scene).
    settings = [
        {
            "namespace": backpack_namespace,
            "obj":"main_SRT_local",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chestDepth_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        # Left side.
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_2_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "R_clavicle_shoulder_FK_CON",
                    "weight": 0.25
                },
                {
                    "namespace": backpack_namespace,
                    "obj": "main_top_head",
                    "weight": 0.25
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_3_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "neck_neck_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "R_clavicle_shoulder_FK_CON",
                    "weight": 0.25
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_4_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "neck_neck_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "R_clavicle_shoulder_FK_CON",
                    "weight": 0.5
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_5_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "neck_neck_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "R_clavicle_shoulder_FK_CON",
                    "weight": 0.5
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_6_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "R_clavicle_shoulder_FK_CON",
                    "weight": 0.25
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_7_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chestDepth_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "R_clavicle_shoulder_FK_CON",
                    "weight": 0.1
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_topStrand_8_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chestDepth_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_bottomStrand_2_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_hipsDepth_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_bottomStrand_3_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_hipsDepth_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": backpack_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"L_ear_bottomStrand_4_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_hipsDepth_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": backpack_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 0.5
                }
            ]
        },

        # Right Side.
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_2_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "L_clavicle_shoulder_FK_CON",
                    "weight": 0.25
                },
                {
                    "namespace": backpack_namespace,
                    "obj": "main_top_head",
                    "weight": 0.25
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_3_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "neck_neck_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "L_clavicle_shoulder_FK_CON",
                    "weight": 0.25
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_4_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "neck_neck_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "L_clavicle_shoulder_FK_CON",
                    "weight": 0.5
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_5_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "neck_neck_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "L_clavicle_shoulder_FK_CON",
                    "weight": 0.5
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_6_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "L_clavicle_shoulder_FK_CON",
                    "weight": 0.25
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_7_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chestDepth_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": joy_namespace,
                    "obj": "L_clavicle_shoulder_FK_CON",
                    "weight": 0.1
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_topStrand_8_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_chestDepth_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_bottomStrand_2_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_hipsDepth_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_bottomStrand_3_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_hipsDepth_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": backpack_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 1.0
                }
            ]
        },
        {
            "namespace": backpack_namespace,
            "obj":"R_ear_bottomStrand_4_CON",
            "targets": [
                {
                    "namespace": joy_namespace,
                    "obj": "spine_hipsDepth_FK_CON",
                    "weight": 1.0
                },
                {
                    "namespace": backpack_namespace,
                    "obj": "spine_chest_FK_CON",
                    "weight": 0.5
                }
            ]
        }
    ]

    for elem in settings:
        namespace = elem["namespace"]
        object = elem["obj"]
        
        if(not cmds.objExists(f"{namespace}:{object}")):
            print(f"Failed to find: {namespace}:{object}")
            continue
        
        print(f"Starting for {namespace}:{object}")
        
        for target in elem["targets"]:
            target_namespace = target["namespace"]
            target_object = target["obj"]
            target_weight = target["weight"]
            
            if(not cmds.objExists(f"{target_namespace}:{target_object}")):
                print(f"Failed to find: {target_namespace}:{target_object}")
                continue
            
            print(f"Working on for {target_namespace}:{target_object}")
                    
            spaceSwitchtools = SpaceSwitchManager(nodeName=f"{namespace}:{object}")
            spaceSwitchtools.add_space(f"{target_namespace}:{target_object}", SpaceSwitchType.SRT, weight=target_weight)