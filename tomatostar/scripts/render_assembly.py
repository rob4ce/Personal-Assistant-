"""Build all four parts in their assembled positions and render assembled +
exploded previews. Also exports an assembled 3MF for viewing."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p
from render import render
from build_body import build_body
from build_faceplate import build_faceplate
from build_badge import build_badge
from build_calyx import build_calyx

OUT = os.path.join(os.path.dirname(__file__), "..", "output")
PRE = os.path.join(os.path.dirname(__file__), "..", "preview")

body = build_body()
face = build_faceplate()
badge = build_badge()
top_z = body.bounds[1][2]
calyx = build_calyx(z0=top_z)

parts = [
    (body, p.RED[:3]),
    (face, p.BLACK[:3]),
    (badge, p.WHITE[:3]),
    (calyx, p.GREEN[:3]),
]
render(parts, os.path.join(PRE, "assembly_v1_5.png"),
       title="Project Mater v1.5 - assembled")

# Exploded along insertion axes.
offs = [(0, 0, 0), (0, 26, 0), (0, 22, 0), (0, 0, 30)]
xparts = []
for (m, col), off in zip(parts, offs):
    mm = m.copy(); mm.apply_translation(off); xparts.append((mm, col))
render(xparts, os.path.join(PRE, "exploded_v1_5.png"),
       title="Project Mater v1.5 - exploded")

# Assembled 3MF for viewing (colored scene).
scene = trimesh.Scene()
for m, col in parts:
    mm = m.copy(); c.set_color(mm, list(col) + [255]); scene.add_geometry(mm)
scene.export(os.path.join(OUT, "Mater_v1_5_Assembly.3mf"))
print("rendered + exported assembly")
