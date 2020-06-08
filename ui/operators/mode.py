import bpy
from bpy.props import StringProperty
from ... utils.registration import get_prefs
from ... utils.view import set_xray, reset_xray, update_local_view
from ... utils.object import parent


user_cavity = True


class EditMode(bpy.types.Operator):
    bl_idname = "machin3.edit_mode"
    bl_label = "Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global user_cavity

        shading = context.space_data.shading
        toggle_cavity = get_prefs().toggle_cavity

        if context.mode == "OBJECT":
            set_xray(context)

            bpy.ops.object.mode_set(mode="EDIT")

            if toggle_cavity:
                user_cavity = shading.show_cavity
                shading.show_cavity = False


        elif context.mode == "EDIT_MESH":
            reset_xray(context)

            bpy.ops.object.mode_set(mode="OBJECT")

            if toggle_cavity and user_cavity:
                shading.show_cavity = True
                user_cavity = True

        return {'FINISHED'}


class MeshMode(bpy.types.Operator):
    bl_idname = "machin3.mesh_mode"
    bl_label = "Mesh Mode"
    bl_options = {'REGISTER', 'UNDO'}

    mode: StringProperty()

    @classmethod
    def description(cls, context, properties):
        return "%s Select\nCTRL + Click: Expand Selection" % (properties.mode.capitalize())

    def invoke(self, context, event):
        global user_cavity
        shading = context.space_data.shading
        toggle_cavity = get_prefs().toggle_cavity

        if context.mode == "OBJECT":
            set_xray(context)

            bpy.ops.object.mode_set(mode="EDIT")

            if toggle_cavity:
                user_cavity = shading.show_cavity
                shading.show_cavity = False

        expand = True if event.ctrl else False

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=expand, type=self.mode)
        return {'FINISHED'}


class ImageMode(bpy.types.Operator):
    bl_idname = "machin3.image_mode"
    bl_label = "MACHIN3: Image Mode"
    bl_options = {'REGISTER'}

    mode: StringProperty()

    def execute(self, context):
        view = context.space_data
        active = context.active_object

        view.mode = self.mode

        if self.mode == "UV" and active:
            if active.mode == "OBJECT":
                uvs = active.data.uv_layers

                # create new uv layer
                if not uvs:
                    uvs.new()

                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="SELECT")

        return {'FINISHED'}


class UVMode(bpy.types.Operator):
    bl_idname = "machin3.uv_mode"
    bl_label = "MACHIN3: UV Mode"
    bl_options = {'REGISTER'}

    mode: StringProperty()

    def execute(self, context):
        toolsettings = context.scene.tool_settings
        view = context.space_data

        if view.mode != "UV":
            view.mode = "UV"

        if toolsettings.use_uv_select_sync:
            bpy.ops.mesh.select_mode(type=self.mode.replace("VERTEX", "VERT"))

        else:
            toolsettings.uv_select_mode = self.mode

        return {'FINISHED'}


class SurfaceDrawMode(bpy.types.Operator):
    bl_idname = "machin3.surface_draw_mode"
    bl_label = "MACHIN3: Surface Draw Mode"
    bl_description = "Surface Draw, create parented, empty GreasePencil object and enter DRAW mode.\nSHIFT: Select the Line tool."
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        # forcing object mode at the beginning, avoids issues when calling this tool from PAINT_WEIGHT mode
        bpy.ops.object.mode_set(mode='OBJECT')

        scene = context.scene
        ts = scene.tool_settings
        mcol = context.collection
        view = context.space_data
        active = context.active_object

        existing_gps = [obj for obj in active.children if obj.type == "GPENCIL"]

        if existing_gps:
            gp = existing_gps[0]

        else:
            name = "%s_SurfaceDrawing" % (active.name)
            gp = bpy.data.objects.new(name, bpy.data.grease_pencils.new(name))

            mcol.objects.link(gp)

            gp.matrix_world = active.matrix_world
            parent(gp, active)

        update_local_view(view, [(gp, True)])

        gp.data.layers.new(name="SurfaceLayer")

        context.view_layer.objects.active = gp
        active.select_set(False)
        gp.select_set(True)

        gp.color = (0, 0, 0, 1)

        bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

        # surface placement
        ts.gpencil_stroke_placement_view3d = 'SURFACE'
        gp.data.zdepth_offset = 0.0001

        if not view.show_region_toolbar:
            view.show_region_toolbar = True

        # optionally select the line tool
        if event.shift:
            bpy.ops.wm.tool_set_by_id(name="builtin.line")

        return {'FINISHED'}
