import bpy
from bpy.props import IntProperty
import bmesh
from math import radians


class ShadeSmooth(bpy.types.Operator):
    bl_idname = "machin3.shade_smooth"
    bl_label = "Shade Smooth"
    bl_description = "Set smooth shading in object and edit mode\nALT: Mark edges sharp if face angle > auto smooth angle"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if context.mode == "OBJECT":
            bpy.ops.object.shade_smooth()

            # set sharps based on face angles + activate auto smooth + enable sharp overlays
            if event.alt:
                for obj in context.selected_objects:
                    self.set_sharps(context.mode, obj)

                context.space_data.overlay.show_edge_sharp = True

        elif context.mode == "EDIT_MESH":
            if event.alt:
                self.set_sharps(context.mode, context.active_object)

                context.space_data.overlay.show_edge_sharp = True
            else:
                bpy.ops.mesh.faces_shade_smooth()

        return {'FINISHED'}

    def set_sharps(self, mode, obj):
        obj.data.use_auto_smooth = True
        angle = obj.data.auto_smooth_angle

        if mode == 'OBJECT':
            bm = bmesh.new()
            bm.from_mesh(obj.data)

        elif mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(obj.data)

            # smooth all faces like in object mode
            for f in bm.faces:
                f.smooth = True

        bm.normal_update()

        sharpen = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle() > angle]

        for e in sharpen:
            e.smooth = False

        if mode == 'OBJECT':
            bm.to_mesh(obj.data)
            bm.clear()

        elif mode == 'EDIT_MESH':
            bmesh.update_edit_mesh(obj.data)

        # obj.data.auto_smooth_angle = radians(180)


class ShadeFlat(bpy.types.Operator):
    bl_idname = "machin3.shade_flat"
    bl_label = "Shade Flat"
    bl_description = "Set flat shading in object and edit mode\nALT: Clear all sharps, bweights, creases and seams."
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if context.mode == "OBJECT":
            bpy.ops.object.shade_flat()

            # clear all sharps, bweights, seams and creases
            if event.alt:
                for obj in context.selected_objects:
                    self.clear_obj_sharps(obj)

        elif context.mode == "EDIT_MESH":
            if event.alt:
                self.clear_mesh_sharps(context.active_object.data)

            else:
                bpy.ops.mesh.faces_shade_flat()

        return {'FINISHED'}

    def clear_obj_sharps(self, obj):
        obj.data.use_auto_smooth = False

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.normal_update()

        bw = bm.edges.layers.bevel_weight.verify()
        cr = bm.edges.layers.crease.verify()

        for e in bm.edges:
            e[bw] = 0
            e[cr] = 0
            e.smooth = True
            e.seam = False

        bm.to_mesh(obj.data)
        bm.clear()

    def clear_mesh_sharps(self, mesh):
        mesh.use_auto_smooth = False

        bm = bmesh.from_edit_mesh(mesh)
        bm.normal_update()

        bw = bm.edges.layers.bevel_weight.verify()
        cr = bm.edges.layers.crease.verify()

        # faltten all faces like in object mode
        for f in bm.faces:
            f.smooth = False

        for e in bm.edges:
            e[bw] = 0
            e[cr] = 0
            e.smooth = True
            e.seam = False

        bmesh.update_edit_mesh(mesh)


class ToggleAutoSmooth(bpy.types.Operator):
    bl_idname = "machin3.toggle_auto_smooth"
    bl_label = "Toggle Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    angle: IntProperty(name="Auto Smooth Angle")

    @classmethod
    def description(cls, context, properties):
        if properties.angle == 0:
            return "Toggle Auto Smooth"
        else:
            return "Auto Smooth Angle Preset: %d" % (properties.angle)

    def execute(self, context):
        active = context.active_object

        if active:
            sel = context.selected_objects

            if active not in sel:
                sel.append(active)

            autosmooth = not active.data.use_auto_smooth if self.angle == 0 else True

            for obj in [obj for obj in sel if obj.type == 'MESH']:
                obj.data.use_auto_smooth = autosmooth

                if self.angle:
                    obj.data.auto_smooth_angle = radians(self.angle)

        return {'FINISHED'}
