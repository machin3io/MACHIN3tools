import bpy
from bpy.props import EnumProperty, BoolProperty
import bmesh
from ... items import uv_axis_items, uv_align_axis_mapping_dict, align_type_items, align_direction_items


class AlignUV(bpy.types.Operator):
    bl_idname = "machin3.align_uv"
    bl_label = "MACHIN3: Align (UV)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Align verts based on min/max UV values"

    type: EnumProperty(name="Type", items=align_type_items, default="MIN")

    axis: EnumProperty(name="Axis", items=uv_axis_items, default="U")

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH" and context.space_data.type == 'IMAGE_EDITOR'

    def execute(self, context):
        self.uv_align(context, self.type, uv_align_axis_mapping_dict[self.axis])
        return {'FINISHED'}

    def uv_align(self, context, type, axis):
        active = context.active_object
        sync = context.scene.tool_settings.use_uv_select_sync

        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        uvs = bm.loops.layers.uv.verify()

        # get selected loops
        if sync:
            loops = [l for v in bm.verts if v.select for l in v.link_loops]

        else:
            loops = [l for f in bm.faces if f.select for l in f.loops if l[uvs].select]

        axiscoords = [l[uvs].uv[axis] for l in loops]

        # get target value depending on type
        if type == "MIN":
            target = min(axiscoords)

        elif type == "MAX":
            target = max(axiscoords)

        elif type == "ZERO":
            target = 0

        elif type == "AVERAGE":
            target = sum(axiscoords) / len(axiscoords)

        elif type == "CURSOR":
            target = context.space_data.cursor_location[axis]

        # set the new coordinates
        for l in loops:
            l[uvs].uv[axis] = target

        bmesh.update_edit_mesh(active.data)
