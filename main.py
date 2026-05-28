bl_info = {
    "name": "Glass Material Pack",
    "author": "Lamskov Daniel",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Glass Materials",
    "description": "Add 5 different glass material types to selected objects",
    "category": "Material",
}

import bpy
import mathutils
from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty

class GlassMaterialBase:
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def create_material(self, name, nodes_data):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (400, 0)

        return mat, nodes, links, output

class GlassType1(GlassMaterialBase):
    def execute(self, context):
        obj = context.active_object
        mat, nodes, links, output = self.create_material("Glass_Clear", {})

        glass_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
        glass_bsdf.location = (0, 0)
        glass_bsdf.inputs['Roughness'].default_value = 0.02
        glass_bsdf.inputs['IOR'].default_value = 1.45
        glass_bsdf.inputs['Color'].default_value = (0.95, 0.98, 1.0, 1.0)

        links.new(glass_bsdf.outputs['BSDF'], output.inputs['Surface'])

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        return {'FINISHED'}

class GlassType2(GlassMaterialBase):
    def execute(self, context):
        obj = context.active_object
        mat, nodes, links, output = self.create_material("Glass_Frosted", {})

        glass_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
        glass_bsdf.location = (-200, 0)
        glass_bsdf.inputs['Roughness'].default_value = 0.25
        glass_bsdf.inputs['IOR'].default_value = 1.49

        rough_glass = nodes.new(type='ShaderNodeBsdfGlossy')
        rough_glass.location = (-200, -150)
        rough_glass.inputs['Roughness'].default_value = 0.3

        mix_shader = nodes.new(type='ShaderNodeMixShader')
        mix_shader.location = (0, 0)
        mix_shader.inputs['Fac'].default_value = 0.7

        links.new(glass_bsdf.outputs['BSDF'], mix_shader.inputs[1])
        links.new(rough_glass.outputs['BSDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        return {'FINISHED'}

class GlassType3(GlassMaterialBase):
    def execute(self, context):
        obj = context.active_object
        mat, nodes, links, output = self.create_material("Glass_Colored", {})

        glass_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
        glass_bsdf.location = (0, 0)
        glass_bsdf.inputs['Roughness'].default_value = 0.05
        glass_bsdf.inputs['IOR'].default_value = 1.52
        glass_bsdf.inputs['Color'].default_value = (0.2, 0.6, 0.9, 1.0)

        volume_abs = nodes.new(type='ShaderNodeVolumeAbsorption')
        volume_abs.location = (-200, -150)
        volume_abs.inputs['Color'].default_value = (0.3, 0.5, 0.8, 1.0)
        volume_abs.inputs['Density'].default_value = 0.5

        volume_out = nodes.new(type='ShaderNodeOutputMaterial')
        volume_out.location = (400, -150)

        links.new(glass_bsdf.outputs['BSDF'], output.inputs['Surface'])
        links.new(volume_abs.outputs['Volume'], volume_out.inputs['Volume'])

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        return {'FINISHED'}

class GlassType4(GlassMaterialBase):
    def execute(self, context):
        obj = context.active_object
        mat, nodes, links, output = self.create_material("Glass_Caustic", {})

        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        transparent.location = (-400, 100)

        glass_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
        glass_bsdf.location = (-400, -100)
        glass_bsdf.inputs['Roughness'].default_value = 0.01
        glass_bsdf.inputs['IOR'].default_value = 1.55

        mix_shader = nodes.new(type='ShaderNodeMixShader')
        mix_shader.location = (-150, 0)
        mix_shader.inputs['Fac'].default_value = 0.15

        refraction = nodes.new(type='ShaderNodeBsdfRefraction')
        refraction.location = (-400, -300)
        refraction.inputs['Roughness'].default_value = 0.02
        refraction.inputs['IOR'].default_value = 1.55

        mix_shader2 = nodes.new(type='ShaderNodeMixShader')
        mix_shader2.location = (0, 0)
        mix_shader2.inputs['Fac'].default_value = 0.8

        links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        links.new(glass_bsdf.outputs['BSDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], mix_shader2.inputs[1])
        links.new(refraction.outputs['BSDF'], mix_shader2.inputs[2])
        links.new(mix_shader2.outputs['Shader'], output.inputs['Surface'])

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        return {'FINISHED'}

class GlassType5(GlassMaterialBase):
    def execute(self, context):
        obj = context.active_object
        mat, nodes, links, output = self.create_material("Glass_Patterned", {})

        glass_bsdf = nodes.new(type='ShaderNodeBsdfGlass')
        glass_bsdf.location = (0, 0)
        glass_bsdf.inputs['Roughness'].default_value = 0.08
        glass_bsdf.inputs['IOR'].default_value = 1.47

        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-500, 100)
        noise.inputs['Scale'].default_value = 15.0
        noise.inputs['Detail'].default_value = 3.0

        bump = nodes.new(type='ShaderNodeBump')
        bump.location = (-300, 100)
        bump.inputs['Strength'].default_value = 0.2
        links.new(noise.outputs['Fac'], bump.inputs['Height'])

        mapping = nodes.new(type='ShaderNodeMapping')
        mapping.location = (-700, 100)

        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-900, 100)
        links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

        links.new(bump.outputs['Normal'], glass_bsdf.inputs['Normal'])
        links.new(glass_bsdf.outputs['BSDF'], output.inputs['Surface'])

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        return {'FINISHED'}

class GLASS_OT_Type1(bpy.types.Operator, GlassType1):
    bl_idname = "glass.add_type1"
    bl_label = "Clear Glass"
    bl_description = "Add standard clear glass material"
    bl_options = {'REGISTER', 'UNDO'}

class GLASS_OT_Type2(bpy.types.Operator, GlassType2):
    bl_idname = "glass.add_type2"
    bl_label = "Frosted Glass"
    bl_description = "Add frosted/matte glass material"
    bl_options = {'REGISTER', 'UNDO'}

class GLASS_OT_Type3(bpy.types.Operator, GlassType3):
    bl_idname = "glass.add_type3"
    bl_label = "Colored Glass"
    bl_description = "Add colored tinted glass material"
    bl_options = {'REGISTER', 'UNDO'}

class GLASS_OT_Type4(bpy.types.Operator, GlassType4):
    bl_idname = "glass.add_type4"
    bl_label = "Caustic Glass"
    bl_description = "Add glass with enhanced caustic effects"
    bl_options = {'REGISTER', 'UNDO'}

class GLASS_OT_Type5(bpy.types.Operator, GlassType5):
    bl_idname = "glass.add_type5"
    bl_label = "Patterned Glass"
    bl_description = "Add glass with noise pattern surface"
    bl_options = {'REGISTER', 'UNDO'}

class GLASS_PT_Panel(bpy.types.Panel):
    bl_label = "Glass Materials"
    bl_idname = "GLASS_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Glass Materials"

    def draw(self, context):
        layout = self.layout
        layout.operator("glass.add_type1", icon='MATERIAL')
        layout.operator("glass.add_type2", icon='MATERIAL')
        layout.operator("glass.add_type3", icon='MATERIAL')
        layout.operator("glass.add_type4", icon='MATERIAL')
        layout.operator("glass.add_type5", icon='MATERIAL')

classes = [
    GLASS_OT_Type1,
    GLASS_OT_Type2,
    GLASS_OT_Type3,
    GLASS_OT_Type4,
    GLASS_OT_Type5,
    GLASS_PT_Panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
