import bpy
from ... utils.registration import get_prefs

solid_show_overlays = True
material_show_overlays = False
rendered_show_overlays = False
wire_show_overlays = True


def get_description(context, shadetype):
    shading = context.space_data.shading
    overlay = context.space_data.overlay

    if shading.type == shadetype:
        return '%s Overlays for %s Shading' % ('Disable' if overlay.show_overlays else 'Enable', shadetype.capitalize())

    else:
        return 'Switch to %s shading' % (shadetype.capitalize())


class ShadeSolid(bpy.types.Operator):
    bl_idname = "machin3.shade_solid"
    bl_label = "Shade Solid"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'SOLID')

    def execute(self, context):
        global solid_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'SOLID':
            solid_show_overlays = not solid_show_overlays
            overlay.show_overlays = solid_show_overlays

        # change shading to SOLID
        else:
            shading.type = 'SOLID'
            overlay.show_overlays = solid_show_overlays

        return {'FINISHED'}


class ShadeMaterial(bpy.types.Operator):
    bl_idname = "machin3.shade_material"
    bl_label = "Shade Material"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'MATERIAL')

    def execute(self, context):
        global material_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'MATERIAL':
            material_show_overlays = not material_show_overlays
            overlay.show_overlays = material_show_overlays

        # change shading to MATERIAL
        else:
            shading.type = 'MATERIAL'
            overlay.show_overlays = material_show_overlays

        return {'FINISHED'}


class ShadeRendered(bpy.types.Operator):
    bl_idname = "machin3.shade_rendered"
    bl_label = "Shade Rendered"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'RENDERED')

    def execute(self, context):
        global rendered_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'RENDERED':
            rendered_show_overlays = not rendered_show_overlays
            overlay.show_overlays = rendered_show_overlays

        # change shading to RENDERED
        else:
            shading.type = 'RENDERED'
            overlay.show_overlays = rendered_show_overlays

        return {'FINISHED'}


class ShadeWire(bpy.types.Operator):
    bl_idname = "machin3.shade_wire"
    bl_label = "Shade Wire"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        return get_description(context, 'WIREFRAME')

    def execute(self, context):
        global wire_show_overlays

        overlay = context.space_data.overlay
        shading = context.space_data.shading

        # toggle overlays
        if shading.type == 'WIREFRAME':
            wire_show_overlays = not wire_show_overlays
            overlay.show_overlays = wire_show_overlays

        # change shading to WIRE
        else:
            shading.type = 'WIREFRAME'
            overlay.show_overlays = wire_show_overlays

        return {'FINISHED'}


class ToggleOutline(bpy.types.Operator):
    bl_idname = "machin3.toggle_outline"
    bl_label = "Toggle Outline"
    bl_description = "Toggle Object Outlines"
    bl_options = {'REGISTER'}

    def execute(self, context):
        shading = context.space_data.shading

        shading.show_object_outline = not shading.show_object_outline

        return {'FINISHED'}


class ToggleCavity(bpy.types.Operator):
    bl_idname = "machin3.toggle_cavity"
    bl_label = "Toggle Cavity"
    bl_description = "Toggle Cavity (Screen Space Ambient Occlusion)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        scene.M3.show_cavity = not scene.M3.show_cavity

        return {'FINISHED'}


class ToggleCurvature(bpy.types.Operator):
    bl_idname = "machin3.toggle_curvature"
    bl_label = "Toggle Curvature"
    bl_description = "Toggle Curvature (Edge Highlighting)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        scene.M3.show_curvature = not scene.M3.show_curvature

        return {'FINISHED'}


class MatcapSwitch(bpy.types.Operator):
    bl_idname = "machin3.matcap_switch"
    bl_label = "Matcap Switch"
    bl_description = "Quickly Switch between two Matcaps"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        shading = context.space_data.shading
        return shading.type == "SOLID" and shading.light == "MATCAP"

    def execute(self, context):
        shading = context.space_data.shading
        matcap1 = get_prefs().switchmatcap1
        matcap2 = get_prefs().switchmatcap2

        if matcap1 and matcap2 and "NOT FOUND" not in [matcap1, matcap2]:
            if shading.studio_light == matcap1:
                shading.studio_light = matcap2

            elif shading.studio_light == matcap2:
                shading.studio_light = matcap1

            else:
                shading.studio_light = matcap1

        return {'FINISHED'}
