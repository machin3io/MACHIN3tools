import bpy
import bmesh
from bpy.props import EnumProperty, BoolProperty
from mathutils import Matrix, Euler, Quaternion
from math import radians
from ... utils.view import reset_viewport
from ... utils.math import average_locations
from ... items import view_axis_items


class ViewAxis(bpy.types.Operator):
    bl_idname = "machin3.view_axis"
    bl_label = "View Axis"
    bl_options = {'REGISTER'}

    axis: EnumProperty(name="Axis", items=view_axis_items, default="FRONT")

    @classmethod
    def description(cls, context, properties):
        if context.scene.M3.custom_view:
            return "Align Custom View (%s)" % (context.scene.M3.custom_view_type.capitalize())
        else:
            return "Align View to World\nALT: Align View to Active"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def invoke(self, context, event):
        if context.scene.M3.custom_view:
            if context.scene.M3.custom_view_type == 'CURSOR':
                mx = context.scene.cursor.matrix

            elif context.scene.M3.custom_view_type == 'OBJECT' and context.active_object:
                mx = context.active_object.matrix_world

            else:
                mx = None
                context.scene.M3.custom_view = False

            if mx:
                loc, rot, _ = mx.decompose()
                rot = self.create_view_rotation(rot, self.axis)

                # in edit mesh mode, also change the viewport location if anything is selected
                if context.scene.M3.custom_view_type == 'OBJECT' and context.mode == 'EDIT_MESH':
                    bm = bmesh.from_edit_mesh(context.active_object.data)

                    verts = [v for v in bm.verts if v.select]

                    if verts:
                        loc = mx @ average_locations([v.co for v in verts])

                r3d = context.space_data.region_3d
                r3d.view_location = loc
                r3d.view_rotation = rot

                r3d.view_perspective = 'ORTHO'

                # setting these props is required for prefs.inputs.use_auto_perspective to work
                r3d.is_orthographic_side_view = True
                r3d.is_perspective = True

                return {'FINISHED'}

        if event.alt:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=True)
        else:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=False)

        return {'FINISHED'}

    def create_view_rotation(self, rot, axis):
        '''
        rotate passed in quaternion based on view axis
        TOP is unchanged
        '''

        if self.axis == 'FRONT':
            rmx = rot.to_matrix()
            rotated = rot.to_matrix()

            rotated.col[1] = rmx.col[2]
            rotated.col[2] = -rmx.col[1]

            rot = rotated.to_quaternion()

        elif self.axis == 'BACK':
            rmx = rot.to_matrix()
            rotated = rot.to_matrix()

            rotated.col[0] = -rmx.col[0]
            rotated.col[1] = rmx.col[2]
            rotated.col[2] = rmx.col[1]

            rot = rotated.to_quaternion()

        elif self.axis == 'RIGHT':
            rmx = rot.to_matrix()
            rotated = rot.to_matrix()

            rotated.col[0] = rmx.col[1]
            rotated.col[1] = rmx.col[2]
            rotated.col[2] = rmx.col[0]

            rot = rotated.to_quaternion()

        elif self.axis == 'LEFT':
            rmx = rot.to_matrix()
            rotated = rot.to_matrix()

            rotated.col[0] = -rmx.col[1]
            rotated.col[1] = rmx.col[2]
            rotated.col[2] = -rmx.col[0]

            rot = rotated.to_quaternion()

        elif self.axis == 'BOTTOM':
            rmx = rot.to_matrix()
            rotated = rot.to_matrix()

            rotated.col[1] = -rmx.col[1]
            rotated.col[2] = -rmx.col[2]

            rot = rotated.to_quaternion()

        return rot


class MakeCamActive(bpy.types.Operator):
    bl_idname = "machin3.make_cam_active"
    bl_label = "Make Active"
    bl_description = "Make selected Camera active."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = context.active_object
        if active:
            return active.type == "CAMERA"

    def execute(self, context):
        context.scene.camera = context.active_object

        return {'FINISHED'}


class SmartViewCam(bpy.types.Operator):
    bl_idname = "machin3.smart_view_cam"
    bl_label = "Smart View Cam"
    bl_description = "Default: View Active Scene Camera\nNo Camera in the Scene: Create Camera from View\nCamera Selected: Make Selected Camera active and view it.\nAlt + Click: Create Camera from current View."
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        cams = [obj for obj in context.scene.objects if obj.type == "CAMERA"]
        view = context.space_data

        # create camera from view
        if not cams or event.alt:
            bpy.ops.object.camera_add()
            context.scene.camera = context.active_object
            bpy.ops.view3d.camera_to_view()

        # view the active cam, or make cam active and view it if active obj is camera
        else:
            active = context.active_object

            if active:
                if active in context.selected_objects and active.type == "CAMERA":
                    context.scene.camera = active

            # if the viewport is already aligned to a camera, toggle two times perspective/ortho. If you stay in cammera mode, the view camera op below will throw an exception. Two times, so you dont swich from perp to ortho
            if view.region_3d.view_perspective == 'CAMERA':
                bpy.ops.view3d.view_persportho()
                bpy.ops.view3d.view_persportho()

            bpy.ops.view3d.view_camera()
            bpy.ops.view3d.view_center_camera()

        return {'FINISHED'}


class NextCam(bpy.types.Operator):
    bl_idname = "machin3.next_cam"
    bl_label = "MACHIN3: Next Cam"
    bl_options = {'REGISTER', 'UNDO'}

    previous: BoolProperty(name="Previous", default=False)

    @classmethod
    def poll(cls, context):
        return context.space_data.region_3d.view_perspective == 'CAMERA'

    def execute(self, context):
        cams = sorted([obj for obj in context.scene.objects if obj.type == "CAMERA"], key=lambda x: x.name)

        if len(cams) > 1:
            active = context.scene.camera

            # print("active:", active)

            idx = cams.index(active)

            # next cam
            if not self.previous:
                idx = 0 if idx == len(cams) - 1 else idx + 1

            # previous cam
            else:
                idx = len(cams) - 1 if idx == 0 else idx - 1


            newcam = cams[idx]

            context.scene.camera = newcam

            bpy.ops.view3d.view_center_camera()


        return {'FINISHED'}


class ToggleCamPerspOrtho(bpy.types.Operator):
    bl_idname = "machin3.toggle_cam_persportho"
    bl_label = "MACHIN3: Toggle Camera Perspective/Ortho"
    bl_description = "Toggle Active Scene Camera Perspective/Ortho"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.camera

    def execute(self, context):
        cam = context.scene.camera

        if cam.data.type == "PERSP":
            cam.data.type = "ORTHO"
        else:
            cam.data.type = "PERSP"

        return {'FINISHED'}


toggledprefs = False


class ToggleViewPerspOrtho(bpy.types.Operator):
    bl_idname = "machin3.toggle_view_persportho"
    bl_label = "MACHIN3: Toggle View Perspective/Ortho"
    bl_description = "Toggle Viewport Perspective/Ortho"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        global toggledprefs

        view = context.space_data
        viewtype = view.region_3d.view_perspective
        prefs = context.preferences.inputs

        if viewtype == "PERSP" and prefs.use_auto_perspective:
            prefs.use_auto_perspective = False
            toggledprefs = True

        if viewtype == "ORTHO" and toggledprefs:
            prefs.use_auto_perspective = True

        bpy.ops.view3d.view_persportho()

        return {'FINISHED'}


class ResetViewport(bpy.types.Operator):
    bl_idname = "machin3.reset_viewport"
    bl_label = "MACHIN3: Reset Viewport"
    bl_description = "Perfectly align the viewport with the Y axis, looking into Y+"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def execute(self, context):
        context.space_data.region_3d.is_orthographic_side_view = False
        context.space_data.region_3d.view_perspective = 'PERSP'

        reset_viewport(context)

        return {'FINISHED'}
