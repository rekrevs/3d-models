"""Independent reload, preserved-region check, and STL round-trip inspection."""
import hashlib
import json
import sys
from pathlib import Path
import bpy
import numpy as np
from mathutils.kdtree import KDTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mesh_checks import mesh_stats


def coords(obj):
    out = np.empty(len(obj.data.vertices) * 3, dtype=np.float32)
    obj.data.vertices.foreach_get("co", out)
    return out.reshape(-1, 3)


def ordered_region(obj):
    points = coords(obj)
    points = points[points[:, 0] < 185]
    return np.unique(points, axis=0)


def protected_region_distance(a, b):
    """Check vertex proximity in both directions, allowing re-tessellation."""
    def unmatched(left, right):
        dtype = np.dtype([("x", "<f4"), ("y", "<f4"), ("z", "<f4")])
        left = np.ascontiguousarray(np.round(left, 4))
        right = np.ascontiguousarray(np.round(right, 4))
        difference = np.setdiff1d(left.view(dtype).ravel(), right.view(dtype).ravel())
        return difference.view(np.float32).reshape(-1, 3)
    max_distance = 0.0
    counts = []
    for left, right in ((a, b), (b, a)):
        missing = unmatched(left, right)
        counts.append(len(missing))
        if len(missing):
            tree = KDTree(len(right))
            for i, point in enumerate(right):
                tree.insert(point, i)
            tree.balance()
            max_distance = max(max_distance, max(tree.find(point)[2] for point in missing))
    return max_distance, counts


bpy.ops.wm.open_mainfile(filepath=str(ROOT / "scenes" / "damaged_01.blend"))
report = {"sources_unchanged": {}, "preserved_corner_region": {}, "roundtrip": {}}
inventory = json.loads((ROOT / "reports" / "source_inventory.json").read_text())
for entry in inventory["files"]:
    with (ROOT / entry["file"]).open("rb") as stream:
        ok = hashlib.file_digest(stream, "sha256").hexdigest() == entry["sha256"]
    report["sources_unchanged"][entry["file"]] = ok
    assert ok, entry["file"]

ground = bpy.data.objects["groundFloor"]
source_ground = bpy.data.objects["groundFloor_source"]
report["ground_mesh_unchanged"] = ground.data == source_ground.data
assert report["ground_mesh_unchanged"]
variant = json.loads((ROOT / "reports" / "damaged_01.json").read_text())
for name in ("firstFloor", "secondFloor"):
    obj = bpy.data.objects[name]
    original = bpy.data.objects[name + "_source"]
    a, b = ordered_region(obj), ordered_region(original)
    distance, counts = protected_region_distance(a, b)
    ok = distance < 0.1
    report["preserved_corner_region"][name] = {"x_less_than": 185, "within_0_1_mm": ok,
        "max_vertex_distance_mm": distance, "unmatched_after_rounding": counts,
        "vertices_after": len(a), "vertices_before": len(b)}
    print("CORNER", name, report["preserved_corner_region"][name], flush=True)
    assert ok, "Protected corner changed"
    expected = coords(obj)
    dimensions = expected.max(axis=0) - expected.min(axis=0)
    bpy.ops.wm.stl_import(filepath=str(ROOT / variant["exports"][name]["file"]))
    imported = bpy.context.object
    stats = mesh_stats(imported)
    bounds = np.array(stats["bounds_local"])
    stats["dimensions_match"] = bool(np.allclose(bounds[1] - bounds[0], dimensions, atol=0.0001, rtol=0))
    stats["on_origin"] = bool(np.allclose(bounds[0], 0, atol=0.0001, rtol=0))
    assert stats["dimensions_match"] and stats["on_origin"] and stats["finite_coordinates"]
    report["roundtrip"][name] = stats
    bpy.data.objects.remove(imported, do_unlink=True)
(ROOT / "reports" / "damaged_01-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2), flush=True)
