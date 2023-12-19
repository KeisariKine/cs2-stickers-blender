bl_info = {
    "name": "Kine's Counter-Strike 2 Sticker Configurator",
    "author": "@keisarikine",
    "version": (1,0),
    "location": "View 3D > Properties Panel",
    "description": "Add-on for adding Counter-Strike 2 styled stickers to models exported from the game",
    "blender": (3, 60, 0),
    "support": "COMMUNITY",
    "category": "Add",
}

import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty
import csv
import os

class CS2_Sticker_Properties(bpy.types.PropertyGroup):
    slot1_file : bpy.props.StringProperty(
        name = "Slot 1 Sticker",
        description="Choose Image File for the Sticker in Slot 1",
        default="",
        maxlen=1023,
        subtype='FILE_PATH')
        
    slot2_file : bpy.props.StringProperty(
        name = "Slot 2 Sticker",
        description="Choose Image File for the Sticker in Slot 2",
        default="",
        maxlen=1023,
        subtype='FILE_PATH')
        
    slot3_file : bpy.props.StringProperty(
        name = "Slot 3 Sticker",
        description="Choose Image File for the Sticker in Slot 3",
        default="",
        maxlen=1023,
        subtype='FILE_PATH')
        
    slot4_file : bpy.props.StringProperty(
        name = "Slot 4 Sticker",
        description="Choose Image File for the Sticker in Slot 4",
        default="",
        maxlen=1023,
        subtype='FILE_PATH')
        
    slot5_file : bpy.props.StringProperty(
        name = "Slot 5 Sticker",
        description="Choose Image File for the Sticker in Slot 5 (will be ignored if weapon has no fifth slot)",
        default="",
        maxlen=1023,
        subtype='FILE_PATH')
        
    weapon_select : bpy.props.EnumProperty(
        name= "Weapon Selection",
        description= "sample text",
        items= [('pist1', "Glock-18", ""),
                ('pist2', "P2000", ""),
                ('pist3', "USP-S", ""),
                ('pist4', "P250", ""),
                ('pist5', "Five-SeveN", ""),
                ('pist6', "Tec-9", ""),
                ('pist7', "CZ75-Auto", ""),
                ('pist8', "Dual Berettas", ""),
                ('pist9', "Desert Eagle", ""),
                ('pist10', "R8 Revolver", ""),
                ('rif1', "AK-47", ""),
                ('rif2', "AUG", ""),
                ('rif3', "FAMAS", ""),
                ('rif4', "Galil AR", ""),
                ('rif5', "M4A1-S", ""),
                ('rif6', "M4A4", ""),
                ('rif7', "SG 553", ""),
                ('snp1',"AWP",""),
                ('snp2',"G3SG1",""),
                ('snp3',"Scar-20",""),
                ('snp4',"SSG-08",""),
                ('smg1', "MAC-10", ""),
                ('smg2', "MP5-SD", ""),
                ('smg3', "MP7", ""),
                ('smg4', "MP9", ""),
                ('smg5', "P90", ""),
                ('smg6', "PP-Bizon", ""),
                ('smg7', "UMP-45", ""),
                ('sh1', "M249", ""),
                ('sh2', "MAG-7", ""),
                ('sh3', "Negev", ""),
                ('sh4', "Nova", ""),
                ('sh5', "Sawed-Off", ""),
                ('sh6', "XM1014", "")
        ]
    )



class VIEW3D_PT_CS2_sticker(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "CS2_Sticker_Configurator_PT_main_panel"
    bl_label = "Kine's Counter-Strike 2 Sticker Configurator 4.0 Fix"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_props
        
        layout.prop(mytool, "weapon_select")
        layout.prop(mytool, "slot1_file")
        layout.prop(mytool, "slot2_file")
        layout.prop(mytool, "slot3_file")
        layout.prop(mytool, "slot4_file")
        layout.prop(mytool, "slot5_file")
        
        layout.operator("cs2_sticker_config.cs2_operator")

def GetOffset(csv_file,selected,slot,offset):
    data = []

    with open(csv_file) as f:
        reader = csv.DictReader(f)

        for row in reader:
            data.append(row)
    for option in data:
        if(option["Operator"] == selected):
            if slot == 1:
                 offset.x = float(option["Slot1X"])
                 offset.y = abs(float(option["Slot1Y"]))
                 offset.s = float(option["Slot1S"])
            elif slot == 2:
                 offset.x = float(option["Slot2X"])
                 offset.y = abs(float(option["Slot2Y"]))
                 offset.s = float(option["Slot2S"])
            elif slot == 3:
                 offset.x = float(option["Slot3X"])
                 offset.y = abs(float(option["Slot3Y"]))
                 offset.s = float(option["Slot3S"])
            elif slot == 4:
                 offset.x = float(option["Slot4X"])
                 offset.y = abs(float(option["Slot4Y"]))
                 offset.s = float(option["Slot4S"])
            elif slot == 5:
                 offset.x = float(option["Slot5X"])
                 offset.y = abs(float(option["Slot5Y"]))
                 offset.s = float(option["Slot5S"])
    return offset

def CreateNodes(node_name, offset,img_path):
    #Create Node Group
    sticker_group = bpy.data.node_groups.new(node_name, 'ShaderNodeTree')
    
    group_outputs = sticker_group.nodes.new(type='NodeGroupOutput')
    group_outputs.location = (1600,0)
    group_inputs = sticker_group.nodes.new(type='NodeGroupInput')
    group_inputs.location = (-400,-400)
    
    #sticker_group.outputs.new('NodeSocketVector','Sticker UV')
    #sticker_group.outputs.new('NodeSocketColor','Sticker Color')
    #sticker_group.outputs.new('NodeSocketFloat','Sticker Alpha')
    
    UVOut = sticker_group.interface.new_socket(name='Sticker UV', in_out='OUTPUT', socket_type='NodeSocketVector',)
    ColorOut = sticker_group.interface.new_socket(name='Sticker Color', in_out='OUTPUT', socket_type='NodeSocketColor',)
    AlphaOut = sticker_group.interface.new_socket(name='Sticker Alpha', in_out='OUTPUT', socket_type='NodeSocketFloat',)
    
    #scale_input = sticker_group.inputs.new('NodeSocketFloat','Sticker Scale')
    scale_input = sticker_group.interface.new_socket(name='Sticker Scale', in_out='INPUT', socket_type='NodeSocketFloat',)
    scale_input.default_value = offset.s
    
    mod_nodes = sticker_group.nodes
    
    #Create nodes inside Group
    #Reversing the axis with multiply add node
    vec_math_transform = mod_nodes.new(type="ShaderNodeVectorMath")
    vec_math_transform.operation = "MULTIPLY_ADD"
    #set multply values
    vec_math_transform.inputs[1].default_value[0] = -1
    vec_math_transform.inputs[1].default_value[1] = -1
    vec_math_transform.inputs[1].default_value[2] = 0
    #set addend values
    vec_math_transform.inputs[2].default_value[0] = 1
    vec_math_transform.inputs[2].default_value[1] = 1
    vec_math_transform.inputs[2].default_value[2] = 0
    vec_math_transform.location=(-400,0)
    
    #creating the centering offset node
    vec_math_center1 = mod_nodes.new(type="ShaderNodeVectorMath")
    vec_math_center1.operation = "ADD"
    vec_math_center1.inputs[1].default_value[0] = -0.5
    vec_math_center1.inputs[1].default_value[1] = -0.5
    vec_math_center1.inputs[1].default_value[2] = 0
    vec_math_center1.location=(-200,0)
    
    #creating the CS2 offset value node
    vec_math_offset = mod_nodes.new(type="ShaderNodeVectorMath")
    vec_math_offset.operation = "ADD"
    vec_math_offset.inputs[1].default_value[0] = offset.x
    vec_math_offset.inputs[1].default_value[1] = offset.y
    vec_math_offset.inputs[1].default_value[2] = 0
    
    #Create node to reverse scale value to negative
    scale_negative = mod_nodes.new(type='ShaderNodeMath')
    scale_negative.operation = "MULTIPLY"
    scale_negative.location = (0,-200)
    scale_negative.inputs[1].default_value = -1
    sticker_group.links.new(group_inputs.outputs[0],scale_negative.inputs[0])
    
    #Create UV map and set property to second UV channel
    uvmap = mod_nodes.new(type='ShaderNodeUVMap')
    sticker_group.nodes["UV Map"].uv_map = "UVMap.001"
    uvmap.location=(-600,0)
    
    #create Mapping node and scale it per CS2 Value
    mapping = mod_nodes.new(type="ShaderNodeMapping")
    #mapping.inputs[3].default_value[0] = ((offset.s)-1)*-1
    #mapping.inputs[3].default_value[1] = ((offset.s)-1)*-1
    #mapping.inputs[3].default_value[2] = ((offset.s)-1)*-1
    #sticker_group.links.new(group_inputs.outputs[0],mapping.inputs[3])
    sticker_group.links.new(scale_negative.outputs[0],mapping.inputs[3])
    mapping.location = (200,0)
    
    #create last centering vector math
    vec_math_center2 = mod_nodes.new(type="ShaderNodeVectorMath")
    vec_math_center2.operation = "ADD"
    vec_math_center2.inputs[1].default_value[0] = 0.5
    vec_math_center2.inputs[1].default_value[1] = 0.5
    vec_math_center2.inputs[1].default_value[2] = 0
    vec_math_center2.location = (400,0)
    
    #create image texture node
    img_node = mod_nodes.new(type="ShaderNodeTexImage")
    sticker_img = bpy.data.images.load(filepath=img_path)
    sticker_img.alpha_mode = 'CHANNEL_PACKED'
    img_node.image = sticker_img
    img_node.extension = 'CLIP'
    img_node.location = (600,-50)
    
    #create alpha math
    alpha_math = mod_nodes.new(type='ShaderNodeMath')
    alpha_math.operation='GREATER_THAN'
    alpha_math.inputs[1].default_value = 0.05
    alpha_math.location = (930,-90)
    
    #Create Links
    sticker_group.links.new(uvmap.outputs[0], vec_math_transform.inputs[0])
    sticker_group.links.new(vec_math_transform.outputs[0], vec_math_center1.inputs[0])
    sticker_group.links.new(vec_math_center1.outputs[0], vec_math_offset.inputs[0])
    sticker_group.links.new(vec_math_offset.outputs[0], mapping.inputs[0])
    sticker_group.links.new(mapping.outputs[0],vec_math_center2.inputs[0])
    #connect UV to output
    sticker_group.links.new(vec_math_center2.outputs[0],group_outputs.inputs[0])
    
    #connect UV to image and image to outputs
    sticker_group.links.new(vec_math_center2.outputs[0],img_node.inputs[0])
    sticker_group.links.new(img_node.outputs[0],group_outputs.inputs[1])
        
    sticker_group.links.new(img_node.outputs[1],alpha_math.inputs[0])
    sticker_group.links.new(alpha_math.outputs[0],group_outputs.inputs[2])
    
    return sticker_group


class VIEW3D_OT_CS2_operator(bpy.types.Operator):
    bl_idname = "cs2_sticker_config.cs2_operator"
    bl_label = "Add Stickers"
    bl_description = "Add Stickers to the active material on the active object based on the options selected"
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_props
        csv_file = './sticker_offsets_db.csv'
        addon_directory = os.path.dirname(os.path.realpath(__file__))
        csv_file_relative_path = 'sticker_offsets_db.csv'
        csv_file = os.path.join(addon_directory, csv_file_relative_path)
        weapon = mytool.weapon_select
        
        class Offset: 
            def __init__(self,x,y,s):
                self.x = x
                self.y = y
                self.s = s

        if mytool.slot1_file != '':       
            offsetvar = GetOffset(csv_file,weapon,1,Offset(0,0,0))
            print(offsetvar.s)
            sticker1_group = CreateNodes('CS2 Sticker Slot 1',offsetvar,mytool.slot1_file)
            mat_tree = bpy.context.active_object.active_material.node_tree
            add_group_node_1 = mat_tree.nodes.new(type='ShaderNodeGroup')
            add_group_node_1.node_tree = sticker1_group

        if mytool.slot2_file != '':       
            offsetvar = GetOffset(csv_file,weapon,2,Offset(0,0,0))
            sticker2_group = CreateNodes('CS2 Sticker Slot 2',offsetvar,mytool.slot2_file)
            mat_tree = bpy.context.active_object.active_material.node_tree
            add_group_node_2 = mat_tree.nodes.new(type='ShaderNodeGroup')
            add_group_node_2.node_tree = sticker2_group

        if mytool.slot3_file != '':       
            offsetvar = GetOffset(csv_file,weapon,3,Offset(0,0,0))
            sticker3_group = CreateNodes('CS2 Sticker Slot 3',offsetvar,mytool.slot3_file)
            mat_tree = bpy.context.active_object.active_material.node_tree
            add_group_node_3 = mat_tree.nodes.new(type='ShaderNodeGroup')
            add_group_node_3.node_tree = sticker3_group

        if mytool.slot4_file != '':       
            offsetvar = GetOffset(csv_file,weapon,4,Offset(0,0,0))
            sticker4_group = CreateNodes('CS2 Sticker Slot 4',offsetvar,mytool.slot4_file)
            mat_tree = bpy.context.active_object.active_material.node_tree
            add_group_node_4 = mat_tree.nodes.new(type='ShaderNodeGroup')
            add_group_node_4.node_tree = sticker4_group

        if mytool.slot5_file != '':       
            offsetvar = GetOffset(csv_file,weapon,5,Offset(0,0,0))
            if offsetvar.s != 0:
                sticker1_group = CreateNodes('CS2 Sticker Slot 5',offsetvar,mytool.slot5_file)
                mat_tree = bpy.context.active_object.active_material.node_tree
                add_group_node_5 = mat_tree.nodes.new(type='ShaderNodeGroup')
                add_group_node_5.node_tree = sticker1_group
    
        return {'FINISHED'}

classes = [CS2_Sticker_Properties, VIEW3D_PT_CS2_sticker, VIEW3D_OT_CS2_operator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_props = bpy.props.PointerProperty(type= CS2_Sticker_Properties)
    

    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(VIEW3D_PT_CS2_sticker)
        del bpy.types.Scene.my_tool
        
if __name__ == "__main__":
    register()
