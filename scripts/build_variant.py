"""Build damaged_01 from the verified baseline, leaving source meshes intact."""
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
TAG = "probe_holes" if "--probe-holes" in sys.argv else "damaged_01"
sys.path.insert(0, str(ROOT / "scripts"))
from mesh_checks import mesh_stats

bpy.ops.wm.open_mainfile(filepath=str(ROOT / "scenes" / "baseline.blend"))
scene = bpy.context.scene
scene.name = "Damaged 01"
OUT = ROOT / "renders" / TAG
OUT.mkdir(parents=True, exist_ok=True)
EXPORT = ROOT / "exports" / TAG
EXPORT.mkdir(parents=True, exist_ok=True)
report = {"variant": TAG, "operations": [], "meshes": {}, "exports": {}}


def prism(name, ring_a, ring_b):
    count = len(ring_a)
    faces = [tuple(reversed(range(count))), tuple(range(count, 2 * count))]
    faces += [(i, (i + 1) % count, (i + 1) % count + count, i + count)
              for i in range(count)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(ring_a + ring_b, [], faces)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    return obj


# World coordinates in millimetres: retain the corner around x=165.
# Fracture descends across the facade at y=-255 and through its window arch.
profile = [(190, 210), (190, 140), (197, 137), (201, 128),
           (208, 130), (211, 118), (218, 115), (222, 105),
           (232, 108), (237, 99), (310, 99), (310, 210)]
wall = prism("Jagged facade fracture",
             [(x, -285, z) for x, z in profile],
             [(x, -223, z) for x, z in profile])
report["operations"].append({"name": wall.name, "xz_profile": profile,
                             "y_range": [-285, -223]})
# A notch in the exposed interior edge, carried through both floor plates.
radii = [29, 26, 31, 27, 30, 25, 32, 27, 30, 26, 31, 28]
ring = [(248 + r * math.cos(i * math.tau / len(radii)),
         -173 + r * math.sin(i * math.tau / len(radii)))
        for i, r in enumerate(radii)]
floor = prism("Floor edge collapse", [(x, y, 60) for x, y in ring],
              [(x, y, 150) for x, y in ring])
report["operations"].append({"name": floor.name, "xy_profile": ring,
                             "z_range": [60, 150]})
for name in (("secondFloor",) if TAG == "probe_holes" else ("firstFloor", "secondFloor")):
    obj = bpy.data.objects[name]
    # Baseline source-coordinate scene shares mesh data: detach before edits.
    obj.data = obj.data.copy()
    report["meshes"][name] = {"before": mesh_stats(obj)}
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    for cutter in (wall, floor):
        print("BOOLEAN", name, cutter.name, flush=True)
        mod = obj.modifiers.new(cutter.name, "BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.solver = "EXACT"
        mod.use_self = False
        mod.use_hole_tolerant = True
        mod.object = cutter
        bpy.ops.object.modifier_apply(modifier=mod.name)
    report["meshes"][name]["after"] = mesh_stats(obj)
    before_bounds = np.array(report["meshes"][name]["before"]["bounds_local"])
    after_bounds = np.array(report["meshes"][name]["after"]["bounds_local"])
    assert np.all(after_bounds[0] >= before_bounds[0] - 0.001), "Subtraction expanded minimum bounds"
    assert np.all(after_bounds[1] <= before_bounds[1] + 0.001), "Subtraction expanded maximum bounds"
    assert report["meshes"][name]["after"]["polygons"] > 0
    assert report["meshes"][name]["after"]["polygons"] != report["meshes"][name]["before"]["polygons"]
    # Place exports on z=0 and near XY origin; record reversible translation.
    bpy.context.view_layer.update()
    bounds = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    lower = Vector([min(v[i] for v in bounds) for i in range(3)])
    saved_location = obj.location.copy()
    obj.location -= lower
    bpy.context.view_layer.update()
    path = EXPORT / (name + "_damaged.stl")
    bpy.ops.wm.stl_export(filepath=str(path), export_selected_objects=True)
    obj.location = saved_location
    report["exports"][name] = {"file": str(path.relative_to(ROOT)),
                               "translation_from_assembly": list(-lower)}
    print("EXPORTED", name, flush=True)
for cutter in (wall, floor):
    bpy.data.objects.remove(cutter, do_unlink=True)
scene.camera = bpy.data.objects["exterior"]
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "scenes" / (TAG + ".blend")))
(ROOT / "reports" / (TAG + ".json")).write_text(json.dumps(report, indent=2) + "\n")
for name in ("exterior", "interior", "facade"):
    scene.camera = bpy.data.objects[name]
    scene.render.filepath = str(OUT / (name + ".png"))
    bpy.ops.render.render(write_still=True)
print("VARIANT_COMPLETE", flush=True)
