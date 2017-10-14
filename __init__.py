'''
Copyright (C) 2017 MACHIN3, machin3.io, support@machin3.io

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


bl_info = {
    "name": "MACHIN3tools",
    "author": "MACHIN3",
    "version": (0, 2),
    "blender": (2, 78, 0),
    "location": "",
    "description": "A collection of blender python scripts.",
    "warning": "",
    "wiki_url": "https://github.com/machin3io/MACHIN3tools",
    "category": "Mesh"}


import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty,FloatVectorProperty
from . import developer_utils as du
from . import M3utils as m3

modules = du.setup_addon_modules(__path__, __name__, "bpy" in locals())


# TODO: add automatic custom blender keymaps option
# TODO: OSD feedback, so you dont have to check into the op props to verify a tool did what you want it to do


class MACHIN3Settings(bpy.types.PropertyGroup):
    debugmode = BoolProperty(name="Debug Mode", default=False)

    pieobjecteditmodehide = BoolProperty(name="Auto Hide", default=False)
    pieobjecteditmodeshow = BoolProperty(name="Auto Reveal", default=False)
    pieobjecteditmodeshowunselect = BoolProperty(name="Unselect", default=False)


preferences_tabs = [("MODULES", "Modules", ""),
                    ("SPECIALMENUS", "Special Menus", ""),
                    ("PIEMENUS", "Pie Menus", ""),
                    ("CUSTOMKEYS", "Custom Keys", "")]


class MACHIN3Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    M3path = __path__[0]

    # TABS

    tabs = EnumProperty(name="Tabs", items=preferences_tabs, default="MODULES")

    # MODULES

    activate_ShadingSwitch = BoolProperty(name="Shading Switch", default=False)
    activate_RedMode = BoolProperty(name="Red Mode", default=False)
    activate_CenterCube = BoolProperty(name="Center Cube", default=False)
    activate_CleansUpGood = BoolProperty(name="Cleans Up Good", default=False)
    activate_ClippingToggle = BoolProperty(name="Clipping Plane Toggle", default=False)
    activate_Focus = BoolProperty(name="Focus", default=False)
    # activate_ThemeSwitch = BoolProperty(name="Theme Switch", default=False)
    activate_Mirror = BoolProperty(name="Mirror", default=False)
    activate_StarConnect = BoolProperty(name="Star Connect", default=False)
    activate_SmartModes = BoolProperty(name="Smart Modes", default=False)
    activate_MoreSmartModes = BoolProperty(name="More Smart Modes", default=False)
    activate_CleanoutMaterials = BoolProperty(name="Cleanout Materials", default=False)
    activate_CleanoutUVs = BoolProperty(name="Cleanout UVs", default=False)
    activate_CleanoutTransforms = BoolProperty(name="Cleanout Transforms", default=False)
    activate_SlideExtend = BoolProperty(name="Slide Extend", default=False)
    activate_LockItAll = BoolProperty(name="Lock It All", default=False)
    activate_HideMeshes = BoolProperty(name="Hide Meshes", default=False)
    activate_ModMachine = BoolProperty(name="Mod Machine", default=False)
    activate_CameraHelper = BoolProperty(name="Camera Helper", default=False)
    activate_Hierarch = BoolProperty(name="Hierarch", default=False)
    activate_FlipNormals = BoolProperty(name="Flip Normals", default=False)
    activate_SurfaceSlide = BoolProperty(name="Surface Slide", default=False)
    activate_QuickJoin = BoolProperty(name="Quick Join", default=False)
    activate_EdgeLength = BoolProperty(name="Edge Length", default=False)
    activate_SymmetrizeGPencil = BoolProperty(name="Symmetrize GPencil", default=False)
    activate_Emboss = BoolProperty(name="Emboss", default=False)

    # SPECIAL MENUS

    activate_special_Object = BoolProperty(name="Object Mode", default=True)
    activate_special_Edit = BoolProperty(name="Edit Mode", default=True)

    # PIE MENUS

    activate_pie_SelectMode = BoolProperty(name="Select Mode", default=False)
    activate_pie_Layouts = BoolProperty(name="Layouts", default=False)
    activate_pie_Snapping = BoolProperty(name="Snapping", default=False)
    activate_pie_Orientations = BoolProperty(name="Orientations", default=False)
    activate_pie_ObjectShading = BoolProperty(name="Object Shading", default=False)
    activate_pie_Align = BoolProperty(name="Align", default=False)
    activate_pie_SaveOpen = BoolProperty(name="Save and Open", default=False)
    activate_pie_UVSelectMode = BoolProperty(name="UV Select Mode", default=False)
    activate_pie_UVWeldAlign = BoolProperty(name="UV Weld and Align", default=False)

    # SETTINGS

    # Shading Switch

    viewportcompensation = BoolProperty(name="Material Viewport Compensation", default=True)

    compensationmodes = [("278", "2.78 Mode", ""),
                         ("279", "2.79 Mode", "")]

    shadingcompensation = EnumProperty(name="Viewport Shading Compensation", description="Adjusts Material Viewport Shading for overly dark metallic Materials in 2.79", items=compensationmodes, default="279")
    targetmetallic = FloatProperty(name="Target Metallic", description="Interpolation Target Metallic Value for Full Metallness", default=0.9, min=0, max=1)
    secondarytargetmetallic = FloatProperty(name="2nd Target Metallic", description="Interpolation Target Metallic Value for Secondary Color Based Adjustment", default=0.1, min=0, max=1)
    targetroughness = FloatProperty(name="Target Roughness", description="Interpolation Target Roughness Value for full Metallness", default=0.6, min=0, max=1)
    targetcolor = FloatProperty(name = "Brighten Color", description = "Brighten color", default = 0.6, min = 0, max = 0.8) #like gamma

    alphafix = BoolProperty(name="Fix white Decal borders in Viewport", default=True)

    def draw(self, context):
        layout=self.layout

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = column.box()

        if self.tabs == "MODULES":
            self.draw_modules(box, kc)
        elif self.tabs == "SPECIALMENUS":
            self.draw_special(box, kc)
        elif self.tabs == "PIEMENUS":
            self.draw_pies(box, kc)

    def draw_modules(self, box, kc):
        col = box.column()

        col.label("Activating modules requires saving user preferences and re-starting Blender.")
        col.separator()

        # SHADING SWITCH

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ShadingSwitch", toggle=True)
        row.label("Switches between Material and Solid shading modes. Also re-assigns Z key for wireframe switching and Shift + Z for render switching accordingly.")
        du.show_keymap(self.activate_ShadingSwitch, kc, "3D View", "machin3.shading_switch", col)

        self.draw_shading_switch(col)

        # RED MODE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_RedMode", toggle=True)
        row.label("In SOLID mode: switch to red matcap and back. In MATERIAL mode: switch turn bevels of WStep materials red and.")
        du.show_keymap(self.activate_RedMode, kc, "3D View", "machin3.red_mode", col)

        # Center Cube

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CenterCube", toggle=True)
        row.label("If nothing is selected, places a cube at the cursor location, with any of X/Y/Z zeroed out, enters edit mode, selects all and initiates the scale tool. If objects are selected, it zeroes out any of X/Y/Z.")
        du.show_keymap(self.activate_CenterCube, kc, "Object Mode", "machin3.center_cube", col)

        # Cleans Up Good

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleansUpGood", toggle=True)
        row.label("Removes doubles, dissolves degenerates, deletes loose vertices and edges, recalculates normals, dissolves 2-edged vertices, selects non-manifold geometry. Works in edit mode and object mode(incl. on multiple objects).")
        du.show_keymap(self.activate_CleansUpGood, kc, "Mesh", "machin3.clean_up", col)

        # CLIPPING TOGGLE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ClippingToggle", toggle=True)
        row.label("Toggle through different clipping plane settings")
        du.show_keymap(self.activate_ClippingToggle, kc, "3D View", "machin3.clipping_toggle", col)

        # FOCUS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Focus", toggle=True)
        row.label("Disables all Mirror modifiers of the selected objects, then enters local view. Renables mirror modifers again, when exiting localview.")
        du.show_keymap(self.activate_Focus, kc, "Object Mode", "machin3.focus", col)

        # MIRROR

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Mirror", toggle=True)
        row.label("Mirrors selected objects across the active object, allows mirroring of multiple objects at once and supports DECALmachine.")
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_x", col)
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_y", col)
        du.show_keymap(self.activate_Mirror, kc, "Object Mode", "machin3.mirror_z", col)

        # STAR CONNECT

        row = col.split(percentage=0.2)
        row.prop(self, "activate_StarConnect", toggle=True)
        row.label("In Vert mode, connects all selected verts to the last one of the selection, in Face mode it creates a center star vert")
        du.show_keymap(self.activate_StarConnect, kc, "Mesh", "machin3.star_connect", col)

        # SMART MODES

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SmartModes", toggle=True)
        row.label("In Vert mode connects vert path or initiates knife, in edge mode is turns the edge, in face mode it converts the selection to a bounder loop.")
        du.show_keymap(self.activate_SmartModes, kc, "Mesh", "machin3.smart_modes", col)

        # MORE SMART MODES

        row = col.split(percentage=0.2)
        row.prop(self, "activate_MoreSmartModes", toggle=True)
        row.label("In Vert or Edge mode runs F2, in Face mode without selection runs Bisect, with selection duplicates and separates it.")
        du.show_keymap(self.activate_SmartModes, kc, "Mesh", "machin3.more_smart_modes", col)

        # CLEANOUT MATERIALS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleanoutMaterials", toggle=True)
        row.label("Removes all material assignments and all materials from the scene.")

        # CLEANOUT UVS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleanoutUVs", toggle=True)
        row.label("Removes all UV channels from selected objects.")

        # CLEANOUT TRANSFORM ORIENTATIONS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CleanoutTransforms", toggle=True)
        row.label("Removes all custom transform orientations.")

        # SLIDE EXTEND

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SlideExtend", toggle=True)
        row.label("Moves selected vert away or closer to active vert.")
        du.show_keymap(self.activate_SlideExtend, kc, "Mesh", "machin3.slide_extend", col)

        # LOCK IT ALL

        row = col.split(percentage=0.2)
        row.prop(self, "activate_LockItAll", toggle=True)
        row.label("Locks any or all selected objects' transforms")

        # HIDE MESHES

        row = col.split(percentage=0.2)
        row.prop(self, "activate_HideMeshes", toggle=True)
        row.label("Hides Meshes of selection in Object Mode.")
        du.show_keymap(self.activate_HideMeshes, kc, "Object Mode", "machin3.hide_meshes", col)

        # MOD MACHINE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_ModMachine", toggle=True)
        row.label("Applys/Shows/Hides the entire modifier stack or any of the selceted mods on objects in selection.")

        # CAMERA HELPER

        row = col.split(percentage=0.2)
        row.prop(self, "activate_CameraHelper", toggle=True)
        row.label("Creates a new camera from view if nothing is selected. If Camera is selcted, aligns camera to current view and makes it the scene camera.")
        du.show_keymap(self.activate_CameraHelper, kc, "Object Mode", "machin3.camera_helper", col)

        # HIERARCHY

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Hierarch", toggle=True)
        row.label("Child of's instead of parents. Works on geo and bones. On geo, can be fired multile times to switch between 'set inverse' and 'clear inverse. On geo defaults to 'set inverse', while on bones defaults to 'clear inverse'.")
        du.show_keymap(self.activate_Hierarch, kc, "3D View", "machin3.hierarch", col)

        # FLIP NORMALS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_FlipNormals", toggle=True)
        row.label("Flips normals of selected objects.")

        # SURFACE SLIDE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SurfaceSlide", toggle=True)
        row.label("Edit Verts, Edges and Polygons while maintaining the Surface and Form.")
        du.show_keymap(self.activate_SurfaceSlide, kc, "Mesh", "machin3.surface_slide", col)

        # QUICK JOIN

        row = col.split(percentage=0.2)
        row.prop(self, "activate_QuickJoin", toggle=True)
        row.label("Creates shortest vertex paths and joins vertex path pairs accordingly.")
        du.show_keymap(self.activate_QuickJoin, kc, "Mesh", "machin3.quick_join_last", col)
        du.show_keymap(self.activate_QuickJoin, kc, "Mesh", "machin3.quick_join_center", col)

        # EDGE LENGTH

        row = col.split(percentage=0.2)
        row.prop(self, "activate_EdgeLength", toggle=True)
        row.label("Average length of selected edges or precisely set their length")

        # SYMMETRIZE GPENCIL

        row = col.split(percentage=0.2)
        row.prop(self, "activate_SymmetrizeGPencil", toggle=True)
        row.label("Symmetrizes the Grease Pencil using the cursor as the mid point.")

        # EMBOSS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_Emboss", toggle=True)
        row.label("Embosses the selected polygons.")

    def draw_special(self, box, kc):
        col = box.column()

        col.label("Activating special menus requires saving user preferences and re-starting Blender.")
        col.separator()

        row = col.split(percentage=0.2)
        row.prop(self, "activate_special_Object", toggle=True)
        row.label("Add MACHIN3tools to Blender's Object Mode Special Menu")
        du.show_keymap(self.activate_special_Object, kc, "Object Mode", "wm.call_menu", col, kmivalue="VIEW3D_MT_object_specials", properties="name", keepactive=True)

        row = col.split(percentage=0.2)
        row.prop(self, "activate_special_Edit", toggle=True)
        row.label("Add MACHIN3tools to Blender's Edit Mode Special Menu")
        du.show_keymap(self.activate_special_Edit, kc, "Mesh", "wm.call_menu", col, kmivalue="VIEW3D_MT_edit_mesh_specials", properties="name", keepactive=True)

    def draw_pies(self, box, kc):
        col = box.column()

        col.label("Activating pie menus requires saving user preferences and re-starting Blender.")
        col.separator()
        col.label("These pie menus are based on the excellent 'Wazou's Pie Menus' with some changes and additions.")
        col.separator()

        # SELECT MODE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_SelectMode", toggle=True)
        row.label("Select Object and Edit Modes.")
        du.show_keymap(self.activate_pie_SelectMode, kc, "Object Non-modal", "wm.call_menu_pie", col, kmivalue="pie.objecteditmode", properties="name")

        # LAYOUTS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_Layouts", toggle=True)
        row.label("Switch Layouts.")
        du.show_keymap(self.activate_pie_Layouts, kc, "Screen", "wm.call_menu_pie", col, kmivalue="pie.areaviews", properties="name")

        # SNAPPING

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_Snapping", toggle=True)
        row.label("Change Snapping.")
        du.show_keymap(self.activate_pie_Snapping, kc, "3D View Generic", "wm.call_menu_pie", col, kmivalue="pie.snapping", properties="name")

        # ORIENTATIONS

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_Orientations", toggle=True)
        row.label("Set Transform Orientations.")
        du.show_keymap(self.activate_pie_Orientations, kc, "3D View Generic", "wm.call_menu_pie", col, kmivalue="pie.orientation", properties="name")

        # OBJECT SHADING

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_ObjectShading", toggle=True)
        row.label("Grid, Wireframe, Smooth, Flat Shading and Auto Smooth, Matcaps, Backface Culling, AO, etc.")
        du.show_keymap(self.activate_pie_ObjectShading, kc, "3D View Generic", "wm.call_menu_pie", col, kmivalue="pie.objectshading", properties="name")

        # ALIGN

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_Align", toggle=True)
        row.label("Align Verts in Edit Mode.")
        du.show_keymap(self.activate_pie_Align, kc, "Mesh", "wm.call_menu_pie", col, kmivalue="pie.align", properties="name")

        # SAVE, OPEN, APPEND, LINK, ...

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_SaveOpen", toggle=True)
        row.label("Save, Open, Append, Link, Export, etc.")
        du.show_keymap(self.activate_pie_UVSelectMode, kc, "Window", "wm.call_menu_pie", col, kmivalue="pie.saveopen", properties="name")

        # UV SELECT MODE

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_UVSelectMode", toggle=True)
        row.label("UV Editor - Select Object and Edit Modes.")
        du.show_keymap(self.activate_pie_UVSelectMode, kc, "Image", "wm.call_menu_pie", col, kmivalue="pie.uvsselectmode", properties="name")

        # UV WELD, ALIGN

        row = col.split(percentage=0.2)
        row.prop(self, "activate_pie_UVWeldAlign", toggle=True)
        row.label("UV Editor - Weld and Align tools.")
        du.show_keymap(self.activate_pie_UVWeldAlign, kc, "UV Editor", "wm.call_menu_pie", col, kmivalue="pie.uvsweldalign", properties="name")

    def draw_shading_switch(self, column):
        if bpy.app.version >= (2, 79, 0):
            if self.activate_ShadingSwitch:
                column.prop(self, "viewportcompensation")

                if self.viewportcompensation:
                    row = column.row()
                    row.prop(self, "shadingcompensation", expand=True)

                    if self.shadingcompensation == "279":
                        row = column.row()
                        row.prop(self, "targetmetallic")
                        row.prop(self, "secondarytargetmetallic")
                        row.prop(self, "targetroughness")
                        row.prop(self, "targetcolor")
                        column.prop(self, "alphafix")

                column.separator()
                column.separator()
                column.separator()


class VIEW3D_MT_object_machin3tools(bpy.types.Menu):
    bl_label = "(W)MACHIN3tools"

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        if m3.M3_prefs().activate_CleansUpGood:
            column.operator("machin3.clean_up", text="Cleans Up Good")
        if m3.M3_prefs().activate_CenterCube:
            column.operator("machin3.center_cube", text="Center Cube")
        if m3.M3_prefs().activate_CleanoutMaterials:
            column.operator("machin3.cleanout_materials", text="Cleanout Materials")
        if m3.M3_prefs().activate_CleanoutUVs:
            column.operator("machin3.cleanout_uvs", text="Cleanout UVs")
        if m3.M3_prefs().activate_CleanoutTransforms:
            column.operator("machin3.cleanout_transforms", text="Cleanout Transforms")
        if m3.M3_prefs().activate_LockItAll:
            column.operator("machin3.lock_it_all", text="Lock It All")
        if m3.M3_prefs().activate_HideMeshes:
            column.operator("machin3.hide_meshes", text="Hide Meshes")
        if m3.M3_prefs().activate_ModMachine:
            column.operator("machin3.mod_machine", text="Mod Machine")
        if m3.M3_prefs().activate_CameraHelper:
            column.operator("machin3.camera_helper", text="Camera Helper")
        if m3.M3_prefs().activate_Hierarch:
            column.operator("machin3.hierarch", text="Hierarch")
        if m3.M3_prefs().activate_FlipNormals:
            column.operator("machin3.flip_normals", text="Flip Normals")
        if m3.M3_prefs().activate_SymmetrizeGPencil:
            if context.gpencil_data:
                column.operator("machin3.symmetrize_gpencil", text="Symmetrize GPencil")


class VIEW3D_MT_edit_mesh_machin3tools(bpy.types.Menu):
    bl_label = "(W)MACHIN3tools"

    # TODO: comp mode availability check

    def draw(self, context):
        mode = m3.get_mode()
        layout = self.layout

        column = layout.column()

        if m3.M3_prefs().activate_QuickJoin:
            column.operator("machin3.quick_join_last", text="Quick Join (Last)")
        if m3.M3_prefs().activate_QuickJoin:
            column.operator("machin3.quick_join_center", text="Quick Join (Center)")
        if m3.M3_prefs().activate_SmartModes:
            column.operator("machin3.smart_modes", text="Smart Modes")
        if m3.M3_prefs().activate_StarConnect:
            column.operator("machin3.star_connect", text="Star Connect")
        if m3.M3_prefs().activate_CleansUpGood:
            column.operator("machin3.clean_up", text="Cleans Up Good")
        if m3.M3_prefs().activate_MoreSmartModes:
            column.operator("machin3.more_smart_modes", text="More Smart Modes")
        if m3.M3_prefs().activate_CleanoutTransforms:
            column.operator("machin3.cleanout_transforms", text="Cleanout Transforms")
        if m3.M3_prefs().activate_SlideExtend:
            if mode == "VERT":
                column.operator("machin3.slide_extend", text="Slide Extend")
        if m3.M3_prefs().activate_SurfaceSlide:
            column.operator("machin3.surface_slide", text="Surface Slide")
        if m3.M3_prefs().activate_EdgeLength:
            column.operator("machin3.edge_length", text="Edge Length")
        if m3.M3_prefs().activate_Emboss:
            if mode == "FACE":
                column.operator("machin3.emboss", text="Emboss")


def edit_menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_machin3tools")
    self.layout.separator()


def object_menu_func(self, context):
    self.layout.menu("VIEW3D_MT_object_machin3tools")
    self.layout.separator()


def register_MACHIN3_keys(wm, keymaps):
    # SHADING SWITCH

    if m3.M3_prefs().activate_ShadingSwitch:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.shading_switch", 'BUTTON5MOUSE', 'PRESS', shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # RED MODE

    if m3.M3_prefs().activate_RedMode:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.red_mode", 'BUTTON5MOUSE', 'PRESS', alt=True)
        MACHIN3_keymaps.append((km, kmi))

    # CENTER CUBE

    if m3.M3_prefs().activate_CenterCube:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.center_cube", 'C', 'PRESS', shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # CLEANS UP GOOD

    if m3.M3_prefs().activate_CleansUpGood:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.clean_up", "THREE", "PRESS")
        MACHIN3_keymaps.append((km, kmi))

    # CLIPPING PLANE TOGGLE

    if m3.M3_prefs().activate_ClippingToggle:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.clipping_toggle", "BUTTON5MOUSE", "PRESS")

    # FOCUS

    if m3.M3_prefs().activate_Focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.focus", "F", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))

    # THEME SWITCH

    # if m3.M3_prefs().activate_ThemeSwitch:
        # km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        # kmi = km.keymap_items.new("machin3.theme_switch", "BUTTON5MOUSE", "PRESS", ctrl=True)

    # MIRROR

    if m3.M3_prefs().activate_Focus:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.mirror_x", "X", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))
        kmi = km.keymap_items.new("machin3.mirror_y", "Y", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))
        kmi = km.keymap_items.new("machin3.mirror_z", "Z", "PRESS", alt=True, shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # STAR MODES

    if m3.M3_prefs().activate_StarConnect:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.star_connect", "TWO", "PRESS", shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # SMART MODES

    if m3.M3_prefs().activate_SmartModes:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.smart_modes", "TWO", "PRESS")
        MACHIN3_keymaps.append((km, kmi))

    # MORE SMART MODES

    if m3.M3_prefs().activate_MoreSmartModes:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.more_smart_modes", "FOUR", "PRESS")
        MACHIN3_keymaps.append((km, kmi))

    # SLIDE EXTEND

    if m3.M3_prefs().activate_SlideExtend:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.slide_extend", "E", "PRESS", shift=True)
        MACHIN3_keymaps.append((km, kmi))

    # HIDE MESHES

    if m3.M3_prefs().activate_HideMeshes:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.hide_meshes", "H", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))

    # CAMERA HELPER

    if m3.M3_prefs().activate_CameraHelper:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.camera_helper", "NUMPAD_0", "PRESS", alt=True)
        MACHIN3_keymaps.append((km, kmi))

    # HIERARCHY

    if m3.M3_prefs().activate_Hierarch:
        # km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("machin3.hierarch", "P", "PRESS", ctrl=True)
        MACHIN3_keymaps.append((km, kmi))

    # SURFACE SLIDE

    if m3.M3_prefs().activate_SurfaceSlide:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.surface_slide", "G", "PRESS", alt=True)
        MACHIN3_keymaps.append((km, kmi))

    # QUICK JOIN

    if m3.M3_prefs().activate_QuickJoin:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.quick_join_last", "ONE", "PRESS", alt=True)
        MACHIN3_keymaps.append((km, kmi))

        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("machin3.quick_join_center", "ONE", "PRESS", shift=True)
        MACHIN3_keymaps.append((km, kmi))


def register_pie_keys(wm, keymaps):
    # SELECT MODE

    if m3.M3_prefs().activate_pie_SelectMode:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = "pie.objecteditmode"
        kmi.active = True
        keymaps.append((km, kmi))

    # LAYOUTS

    if m3.M3_prefs().activate_pie_Layouts:
        km = wm.keyconfigs.addon.keymaps.new(name='Screen')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', ctrl=True)
        kmi.properties.name = "pie.areaviews"
        kmi.active = True
        keymaps.append((km, kmi))

    # SNAPPING

    if m3.M3_prefs().activate_pie_Snapping:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'MIDDLEMOUSE', 'PRESS', alt=True)
        kmi.properties.name = "pie.snapping"
        kmi.active = True
        keymaps.append((km, kmi))

    # ORIENTATIONS

    if m3.M3_prefs().activate_pie_Orientations:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', alt=True)
        kmi.properties.name = "pie.orientation"
        kmi.active = True
        keymaps.append((km, kmi))

    # OBJECT SHADING

    if m3.M3_prefs().activate_pie_ObjectShading:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', alt=True)
        kmi.properties.name = "pie.objectshading"
        kmi.active = True
        keymaps.append((km, kmi))

    # ALIGN

    if m3.M3_prefs().activate_pie_Align:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS', alt=True)
        kmi.properties.name = "pie.align"
        kmi.active = True
        keymaps.append((km, kmi))

    # SAVE, OPEN, APPEND, LINK, ...

    if m3.M3_prefs().activate_pie_SaveOpen:
        km = wm.keyconfigs.addon.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True)
        kmi.properties.name = "pie.saveopen"
        kmi.active = True
        keymaps.append((km, kmi))

    # UV SELECT MODE

    if m3.M3_prefs().activate_pie_UVSelectMode:
        km = wm.keyconfigs.addon.keymaps.new(name='Image', space_type='IMAGE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS')
        kmi.properties.name = "pie.uvsselectmode"
        kmi.active = True
        keymaps.append((km, kmi))

    # UV WELD, ALIGN

    if m3.M3_prefs().activate_pie_UVWeldAlign:
        km = wm.keyconfigs.addon.keymaps.new(name='UV Editor')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS')
        kmi.properties.name = "pie.uvsweldalign"
        kmi.active = True
        keymaps.append((km, kmi))


MACHIN3_keymaps = []


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.machin3 = bpy.props.PointerProperty(type=MACHIN3Settings)

    # SPECIAL MENUS

    if m3.M3_prefs().activate_special_Edit:
        bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(edit_menu_func)

    if m3.M3_prefs().activate_special_Object:
        bpy.types.VIEW3D_MT_object_specials.prepend(object_menu_func)

    wm = bpy.context.window_manager

    # MACHIN3 MODULE KEYS

    register_MACHIN3_keys(wm, MACHIN3_keymaps)

    # PIE MENUS  KEYS

    register_pie_keys(wm, MACHIN3_keymaps)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(edit_menu_func)
    bpy.types.VIEW3D_MT_object_specials.remove(object_menu_func)

    for km, kmi in MACHIN3_keymaps:
        km.keymap_items.remove(kmi)

    MACHIN3_keymaps.clear()
