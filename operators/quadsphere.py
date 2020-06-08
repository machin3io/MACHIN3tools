import bpy
from bpy.props import IntProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper
from math import radians


class QuadSphere(bpy.types.Operator):
    bl_idname = "machin3.quadsphere"
    bl_label = "MACHIN3: Quadsphere"
    bl_description = "Creates a Quadsphere"
    bl_options = {'REGISTER', 'UNDO'}

    subdivisions: IntProperty(name='Subdivisions', default=4, min=1, max=8)
    shade_smooth: BoolProperty(name="Shade Smooth", default=True)

    align_rotation: BoolProperty(name="Align Rotation", default=True)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row(align=True)
        row.prop(self, "subdivisions")
        row.prop(self, "shade_smooth", toggle=True)
        row.prop(self, "align_rotation", toggle=True)

    @classmethod
    def poll(cls, context):
        return context.mode in ['OBJECT', 'EDIT_MESH']

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(align='CURSOR' if self.align_rotation else 'WORLD')

        if self.shade_smooth:
            bpy.ops.object.shade_smooth()

        mode = bpy.context.mode

        if mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='EDIT')

        for sub in range(self.subdivisions):
            bpy.ops.mesh.subdivide(number_cuts=1, smoothness=1)
            bpy.ops.transform.tosphere(value=1)

        if mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        quadsphere = context.active_object
        quadsphere.data.auto_smooth_angle = radians(60)

        # clear uvs
        mesh = quadsphere.data

        while mesh.uv_layers:
            mesh.uv_layers.remove(mesh.uv_layers[0])

        return {'FINISHED'}
