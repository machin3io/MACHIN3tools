import bpy
from bpy.props import StringProperty, BoolProperty
from .. import M3utils as m3
from .. import developer_utils as du
from math import pow

# TODO: ShadingSwitch() must call prepare_for_viewport_shading() when switching from solid to material shading


class ShadingSwitch(bpy.types.Operator):
    bl_idname = "machin3.shading_switch"
    bl_label = "MACHIN3: Shading Switch"
    bl_options = {'REGISTER'}

    def execute(self, context):
        shadingmode = bpy.context.space_data.viewport_shade

        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)

        # deactivate the default render toggle
        defaultrendertoggle = wm.keyconfigs.default.keymaps['3D View'].keymap_items['view3d.toggle_render']

        if defaultrendertoggle.active:
            defaultrendertoggle.active = False

        # look for an existing machin3 render toggle
        try:
            wm.keyconfigs.addon.keymaps['3D View'].keymap_items['machin3.toggle_rendered']
        except:
            km.keymap_items.new('machin3.toggle_rendered', "Z", 'PRESS', shift=True)

        # look for an existing machin3 wire toggle
        try:
            machin3wiretoggle = wm.keyconfigs.addon.keymaps['3D View'].keymap_items['machin3.toggle_wireframe']
        except:
            machin3wiretoggle = None

        if shadingmode == "SOLID":
            bpy.context.space_data.viewport_shade = "MATERIAL"
            print("Switched to MATERIAL shading mode.")

            if machin3wiretoggle:
                km.keymap_items.remove(machin3wiretoggle)

            kmi = km.keymap_items.new('machin3.toggle_wireframe', "Z", 'PRESS')
            du.kmi_props_setattr(kmi.properties, 'shading', 'MATERIAL')

            print(" » '%s' switches between MATERIAL and RENDERED." % ("SHIFT + Z"))
            print(" » '%s' switches between MATERIAL and WIREFRAME." % ("Z"))

        elif shadingmode == "MATERIAL":
            bpy.context.space_data.viewport_shade = "SOLID"
            print("Switched to SOLID shading mode.")

            if machin3wiretoggle:
                km.keymap_items.remove(machin3wiretoggle)

            kmi = km.keymap_items.new('machin3.toggle_wireframe', "Z", 'PRESS')
            du.kmi_props_setattr(kmi.properties, 'shading', 'SOLID')

            print(" » '%s' switches between SOLID and RENDERED." % ("SHIFT + Z"))
            print(" » '%s' switches between SOLID and WIREFRAME." % ("Z"))

        print()

        return {'FINISHED'}


class ToggleWireframe(bpy.types.Operator):
    bl_idname = "machin3.toggle_wireframe"
    bl_label = "MACHIN3: Toggle Wireframe"

    shading = StringProperty(name="Shading", description="Toggle enum", maxlen=1024)

    def execute(self, context):
        bpy.ops.wm.context_toggle_enum(data_path="space_data.viewport_shade", value_1=self.shading, value_2="WIREFRAME")
        return {'FINISHED'}


class ToggleRendered(bpy.types.Operator):
    bl_idname = "machin3.toggle_rendered"
    bl_label = "MACHIN3: Toggle Rendered"

    # shading = StringProperty(name="Shading", description="Toggle enum", maxlen=1024)

    def execute(self, context):
        if bpy.app.version >= (2, 79, 0) and m3.M3_prefs().viewportcompensation:
            # print("Viewport Material Compensation normal switching")

            shadingmode = bpy.context.space_data.viewport_shade

            if shadingmode == "RENDERED":
                prepare_for_material_shading()
            else:
                prepare_for_rendering()

        # NOTE: since 2.79 blender is smart enough to do the rendered swithing on its own

        # bpy.ops.wm.context_toggle_enum(data_path="space_data.viewport_shade", value_1=self.shading, value_2="RENDERED")
        bpy.ops.view3d.toggle_render()

        return {'FINISHED'}


class ResetMaterialViewportComensation(bpy.types.Operator):
    bl_idname = "machin3.reset_material_viewport_compensation"
    bl_label = "MACHIN3: Reset Material Viewport Compensation"

    def execute(self, context):
        if bpy.app.version >= (2, 79, 0):
            prepare_for_rendering()

        return {'FINISHED'}


def prepare_for_rendering():
    mode = m3.M3_prefs().shadingcompensation

    print("Preparing Materials for Rendering")

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    reset_principledpbr_node(mode, mat, node)
                elif node.type == "GROUP":
                    if "Decal" in node.node_tree.name:
                        for n in node.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                reset_principledpbr_node(mode, mat, n, node)


def reset_principledpbr_node(mode, material, node, group=None):
    try:
        if node["M3"]:
            ischanged = True
    except:
        ischanged = False

    if ischanged:  # reset changes and delete M3 id prop

        # Decal Material
        if group:
            groupname = group.node_tree.name
            if "Subset" in groupname:
                if node.name == "Principled BSDF":
                    color = group.inputs['Material Color'].links[0].from_socket
                    metallic = group.inputs['Material Metallic']
                    roughness = group.inputs['Material Roughness']
                elif node.name == "Principled BSDF.001":
                    color = group.inputs['Subset Color'].links[0].from_socket
                    metallic = group.inputs['Subset Metallic']
                    roughness = group.inputs['Subset Roughness']

            elif "Panel" in groupname:
                if node.name == "Principled BSDF":
                    color = group.inputs['Material 1 Color'].links[0].from_socket
                    metallic = group.inputs['Material 1 Metallic']
                    roughness = group.inputs['Material 1 Roughness']
                elif node.name == "Principled BSDF.001":
                    color = group.inputs['Material 2 Color'].links[0].from_socket
                    metallic = group.inputs['Material 2 Metallic']
                    roughness = group.inputs['Material 2 Roughness']

            elif "Info" in groupname:
                color = group.inputs['Info Color']
                metallic = group.inputs['Info Metallic']
                roughness = group.inputs['Info Roughness']

            # Subtractors have either 'Subtractor' in the group name or are just called 'Decal Group'
            else:
                color = group.inputs['Material Color'].links[0].from_socket
                metallic = group.inputs['Material Metallic']
                roughness = group.inputs['Material Roughness']


            transparent = group.node_tree.nodes.get("Transparent BSDF")
            transparent.inputs[0].default_value = (1, 1, 1, 1)

        # Non-Decal Material
        else:
            metallic = node.inputs[4]
            roughness = node.inputs[7]
            color = node.inputs[0]

        metallic.default_value = node["M3"]["metallic"]
        roughness.default_value = node["M3"]["roughness"]
        color.default_value = node["M3"]["color"]

        del node["M3"]

        # print("Material: '%s', Node: '%s' - Reset PBR values and deleted M3 ID Property" % (material.name, node.name))
    else:
        # print("Material: '%s', Node: '%s' - No M3 ID Property found" % (material.name, node.name))
        pass


def prepare_for_material_shading():
    mode = m3.M3_prefs().shadingcompensation

    print("Preparing Materials for Viewport Display")

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    adjust_principledpbr_node(mode, mat, node)
                elif node.type == "GROUP":
                    if "Decal" in node.node_tree.name:
                        for n in node.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                adjust_principledpbr_node(mode, mat, n, node)


class AdjustPrincipledPBRnode(bpy.types.Operator):
    bl_idname = "machin3.adjust_principled_pbr_node"
    bl_label = "MACHIN3: Adjust Principled PBR Node Rendered"

    isdecal = BoolProperty(name="Is Decal?", default=True)

    def execute(self, context):
        mode = m3.M3_prefs().shadingcompensation
        obj = m3.get_active()

        mat = obj.material_slots[0].material

        if self.isdecal:
            decalgroup = mat.node_tree.nodes['Material Output'].inputs['Surface'].links[0].from_node
            groupname = decalgroup.node_tree.name

            shadernodes = []

            shadernodes.append(decalgroup.node_tree.nodes.get("Principled BSDF"))
            if "Subset" in groupname or "Panel" in groupname:
                shadernodes.append(decalgroup.node_tree.nodes.get("Principled BSDF.001"))

            for node in shadernodes:
                # only adjust, when there isn't a M3 prop already!
                try:
                    node["M3"]
                except:
                    adjust_principledpbr_node(mode, mat, node, decalgroup)
                    print("Material Viewport Compensation for Material: '%s', Node: '%s'" % (mat.name, node.name))
        else:
            node = mat.node_tree.nodes['Material Output'].inputs['Surface'].links[0].from_node

            try:
                node["M3"]
            except:
                adjust_principledpbr_node(mode, mat, node)
                print("Material Viewport Compensation for Material: '%s', Node: '%s'" % (mat.name, node.name))

        return {'FINISHED'}


def adjust_principledpbr_node(mode, material, node, group=None):
    targetmetallic = m3.M3_prefs().targetmetallic
    secondarytargetmetallic = m3.M3_prefs().secondarytargetmetallic
    targetroughness = m3.M3_prefs().targetroughness
    targetcolor = m3.M3_prefs().targetcolor
    alphafix = m3.M3_prefs().alphafix

    # get render parameters

    # Decal Material
    if group:
        groupname = group.node_tree.name

        if "Subset" in groupname:
            if node.name == "Principled BSDF":
                color = group.inputs['Material Color'].links[0].from_socket
                metallic = group.inputs['Material Metallic']
                roughness = group.inputs['Material Roughness']
            elif node.name == "Principled BSDF.001":
                color = group.inputs['Subset Color'].links[0].from_socket
                metallic = group.inputs['Subset Metallic']
                roughness = group.inputs['Subset Roughness']

        elif "Panel" in groupname:
            if node.name == "Principled BSDF":
                color = group.inputs['Material 1 Color'].links[0].from_socket
                metallic = group.inputs['Material 1 Metallic']
                roughness = group.inputs['Material 1 Roughness']
            elif node.name == "Principled BSDF.001":
                color = group.inputs['Material 2 Color'].links[0].from_socket
                metallic = group.inputs['Material 2 Metallic']
                roughness = group.inputs['Material 2 Roughness']

        elif "Info" in groupname:
            color = node.inputs[0]  # color is irrelevant for info decals, as it comes from an image, we just need it for the dict below
            metallic = group.inputs['Info Metallic']
            roughness = group.inputs['Info Roughness']

        # Subtractors have either 'Subtractor' in the group name or are just called 'Decal Group'
        else:  # Subtractors have either 'Subtractor' in the group name or are just called 'Decal Group'
            color = group.inputs['Material Color'].links[0].from_socket
            metallic = group.inputs['Material Metallic']
            roughness = group.inputs['Material Roughness']

    # Non-Decal Material
    else:
        groupname = ""
        color = node.inputs[0]
        metallic = node.inputs[4]
        roughness = node.inputs[7]

    # save render parameters
    node["M3"] = {"color": color.default_value,
                  "metallic": metallic.default_value,
                  "roughness": roughness.default_value}

    # print("Material: '%s', Node: '%s' - Set M3 ID Property" % (material.name, node.name))

    # set viewport parameters
    if mode == "278":  # this mode mirrors the look in 2.78, very rough and without metallic darkening
        metallic.default_value = 0.5
        roughness.default_value = 1
        color.default_value = (.8,.8,.8)
    elif mode == "279":  # this mode lerps between render values and target values based on the metallic amount and color average

        if "Info" in groupname:
            metallic.default_value = m3.lerp(metallic.default_value, targetmetallic, metallic.default_value)
            roughness.default_value = m3.lerp(roughness.default_value, targetroughness, metallic.default_value)
        else:
            coloravg = (color.default_value[0] + color.default_value[1] + color.default_value[2]) / 3
            color.default_value = (pow(color.default_value[0],1-targetcolor), #brighten color
                                   pow(color.default_value[0], 1-targetcolor),
                                   pow(color.default_value[0], 1-targetcolor),color.default_value[3])

            metallic.default_value = m3.lerp(m3.lerp(metallic.default_value, targetmetallic, metallic.default_value), secondarytargetmetallic, coloravg)
            roughness.default_value = m3.lerp(roughness.default_value, targetroughness, metallic.default_value)

    if group:
        if mode == "279" and alphafix:
            transparent = group.node_tree.nodes.get("Transparent BSDF")
            transparent.inputs[0].default_value = (0, 0, 0, 1)
