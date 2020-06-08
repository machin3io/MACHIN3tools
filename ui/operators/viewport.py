import bpy
from bpy.props import EnumProperty, BoolProperty
axisitems = [("FRONT", "Front", ""),
             ("BACK", "Back", ""),
             ("LEFT", "Left", ""),
             ("RIGHT", "Right", ""),
             ("TOP", "Top", ""),
             ("BOTTOM", "Bottom", "")]


class ViewAxis(bpy.types.Operator):
    bl_idname = "machin3.view_axis"
    bl_label = "View Axis"
    bl_description = "Click: Align View\nALT + Click: Align View to Active"
    bl_options = {'REGISTER'}

    axis: EnumProperty(name="Axis", items=axisitems, default="FRONT")

    def invoke(self, context, event):

        if event.alt:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=True)
        else:
            bpy.ops.view3d.view_axis(type=self.axis, align_active=False)

        return {'FINISHED'}


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
