import json
import sys
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mesh_checks import mesh_stats

bpy.ops.wm.open_mainfile(filepath=str(ROOT / "scenes" / "baseline.blend"))
report = {name: mesh_stats(bpy.data.objects[name])
          for name in ("groundFloor", "firstFloor", "secondFloor")}
(ROOT / "reports" / "baseline-mesh.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2), flush=True)
