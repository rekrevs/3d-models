"""Run with Blender --background --python scripts/build_baseline.py."""
import hashlib
import json
import struct
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "renders" / "baseline"
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "Assembled"
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 0.001
raw = bpy.data.scenes.new("Source coordinates")
raw.unit_settings.system = "METRIC"
raw.unit_settings.scale_length = 0.001
inventory = {"blender": bpy.app.version_string, "assumed_unit": "mm",
             "assembly_note": "Source levels spaced at 85; broad mating planes spaced at 70. Two-unit protrusions do not set stacking height. XY unchanged.",
             "files": []}
material = bpy.data.materials.new("Neutral limestone")
material.diffuse_color = (0.52, 0.55, 0.59, 1)
material.use_nodes = True
bsdf = material.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.52, 0.55, 0.59, 1)
bsdf.inputs["Roughness"].default_value = 0.82
for filename, dz in [("groundFloor.stl", 0), ("firstFloor.stl", -15), ("secondFloor.stl", -30)]:
    path = ROOT / "sources" / "stl" / filename
    print("IMPORT", filename, flush=True)
    bpy.ops.wm.stl_import(filepath=str(path))
    obj = bpy.context.object
    obj.name = path.stem
    obj.data.materials.clear()
    obj.data.materials.append(material)
    lo = [min(v[i] for v in obj.bound_box) for i in range(3)]
    hi = [max(v[i] for v in obj.bound_box) for i in range(3)]
    source_obj = obj.copy()
    source_obj.name = path.stem + "_source"
    raw.collection.objects.link(source_obj)
    obj.location.z += dz
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    with path.open("rb") as stream:
        source_triangles = struct.unpack("<I", stream.read(84)[80:])[0]
    inventory["files"].append({"file": path.relative_to(ROOT).as_posix(), "sha256": digest,
        "bytes": path.stat().st_size, "source_triangles": source_triangles,
        "imported_triangles": len(obj.data.polygons),
        "vertices": len(obj.data.vertices), "source_bounds": [lo, hi],
        "assembly_translation": [0, 0, dz]})

target = Vector((215, -205, 87))
for name, offset in [("exterior", (-310, -350, 190)),
                     ("interior", (310, 350, 240)),
                     ("facade", (0, -450, 65))]:
    data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name, data)
    scene.collection.objects.link(cam)
    cam.location = target + Vector(offset)
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    data.type = "ORTHO"
    data.ortho_scale = 242
    data.clip_end = 3000

for name, location, energy, size in [
    ("Key", (20, -430, 380), 2500000, 220),
    ("Fill", (440, -70, 310), 1800000, 190),
    ("Rim", (90, 80, 260), 1500000, 160),
]:
    light = bpy.data.lights.new(name, "AREA")
    light.energy, light.shape, light.size = energy, "DISK", size
    obj = bpy.data.objects.new(name, light)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()
scene.world = bpy.data.worlds.new("Studio")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.24, 0.24, 0.24, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.render.resolution_x = 1100
scene.render.resolution_y = 1100
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.view_settings.exposure = -0.8
scene.camera = bpy.data.objects["exterior"]
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == "VIEW_3D":
            space = area.spaces.active
            space.clip_end = 3000
            space.region_3d.view_distance = 320
            space.region_3d.view_location = target
            space.region_3d.view_rotation = scene.camera.rotation_euler.to_quaternion()
            space.shading.light = "STUDIO"
            space.shading.color_type = "MATERIAL"
bpy.ops.object.select_all(action="DESELECT")
bpy.data.objects["firstFloor"].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["firstFloor"]
(ROOT / "reports" / "source_inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "scenes" / "baseline.blend"))
for name in ("exterior", "interior", "facade"):
    scene.camera = bpy.data.objects[name]
    scene.render.filepath = str(OUT / (name + ".png"))
    bpy.ops.render.render(write_still=True)
print("BASELINE_COMPLETE", flush=True)
