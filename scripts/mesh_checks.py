"""Read-only topology counts, usable inside Blender's Python."""
import numpy as np


def mesh_stats(obj):
    mesh = obj.data
    loop_edges = np.empty(len(mesh.loops), dtype=np.int32)
    mesh.loops.foreach_get("edge_index", loop_edges)
    uses = np.bincount(loop_edges, minlength=len(mesh.edges))
    coords = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
    mesh.vertices.foreach_get("co", coords)
    mesh.calc_loop_triangles()
    return {
        "vertices": len(mesh.vertices), "polygons": len(mesh.polygons),
        "triangles": len(mesh.loop_triangles), "edges": len(mesh.edges),
        "boundary_edges": int(np.count_nonzero(uses == 1)),
        "wire_edges": int(np.count_nonzero(uses == 0)),
        "edges_over_two_faces": int(np.count_nonzero(uses > 2)),
        "finite_coordinates": bool(np.isfinite(coords).all()),
        "bounds_local": [coords.reshape(-1, 3).min(axis=0).tolist(),
                         coords.reshape(-1, 3).max(axis=0).tolist()],
    }
