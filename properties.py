import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty, FloatProperty
import bmesh
from . utils.world import get_world_output
from . items import eevee_preset_items, align_mode_items, render_engine_items, cycles_device_items


# COLLECTIONS

class AppendMatsCollection(bpy.types.PropertyGroup):
    name: StringProperty()


class HistoryObjectsCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Object", type=bpy.types.Object)


class HistoryUnmirroredCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    obj: PointerProperty(name="History Unmirror", type=bpy.types.Object)


class HistoryEpochCollection(bpy.types.PropertyGroup):
    name: StringProperty()
    objects: CollectionProperty(type=HistoryObjectsCollection)
    unmirrored: CollectionProperty(type=HistoryUnmirroredCollection)


# SCENE PROPERTIES

selected = []


class M3SceneProperties(bpy.types.PropertyGroup):
    def update_xray(self, context):
        x = (self.pass_through, self.show_edit_mesh_wire)
        shading = context.space_data.shading

        shading.show_xray = True if any(x) else False

        if self.show_edit_mesh_wire:
            shading.xray_alpha = 0.1

        elif self.pass_through:
            shading.xray_alpha = 1 if context.active_object and context.active_object.type == "MESH" else 0.5

    def update_uv_sync_select(self, context):
        ts = context.scene.tool_settings
        ts.use_uv_select_sync = self.uv_sync_select

        global selected
        active = context.active_object

        # restore previous selection
        if ts.use_uv_select_sync:
            bpy.ops.mesh.select_all(action='DESELECT')

            bm = bmesh.from_edit_mesh(active.data)
            bm.normal_update()
            bm.verts.ensure_lookup_table()

            if selected:
                for v in bm.verts:
                    if v.index in selected:
                        v.select_set(True)

            bm.select_flush(True)

            bmesh.update_edit_mesh(active.data)

            # also sync the selection mode
            # NOTE: disabled again, seems like it's beneficial to just go back to the previous mesh selection mode
            # if ts.uv_select_mode in ["VERTEX", "EDGE", "FACE"]:
                # bpy.ops.mesh.select_mode(type=ts.uv_select_mode.replace("VERTEX", "VERT"))

        # store the active selection
        else:
            bm = bmesh.from_edit_mesh(active.data)
            bm.normal_update()
            bm.verts.ensure_lookup_table()

            selected = [v.index for v in bm.verts if v.select]

            bpy.ops.mesh.select_all(action="SELECT")

            # also sync the selection mode
            mode = tuple(ts.mesh_select_mode)

            # EDGE mode in the mesh becomes, EDGE in uv as well
            if mode == (False, True, False):
                ts.uv_select_mode = "EDGE"

            # everything else becomes VERTEX, including FACE
            # that's because there's no reason to turn off sync for face selections in the first place, faces unlike verts and edges, are always only present once in uv space
            else:
                ts.uv_select_mode = "VERTEX"

    def update_show_cavity(self, context):
        t = (self.show_cavity, self.show_curvature)
        shading = context.space_data.shading

        shading.show_cavity = True if any(t) else False

        if t == (True, True):
            shading.cavity_type = "BOTH"

        elif t == (True, False):
            shading.cavity_type = "WORLD"

        elif t == (False, True):
            shading.cavity_type = "SCREEN"

    def update_grouppro_dotnames(self, context):
        gpcols = [col for col in bpy.data.collections if col.created_with_gp]

        for col in gpcols:
            # hide collections
            if self.grouppro_dotnames:
                if not col.name.startswith("."):
                    col.name = ".%s" % col.name

            else:
                if col.name.startswith("."):
                    col.name = col.name[1:]

    pass_through: BoolProperty(name="Pass Through", default=False, update=update_xray)
    show_edit_mesh_wire: BoolProperty(name="Show Edit Mesh Wireframe", default=False, update=update_xray)
    uv_sync_select: BoolProperty(name="Synce Selection", default=False, update=update_uv_sync_select)

    show_cavity: BoolProperty(name="Cavity", default=True, update=update_show_cavity)
    show_curvature: BoolProperty(name="Curvature", default=False, update=update_show_cavity)

    focus_history: CollectionProperty(type=HistoryEpochCollection)

    grouppro_dotnames: BoolProperty(name=".dotname GroupPro collections", default=False, update=update_grouppro_dotnames)

    def update_eevee_preset(self, context):
        eevee = context.scene.eevee
        shading = context.space_data.shading

        if self.eevee_preset == 'NONE':
            eevee.use_ssr = False
            eevee.use_gtao = False
            eevee.use_bloom = False
            eevee.use_volumetric_lights = False

            shading.use_scene_lights = False
            shading.use_scene_world = False

            if context.scene.render.engine == 'BLENDER_EEVEE':
                shading.use_scene_lights_render = False
                shading.use_scene_world_render = False

        elif self.eevee_preset == 'LOW':
            eevee.use_ssr = True
            eevee.use_ssr_halfres = True
            eevee.use_ssr_refraction = False
            eevee.use_gtao = True
            eevee.use_bloom = False
            eevee.use_volumetric_lights = False

            shading.use_scene_lights = True
            shading.use_scene_world = False

            if context.scene.render.engine == 'BLENDER_EEVEE':
                shading.use_scene_lights_render = True
                shading.use_scene_world_render = False

        elif self.eevee_preset == 'HIGH':
            eevee.use_ssr = True
            eevee.use_ssr_halfres = False
            eevee.use_ssr_refraction = True
            eevee.use_gtao = True
            eevee.use_bloom = True
            eevee.use_volumetric_lights = False

            shading.use_scene_lights = True
            shading.use_scene_world = False

            if context.scene.render.engine == 'BLENDER_EEVEE':
                shading.use_scene_lights_render = True
                shading.use_scene_world_render = False

        elif self.eevee_preset == 'ULTRA':
            eevee.use_ssr = True
            eevee.use_ssr_halfres = False
            eevee.use_ssr_refraction = True
            eevee.use_gtao = True
            eevee.use_bloom = True
            eevee.use_volumetric_lights = True

            shading.use_scene_lights = True

            if context.scene.render.engine == 'BLENDER_EEVEE':
                shading.use_scene_lights_render = True

            world = context.scene.world
            if world:
                shading.use_scene_world = True

                if context.scene.render.engine == 'BLENDER_EEVEE':
                    shading.use_scene_world_render = True

                output = get_world_output(world)
                links = output.inputs[1].links

                if not links:
                    tree = world.node_tree

                    volume = tree.nodes.new('ShaderNodeVolumePrincipled')
                    tree.links.new(volume.outputs[0], output.inputs[1])

                    volume.inputs[2].default_value = 0.1
                    volume.location = (-200, 200)

    def update_eevee_gtao_factor(self, context):
        context.scene.eevee.gtao_factor = self.eevee_gtao_factor

    def update_eevee_bloom_intensity(self, context):
        context.scene.eevee.bloom_intensity = self.eevee_bloom_intensity

    def update_render_engine(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        context.scene.render.engine = self.render_engine

    def update_cycles_device(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        context.scene.cycles.device = self.cycles_device


    eevee_preset: EnumProperty(name="Eevee Preset", description="Eevee Quality Presets", items=eevee_preset_items, default='NONE', update=update_eevee_preset)
    eevee_gtao_factor: FloatProperty(name="Factor", default=1, min=0, step=0.1, update=update_eevee_gtao_factor)
    eevee_bloom_intensity: FloatProperty(name="Intensity", default=0.05, min=0, step=0.1, update=update_eevee_bloom_intensity)

    render_engine: EnumProperty(name="Render Engine", description="Render Engine", items=render_engine_items, default='BLENDER_EEVEE', update=update_render_engine)
    cycles_device: EnumProperty(name="Render Device", description="Render Device", items=cycles_device_items, default='CPU', update=update_cycles_device)

    object_axes_size: FloatProperty(name="Object Axes Size", default=0.3, min=0)
    object_axes_alpha: FloatProperty(name="Object Axes Alpha", default=0.75, min=0, max=1)

    align_mode: EnumProperty(name="Align Mode", items=align_mode_items, default="VIEW")

    avoid_update: BoolProperty()
