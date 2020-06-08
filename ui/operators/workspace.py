import bpy
from bpy.props import StringProperty


class SwitchWorkspace(bpy.types.Operator):
    bl_idname = "machin3.switch_workspace"
    bl_label = "Switch Workspace"
    bl_options = {'REGISTER'}

    name: StringProperty()

    @classmethod
    def description(cls, context, properties):
        return "Switch to Workplace '%s'" % (properties.name)

    def execute(self, context):

        # get current workspace
        ws = bpy.data.workspaces.get(self.name)

        # get view matrix from 3d view (if present)
        view = self.get_view(context, ws)
        shading = self.get_shading(context, ws)
        overlay = self.get_overlay(context, ws)

        # if the chosen workspace is already active, select the alternative one, if present and sync the shading
        if ws and context.window.workspace == ws:
            ws = bpy.data.workspaces.get('%s.alt' % self.name)

            if ws:
                bpy.context.window.workspace = ws
                if shading:
                    self.set_shading_and_overlay(ws, shading, overlay)

        # switch back to original(non-alt workspace) and sync shading
        elif ws and ws.name + ".alt" == context.workspace.name:
            bpy.context.window.workspace = ws
            if shading:
                self.set_shading_and_overlay(ws, shading, overlay)

        # otherwise just switch to the chosen one, and don't set shading
        elif ws:
            bpy.context.window.workspace = ws

        # for all cases, sync the view
        if ws and view:
            self.set_view(ws, view)

        return {'FINISHED'}

    def set_shading_and_overlay(self, workspace, shading, overlay):
        for screen in workspace.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = shading['shading_type']
                            space.shading.color_type = shading['shading_color_type']
                            space.shading.light = shading['shading_light']
                            space.shading.studio_light = shading['studio_light']
                            space.shading.studiolight_rotate_z = shading['rotate_z']
                            space.shading.studiolight_background_alpha = shading['background_alpha']
                            space.shading.studiolight_background_blur = shading['background_blur']
                            space.shading.studiolight_intensity = shading['studiolight_intensity']

                            space.shading.use_scene_lights = shading['use_scene_lights']
                            space.shading.use_scene_world = shading['use_scene_world']
                            space.shading.use_scene_lights_render = shading['use_scene_lights_render']
                            space.shading.use_scene_world_render = shading['use_scene_world_render']

                            space.shading.show_cavity = shading['show_cavity']
                            space.shading.cavity_type = shading['cavity_type']
                            space.shading.cavity_ridge_factor = shading['cavity_ridge_factor']
                            space.shading.cavity_valley_factor = shading['cavity_valley_factor']
                            space.shading.curvature_ridge_factor = shading['curvature_ridge_factor']
                            space.shading.curvature_valley_factor = shading['curvature_valley_factor']
                            space.shading.show_object_outline = shading['show_object_outline']

                            space.shading.show_xray = shading['show_xray']
                            space.shading.xray_alpha = shading['xray_alpha']

                            space.shading.show_backface_culling = shading['show_backface_culling']

                            space.overlay.show_overlays = overlay['show_overlays']

                            space.overlay.show_wireframes = overlay['show_wireframes']
                            space.overlay.wireframe_threshold = overlay['wireframe_threshold']

                            space.overlay.show_face_orientation = overlay['show_face_orientation']

                            space.overlay.show_floor = overlay['show_floor']
                            space.overlay.show_ortho_grid = overlay['show_ortho_grid']
                            space.overlay.show_axis_x = overlay['show_axis_x']
                            space.overlay.show_axis_y = overlay['show_axis_y']
                            space.overlay.show_axis_z = overlay['show_axis_z']

                            space.overlay.show_relationship_lines = overlay['show_relationship_lines']

                            space.overlay.show_cursor = overlay['show_cursor']
                            space.overlay.show_object_origins = overlay['show_object_origins']
                            space.overlay.show_object_origins_all = overlay['show_object_origins_all']

                            return

    def get_shading(self, context, workspace):
        if context.space_data.type == 'VIEW_3D':
            shading = context.space_data.shading

            s = {}

            s['shading_type'] = shading.type
            s['shading_color_type'] = shading.color_type
            s['shading_light'] = shading.light
            s['studio_light'] = shading.studio_light
            s['rotate_z'] = shading.studiolight_rotate_z
            s['background_alpha'] = shading.studiolight_background_alpha
            s['background_blur'] = shading.studiolight_background_blur
            s['studiolight_intensity'] = shading.studiolight_intensity

            s['use_scene_lights'] = shading.use_scene_lights
            s['use_scene_world'] = shading.use_scene_world
            s['use_scene_lights_render'] = shading.use_scene_lights_render
            s['use_scene_world_render'] = shading.use_scene_world_render

            s['show_cavity'] = shading.show_cavity
            s['cavity_type'] = shading.cavity_type
            s['cavity_ridge_factor'] = shading.cavity_ridge_factor
            s['cavity_valley_factor'] = shading.cavity_valley_factor
            s['curvature_ridge_factor'] = shading.curvature_ridge_factor
            s['curvature_valley_factor'] = shading.curvature_valley_factor
            s['show_object_outline'] = shading.show_object_outline

            s['show_xray'] = shading.show_xray
            s['xray_alpha'] = shading.xray_alpha

            s['show_backface_culling'] = shading.show_backface_culling

            return s

    def get_overlay(self, context, workspace):
        if context.space_data.type == 'VIEW_3D':
            overlay = context.space_data.overlay

            o = {}

            o['show_overlays'] = overlay.show_overlays

            o['show_wireframes'] = overlay.show_wireframes
            o['wireframe_threshold'] = overlay.wireframe_threshold

            o['show_face_orientation'] = overlay.show_face_orientation

            o['show_floor'] = overlay.show_floor
            o['show_ortho_grid'] = overlay.show_ortho_grid
            o['show_axis_x'] = overlay.show_axis_x
            o['show_axis_y'] = overlay.show_axis_y
            o['show_axis_z'] = overlay.show_axis_z

            o['show_relationship_lines'] = overlay.show_relationship_lines

            o['show_cursor'] = overlay.show_cursor
            o['show_object_origins'] = overlay.show_object_origins
            o['show_object_origins_all'] = overlay.show_object_origins_all

            return o

    def set_view(self, workspace, view):
        for screen in workspace.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            r3d = space.region_3d

                            r3d.view_location = view['view_location']
                            r3d.view_rotation = view['view_rotation']
                            r3d.view_distance = view['view_distance']

                            # don't set camera views
                            if r3d.view_perspective != 'CAMERA':
                                r3d.view_perspective = view['view_perspective']

                                r3d.is_perspective = view['is_perspective']
                                r3d.is_orthographic_side_view = view['is_side_view']

                            return

    def get_view(self, context, workspace):
        if context.space_data.type == 'VIEW_3D':
            r3d = context.space_data.region_3d

            view = {}

            # note, you could get/set the view_matrix, but matrix even with view_distance won't bring over the cameras orbit/focus point
            view['view_location'] = r3d.view_location
            view['view_rotation'] = r3d.view_rotation
            view['view_distance'] = r3d.view_distance

            view['view_perspective'] = r3d.view_perspective

            view['is_perspective'] = r3d.is_perspective
            view['is_side_view'] = r3d.is_orthographic_side_view

            # don't get camera views
            return view if r3d.view_perspective != 'CAMERA' else None
