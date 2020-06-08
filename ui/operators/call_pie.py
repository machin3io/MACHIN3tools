import bpy
from bpy.props import StringProperty


class CallMACHIN3toolsPie(bpy.types.Operator):
    bl_idname = "machin3.call_machin3tools_pie"
    bl_label = "MACHIN3: Call MACHIN3tools Pie"
    bl_options = {'REGISTER', 'UNDO'}

    idname: StringProperty()

    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            if self.idname == 'shading_pie':
                engine = context.scene.render.engine
                device = context.scene.cycles.device

                # sync render engine settings
                if engine != context.scene.M3.render_engine and engine in ['BLENDER_EEVEE', 'CYCLES']:
                    context.scene.M3.avoid_update = True
                    context.scene.M3.render_engine = engine

                # sync cyclces device settings
                if engine == 'CYCLES' and device != context.scene.M3.cycles_device:
                    print("syncing device")
                    context.scene.M3.avoid_update = True
                    context.scene.M3.cycles_device = device

                bpy.ops.wm.call_menu_pie(name='MACHIN3_MT_%s' % (self.idname))

        return {'FINISHED'}
