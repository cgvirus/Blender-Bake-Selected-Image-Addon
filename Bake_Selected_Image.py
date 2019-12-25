bl_info = {
    "name": "Bake Selected Image",
    "author": "Fahad Hasan Pathik CGVIRUS",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "location": "Toolshelf > Layers Tab",
    "description": "Bake Texture Easily with Selected Image",
    "warning": "",
    "wiki_url": "https://github.com/cgvirus/Blender-Bake-Selected-Image-Addon",
    "category": "Bake",
    }


import bpy
from bpy.props import *
from bpy.types import Menu, Operator, Panel, UIList
from bpy.app.handlers import persistent

class Bake_OT_InputImage(bpy.types.Operator):
    """Input selected image as Image Texture in Material Editor"""
    bl_idname = "obj.image_input"
    bl_label = "Input Selected Image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def execute(self, context):        
        for o in context.selected_objects:
            if o.type == 'MESH':
                for m in bpy.data.objects[o.name].material_slots:

                    m.material.use_nodes = True
                    node_tree = bpy.data.materials[m.material.name].node_tree


                    img_name = bpy.context.texture.image


                    node = node_tree.nodes.new("ShaderNodeTexImage")
                    node.name = "BakeTex"

                    node.image = img_name

                    node.select = True
                    

                    node_tree.nodes.active = node



            else:
                pass


        return {'FINISHED'}



class Bake_OT_SelectedImage(bpy.types.Operator):
    """Bake image textures of selected objects"""
    bl_idname = "obj.bake_image"
    bl_label = "Bake"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def execute(self, context):
        bake_type = context.scene.cycles.bake_type
        bpy.ops.object.bake('INVOKE_DEFAULT',type = bake_type)


        return {'FINISHED'}




class BAKESELECTED_PT_Panel(bpy.types.Panel):
    
    bl_idname = "BAKESELECTED_PT_Panel"
    bl_label = "Bake Selcted Image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'CYCLES'}




    def draw(self, context):
        layout = self.layout

        tex = context.texture
        space = context.space_data
        pin_id = space.pin_id
        use_pin_id = space.use_pin_id
        user = context.texture_user


        col = layout.column()

        if not (use_pin_id and isinstance(pin_id, bpy.types.Texture)):
            pin_id = None

        if not pin_id:
            col.template_texture_user()

        if user or pin_id:
            col.separator()

            if pin_id:
                col.template_ID(space, "pin_id")
            else:
                propname = context.texture_user_property.identifier
                col.template_ID(user, propname, new="texture.new")

            if tex:
                col.separator()

                split = col.split(factor=0.2)
                split.label(text="Type")
                split.prop(tex, "type", text="")

        layout = self.layout

        row = col.row(align=True)
        row = col.row(align=True)
        row.operator("obj.image_input",icon='TRACKING_FORWARDS')

        row = col.row(align=True)
        row = col.row(align=True)
        row.operator("obj.bake_image",icon='RENDER_STILL')

        row = col.row(align=True)
        tex = context.texture
        layout.template_image(tex, "image", tex.image_user)

classes = (
    Bake_OT_InputImage,
    Bake_OT_SelectedImage,
    BAKESELECTED_PT_Panel,
    )


def register():
    # add operator
    from bpy.utils import register_class
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    # remove operator and preferences
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()