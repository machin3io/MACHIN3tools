import bpy
from bpy.types import Menu
import os
from .. utils.registration import get_prefs, get_addon
from .. utils.ui import get_icon
from .. utils.collection import get_scene_collections
from .. utils.system import abspath

# TODO: snapping pie

# TODO: origin to selection
# TODO: origin to bbox center, top, bottom, etc
# TODO: align origin to cursor, incl rotatation, see https://polycount.com/discussion/comment/2683194/#Comment_2683194

# TODO: modes gpencil: add modal shrinkwrap tool, if gpencil is parented


grouppro = None
decalmachine = None


class PieModes(Menu):
    bl_idname = "MACHIN3_MT_modes_pie"
    bl_label = "Modes"

    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings

        global grouppro
        global decalmachine

        if grouppro is None:
            grouppro, _, _, _ = get_addon("Group Pro")

        if decalmachine is None:
            decalmachine, _, _, _ = get_addon("DECALmachine")


        active = context.active_object

        pie = layout.menu_pie()

        if active:
            if context.mode in ['OBJECT', 'EDIT_MESH', 'EDIT_ARMATURE', 'POSE', 'EDIT_CURVE', 'EDIT_TEXT', 'EDIT_SURFACE', 'EDIT_METABALL', 'EDIT_LATTICE', 'EDIT_GPENCIL', 'PAINT_GPENCIL', 'SCULPT_GPENCIL', 'WEIGHT_GPENCIL']:
                if active.type == 'MESH':
                    if context.area.type == "VIEW_3D":

                        if active.library:
                            blendpath = abspath(active.library.filepath)
                            library = active.library.name

                            op = pie.operator("machin3.open_library_blend", text="Open %s" % (os.path.basename(blendpath)))
                            op.blendpath = blendpath
                            op.library = library

                        else:
                            # 4 - LEFT
                            pie.operator("machin3.mesh_mode", text="Vertex", icon_value=get_icon('vertex')).mode = 'VERT'

                            # 6 - RIGHT
                            pie.operator("machin3.mesh_mode", text="Face", icon_value=get_icon('face')).mode = 'FACE'

                            # 2 - BOTTOM
                            pie.operator("machin3.mesh_mode", text="Edge", icon_value=get_icon('edge')).mode = 'EDGE'

                            # 8 - TOP
                            if context.mode == 'OBJECT' and grouppro and len(context.scene.storedGroupSettings):
                                pie.operator("object.close_grouppro", text="Close Group")

                            else:
                                text, icon = ("Edit", get_icon('edit_mesh')) if active.mode == "OBJECT" else ("Object", get_icon('object'))
                                pie.operator("machin3.edit_mode", text=text, icon_value=icon)

                            # 7 - TOP - LEFT
                            self.draw_mesh_modes(context, pie)

                            # 9 - TOP - RIGHT
                            if context.mode == 'OBJECT' and grouppro:
                                self.draw_grouppro(context, pie)

                            else:
                                pie.separator()

                            # 1 - BOTTOM - LEFT
                            pie.separator()

                            # 3 - BOTTOM - RIGHT
                            if context.mode == "EDIT_MESH":
                                box = pie.split()
                                column = box.column()

                                row = column.row()
                                row.scale_y = 1.2
                                row.prop(context.scene.M3, "pass_through", text="Pass Through" if context.scene.M3.pass_through else "Occlude", icon="XRAY")

                                column.prop(toolsettings, "use_mesh_automerge", text="Auto Merge")

                            else:
                                pie.separator()

                    if context.area.type == "IMAGE_EDITOR":
                        toolsettings = context.scene.tool_settings

                        if context.mode == "OBJECT":
                            # 4 - LEFT
                            pie.operator("machin3.image_mode", text="UV Edit", icon="GROUP_UVS").mode = "UV"

                            # 6 - RIGHT
                            pie.operator("machin3.image_mode", text="Paint", icon="TPAINT_HLT").mode = "PAINT"

                            # 2 - BOTTOM)
                            pie.operator("machin3.image_mode", text="Mask", icon="MOD_MASK").mode = "MASK"

                            # 8 - TOP
                            pie.operator("machin3.image_mode", text="View", icon="FILE_IMAGE").mode = "VIEW"


                        elif context.mode == "EDIT_MESH":
                            # 4 - LEFT
                            pie.operator("machin3.uv_mode", text="Vertex", icon_value=get_icon('vertex')).mode = "VERTEX"

                            # 6 - RIGHT
                            pie.operator("machin3.uv_mode", text="Face", icon_value=get_icon('face')).mode = "FACE"

                            # 2 - BOTTOM
                            pie.operator("machin3.uv_mode", text="Edge", icon_value=get_icon('edge')).mode = "EDGE"

                            # 8 - TOP
                            pie.operator("object.mode_set", text="Object", icon_value=get_icon('object')).mode = "OBJECT"

                            # 7 - TOP - LEFT
                            pie.prop(context.scene.M3, "uv_sync_select", text="Sync Selection", icon="UV_SYNC_SELECT")

                            # 9 - TOP - RIGHT
                            if toolsettings.use_uv_select_sync:
                                pie.separator()
                            else:
                                pie.operator("machin3.uv_mode", text="Island", icon_value=get_icon('island')).mode = "ISLAND"

                            # 1 - BOTTOM - LEFT
                            pie.separator()

                            # 3 - BOTTOM - RIGHT
                            pie.separator()

                elif active.type == 'ARMATURE':
                    # 4 - LEFT
                    pie.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = "EDIT"

                    # 6 - RIGHT
                    pie.operator("object.mode_set", text="Pose", icon='POSE_HLT').mode = "POSE"

                    # 2 - BOTTOM
                    pie.separator()

                    # 8 - TOP
                    if context.mode == "OBJECT" and grouppro and len(context.scene.storedGroupSettings):
                        pie.operator("object.close_grouppro", text="Close Group")

                    else:
                        text, icon = ("Edit", "EDITMODE_HLT") if active.mode == "OBJECT" else ("Object", "OBJECT_DATAMODE")
                        if active.mode == "POSE":
                            pie.operator("object.posemode_toggle", text=text, icon=icon)
                        else:
                            pie.operator("object.editmode_toggle", text=text, icon=icon)

                    # 7 - TOP - LEFT
                    pie.separator()

                    # 9 - TOP - RIGHT
                    if context.mode == 'OBJECT' and grouppro:
                        self.draw_grouppro(context, pie)

                    else:
                        pie.separator()

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    pie.separator()

                elif active.type in ['CURVE', 'FONT', 'SURFACE', 'META', 'LATTICE']:
                    # 4 - LEFT
                    pie.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = "EDIT"

                    # & - RIGHT
                    pie.separator()

                    # 1 - BOTTOM
                    pie.separator()

                    # 9 - TOP
                    if context.mode == 'OBJECT' and grouppro and len(context.scene.storedGroupSettings):
                        pie.operator("object.close_grouppro", text="Close Group")

                    else:
                        text, icon = ("Edit", "EDITMODE_HLT") if active.mode == "OBJECT" else ("Object", "OBJECT_DATAMODE")
                        pie.operator("object.editmode_toggle", text=text, icon=icon)

                    # 7 - TOP - LEFT
                    pie.separator()

                    # 9 - TOP - RIGHT
                    if context.mode == 'OBJECT' and grouppro:
                        self.draw_grouppro(context, pie)

                    else:
                        pie.separator()

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    if bpy.context.mode in ['EDIT_SURFACE', 'EDIT_METABALL']:
                        box = pie.split()
                        column = box.column()

                        row = column.row()
                        row.scale_y = 1.2
                        row.prop(context.scene.M3, "pass_through", text="Pass Through" if context.scene.M3.pass_through else "Occlude", icon="XRAY")
                    else:
                        pie.separator()

                elif active.type == 'GPENCIL':
                    gpd = context.gpencil_data

                    # 4 - LEFT
                    pie.operator("object.mode_set", text="Draw", icon='GREASEPENCIL').mode = "PAINT_GPENCIL"

                    # 6 - RIGHT
                    pie.operator("object.mode_set", text="Sculpt", icon='SCULPTMODE_HLT').mode = "SCULPT_GPENCIL"

                    # 2 - BOTTOM
                    pie.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = "EDIT_GPENCIL"

                    # 8 - TOP
                    if context.mode == 'OBJECT' and grouppro and len(context.scene.storedGroupSettings):
                        pie.operator("object.close_grouppro", text="Close Group")

                    else:
                        text, icon = ("Draw", "GREASEPENCIL") if active.mode == "OBJECT" else ("Object", "OBJECT_DATAMODE")

                        if active.mode == "WEIGHT_GPENCIL":
                            pie.operator("gpencil.weightmode_toggle", text=text, icon=icon)
                        elif active.mode == "EDIT_GPENCIL":
                            pie.operator("gpencil.editmode_toggle", text=text, icon=icon)
                        elif active.mode == "SCULPT_GPENCIL":
                            pie.operator("gpencil.sculptmode_toggle", text=text, icon=icon)
                        else:
                            pie.operator("gpencil.paintmode_toggle", text=text, icon=icon)

                    # 7 - TOP - LEFT
                    self.draw_gp_modes(context, pie)

                    # 9 - TOP - RIGHT
                    if context.mode == 'OBJECT' and grouppro:
                        self.draw_grouppro(context, pie)

                    else:
                        pie.separator()

                    # 1 - BOTTOM - LEFT
                    box = pie.split()
                    column = box.column()
                    column.scale_y = 1.2
                    column.scale_x = 1.2

                    if context.mode == "PAINT_GPENCIL":
                        row = column.row(align=True)
                        row.prop(toolsettings, "use_gpencil_draw_onback", text="", icon="MOD_OPACITY")
                        row.prop(toolsettings, "use_gpencil_weight_data_add", text="", icon="WPAINT_HLT")
                        row.prop(toolsettings, "use_gpencil_draw_additive", text="", icon="FREEZE")

                    elif context.mode == "EDIT_GPENCIL":
                        row = column.row(align=True)
                        row.prop(toolsettings, "gpencil_selectmode", text="", expand=True)


                    # 3 - BOTTOM - RIGHT
                    box = pie.split()
                    column = box.column()

                    if context.mode == "EDIT_GPENCIL":
                        row = column.row(align=True)
                        row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

                        r = row.row(align=True)
                        r.active = gpd.use_multiedit
                        r.popover(panel="VIEW3D_PT_gpencil_multi_frame", text="Multiframe")

                        row = column.row(align=True)
                        row.prop(toolsettings.gpencil_sculpt, "use_select_mask", text="")

                        row.popover(panel="VIEW3D_PT_tools_grease_pencil_interpolate", text="Interpolate")

                    elif context.mode == "SCULPT_GPENCIL":
                        row = column.row(align=True)
                        row.prop(toolsettings.gpencil_sculpt, "use_select_mask", text="")

                        row.separator()
                        row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

                        r = row.row(align=True)
                        r.active = gpd.use_multiedit
                        r.popover(panel="VIEW3D_PT_gpencil_multi_frame", text="Multiframe")

                elif active.type == 'EMPTY':
                    # 4 - LEFT
                    if grouppro and active.instance_collection and active.instance_collection.created_with_gp and not active.instance_collection.library:
                        pie.operator("object.edit_grouppro", text="Edit Group")

                    elif active.instance_collection and active.instance_collection.library:
                        blendpath = abspath(active.instance_collection.library.filepath)
                        library = active.instance_collection.library.name

                        op = pie.operator("machin3.open_library_blend", text="Open %s" % (os.path.basename(blendpath)))
                        op.blendpath = blendpath
                        op.library = library

                    else:
                        pie.separator()

                    # 6 - RIGHT
                    pie.separator()

                    # 2 - BOTTOM
                    if grouppro and active.instance_collection and active.instance_collection.created_with_gp and not active.instance_collection.library:
                        if decalmachine:
                            pie.operator("machin3.grouppro_dissolve", text="Dissolve", icon='OUTLINER_OB_GROUP_INSTANCE').maxDept = 0
                        else:
                            pie.operator("object.gpro_converttogeo", icon='OUTLINER_OB_GROUP_INSTANCE').maxDept = 0
                    else:
                        pie.separator()

                    # 8 - TOP
                    if grouppro and len(context.scene.storedGroupSettings):
                        pie.operator("object.close_grouppro", text="Close Group")

                    else:
                        pie.separator()

                    # 7 - TOP - LEFT
                    pie.separator()

                    # 9 - TOP - RIGHT
                    if context.mode == 'OBJECT' and grouppro:
                        self.draw_grouppro(context, pie)

                    else:
                        pie.separator()

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    pie.separator()

            elif context.mode == "SCULPT":
                    # 4 - LEFT
                    pie.separator()

                    # 6 - RIGHT
                    pie.separator()

                    # 2 - BOTTOM
                    pie.separator()

                    # 8 - TOP
                    pie.separator()

                    # 7 - TOP - LEFT
                    self.draw_mesh_modes(context, pie)

                    # 9 - TOP - RIGHT
                    pie.separator()

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    pie.separator()

            elif context.mode == "PAINT_TEXTURE":
                    # 4 - LEFT
                    pie.separator()

                    # 6 - RIGHT
                    pie.separator()

                    # 2 - BOTTOM
                    pie.separator()

                    # 8 - TOP
                    pie.separator()

                    # 7 - TOP - LEFT
                    self.draw_mesh_modes(context, pie)

                    # 9 - TOP - RIGHT
                    box = pie.split()
                    column = box.column()
                    column.scale_y = 1.5
                    column.scale_x = 1.5

                    row = column.row(align=True)
                    row.prop(active.data, "use_paint_mask", text="", icon="FACESEL")

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    pie.separator()

            elif context.mode == "PAINT_WEIGHT":
                    # 4 - LEFT
                    pie.separator()

                    # 6 - RIGHT
                    pie.separator()

                    # 2 - BOTTOM
                    pie.separator()

                    # 8 - TOP
                    pie.separator()

                    # 7 - TOP - LEFT
                    self.draw_mesh_modes(context, pie)

                    # 9 - TOP - RIGHT
                    box = pie.split()
                    column = box.column()
                    column.scale_y = 1.5
                    column.scale_x = 1.5

                    row = column.row(align=True)
                    row.prop(active.data, "use_paint_mask", text="", icon="FACESEL")
                    row.prop(active.data, "use_paint_mask_vertex", text="", icon="VERTEXSEL")

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    pie.separator()

            elif context.mode == "PAINT_VERTEX":
                    # 4 - LEFT
                    pie.separator()

                    # 6 - RIGHT
                    pie.separator()

                    # 2 - BOTTOM
                    pie.separator()

                    # 8 - TOP
                    pie.separator()

                    # 7 - TOP - LEFT
                    self.draw_mesh_modes(context, pie)

                    # 9 - TOP - RIGHT
                    box = pie.split()
                    column = box.column()
                    column.scale_y = 1.5
                    column.scale_x = 1.5

                    row = column.row(align=True)
                    row.prop(active.data, "use_paint_mask", text="", icon="FACESEL")
                    row.prop(active.data, "use_paint_mask_vertex", text="", icon="VERTEXSEL")

                    # 1 - BOTTOM - LEFT
                    pie.separator()

                    # 3 - BOTTOM - RIGHT
                    pie.separator()

        # no active object
        else:
            # 4 - LEFT
            pie.separator()

            # 6 - RIGHT
            pie.separator()

            # 2 - BOTTOM
            pie.separator()

            # 8 - TOP
            if grouppro and len(context.scene.storedGroupSettings):
                pie.operator("object.close_grouppro", text="Close Group")

            else:
                pie.separator()

            # 7 - TOP - LEFT
            pie.separator()

            # 9 - TOP - RIGHT
            if context.mode == 'OBJECT' and grouppro:
                self.draw_grouppro(context, pie, addremove=False)

            else:
                pie.separator()

            # 1 - BOTTOM - LEFT
            pie.separator()

            # 3 - BOTTOM - RIGHT
            pie.separator()

    def draw_grouppro(self, context, layout, addremove=True):
        box = layout.split()
        column = box.column()
        column.scale_y = 1.5

        # group pro "object mode"
        if len(context.scene.storedGroupSettings) == 0:
            row = column.split(factor=0.7, align=True)
            row.operator("wm.call_menu_pie", text="GroupPro", icon='STICKY_UVS_LOC').name = "GP_MT_grouppro_main_pie"
            row.operator("object.create_grouppro", text="Create")

        # group pro "edit mode"
        else:
            row = column.row()
            row.operator("wm.call_menu_pie", text="GroupPro", icon='STICKY_UVS_LOC').name = "GP_MT_grouppro_main_pie"

            if addremove:
                r = row.row(align=True)
                r.scale_x = 1.2
                r.operator("object.add_to_grouppro", text="", icon='ADD')
                r.operator("object.remove_from_grouppro", text="", icon='REMOVE')

    def draw_gp_modes(self, context, pie):
        box = pie.split()
        column = box.column()
        column.scale_y = 1.5
        column.scale_x = 1.5

        row = column.row(align=True)
        r = row.row(align=True)
        r.active = False if context.mode == "WEIGHT_GPENCIL" else True
        r.operator("object.mode_set", text="", icon="WPAINT_HLT").mode = 'WEIGHT_GPENCIL'
        r = row.row(align=True)
        r.active = False if context.mode == "PAINT_GPENCIL" else True
        r.operator("object.mode_set", text="", icon="GREASEPENCIL").mode = 'PAINT_GPENCIL'
        r = row.row(align=True)
        r.active = False if context.mode == "SCULPT_GPENCIL" else True
        r.operator("object.mode_set", text="", icon="SCULPTMODE_HLT").mode = 'SCULPT_GPENCIL'
        r = row.row(align=True)
        r.active = False if context.mode == "OBJECT" else True
        r.operator("object.mode_set", text="", icon="OBJECT_DATA").mode = 'OBJECT'
        r = row.row(align=True)
        r.active = False if context.mode == 'EDIT_GPENCIL' else True
        r.operator("object.mode_set", text="", icon="EDITMODE_HLT").mode = 'EDIT_GPENCIL'

    def draw_mesh_modes(self, context, pie):
        box = pie.split()
        column = box.column()
        column.scale_y = 1.5
        column.scale_x = 1.5

        row = column.row(align=True)

        r = row.row(align=True)
        r.active = False if context.mode == 'PAINT_GPENCIL' else True
        r.operator("machin3.surface_draw_mode", text="", icon="GREASEPENCIL")

        r = row.row(align=True)
        r.active = False if context.mode == 'TEXTURE_PAINT' else True
        r.operator("object.mode_set", text="", icon="TPAINT_HLT").mode = 'TEXTURE_PAINT'

        r = row.row(align=True)
        r.active = False if context.mode == 'WEIGHT_PAINT' else True
        r.operator("object.mode_set", text="", icon="WPAINT_HLT").mode = 'WEIGHT_PAINT'

        r = row.row(align=True)
        r.active = False if context.mode == 'VERTEX_PAINT' else True
        r.operator("object.mode_set", text="", icon="VPAINT_HLT").mode = 'VERTEX_PAINT'

        r = row.row(align=True)
        r.active = False if context.mode == 'SCULPT' else True
        r.operator("object.mode_set", text="", icon="SCULPTMODE_HLT").mode = 'SCULPT'

        r = row.row(align=True)
        r.active = False if context.mode == 'OBJECT' else True
        r.operator("object.mode_set", text="", icon="OBJECT_DATA").mode = 'OBJECT'

        r = row.row(align=True)
        r.active = False if context.mode == 'EDIT_MESH' else True
        r.operator("object.mode_set", text="", icon="EDITMODE_HLT").mode = 'EDIT'


class PieSave(Menu):
    bl_idname = "MACHIN3_MT_save_pie"
    bl_label = "Save, Open, Append"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("wm.open_mainfile", text="Open...", icon_value=get_icon('open'))

        # 6 - RIGHT
        pie.operator("machin3.save", text="Save", icon_value=get_icon('save'))

        # 2 - BOTTOM
        pie.operator("wm.save_as_mainfile", text="Save As..", icon_value=get_icon('save_as'))

        # 8 - TOP
        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        self.draw_left_column(b)

        column = box.column()
        b = column.box()
        self.draw_center_column_top(context, b)

        if bpy.data.filepath:
            b = column.box()
            self.draw_center_column_bottom(b)

        b = box.box()
        self.draw_right_column(b)

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        pie.operator("machin3.new", text="New", icon_value=get_icon('new'))

        # 3 - BOTTOM - RIGHT
        pie.operator("machin3.save_incremental", text="Incremental Save", icon_value=get_icon('save_incremental'))

    def draw_left_column(self, layout):
        column = layout.column(align=True)

        column.scale_x = 1.1

        row = column.row(align=True)
        row.scale_y = 1.2
        row.operator("machin3.load_most_recent", text="(R) Most Recent", icon_value=get_icon('open_recent'))
        # row.operator("wm.call_menu", text="All Recent", icon_value=get_icon('open_recent')).name = "INFO_MT_file_open_recent"
        row.operator("wm.call_menu", text="All Recent", icon_value=get_icon('open_recent')).name = "TOPBAR_MT_file_open_recent"

        column.separator()
        column.operator("wm.recover_auto_save", text="Recover Auto Save...", icon_value=get_icon('recover_auto_save'))
        # col.operator("wm.recover_last_session", text="Recover Last Session", icon='RECOVER_LAST')
        column.operator("wm.revert_mainfile", text="Revert", icon_value=get_icon('revert'))

    def draw_center_column_top(self, context, layout):
        column = layout.column(align=True)

        row = column.split(factor=0.25, align=True)
        row.label(text="OBJ")
        r = row.row(align=True)
        r.operator("import_scene.obj", text="Import", icon_value=get_icon('import'))
        r.operator("export_scene.obj", text="Export", icon_value=get_icon('export')).use_selection = True if context.selected_objects else False

        row = column.split(factor=0.25, align=True)
        row.label(text="FBX")
        r = row.row(align=True)
        r.operator("import_scene.fbx", text="Import", icon_value=get_icon('import'))
        r.operator("export_scene.fbx", text="Export", icon_value=get_icon('export')).use_selection = True if context.selected_objects else False

    def draw_center_column_bottom(self, layout):
        column = layout.column(align=True)

        row = column.split(factor=0.5, align=True)
        row.scale_y = 1.2
        row.operator("machin3.load_previous", text="Previous", icon_value=get_icon('open_previous'))
        row.operator("machin3.load_next", text="Next", icon_value=get_icon('open_next'))

    def draw_right_column(self, layout):
        column = layout.column(align=True)

        row = column.row()
        r = row.row(align=True)
        r.operator("wm.append", text="Append", icon_value=get_icon('append'))
        r.operator("wm.link", text="Link", icon_value=get_icon('link'))

        r = row.row(align=True)
        r.operator("wm.call_menu", text='', icon_value=get_icon('external_data')).name = "TOPBAR_MT_file_external_data"
        r.operator("machin3.purge_orphans", text="Purge")

        # append world and materials

        appendworldpath = get_prefs().appendworldpath
        appendmatspath = get_prefs().appendmatspath

        if any([appendworldpath, appendmatspath]):
            column.separator()

            if appendworldpath:
                row = column.split(factor=0.8, align=True)
                row.scale_y = 1.2
                row.operator("machin3.append_world", text="World", icon_value=get_icon('world'))
                row.operator("machin3.load_world_source", text="", icon_value=get_icon('open_world'))

            if appendmatspath:
                row = column.split(factor=0.8, align=True)
                row.scale_y = 1.2
                row.operator("wm.call_menu", text="Material", icon_value=get_icon('material')).name = "MACHIN3_MT_append_materials"
                row.operator("machin3.load_materials_source", text="", icon_value=get_icon('open_material'))


class PieShading(Menu):
    bl_idname = "MACHIN3_MT_shading_pie"
    bl_label = "Shading and Overlays"

    def draw(self, context):
        layout = self.layout

        view = context.space_data
        active = context.active_object

        overlay = view.overlay
        shading = view.shading

        pie = layout.menu_pie()

        # 4 - LEFT
        text, icon = self.get_text_icon(context, "SOLID")
        pie.operator("machin3.shade_solid", text=text, icon=icon, depress=shading.type == 'SOLID' and overlay.show_overlays)

        # 6 - RIGHT
        text, icon = self.get_text_icon(context, "MATERIAL")
        pie.operator("machin3.shade_material", text=text, icon=icon, depress=shading.type == 'MATERIAL' and overlay.show_overlays)

        # 2 - BOTTOM
        pie.separator()

        # 8 - TOP
        box = pie.split()

        if (active and active.select_get()) or context.mode == 'EDIT_MESH':
            b = box.box()
            self.draw_object_box(active, view, b)


        if overlay.show_overlays and shading.type == 'SOLID':
            column = box.column()
            b = column.box()
            self.draw_overlay_box(context, view, b)

            b = column.box()
            self.draw_solid_box(context, view, b)

        elif overlay.show_overlays:
            b = box.box()
            self.draw_overlay_box(context, view, b)

        elif shading.type == 'SOLID':
            b = box.box()
            self.draw_solid_box(context, view, b)


        b = box.box()
        self.draw_shade_box(context, view, b)

        if view.shading.type == "MATERIAL" or (view.shading.type == 'RENDERED' and context.scene.render.engine == 'BLENDER_EEVEE'):
            b = box.box()
            self.draw_eevee_box(context, view, b)

        elif view.shading.type == 'RENDERED' and context.scene.render.engine == 'CYCLES':
            b = box.box()
            self.draw_cycles_box(context, view, b)

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        text, icon = self.get_text_icon(context, "WIREFRAME")
        pie.operator("machin3.shade_wire", text=text, icon=icon, depress=shading.type == 'WIREFRAME' and overlay.show_overlays)

        # 3 - BOTTOM - RIGHT
        text, icon = self.get_text_icon(context, "RENDERED")
        pie.operator("machin3.shade_rendered", text=text, icon=icon, depress=shading.type == 'RENDERED' and overlay.show_overlays)

    def draw_overlay_box(self, context, view, layout):
        overlay = context.space_data.overlay
        perspective_type = view.region_3d.view_perspective

        column = layout.column(align=True)

        row = column.split(factor=0.5, align=True)
        row.prop(view.overlay, "show_cursor", text="3D Cursor")
        r = row.row(align=True)
        r.prop(view.overlay, "show_object_origins", text="Origins")

        rr = r.row(align=True)
        rr.active = view.overlay.show_object_origins
        rr.prop(view.overlay, "show_object_origins_all", text="All")

        if view.shading.type == 'SOLID' and view.overlay.show_overlays:
            row = column.split(factor=0.5, align=True)
            row.prop(view.shading, "show_backface_culling")
            row.prop(view.overlay, "show_relationship_lines")

        elif view.shading.type == 'SOLID':
            row = column.row(align=True)
            row.prop(view.shading, "show_backface_culling")

        elif view.overlay.show_overlays:
            row = column.row(align=True)
            row.prop(view.overlay, "show_relationship_lines")

        if view.overlay.show_overlays:
            if context.mode == 'EDIT_MESH':
                row = column.split(factor=0.5, align=True)
                row.prop(view.overlay, "show_face_orientation")
                row.prop(view.overlay, "show_extra_indices")
            else:
                row = column.row(align=True)
                row.prop(view.overlay, "show_face_orientation")

        column.separator()

        row = column.split(factor=0.4, align=True)
        row.operator("machin3.toggle_grid", text="Grid", icon="GRID", depress=overlay.show_ortho_grid if perspective_type == 'ORTHO' and view.region_3d.is_orthographic_side_view else overlay.show_floor)
        r = row.row(align=True)
        r.active = view.overlay.show_floor
        r.prop(view.overlay, "show_axis_x", text="X", toggle=True)
        r.prop(view.overlay, "show_axis_y", text="Y", toggle=True)
        r.prop(view.overlay, "show_axis_z", text="Z", toggle=True)

        row = column.split(factor=0.4, align=True)
        row.operator("machin3.toggle_wireframe", text="Wireframe", icon_value=get_icon('wireframe'), depress=context.mode=='OBJECT' and overlay.show_wireframes)

        r = row.row(align=True)
        if context.mode == "OBJECT":
            r.active = view.overlay.show_wireframes
            r.prop(view.overlay, "wireframe_threshold", text="Threshold")
        elif context.mode == "EDIT_MESH":
            r.active = view.shading.show_xray
            r.prop(view.shading, "xray_alpha", text="X-Ray")

        # object axes
        hasobjectaxes = True if bpy.app.driver_namespace.get('draw_object_axes') else False

        row = column.split(factor=0.4, align=True)
        row.operator("machin3.toggle_object_axes", text="(E) Object Axes", depress=hasobjectaxes)
        r = row.row(align=True)
        r.active = hasobjectaxes
        r.prop(context.scene.M3, "object_axes_size", text="")
        r.prop(context.scene.M3, "object_axes_alpha", text="")

        column.separator()

        # camera clipping
        row = column.split(factor=0.4, align=True)
        row.label(text='Camera Clipping')
        r = row.row(align=True)
        r.active = True
        r.prop(view, "clip_start", text="")
        r.prop(view, "clip_end", text="")

    def draw_solid_box(self, context, view, layout):
        shading = context.space_data.shading

        column = layout.column(align=True)

        row = column.split(factor=0.4, align=True)
        row.operator("machin3.toggle_outline", text="(Q) Outline", depress=shading.show_object_outline)
        row.prop(view.shading, "object_outline_color", text="")

        # cavity
        hascavity = view.shading.show_cavity and view.shading.cavity_type in ['WORLD', 'BOTH']

        row = column.split(factor=0.4, align=True)
        row.operator("machin3.toggle_cavity", text="Cavity", depress=hascavity)
        r = row.row(align=True)
        r.active = hascavity
        r.prop(view.shading, "cavity_valley_factor", text="")
        r.prop(context.scene.display, "matcap_ssao_distance", text="")

        # curvature
        hascurvature = view.shading.show_cavity and view.shading.cavity_type in ['SCREEN', 'BOTH']

        row = column.split(factor=0.4, align=True)
        row.operator("machin3.toggle_curvature", text="(V) Curvature", depress=hascurvature)
        r = row.row(align=True)
        r.active = hascurvature
        r.prop(view.shading, "curvature_ridge_factor", text="")
        r.prop(view.shading, "curvature_valley_factor", text="")

    def draw_object_box(self, active, view, layout):
        overlay = view.overlay
        shading = view.shading

        column = layout.column(align=True)

        row = column.row()
        row = column.split(factor=0.6)
        row.prop(active, "name", text="")

        if active.type == 'ARMATURE':
            row.prop(active.data, "display_type", text="")
        else:
            row.prop(active, "display_type", text="")

        if overlay.show_overlays and shading.type == 'SOLID':
            row = column.split(factor=0.6)
            r = row.row(align=True)
            r.prop(active, "show_name", text="Name")

            if active.type == 'ARMATURE':
                r.prop(active.data, "show_axes", text="Axes")
            else:
                r.prop(active, "show_axis", text="Axis")

            r = row.row()
            r.prop(active, "show_in_front", text="In Front")
            if shading.color_type == 'OBJECT':
                r.prop(active, "color", text="")

        elif overlay.show_overlays:
            row = column.split(factor=0.6)
            row.prop(active, "show_name", text="Name")

            if active.type == 'ARMATURE':
                row.prop(active.data, "show_axes", text="Axes")
            else:
                row.prop(active, "show_axis", text="Axis")

        elif shading.type == 'SOLID':
            if shading.color_type == 'OBJECT':
                row = column.split(factor=0.5)
                row.prop(active, "show_in_front", text="In Front")
                row.prop(active, "color", text="")

            else:
                row = column.row()
                row.prop(active, "show_in_front", text="In Front")


        if active.type == "MESH":
            mesh = active.data

            column.separator()
            row = column.split(factor=0.55, align=True)
            r = row.row(align=True)
            r.operator("machin3.shade_smooth", text="Smooth", icon_value=get_icon('smooth'))
            r.operator("machin3.shade_flat", text="Flat", icon_value=get_icon('flat'))

            icon = "CHECKBOX_HLT" if mesh.use_auto_smooth else "CHECKBOX_DEHLT"
            row.operator("machin3.toggle_auto_smooth", text="AutoSmooth", icon=icon).angle = 0

            row = column.split(factor=0.55, align=True)
            r = row.row(align=True)
            r.active = not mesh.has_custom_normals
            for angle in [30, 60, 90, 180]:
                r.operator("machin3.toggle_auto_smooth", text=str(angle)).angle = angle

            r = row.row(align=True)
            r.active = not mesh.has_custom_normals and mesh.use_auto_smooth
            r.prop(mesh, "auto_smooth_angle")

            if mesh.use_auto_smooth:
                if mesh.has_custom_normals:
                    column.operator("mesh.customdata_custom_splitnormals_clear", text="Clear Custom Normals")

            if active.mode == 'EDIT' and view.overlay.show_overlays:
                column.separator()

                row = column.split(factor=0.25, align=True)
                row.label(text='Normals')
                row.prop(view.overlay, "show_vertex_normals", text="", icon='NORMALS_VERTEX')
                row.prop(view.overlay, "show_split_normals", text="", icon='NORMALS_VERTEX_FACE')
                row.prop(view.overlay, "show_face_normals", text="", icon='NORMALS_FACE')

                r = row.row(align=True)
                r.active = any([view.overlay.show_vertex_normals, view.overlay.show_face_normals, view.overlay.show_split_normals])
                r.prop(view.overlay, "normals_length", text="Size")

                row = column.split(factor=0.25, align=True)
                row.label(text='Edges')
                row.prop(view.overlay, "show_edge_crease", text="Creases", toggle=True)
                row.prop(view.overlay, "show_edge_sharp", text="Sharp", toggle=True)
                row.prop(view.overlay, "show_edge_bevel_weight", text="Bevel", toggle=True)
                row.prop(view.overlay, "show_edge_seams", text="Seams", toggle=True)
                # row.prop(view.overlay, "show_freestyle_edge_marks", text="Freestyle", toggle=True)

    def draw_shade_box(self, context, view, layout):
        column = layout.column(align=True)

        # SOLID

        if view.shading.type == "SOLID":

            # light type
            row = column.row(align=True)
            # row.scale_y = 1.5
            row.prop(view.shading, "light", expand=True)

            # studio / matcap selection
            if view.shading.light in ["STUDIO", "MATCAP"]:
                row = column.row()
                row.template_icon_view(view.shading, "studio_light", show_labels=True, scale=4, scale_popup=3)

            # studio rotation, same as world rotation in lookdev
            if view.shading.light == "STUDIO":
                row = column.split(factor=0.3, align=True)
                row.prop(view.shading, "use_world_space_lighting", text='World Space', icon='WORLD')
                r = row.row(align=True)
                r.active = view.shading.use_world_space_lighting
                r.prop(view.shading, "studiolight_rotate_z", text="Rotation")

            # switch matcap
            if view.shading.light == "MATCAP":
                row = column.row(align=True)
                row.operator("machin3.matcap_switch", text="(X) Matcap Switch")
                row.operator('view3d.toggle_matcap_flip', text="Matcap Flip", icon='ARROW_LEFTRIGHT')

            # color type
            row = column.row(align=True)
            row.prop(view.shading, "color_type", expand=True)

            # single color
            if view.shading.color_type == 'SINGLE':
                column.prop(view.shading, "single_color", text="")

            elif view.shading.color_type == 'MATERIAL':
                column.operator("machin3.colorize_materials", text='Colorize Materials', icon='MATERIAL')

            elif view.shading.color_type == 'OBJECT':
                r = column.split(factor=0.12, align=True)
                r.label(text="from")
                r.operator("machin3.colorize_objects_from_active", text='Active', icon='OBJECT_DATA')
                r.operator("machin3.colorize_objects_from_materials", text='Material', icon='MATERIAL')
                r.operator("machin3.colorize_objects_from_collections", text='Collection', icon='OUTLINER_OB_GROUP_INSTANCE')


        # WIREFRAME

        elif view.shading.type == "WIREFRAME":
            row = column.row()
            # # TODO: make the whoe scene toggle an op called by pressing X
            row.prop(view.shading, "show_xray_wireframe", text="")
            row.prop(view.shading, "xray_alpha_wireframe", text="X-Ray")

            # wireframe color type
            row = column.row(align=True)
            row.prop(view.shading, "wireframe_color_type", expand=True)


        # LOOKDEV and RENDERED

        elif view.shading.type in ['MATERIAL', 'RENDERED']:

            if view.shading.type == 'RENDERED':
                row = column.split(factor=0.3, align=True)
                row.scale_y = 1.2
                row.label(text='Engine')
                row.prop(context.scene.M3, 'render_engine', expand=True)
                column.separator()


            # use scene lights and world
            studio_worlds = [w for w in context.preferences.studio_lights if os.path.basename(os.path.dirname(w.path)) == "world"]

            if any([bpy.data.lights, studio_worlds]):
                row = column.row(align=True)

                if bpy.data.lights:
                    if view.shading.type == 'MATERIAL':
                        row.prop(view.shading, "use_scene_lights")

                    elif view.shading.type == 'RENDERED':
                        row.prop(view.shading, "use_scene_lights_render")

                if studio_worlds:
                    if view.shading.type == 'MATERIAL':
                        row.prop(view.shading, "use_scene_world")
                    elif view.shading.type == 'RENDERED':
                        row.prop(view.shading, "use_scene_world_render")


                    # world hdri selection and manipulation
                    if (view.shading.type == 'MATERIAL' and not view.shading.use_scene_world) or (view.shading.type == 'RENDERED' and not view.shading.use_scene_world_render):
                        row = column.row(align=True)
                        row.template_icon_view(view.shading, "studio_light", scale=4, scale_popup=4)

                        if (view.shading.type == 'MATERIAL' or (view.shading.type == 'RENDERED' and context.scene.render.engine == 'BLENDER_EEVEE')) and view.shading.studiolight_background_alpha:
                            r = column.split(factor=0.5, align=True)
                            r.prop(view.shading, "studiolight_rotate_z", text="Rotation")
                            r.prop(view.shading, "studiolight_background_blur")
                        else:
                            column.prop(view.shading, "studiolight_rotate_z", text="Rotation")

                        r = column.split(factor=0.5, align=True)
                        r.prop(view.shading, "studiolight_intensity")
                        r.prop(view.shading, "studiolight_background_alpha")


            # world background node props

            if not studio_worlds or (view.shading.type == 'MATERIAL' and view.shading.use_scene_world) or (view.shading.type == 'RENDERED' and view.shading.use_scene_world_render):
                world = context.scene.world
                if world:
                    if world.use_nodes:
                        tree = context.scene.world.node_tree
                        output = tree.nodes.get("World Output")

                        if output:
                            input_surf = output.inputs.get("Surface")

                            if input_surf:
                                if input_surf.links:
                                    node = input_surf.links[0].from_node

                                    if node.type == "BACKGROUND":
                                        color = node.inputs['Color']
                                        strength = node.inputs['Strength']

                                        if color.links:
                                            column.prop(strength, "default_value", text="Background Strength")
                                        else:
                                            row = column.split(factor=0.7, align=True)
                                            row.prop(strength, "default_value", text="Background Strength")
                                            row.prop(color, "default_value", text="")

            if view.shading.type == 'RENDERED':
                column.prop(context.scene.render, 'film_transparent')

    def draw_eevee_box(self, context, view, layout):
        column = layout.column(align=True)

        row = column.row(align=True)
        row.label(text='Eevee Settings')
        row.prop(context.scene.M3, "eevee_preset", expand=True)

        # SSR

        col = column.column(align=True)

        icon = "TRIA_DOWN" if context.scene.eevee.use_ssr else "TRIA_RIGHT"
        col.prop(context.scene.eevee, "use_ssr", icon=icon)
        if context.scene.eevee.use_ssr:
            row = col.row(align=True)
            row.prop(context.scene.eevee, "ssr_thickness")
            row.prop(context.scene.eevee, "use_ssr_halfres")

            row = col.row(align=True)
            row.prop(context.scene.eevee, "use_ssr_refraction")


        # SSAO

        col = column.column(align=True)

        icon = "TRIA_DOWN" if context.scene.eevee.use_gtao else "TRIA_RIGHT"
        col.prop(context.scene.eevee, "use_gtao", icon=icon)
        if context.scene.eevee.use_gtao:
            row = col.row(align=True)
            row.prop(context.scene.eevee, "gtao_distance")
            # row.prop(context.scene.eevee, "gtao_factor")
            row.prop(context.scene.M3, "eevee_gtao_factor")


        # BLOOM

        col = column.column(align=True)

        icon = "TRIA_DOWN" if context.scene.eevee.use_bloom else "TRIA_RIGHT"
        col.prop(context.scene.eevee, "use_bloom", icon=icon)
        if context.scene.eevee.use_bloom:
            row = col.row(align=True)
            row.prop(context.scene.eevee, "bloom_threshold")
            row.prop(context.scene.eevee, "bloom_radius")
            row = col.row(align=True)
            row.prop(context.scene.M3, "eevee_bloom_intensity")


        # VOLUMETRICS

        col = column.column(align=True)

        icon = "TRIA_DOWN" if context.scene.eevee.use_volumetric_lights else "TRIA_RIGHT"
        col.prop(context.scene.eevee, "use_volumetric_lights", icon=icon)
        if context.scene.eevee.use_volumetric_lights:
            row = col.row(align=True)
            row.prop(context.scene.eevee, "volumetric_start")
            row.prop(context.scene.eevee, "volumetric_end")

            row = col.split(factor=0.4, align=True)
            row.prop(context.scene.eevee, "volumetric_tile_size", text='')
            row.prop(context.scene.eevee, "volumetric_samples")

            if context.scene.eevee.use_volumetric_shadows:
                row = col.split(factor=0.4, align=True)
            else:
                row = col.row(align=True)

            row.prop(context.scene.eevee, "use_volumetric_shadows", text='Shadows')
            if context.scene.eevee.use_volumetric_shadows:
                row.prop(context.scene.eevee, "volumetric_shadow_samples", text='Samples')

    def draw_cycles_box(self, context, view, layout):
        column = layout.column(align=True)

        row = column.split(factor=0.5, align=True)
        row.label(text='Cycles Settings')
        row.prop(context.scene.M3, 'cycles_device', expand=True)

        row = column.split(factor=0.5, align=True)
        row.prop(context.scene.cycles, 'use_adaptive_sampling', text='Adaptive')
        row.prop(context.scene.cycles, 'seed')

        row = column.split(factor=0.5, align=True)
        row.prop(context.scene.cycles, 'preview_samples', text='Viewport')
        row.prop(context.scene.cycles, 'samples', text='Render')

    def get_text_icon(self, context, shading):
        if context.space_data.shading.type == shading:
            text = "Overlays"
            icon = "OVERLAY"
        else:
            if shading == "SOLID":
                text = "Solid"
                icon = "SHADING_SOLID"
            elif shading == "MATERIAL":
                text = "Material"
                icon = "SHADING_TEXTURE"
            elif shading == "RENDERED":
                text = "Rendered"
                icon = "SHADING_RENDERED"
            elif shading == "WIREFRAME":
                text = "Wireframe"
                icon = "SHADING_WIRE"

        return text, icon


class PieViewport(Menu):
    bl_idname = "MACHIN3_MT_viewport_pie"
    bl_label = "Viewport and Cameras"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # ob = bpy.context.object
        # obj = context.object
        scene = context.scene
        view = context.space_data
        r3d = view.region_3d
        # rd = scene.render

        # align_active = bpy.context.scene.machin3.pieviewsalignactive

        # 4 - LEFT
        op = pie.operator("machin3.view_axis", text="Front")
        op.axis='FRONT'

        # 6 - RIGHT
        op = pie.operator("machin3.view_axis", text="Right")
        op.axis='RIGHT'
        # 2 - BOTTOM
        op = pie.operator("machin3.view_axis", text="Top")
        op.axis='TOP'
        # 8 - TOP

        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(scene, view, column)

        b = box.box()
        column = b.column()
        self.draw_center_column(column)

        b = box.box()
        column = b.column()
        self.draw_right_column(context, view, r3d, column)


        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()


        """
        box = pie.split()
        column = box.column()
        column.scale_x = 0.8


        row = column.row()
        row.label("Resolution")
        row.prop(context.scene.machin3, "preview_percentage", text="")
        row.prop(context.scene.machin3, "final_percentage", text="")

        row = column.row()
        row.label("Samples")
        row.prop(context.scene.machin3, "preview_samples", text="")
        row.prop(context.scene.machin3, "final_samples", text="")

        row = column.row(align=True)
        row.label("Set")
        row.operator("machin3.set_preview", text="Preview")
        row.operator("machin3.set_final", text="Final")

        column.separator()
        column.operator("machin3.pack_images", text="Pack Images")
        column.separator()
        column.separator()
        column.separator()
        # """

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.separator()

    def draw_left_column(self, scene, view, col):
        col.scale_x = 2

        row = col.row()
        row.scale_y = 1.5
        row.operator("machin3.smart_view_cam", text="Smart View Cam", icon='HIDE_OFF')

        if view.region_3d.view_perspective == 'CAMERA':
            cams = [obj for obj in scene.objects if obj.type == "CAMERA"]

            if len(cams) > 1:
                row = col.row()
                row.operator("machin3.next_cam", text="(Q) Previous Cam").previous = True
                row.operator("machin3.next_cam", text="(W) Next Cam").previous = False


        row = col.split()
        row.operator("machin3.make_cam_active")
        row.prop(scene, "camera", text="")


        row = col.split()
        row.operator("view3d.camera_to_view", text="Cam to view", icon='VIEW_CAMERA')

        text, icon = ("Unlock from View", "UNLOCKED") if view.lock_camera else ("Lock to View", "LOCKED")
        row.operator("wm.context_toggle", text=text, icon=icon).data_path = "space_data.lock_camera"

    def draw_center_column(self, col):
        col.scale_y = 1.5
        op = col.operator("machin3.view_axis", text="Bottom")
        op.axis='BOTTOM'

        row = col.row(align=True)
        op = row.operator("machin3.view_axis", text="Left")
        op.axis='LEFT'

        op = row.operator("machin3.view_axis", text="Back")
        op.axis='BACK'

    def draw_right_column(self, context, view, r3d, col):
        row = col.row()
        row.scale_y = 1.5

        # CAMERA ALIGNED

        if view.region_3d.view_perspective == 'CAMERA':
            cam = context.scene.camera

            text, icon = ("Orthographic", "VIEW_ORTHO") if cam.data.type == "PERSP" else ("Perspective", "VIEW_PERSPECTIVE")
            row.operator("machin3.toggle_cam_persportho", text=text, icon=icon)

            if cam.data.type == "PERSP":
                col.prop(cam.data, "lens")

            elif cam.data.type == "ORTHO":
                col.prop(cam.data, "ortho_scale")

        # USER VIEW

        else:
            text, icon = ("Orthographic", "VIEW_ORTHO") if r3d.is_perspective else ("Perspective", "VIEW_PERSPECTIVE")
            row.operator("machin3.toggle_view_persportho", text=text, icon=icon)

            col.prop(view, "lens")


class PieAlign(Menu):
    bl_idname = "MACHIN3_MT_align_pie"
    bl_label = "Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        m3 = context.scene.M3
        active = context.active_object
        sel = [obj for obj in context.selected_objects if obj != active]

        if m3.align_mode == 'AXES':
            self.draw_align_with_axes(pie, m3, sel)
        elif m3.align_mode == "VIEW":
            self.draw_align_with_view(pie, m3, sel)

    def draw_align_with_axes(self, pie, m3, sel):
        """
        draw alignment options with axes as inputs
        """

        # 4 - LEFT
        op = pie.operator("machin3.align_editmesh", text="Y min")
        op.axis = "Y"
        op.type = "MIN"

        # 6 - RIGHT
        op = pie.operator("machin3.align_editmesh", text="Y max")
        op.axis = "Y"
        op.type = "MAX"

        # 2 - BOTTOM
        box = pie.split()
        column = box.column()

        column.separator()

        row = column.split(factor=0.2)
        row.separator()
        row.label(text="Center")

        row = column.row(align=True)
        row.scale_y = 1.2
        row.operator("machin3.center_editmesh", text="X").axis = "X"
        row.operator("machin3.center_editmesh", text="Y").axis = "Y"
        row.operator("machin3.center_editmesh", text="Z").axis = "Z"

        row = column.row(align=True)
        row.scale_y = 1.2
        row.operator("machin3.straighten", text="Straighten")

        if sel:
            row = column.row()
            row.scale_y = 1.2
            row.operator("machin3.align_object_to_vert", text="Align Object to Vert")

            column.separator()
            row = column.row()
            row.scale_y = 1.2
            row.operator("machin3.align_object_to_edge", text="Align Object to Edge")


        # 8 - TOP
        box = pie.split()
        column = box.column()

        row = column.split(factor=0.2)
        row.label(icon="FREEZE")
        r = row.row(align=True)
        r.scale_y = 1.2
        op = r.operator("machin3.align_editmesh", text="X")
        op.axis = "X"
        op.type = "ZERO"
        op = r.operator("machin3.align_editmesh", text="Y")
        op.axis = "Y"
        op.type = "ZERO"
        op = r.operator("machin3.align_editmesh", text="Z")
        op.axis = "Z"
        op.type = "ZERO"


        row = column.split(factor=0.2)
        row.label(icon="ARROW_LEFTRIGHT")
        r = row.row(align=True)
        r.scale_y = 1.2
        op = r.operator("machin3.align_editmesh", text="X")
        op.axis = "X"
        op.type = "AVERAGE"
        op = r.operator("machin3.align_editmesh", text="Y")
        op.axis = "Y"
        op.type = "AVERAGE"
        op = r.operator("machin3.align_editmesh", text="Z")
        op.axis = "Z"
        op.type = "AVERAGE"


        row = column.split(factor=0.2)
        row.label(icon="PIVOT_CURSOR")
        r = row.row(align=True)
        r.scale_y = 1.2
        op = r.operator("machin3.align_editmesh", text="X")
        op.axis = "X"
        op.type = "CURSOR"
        op = r.operator("machin3.align_editmesh", text="Y")
        op.axis = "Y"
        op.type = "CURSOR"
        op = r.operator("machin3.align_editmesh", text="Z")
        op.axis = "Z"
        op.type = "CURSOR"

        column.separator()

        row = column.split(factor=0.15)
        row.separator()
        r = row.split(factor=0.8)
        rr = r.row(align=True)
        rr.prop(m3, "align_mode", expand=True)

        column.separator()


        # 7 - TOP - LEFT
        op = pie.operator("machin3.align_editmesh", text="X min")
        op.axis = "X"
        op.type = "MIN"

        # 9 - TOP - RIGHT
        op = pie.operator("machin3.align_editmesh", text="X max")
        op.axis = "X"
        op.type = "MAX"

        # 1 - BOTTOM - LEFT
        op = pie.operator("machin3.align_editmesh", text="Z min")
        op.axis = "Z"
        op.type = "MIN"

        # 3 - BOTTOM - RIGHT
        op = pie.operator("machin3.align_editmesh", text="Z max")
        op.axis = "Z"
        op.type = "MAX"

    def draw_align_with_view(self, pie, m3, sel):
        """
        draw align alignment options using directions in the view as inputs
        """

        # 4 - LEFT
        op = pie.operator("machin3.align_editmesh", text="Left")
        op.type = "MINMAX"
        op.direction = "LEFT"

        # 6 - RIGHT
        op = pie.operator("machin3.align_editmesh", text="Right")
        op.type = "MINMAX"
        op.direction = "RIGHT"

        # 2 - BOTTOM
        op = pie.operator("machin3.align_editmesh", text="Bottom")
        op.type = "MINMAX"
        op.direction = "BOTTOM"

        # 2 - TOP
        op = pie.operator("machin3.align_editmesh", text="Top")
        op.type = "MINMAX"
        op.direction = "TOP"

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        box = pie.split()
        column = box.column()

        row = column.row(align=True)
        row.prop(m3, "align_mode", expand=True)

        # 1 - BOTTOM - LEFT
        box = pie.split()
        column = box.column()

        column.separator()

        row = column.split(factor=0.25)
        row.label(text="Center")

        r = row.row(align=True)
        r.scale_y = 1.2
        op = r.operator("machin3.center_editmesh", text="Horizontal")
        op.direction = "HORIZONTAL"
        op = r.operator("machin3.center_editmesh", text="Vertical")
        op.direction = "VERTICAL"

        column.separator()
        row = column.split(factor=0.25)
        row.scale_y = 1.2
        row.separator()
        row.operator("machin3.straighten", text="Straighten")

        if sel:
            row = column.split(factor=0.25)
            row.scale_y = 1.2
            row.separator()
            row.operator("machin3.align_object_to_vert", text="Align Object to Vert")

            row = column.split(factor=0.25)
            row.scale_y = 1.2
            row.separator()
            row.operator("machin3.align_object_to_edge", text="Align Object to Edge")


        # 3 - BOTTOM - RIGHT
        box = pie.split()
        column = box.column()

        row = column.split(factor=0.2)
        # row.label(text="Zero")
        row.label(icon="FREEZE")

        r = row.row(align=True)
        r.scale_y = 1.2
        op = r.operator("machin3.align_editmesh", text="Horizontal")
        op.type = "ZERO"
        op.direction = "HORIZONTAL"
        op = r.operator("machin3.align_editmesh", text="Vertical")
        op.type = "ZERO"
        op.direction = "VERTICAL"

        row = column.split(factor=0.2)
        # row.label(text="Average")
        row.label(icon="ARROW_LEFTRIGHT")

        r = row.row(align=True)
        row.scale_y = 1.2
        op = r.operator("machin3.align_editmesh", text="Horizontal")
        op.type = "AVERAGE"
        op.direction = "HORIZONTAL"
        op = r.operator("machin3.align_editmesh", text="Vertical")
        op.type = "AVERAGE"
        op.direction = "VERTICAL"

        row = column.split(factor=0.2)
        # row.label(text="Cursor")
        row.label(icon="PIVOT_CURSOR")

        r = row.row(align=True)
        row.scale_y = 1.2
        op = r.operator("machin3.align_editmesh", text="Horizontal")
        op.type = "CURSOR"
        op.direction = "HORIZONTAL"
        op = r.operator("machin3.align_editmesh", text="Vertical")
        op.type = "CURSOR"
        op.direction = "VERTICAL"


class PieUVAlign(Menu):
    bl_idname = "MACHIN3_MT_uv_align_pie"
    bl_label = "UV Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        m3 = context.scene.M3

        if m3.align_mode == 'AXES':
            self.draw_align_with_axes(pie, m3)
        elif m3.align_mode == "VIEW":
            self.draw_align_with_view(pie, m3)

    def draw_align_with_axes(self, pie, m3):
        """
        draw alignment options with axes as inputsw
        """

        # 4 - LEFT
        op = pie.operator("machin3.align_uv", text="V min")
        op.axis = "V"
        op.type = "MIN"

        # 6 - RIGHT
        op = pie.operator("machin3.align_uv", text="V max")
        op.axis = "V"
        op.type = "MAX"

        # 2 - BOTTOM
        pie.separator()

        # 8 - TOP
        box = pie.split()
        column = box.column()

        row = column.row(align=True)
        row.prop(m3, "align_mode", expand=True)

        column.separator()
        column.separator()

        # 7 - TOP - LEFT
        op = pie.operator("machin3.align_uv", text="U min")
        op.axis = "U"
        op.type = "MIN"

        # 9 - TOP - RIGHT
        op = pie.operator("machin3.align_uv", text="U max")
        op.axis = "U"
        op.type = "MAX"

        # 1 - BOTTOM - LEFT
        op = pie.operator("machin3.align_uv", text="U Cursor")
        op.axis = "U"
        op.type = "CURSOR"

        # 3 - BOTTOM - RIGHT
        op = pie.operator("machin3.align_uv", text="V Cursor")
        op.axis = "V"
        op.type = "CURSOR"

    def draw_align_with_view(self, pie, m3):
        """
        draw align alignment options using directions in the view as inputs
        """

        # 4 - LEFT
        op = pie.operator("machin3.align_uv", text="Left")
        op.axis = "U"
        op.type = "MIN"

        # 6 - RIGHT
        op = pie.operator("machin3.align_uv", text="Right")
        op.axis = "U"
        op.type = "MAX"

        # 2 - BOTTOM
        op = pie.operator("machin3.align_uv", text="Bottom")
        op.axis = "V"
        op.type = "MIN"

        # 8 - TOP
        op = pie.operator("machin3.align_uv", text="Top")
        op.axis = "V"
        op.type = "MAX"

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        box = pie.split()
        column = box.column()

        row = column.row(align=True)
        row.prop(m3, "align_mode", expand=True)

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        box = pie.split()
        column = box.column()

        row = column.split(factor=0.2)

        row.label(icon="PIVOT_CURSOR")

        r = row.row(align=True)
        row.scale_y = 1.2
        op = r.operator("machin3.align_uv", text="Horizontal")
        op.type = "CURSOR"
        op.axis = "U"
        op = r.operator("machin3.align_uv", text="Vertical")
        op.type = "CURSOR"
        op.axis = "V"


class PieCursor(Menu):
    bl_idname = "MACHIN3_MT_cursor_pie"
    bl_label = "Cursor and Origin"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()


        # 4 - LEFT
        pie.operator("machin3.cursor_to_origin", text="to Origin", icon="PIVOT_CURSOR")

        # 6 - RIGHT
        pie.operator("view3d.snap_selected_to_cursor", text="to Cursor", icon="RESTRICT_SELECT_OFF").use_offset = False

        # 2 - BOTTOM

        if context.mode == "OBJECT":
            box = pie.split()
            column = box.column()

            column.separator()
            column.separator()

            row = column.split(factor=0.25)
            row.separator()
            row.label(text="Object Origin")

            column.scale_x = 1.1

            row = column.split(factor=0.5)
            row.scale_y = 1.5
            row.operator("object.origin_set", text="to Cursor", icon="LAYER_ACTIVE").type = "ORIGIN_CURSOR"
            row.operator("object.origin_set", text="to Geometry", icon="OBJECT_ORIGIN").type = "ORIGIN_GEOMETRY"

            row = column.split(factor=0.20)
            row.scale_y = 1.5
            row.separator()
            r = row.split(factor=0.7)
            r.operator("machin3.origin_to_active", text="to Active", icon="TRANSFORM_ORIGINS")


        else:
            pie.separator()

        # 8 - TOP
        pie.separator()

        # 7 - TOP - LEFT
        pie.operator("machin3.cursor_to_selected", text="to Selected", icon="PIVOT_CURSOR")

        # 9 - TOP - RIGHT
        pie.operator("view3d.snap_selected_to_cursor", text="to Cursor, Offset", icon="RESTRICT_SELECT_OFF").use_offset = True

        # 1 - BOTTOM - LEFT
        pie.operator("view3d.snap_cursor_to_grid", text="to Grid", icon="PIVOT_CURSOR")

        # 3 - BOTTOM - RIGHT
        pie.operator("view3d.snap_selected_to_grid", text="to Grid", icon="RESTRICT_SELECT_OFF")


class PieTransform(Menu):
    bl_idname = "MACHIN3_MT_transform_pie"
    bl_label = "Transform"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        scene = context.scene

        # 4 - LEFT
        op = pie.operator('machin3.set_transform_preset', text='Local')
        op.pivot = 'MEDIAN_POINT'
        op.orientation = 'LOCAL'

        # 6 - RIGHT
        op = pie.operator('machin3.set_transform_preset', text='Global')
        op.pivot = 'MEDIAN_POINT'
        op.orientation = 'GLOBAL'

        # 2 - BOTTOM
        op = pie.operator('machin3.set_transform_preset', text='Active')
        op.pivot = 'ACTIVE_ELEMENT'
        op.orientation = 'NORMAL' if context.mode in ['EDIT_MESH', 'EDIT_ARMATURE'] else 'LOCAL'

        # 8 - TOP

        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(scene, column)

        b = box.box()
        column = b.column()
        self.draw_center_column(scene, column)

        b = box.box()
        column = b.column()
        self.draw_right_column(context, scene, column)


        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        op = pie.operator('machin3.set_transform_preset', text='Individual')
        op.pivot = 'INDIVIDUAL_ORIGINS'
        op.orientation = 'NORMAL' if context.mode in ['EDIT_MESH', 'EDIT_ARMATURE'] else 'LOCAL'

        # 3 - BOTTOM - RIGHT
        op = pie.operator('machin3.set_transform_preset', text='Cursor')
        # op.pivot = 'MEDIAN_POINT'
        op.pivot = 'CURSOR'
        op.orientation = 'CURSOR'

    def draw_left_column(self, scene, layout):
        layout.scale_x = 3

        column = layout.column(align=True)
        column.label(text="Pivot Point")

        column.prop(scene.tool_settings, "transform_pivot_point", expand=True)

    def draw_center_column(self, scene, layout):
        slot = scene.transform_orientation_slots[0]
        custom = slot.custom_orientation

        column = layout.column(align=True)
        column.label(text="Orientation")

        column.prop(slot, "type", expand=True)

        column = layout.column(align=True)
        row = column.row(align=True)
        row.scale_y = 1.2
        row.operator("transform.create_orientation", text="Custom", icon='ADD', emboss=True).use = True

        if custom:
            row = column.row(align=True)
            row.prop(custom, "name", text="")
            row.operator("transform.delete_orientation", text="X", emboss=True)

    def draw_right_column(self, context, scene, layout):
        column = layout.column(align=True)

        if context.mode == 'OBJECT':
            column.label(text="Affect Only")

            col = column.column(align=True)
            col.scale_y = 1.2
            col.prop(scene.tool_settings, "use_transform_data_origin", text="Origins")
            col.prop(scene.tool_settings, "use_transform_pivot_point_align", text="Locations")
            col.prop(scene.tool_settings, "use_transform_skip_children", text="Parents")

        elif context.mode == 'EDIT_MESH':
            column.label(text="Mirror Editing")

            active = context.active_object

            row = column.row(align=True)
            row.prop(active.data, "use_mirror_x")
            row.prop(active.data, "use_mirror_y")
            row.prop(active.data, "use_mirror_z")

            column.prop(active.data, "use_mirror_topology", toggle=True)


class PieCollections(Menu):
    bl_idname = "MACHIN3_MT_collections_pie"
    bl_label = "Collections"

    def draw(self, context):
        sel = context.selected_objects
        active = context.active_object

        grouppro, _, _, _ = get_addon("Group Pro")
        batchops, _, _, _ = get_addon("Batch Operations™")
        decalmachine, _, _, _ = get_addon("DECALmachine")

        if sel:
            collections = list(set(col for obj in sel for col in obj.users_collection if not (decalmachine and (col.DM.isdecaltypecol or col.DM.isdecalparentcol))))[:10]

            if decalmachine:
                decalparentcollections = list(set(col for obj in sel for col in obj.users_collection if col.DM.isdecalparentcol))[:10]

        else:
            if context.scene.collection.objects:
                collections = get_scene_collections(context.scene)[:9]
                collections.insert(0, context.scene.collection)

            else:
                collections = get_scene_collections(context.scene)[:10]

            if decalmachine:
                decalparentcollections = [col for col in get_scene_collections(context.scene, ignore_decals=False) if col.DM.isdecalparentcol][:10]


        if decalmachine:
            decalsname = ".Decals" if context.scene.DM.hide_decaltype_collections else "Decals"
            dcol = bpy.data.collections.get(decalsname)



        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        if sel:
            pie.operator("machin3.remove_from_collection", text="Remove from", icon="REMOVE")

        else:
            pie.separator()

        # 6 - RIGHT
        if sel:
            pie.operator("machin3.add_to_collection", text="Add to", icon="ADD")

        else:
            pie.separator()


        # 2 - BOTTOM
        if sel:
            pie.operator("machin3.move_to_collection", text="Move to")

        else:
            pie.operator("machin3.create_collection", text="Create", icon="GROUP")

        # 8 - TOP

        if decalmachine and (decalparentcollections or dcol):

            # 1 - 1 - 1
            if len(collections) <= 5 and len(decalparentcollections) <= 5:
                row = pie.split(factor=0.34)

            # 1 - 2 - 1
            elif len(collections) > 5 and len(decalparentcollections) <= 5:
                row = pie.split(factor=0.25)
                row.scale_x = 0.8

            # 1 - 1 - 2
            elif len(collections) <= 5 and len(decalparentcollections) > 5:
                row = pie.split(factor=0.25)
                row.scale_x = 0.8

            # 1 - 2 - 2
            else:
                row = pie.split(factor=0.20)
                row.scale_x = 0.8

        else:
            # 1 - 1
            if len(collections) <= 5:
                row = pie.split(factor=0.5)
                row.scale_x = 1.5

            # 1 - 2
            elif len(collections) > 5:
                row = pie.split(factor=0.33)
                row.scale_x = 0.8


        # LEFT

        column = row.column()

        box = column.box()
        self.draw_left_top_column(context, box)

        if grouppro:
            box = column.box()
            self.draw_left_bottom_column(context, box)


        # MIDDLE

        if decalmachine and (decalparentcollections or dcol):

            # 1 - 1 - 1
            if len(collections) <= 5 and len(decalparentcollections) <= 5:
                r = row.split(factor=0.5)

            # 1 - 2 - 1
            elif len(collections) > 5 and len(decalparentcollections) <= 5:
                r = row.split(factor=0.66)

            # 1 - 1 - 2
            elif len(collections) <= 5 and len(decalparentcollections) > 5:
                r = row.split(factor=0.33)

            # 1 - 2 - 2
            else:
                r = row.split(factor=0.5)


        else:
            r = row

        box = r.box()
        self.draw_center_column(context, batchops, sel, collections, box)


        # RIGHT

        if decalmachine and (decalparentcollections or dcol):

            column = r.column()

            # decal parent collections

            if decalparentcollections:
                box = column.box()
                self.draw_right_top_column(context, batchops, sel, decalparentcollections, box)

            # decal type collections

            if dcol and dcol.DM.isdecaltypecol:
                box = column.box()
                self.draw_right_bottom_column(context, box)


        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.separator()

    def draw_left_top_column(self, context, layout):
        column = layout.column()

        row = column.row()
        row.scale_y = 1.5
        row.operator("machin3.purge_collections", text="Purge", icon='MONKEY')

    def draw_left_bottom_column(self, context, layout):
        m3 = context.scene.M3

        column = layout.column()

        column.label(text="GroupPro")

        row = column.row()
        row.prop(m3, "grouppro_dotnames", text=".hide", icon_only=True)
        row.operator("object.gpro_cleanup", text="Cleanup")

        row = column.row()
        row.operator("machin3.sort_grouppro_groups", text="Sort Groups")

    def draw_center_column(self, context, batchops, sel, collections, layout):
        if sel:
            layout.label(text="Scene Collections (Selection)")

        else:
            layout.label(text="Scene Collections")

        if len(collections) <= 5:
            column = layout.column(align=True)

            for col in collections:
                row = column.row(align=True)

                # regular collections are drawn as a button
                if col.children or col.objects:
                    icon = "RESTRICT_SELECT_ON" if col.objects and col.objects[0].hide_select else "RESTRICT_SELECT_OFF"
                    row.operator("machin3.select_collection", text=col.name, icon=icon).name = col.name
                    row.prop(col, "hide_viewport", text="", icon="HIDE_OFF")

                # empty collections are drawn as text
                else:
                    row.label(text=col.name)

                if batchops and col != context.scene.collection:
                    row.operator("batch_ops_collections.contextual_click", text="", icon="GROUP").idname = col.name

        else:
            layout.scale_x = 2

            cols1 = collections[:5]
            cols2 = collections[5:10]

            split = layout.split(factor=0.5)
            column = split.column(align=True)

            for col in cols1:
                row = column.row(align=True)
                if col.children or col.objects:
                    icon = "RESTRICT_SELECT_ON" if col.objects and col.objects[0].hide_select else "RESTRICT_SELECT_OFF"
                    row.operator("machin3.select_collection", text=col.name, icon=icon).name = col.name
                    row.prop(col, "hide_viewport", text="", icon="HIDE_OFF")

                else:
                    row.label(text=col.name)

                if batchops:
                    row.operator("batch_ops_collections.contextual_click", text="", icon="GROUP").idname = col.name

            column = split.column(align=True)

            for col in cols2:
                row = column.row(align=True)
                if col.children or col.objects:
                    icon = "RESTRICT_SELECT_ON" if col.objects and col.objects[0].hide_select else "RESTRICT_SELECT_OFF"
                    row.operator("machin3.select_collection", text=col.name, icon=icon).name = col.name
                    row.prop(col, "hide_viewport", text="", icon="HIDE_OFF")
                else:
                    row.label(text=col.name)

                if batchops:
                    row.operator("batch_ops_collections.contextual_click", text="", icon="GROUP").idname = col.name

    def draw_right_top_column(self, context, batchops, sel, collections, layout):
        if sel:
            layout.label(text="Decal Parent Collections (Selection)")

        else:
            layout.label(text="Decal Parent Collections")


        if len(collections) <= 5:
            column = layout.column(align=True)

            for col in collections:
                row = column.row(align=True)

                # regular collections are drawn as a button
                if col.children or col.objects:
                    icon = "RESTRICT_SELECT_ON" if col.objects and col.objects[0].hide_select else "RESTRICT_SELECT_OFF"
                    row.operator("machin3.select_collection", text=col.name, icon=icon).name = col.name
                    row.prop(col, "hide_viewport", text="", icon="HIDE_OFF")

                # empty collections are drawn as text
                else:
                    row.label(text=col.name)

                if batchops:
                    row.operator("batch_ops_collections.contextual_click", text="", icon="GROUP").idname = col.name

        else:
            layout.scale_x = 2

            cols1 = collections[:5]
            cols2 = collections[5:10]

            split = layout.split(factor=0.5)
            column = split.column(align=True)

            for col in cols1:
                row = column.row(align=True)
                if col.children or col.objects:
                    icon = "RESTRICT_SELECT_ON" if col.objects and col.objects[0].hide_select else "RESTRICT_SELECT_OFF"
                    row.operator("machin3.select_collection", text=col.name, icon=icon).name = col.name
                    row.prop(col, "hide_viewport", text="", icon="HIDE_OFF")

                else:
                    row.label(text=col.name)

                if batchops:
                    row.operator("batch_ops_collections.contextual_click", text="", icon="GROUP").idname = col.name

            column = split.column(align=True)

            for col in cols2:
                row = column.row(align=True)
                if col.children or col.objects:
                    icon = "RESTRICT_SELECT_ON" if col.objects and col.objects[0].hide_select else "RESTRICT_SELECT_OFF"
                    row.operator("machin3.select_collection", text=col.name, icon=icon).name = col.name
                    row.prop(col, "hide_viewport", text="", icon="HIDE_OFF")
                else:
                    row.label(text=col.name)

                if batchops:
                    row.operator("batch_ops_collections.contextual_click", text="", icon="GROUP").idname = col.name

    def draw_right_bottom_column(self, context, layout):
        layout.label(text="Decal Type Collections")

        row = layout.row(align=True)

        decalsname = ".Decals" if context.scene.DM.hide_decaltype_collections else "Decals"
        simplename = ".Simple" if context.scene.DM.hide_decaltype_collections else "Simple"
        subsetname = ".Subset" if context.scene.DM.hide_decaltype_collections else "Subset"
        infoname = ".Info" if context.scene.DM.hide_decaltype_collections else "Info"
        panelname = ".Panel" if context.scene.DM.hide_decaltype_collections else "Panel"

        op = row.operator("machin3.select_collection", text="Decals")
        op.name = decalsname
        op.force_all = True

        decals = bpy.data.collections.get(decalsname)
        simple = bpy.data.collections.get(simplename)
        subset = bpy.data.collections.get(subsetname)
        info = bpy.data.collections.get(infoname)
        panel = bpy.data.collections.get(panelname)

        row.prop(decals, "hide_viewport", text="", icon="HIDE_OFF")

        if simple and simple.DM.isdecaltypecol and simple.objects:
            row.operator("machin3.select_collection", text="Simple").name = simplename
            row.prop(simple, "hide_viewport", text="", icon="HIDE_OFF")
        else:
            row.label(text="Simple")

        if subset and subset.DM.isdecaltypecol and subset.objects:
            row.operator("machin3.select_collection", text="Subset").name = subsetname
            row.prop(subset, "hide_viewport", text="", icon="HIDE_OFF")
        else:
            row.label(text="Subset")

        if panel and panel.DM.isdecaltypecol and panel.objects:
            row.operator("machin3.select_collection", text="Panel").name = panelname
            row.prop(panel, "hide_viewport", text="", icon="HIDE_OFF")
        else:
            row.label(text="Panel")

        if info and info.DM.isdecaltypecol and info.objects:
            row.operator("machin3.select_collection", text="Info").name = infoname
            row.prop(info, "hide_viewport", text="", icon="HIDE_OFF")
        else:
            row.label(text="Info")


class PieWorkspace(Menu):
    bl_idname = "MACHIN3_MT_workspace_pie"
    bl_label = "Workspaces"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("machin3.switch_workspace", text="MACHIN3", icon='VIEW3D').name="General"

        # 6 - RIGHT
        # pie.operator("machin3.switch_workspace", text="Compositing", icon='NODE_COMPOSITING').name="Compositing"
        pie.separator()

        # 2 - BOTTOM
        pie.operator("machin3.switch_workspace", text="Scripting", icon='CONSOLE').name="Scripting"

        # 8 - TOP
        pie.operator("machin3.switch_workspace", text="Material", icon='MATERIAL_DATA').name="Material"

        # 7 - TOP - LEFT
        pie.operator("machin3.switch_workspace", text="UVs", icon='GROUP_UVS').name="UVs"

        # 9 - TOP - RIGHT
        pie.operator("machin3.switch_workspace", text="World", icon='WORLD').name="World"

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        # pie.operator("machin3.switch_workspace", text="Video", icon='FILE_MOVIE').name="Video"
        pie.separator()
