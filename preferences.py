import bpy
from bpy.props import IntProperty, StringProperty, CollectionProperty, BoolProperty, EnumProperty
import os
import rna_keymap_ui
from . properties import AppendMatsCollection
from . utils.ui import get_icon
from . utils.registration import activate, get_path, get_name


preferences_tabs = [("GENERAL", "General", ""),
                    ("KEYMAPS", "Keymaps", ""),
                    ("ABOUT", "About", "")]


links = [("Documentation", "https://machin3.io/MACHIN3tools/docs/", "INFO"),
         ("MACHINƎ.io", "https://machin3.io", "WORLD"),
         ("Youtube", "https://www.youtube.com/channel/UC4yaFzFDILd2yAqOWRuLOvA", "NONE"),
         ("Twitter", "https://twitter.com/machin3io", "NONE"),
         ("", "", ""),
         ("", "", ""),
         ("DECALmachine", "https://machin3.io/DECALmachine", "NONE"),
         ("MESHmachine", "https://machin3.io/MESHmachine", "NONE"),
         ("", "", ""),
         ("", "", ""),
         ("MACHINƎ @ Artstation", "https://www.artstation.com/artist/machin3", "NONE"),
         ("", "", ""),
         ]


# TODO: check if the append world/materials paths exist and make them abosolute


class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    path = get_path()
    bl_idname = get_name()


    # APPENDMATS

    def update_appendmatsname(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        else:
            if self.appendmatsname and self.appendmatsname not in self.appendmats:
                am = self.appendmats.add()
                am.name = self.appendmatsname

                self.appendmatsIDX = len(self.appendmats) - 1

            self.avoid_update = True
            self.appendmatsname = ""


    # CHECKS

    def update_switchmatcap1(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.preferences.studio_lights if os.path.basename(os.path.dirname(mc.path)) == "matcap"]
        if self.switchmatcap1 not in matcaps:
            self.avoid_update = True
            self.switchmatcap1 = "NOT FOUND"

    def update_switchmatcap2(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.preferences.studio_lights if os.path.basename(os.path.dirname(mc.path)) == "matcap"]
        if self.switchmatcap2 not in matcaps:
            self.avoid_update = True
            self.switchmatcap2 = "NOT FOUND"

    def update_custom_preferences_keymap(self, context):
        if self.custom_preferences_keymap:
            kc = context.window_manager.keyconfigs.user

            for km in kc.keymaps:
                if km.is_user_modified:
                    self.custom_preferences_keymap = False
                    self.dirty_keymaps = True
                    return

            self.dirty_keymaps = False


    # RUNTIME TOOL ACTIVATION

    def update_activate_smart_vert(self, context):
        activate(self, register=self.activate_smart_vert, tool="smart_vert")

    def update_activate_smart_edge(self, context):
        activate(self, register=self.activate_smart_edge, tool="smart_edge")

    def update_activate_smart_face(self, context):
        activate(self, register=self.activate_smart_face, tool="smart_face")

    def update_activate_clean_up(self, context):
        activate(self, register=self.activate_clean_up, tool="clean_up")

    def update_activate_clipping_toggle(self, context):
        activate(self, register=self.activate_clipping_toggle, tool="clipping_toggle")

    def update_activate_focus(self, context):
        activate(self, register=self.activate_focus, tool="focus")

    def update_activate_mirror(self, context):
        activate(self, register=self.activate_mirror, tool="mirror")

    def update_activate_align(self, context):
        activate(self, register=self.activate_align, tool="align")

    def update_activate_apply(self, context):
        activate(self, register=self.activate_apply, tool="apply")

    def update_activate_select(self, context):
        activate(self, register=self.activate_select, tool="select")

    def update_activate_mesh_cut(self, context):
        activate(self, register=self.activate_mesh_cut, tool="mesh_cut")

    def update_activate_customize(self, context):
        activate(self, register=self.activate_customize, tool="customize")

    def update_activate_filebrowser_tools(self, context):
        activate(self, register=self.activate_filebrowser_tools, tool="filebrowser")


    # RUNTIME PIE ACTIVATION

    def update_activate_modes_pie(self, context):
        activate(self, register=self.activate_modes_pie, tool="modes_pie")

    def update_activate_save_pie(self, context):
        activate(self, register=self.activate_save_pie, tool="save_pie")

    def update_activate_shading_pie(self, context):
        activate(self, register=self.activate_shading_pie, tool="shading_pie")

    def update_activate_views_pie(self, context):
        activate(self, register=self.activate_views_pie, tool="views_pie")

    def update_activate_align_pie(self, context):
        activate(self, register=self.activate_align_pie, tool="align_pie")

    def update_activate_cursor_pie(self, context):
        activate(self, register=self.activate_cursor_pie, tool="cursor_pie")

    def update_activate_transform_pie(self, context):
        activate(self, register=self.activate_transform_pie, tool="transform_pie")

    def update_activate_collections_pie(self, context):
        activate(self, register=self.activate_collections_pie, tool="collections_pie")

    def update_activate_workspace_pie(self, context):
        activate(self, register=self.activate_workspace_pie, tool="workspace_pie")


    # RUNTIME MENU ACTIVATION

    def update_activate_object_context_menu(self, context):
        activate(self, register=self.activate_object_context_menu, tool="object_context_menu")


    # PROPERTIES

    appendworldpath: StringProperty(name="World Source .blend", subtype='FILE_PATH')
    appendworldname: StringProperty(name="Name of World")

    appendmatspath: StringProperty(name="Materials Source .blend", subtype='FILE_PATH')
    appendmats: CollectionProperty(type=AppendMatsCollection)
    appendmatsIDX: IntProperty()
    appendmatsname: StringProperty(name="Name of Material to append", update=update_appendmatsname)

    switchmatcap1: StringProperty(name="Matcap 1", update=update_switchmatcap1)
    switchmatcap2: StringProperty(name="Matcap 2", update=update_switchmatcap2)

    obj_mode_rotate_around_active: BoolProperty(name="Rotate Around Selection, but only in Object Mode", default=False)
    toggle_cavity: BoolProperty(name="Toggle Cavity/Curvature OFF in Edit Mode, ON in Object Mode", default=True)

    focus_view_transition: BoolProperty(name="Viewport Transitional Motion", default=True)

    custom_startup: BoolProperty(name="Startup Scene", default=True)
    custom_theme: BoolProperty(name="Theme", default=True)
    custom_matcaps: BoolProperty(name="Matcaps", default=True)
    custom_shading: BoolProperty(name="Shading", default=True)
    custom_overlays: BoolProperty(name="Overlays", default=True)
    custom_outliner: BoolProperty(name="Outliner", default=True)
    custom_preferences_interface: BoolProperty(name="Preferences: Interface", default=True)
    custom_preferences_viewport: BoolProperty(name="Preferences: Viewport", default=True)
    custom_preferences_navigation: BoolProperty(name="Preferences: Navigation", default=True)
    custom_preferences_keymap: BoolProperty(name="Preferences: Keymap", default=False, update=update_custom_preferences_keymap)
    custom_preferences_system: BoolProperty(name="Preferences: System", default=False)
    custom_preferences_save: BoolProperty(name="Preferences: Save & Load", default=True)


    # MACHIN3tools

    activate_smart_vert: BoolProperty(name="Smart Vert", default=True, update=update_activate_smart_vert)
    activate_smart_edge: BoolProperty(name="Smart Edge", default=True, update=update_activate_smart_edge)
    activate_smart_face: BoolProperty(name="Smart Face", default=True, update=update_activate_smart_face)
    activate_clean_up: BoolProperty(name="Clean Up", default=True, update=update_activate_clean_up)
    activate_clipping_toggle: BoolProperty(name="Clipping Toggle", default=True, update=update_activate_clipping_toggle)
    activate_focus: BoolProperty(name="Focus", default=True, update=update_activate_focus)
    activate_mirror: BoolProperty(name="Mirror", default=True, update=update_activate_mirror)
    activate_align: BoolProperty(name="Align", default=True, update=update_activate_align)
    activate_apply: BoolProperty(name="Apply", default=True, update=update_activate_apply)
    activate_select: BoolProperty(name="Select", default=True, update=update_activate_select)
    activate_mesh_cut: BoolProperty(name="Mesh Cut", default=True, update=update_activate_mesh_cut)
    activate_filebrowser_tools: BoolProperty(name="Filebrowser Tools", default=True, update=update_activate_filebrowser_tools)
    activate_customize: BoolProperty(name="Customize", default=False, update=update_activate_customize)


    # MACHIN3pies

    activate_modes_pie: BoolProperty(name="Modes Pie", default=True, update=update_activate_modes_pie)
    activate_save_pie: BoolProperty(name="Save Pie", default=True, update=update_activate_save_pie)
    activate_shading_pie: BoolProperty(name="Shading Pie", default=True, update=update_activate_shading_pie)
    activate_views_pie: BoolProperty(name="Views Pie", default=True, update=update_activate_views_pie)
    activate_align_pie: BoolProperty(name="Align Pies", default=True, update=update_activate_align_pie)
    activate_cursor_pie: BoolProperty(name="Cursor Pie", default=True, update=update_activate_cursor_pie)
    activate_transform_pie: BoolProperty(name="Transform Pie", default=True, update=update_activate_transform_pie)
    activate_collections_pie: BoolProperty(name="Collections Pie", default=True, update=update_activate_collections_pie)
    activate_workspace_pie: BoolProperty(name="Workspace Pie", default=False, update=update_activate_workspace_pie)


    # MACHIN3menus
    activate_object_context_menu: BoolProperty(name="Object Context Menu", default=True, update=update_activate_object_context_menu)


    # hidden

    tabs: EnumProperty(name="Tabs", items=preferences_tabs, default="GENERAL")
    avoid_update: BoolProperty(default=False)
    dirty_keymaps: BoolProperty(default=False)


    def draw(self, context):
        layout=self.layout


        # TAB BAR

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = column.box()

        if self.tabs == "GENERAL":
            self.draw_general(box)

        elif self.tabs == "KEYMAPS":
            self.draw_keymaps(box)

        elif self.tabs == "ABOUT":
            self.draw_about(box)

    def draw_general(self, box):
        split = box.split()

        # LEFT

        b = split.box()
        b.label(text="Activate")


        # MACHIN3tools

        bb = b.box()
        bb.label(text="Tools")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_vert", toggle=True)
        row.label(text="Smart vertex manipulation.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_edge", toggle=True)
        row.label(text="Smart edge creation, manipulation and selection conversion.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_face", toggle=True)
        row.label(text="Smart face creation and object-from-face creation.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clean_up", toggle=True)
        row.label(text="Quick geometry clean up.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clipping_toggle", toggle=True)
        row.label(text="Viewport clipping plane toggle.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_focus", toggle=True)
        row.label(text="Object isolation with history.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_mirror", toggle=True)
        row.label(text="Object Mirroring + Un-Mirroring")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align", toggle=True)
        row.label(text="Object per-axis location, rotation and scale alignment.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_apply", toggle=True)
        row.label(text="Apply Transformations while keeping the bevel width as well as the child transformations unchanged")

        row = column.split(factor=0.25)
        row.prop(self, "activate_select", toggle=True)
        row.label(text="Selection helpers.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_mesh_cut", toggle=True)
        row.label(text="Knife intersect a mesh, using another object.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_filebrowser_tools", toggle=True)
        row.label(text="Additional tools for the Filebrowser.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_customize", toggle=True)
        row.label(text="Customize various Blender preferences, settings and keymaps.")


        # MACHIN3pies

        bb = b.box()
        bb.label(text="Pie Menus")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_modes_pie", toggle=True)
        row.label(text="Quick mode changing.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_save_pie", toggle=True)
        row.label(text="Save, open, append. Load recent, previous and next. Append World and Materials.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_shading_pie", toggle=True)
        row.label(text="Control shading, overlays, eevee and some object properties.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_views_pie", toggle=True)
        row.label(text="Control views. Create and manage cameras.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align_pie", toggle=True)
        row.label(text="Edit mesh and UV alignments.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_cursor_pie", toggle=True)
        row.label(text="Cursor and Origin manipulation.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_transform_pie", toggle=True)
        row.label(text="Transform Orientations and Pivots.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_collections_pie", toggle=True)
        row.label(text="Collection management.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_workspace_pie", toggle=True)
        r = row.split(factor=0.4)
        r.label(text="Switch Workplaces.")
        r.label(text="If enabled, customize it in ui/pies.py", icon="INFO")


        # MACHIN3menus

        bb = b.box()
        bb.label(text="Menus")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_object_context_menu", toggle=True)
        row.label(text="Object Context Menu, access tools, that aren't keymapped.")


        # RIGHT

        b = split.box()
        b.label(text="Settings")

        # FOCUS

        if getattr(bpy.types, "MACHIN3_OT_focus", False):
            bb = b.box()
            bb.label(text="Focus")

            column = bb.column()
            column.prop(self, "focus_view_transition")


        # CUSTOMIZE

        if getattr(bpy.types, "MACHIN3_OT_customize", False):
            bb = b.box()
            bb.label(text="Customize")

            bbb = bb.box()
            column = bbb.column()

            row = column.row()
            row.prop(self, "custom_theme")
            row.prop(self, "custom_matcaps")
            row.prop(self, "custom_shading")

            row = column.row()
            row.prop(self, "custom_overlays")
            row.prop(self, "custom_outliner")
            row.prop(self, "custom_startup")

            bbb = bb.box()
            column = bbb.column()

            row = column.row()

            col = row.column()
            col.prop(self, "custom_preferences_interface")
            col.prop(self, "custom_preferences_viewport")

            col = row.column()
            col.prop(self, "custom_preferences_navigation")
            col.prop(self, "custom_preferences_keymap")

            col = row.column()
            col.prop(self, "custom_preferences_system")
            col.prop(self, "custom_preferences_save")

            if self.dirty_keymaps:
                row = column.row()
                row.label(text="Keymaps have been modified, restore them first.", icon="ERROR")
                row.operator("machin3.restore_keymaps", text="Restore now")
                row.label()

            column = bb.column()
            row = column.row()

            row.label()
            row.operator("machin3.customize", text="Customize")
            row.label()


        # MODES PIE

        if getattr(bpy.types, "MACHIN3_MT_modes_pie", False):
            bb = b.box()
            bb.label(text="Modes Pie")

            column = bb.column()

            column.prop(self, "toggle_cavity")


        # SAVE PIE

        if getattr(bpy.types, "MACHIN3_MT_save_pie", False):
            bb = b.box()
            bb.label(text="Save Pie: Append World and Materials")

            column = bb.column()

            column.prop(self, "appendworldpath")
            column.prop(self, "appendworldname")
            column.separator()

            column.prop(self, "appendmatspath")


            column = bb.column()

            row = column.row()
            rows = len(self.appendmats) if len(self.appendmats) > 6 else 6
            row.template_list("MACHIN3_UL_append_mats", "", self, "appendmats", self, "appendmatsIDX", rows=rows)

            c = row.column(align=True)
            c.operator("machin3.move_appendmat", text="", icon='TRIA_UP').direction = "UP"
            c.operator("machin3.move_appendmat", text="", icon='TRIA_DOWN').direction = "DOWN"

            c.separator()
            c.operator("machin3.clear_appendmats", text="", icon='LOOP_BACK')
            c.operator("machin3.remove_appendmat", text="", icon_value=get_icon('cancel'))
            c.separator()
            c.operator("machin3.populate_appendmats", text="", icon='MATERIAL')
            c.operator("machin3.rename_appendmat", text="", icon='OUTLINER_DATA_FONT')


            row = column.row()
            row.prop(self, "appendmatsname")
            row.operator("machin3.add_separator", text="", icon_value=get_icon('separator'))


        # SHADING PIE

        if getattr(bpy.types, "MACHIN3_MT_shading_pie", False):
            bb = b.box()
            bb.label(text="Shading Pie: Matcap Switch")

            column = bb.column()

            row = column.row()

            row.prop(self, "switchmatcap1")
            row.prop(self, "switchmatcap2")


        # NO SETTINGS

        if not any([getattr(bpy.types, "MACHIN3_" + name, False) for name in ["MT_modes_pie", "MT_save_pie", "MT_shading_pie"]]):
            b.label(text="No tools or pie menus with settings have been activated.")

    def draw_keymaps(self, box):
        wm = bpy.context.window_manager
        # kc = wm.keyconfigs.addon
        kc = wm.keyconfigs.user

        from . registration import keys

        split = box.split()

        b = split.box()
        b.label(text="Tools")

        if not self.draw_tool_keymaps(kc, keys, b):
            b.label(text="No keymappings available, because none of the tools have been activated.")


        b = split.box()
        b.label(text="Pie Menus")

        if not self.draw_pie_keymaps(kc, keys, b):
            b.label(text="No keymappings created, because none of the pies have been activated.")

    def draw_about(self, box):
        column = box.column()

        for idx, (text, url, icon) in enumerate(links):
            if idx % 2 == 0:
                row = column.row()
                if text == "":
                    row.separator()
                else:
                    row.operator("wm.url_open", text=text, icon=icon).url = url
            else:
                if text == "":
                    row.separator()
                else:
                    row.operator("wm.url_open", text=text, icon=icon).url = url

    def draw_tool_keymaps(self, kc, keysdict, layout):
        drawn = False

        for name in keysdict:
            if "PIE" not in name:
                keylist = keysdict.get(name)

                if self.draw_keymap_items(kc, name, keylist, layout):
                    drawn = True

        return drawn

    def draw_pie_keymaps(self, kc, keysdict, layout):
        drawn = False

        for name in keysdict:
            if "PIE" in name:
                keylist = keysdict.get(name)

                if self.draw_keymap_items(kc, name, keylist, layout):
                    drawn = True

        return drawn

    def draw_keymap_items(self, kc, name, keylist, layout):
        drawn = []

        # index keeping track of SUCCESSFULL kmi iterations
        idx = 0

        for item in keylist:
            keymap = item.get("keymap")
            isdrawn = False

            if keymap:
                km = kc.keymaps.get(keymap)

                kmi = None
                if km:
                    idname = item.get("idname")

                    for kmitem in km.keymap_items:
                        if kmitem.idname == idname:
                            properties = item.get("properties")

                            if properties:
                                if all([getattr(kmitem.properties, name, None) == value for name, value in properties]):
                                    kmi = kmitem
                                    break

                            else:
                                kmi = kmitem
                                break

                # draw keymap item

                if kmi:
                    # multi kmi tools, will share a single box, created for the first kmi
                    if idx == 0:
                        box = layout.box()

                    # single kmi tools, get their label from the title
                    if len(keylist) == 1:
                        label = name.title().replace("_", " ")

                    # multi kmi tools, get it from the label tag, while the title is printed once, before the first item
                    else:
                        if idx == 0:
                            box.label(text=name.title().replace("_", " "))

                        label = item.get("label")

                    row = box.split(factor=0.15)
                    row.label(text=label)

                    # layout.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, row, 0)

                    # draw info, if available
                    infos = item.get("info", [])
                    for text in infos:
                        row = box.split(factor=0.15)
                        row.separator()
                        row.label(text=text, icon="INFO")

                    isdrawn = True
                    idx += 1

            drawn.append(isdrawn)
        return drawn
