import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty
from .. utils.registration import get_prefs, get_addon
from .. utils.view import update_local_view
from .. items import focus_method_items, focus_levels_items


# TODO: add HUD for local view levels


class Focus(bpy.types.Operator):
    bl_idname = "machin3.focus"
    bl_label = "MACHIN3: Focus"
    bl_options = {'REGISTER', 'UNDO'}

    method: EnumProperty(name="Method", items=focus_method_items, default='VIEW_SELECTED')

    levels: EnumProperty(name="Levels", items=focus_levels_items, description="Switch between single-level Blender native Local View and multi-level MACHIN3 Focus", default="MULTIPLE")
    unmirror: BoolProperty(name="Un-Mirror", default=True)
    ignore_mirrors: BoolProperty(name="Ignore Mirrors", default=True)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text='View Selected' if self.method == 'VIEW_SELECTED' else 'Local View')
        column = box.column()

        if self.method == 'VIEW_SELECTED':
            column.prop(self, "ignore_mirrors", toggle=True)

        # only show tool props when initializing local view, this prevents switching modes and settings while in local view
        elif self.method == 'LOCAL_VIEW' and self.show_tool_props:
            row = column.row()
            row.label(text="Levels")
            row.prop(self, "levels", expand=True)

            column.prop(self, "unmirror", toggle=True)

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D' and context.region.type == 'WINDOW'

    def execute(self, context):
        if self.method == 'VIEW_SELECTED':
            self.view_selected(context)

        elif self.method == 'LOCAL_VIEW':
            self.local_view(context)

        return {'FINISHED'}

    def view_selected(self, context):
        mirrors = []

        if context.mode == 'OBJECT':
            sel = context.selected_objects
            if self.ignore_mirrors:
                mirrors = [mod for obj in sel for mod in obj.modifiers if mod.type == 'MIRROR' and mod.show_viewport]

                for mod in mirrors:
                    mod.show_viewport = False

        if get_prefs().focus_view_transition:
            bpy.ops.view3d.view_selected('INVOKE_DEFAULT')

        else:
            bpy.ops.view3d.view_selected()

        for mod in mirrors:
            mod.show_viewport = True

    def local_view(self, context, debug=False):
        def focus(context, view, sel, history, init=False):
            vis = context.visible_objects
            hidden = [obj for obj in vis if obj not in sel]

            if hidden:
                # initialize
                if init:
                    bpy.ops.view3d.localview(frame_selected=False)

                # hide
                else:
                    update_local_view(view, [(obj, False) for obj in hidden])

                # create new epoch
                epoch = history.add()
                epoch.name = "Epoch %d" % (len(history) - 1)

                # store hidden objects in epoch
                for obj in hidden:
                    entry = epoch.objects.add()
                    entry.obj = obj
                    entry.name = obj.name

                # disable mirror mods and store these unmirrored objects
                if self.unmirror:
                    mirrored = [(obj, mod) for obj in sel for mod in obj.modifiers if mod.type == "MIRROR"]

                    for obj, mod in mirrored:
                        if mod.show_viewport:
                            mod.show_viewport = False

                            entry = epoch.unmirrored.add()
                            entry.obj = obj
                            entry.name = obj.name

        def unfocus(context, view, history):
            last_epoch = history[-1]

            # de-inititalize
            if len(history) == 1:
                bpy.ops.view3d.localview(frame_selected=False)

            # unhide
            else:
                update_local_view(view, [(entry.obj, True) for entry in last_epoch.objects])

            # re-enbable mirror mods
            for entry in last_epoch.unmirrored:
                for mod in entry.obj.modifiers:
                    if mod.type == "MIRROR":
                        mod.show_viewport = True


            # delete the last epoch
            idx = history.keys().index(last_epoch.name)
            history.remove(idx)

        view = context.space_data
        self.show_tool_props = False

        sel = context.selected_objects
        vis = context.visible_objects

        # blender native local view
        if self.levels == "SINGLE":
            if self.unmirror:
                if view.local_view:
                    mirrored = [(obj, mod) for obj in vis for mod in obj.modifiers if mod.type == "MIRROR"]

                else:
                    mirrored = [(obj, mod) for obj in sel for mod in obj.modifiers if mod.type == "MIRROR"]

                for obj, mod in mirrored:
                    mod.show_viewport = True if view.local_view else False


            if not view.local_view:
                self.show_tool_props = True

            bpy.ops.view3d.localview(frame_selected=False)


        # multi level local view
        else:
            history = context.scene.M3.focus_history

            # already in local view
            if view.local_view:

                # go deeper
                if context.selected_objects and not (len(vis) == 1 and vis == sel):
                    focus(context, view, sel, history)

                # go higher
                else:
                    if history:
                        unfocus(context, view, history)

                    # exit local view (for instance, when local view was initiated from batch ops, there won't be a history in that case)
                    else:
                        bpy.ops.view3d.localview(frame_selected=False)

            # initialize local view
            elif context.selected_objects:

                # if you are not in local view, and yet there is a history, clear it
                if history:
                    history.clear()

                self.show_tool_props = True
                focus(context, view, sel, history, init=True)

            if debug:
                for epoch in history:
                    print(epoch.name, ", hidden: ", [obj.name for obj in epoch.objects], ", unmirrored: ", [obj.name for obj in epoch.unmirrored])
