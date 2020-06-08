import bpy
from bpy.props import StringProperty, BoolProperty
from ... utils.collection import get_groups_collection, get_scene_collections


# TODO: store selected objects in blend file an immedeatly relink it into the current scene, call it StoreCollection() or SaveCollection()


class CreateCollection(bpy.types.Operator):
    bl_idname = "machin3.create_collection"
    bl_label = "MACHIN3: Create Collection"
    bl_description = "description"
    bl_options = {'REGISTER', 'UNDO'}

    def update_name(self, context):
        name = self.name.strip()
        col = bpy.data.collections.get(name)

        if col:
            self.isduplicate = True
        else:
            self.isduplicate = False


    name: StringProperty("Collection Name", default="", update=update_name)

    # hiddem
    isduplicate: BoolProperty("is duplicate name")


    def draw(self, context):
        layout = self.layout

        column = layout.column()

        column.prop(self, "name", text="Name")
        if self.isduplicate:
            column.label(text="Collection '%s' exists already" % (self.name.strip()), icon='ERROR')

    def invoke(self, context, event):
        wm = context.window_manager

        return wm.invoke_props_dialog(self, width=300)

    def execute(self, context):
        name = self.name.strip()

        # create collection
        col = bpy.data.collections.new(name=name)

        # link it to the active collection
        acol = context.view_layer.active_layer_collection.collection
        acol.children.link(col)

        # reset the name prop
        self.name = ''

        return {'FINISHED'}


class AddToCollection(bpy.types.Operator):
    bl_idname = "machin3.add_to_collection"
    bl_label = "MACHIN3: Add to Collection"
    bl_description = "description"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        # ensure selection has an active object, otherwise link_to_collection will throw and error
        active = context.active_object
        if active not in context.selected_objects:
            context.view_layer.objects.active = context.selected_objects[0]

        bpy.ops.object.link_to_collection('INVOKE_DEFAULT')

        return {'FINISHED'}


class RemoveFromCollection(bpy.types.Operator):
    bl_idname = "machin3.remove_from_collection"
    bl_label = "MACHIN3: Remove from Collection"
    bl_description = "description"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        # ensure selection has an active object, otherwise link_to_collection will throw and error
        active = context.active_object
        if active not in context.selected_objects:
            context.view_layer.objects.active = context.selected_objects[0]


        bpy.ops.collection.objects_remove('INVOKE_DEFAULT')

        return {'FINISHED'}


class MoveToCollection(bpy.types.Operator):
    bl_idname = "machin3.move_to_collection"
    bl_label = "MACHIN3: Move to Collection"
    bl_description = "description"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # ensure selection has an active object, otherwise link_to_collection will throw and error
        active = context.active_object
        if active not in context.selected_objects:
            context.view_layer.objects.active = context.selected_objects[0]

        bpy.ops.object.move_to_collection('INVOKE_DEFAULT')

        return {'FINISHED'}


class SortGroupProGroups(bpy.types.Operator):
    bl_idname = "machin3.sort_grouppro_groups"
    bl_label = "MACHIN3: sort_grouppro_groups"
    bl_description = "Sort GroupPro Groups into Groups Collection"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        gpcol = get_groups_collection(context.scene)

        groups = [obj for obj in bpy.data.objects if obj.type == "EMPTY" and obj.instance_collection]

        # link
        for group in groups:
            if group.name not in gpcol.objects:
                gpcol.objects.link(group)

        # TODO: investigate why GP has a once collection requirement for the empties
        # remove from other collections
        for group in groups:
            for col in group.users_collection:
                if col != gpcol:
                    col.objects.unlink(group)

        return {'FINISHED'}


class Purge(bpy.types.Operator):
    bl_idname = "machin3.purge_collections"
    bl_label = "MACHIN3: Purge Collections"
    bl_description = "Remove empty Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for col in get_scene_collections(context.scene):
            if not any([col.children, col.objects]):
                print("Removing collection '%s'." % (col.name))
                bpy.data.collections.remove(col, do_unlink=True)

        return {'FINISHED'}


class Select(bpy.types.Operator):
    bl_idname = "machin3.select_collection"
    bl_label = "MACHIN3: (De)Select Collection"
    bl_description = "Select Collection Objects\nSHIFT: Select all Collection Objects\nALT: Deselect Collection Objects\nSHIFT+ALT: Deselect all Collection Objects\nCTRL: Toggle Viewport Selection of Collection Objects"
    bl_options = {'REGISTER'}

    name: StringProperty()
    force_all: BoolProperty()

    def invoke(self, context, event):
        col = bpy.data.collections.get(self.name, context.scene.collection)

        objects = col.all_objects if event.shift or self.force_all else col.objects

        if objects:
            hideselect = objects[0].hide_select

            if col:
                for obj in objects:
                    # deselect
                    if event.alt:
                        obj.select_set(False)

                    # toggle hide_select (but only for objects not all_objects)
                    elif event.ctrl:
                        if obj.name in col.objects:
                            obj.hide_select = not hideselect

                    # seleect
                    else:
                        obj.select_set(True)

        self.force_all = False
        return {'FINISHED'}
