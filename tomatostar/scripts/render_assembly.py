"""Render all four parts assembled together, plus an exploded view."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
from render import render
import common as c

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

parts = [
    ("1_body_red.stl", [214, 40, 40]),
    ("2_faceplate_black.stl", [26, 26, 26]),
    ("3_badge_white.stl", [245, 245, 245]),
    ("4_calyx_green.stl", [90, 160, 45]),
]

meshes_colors = []
for fn, col in parts:
    m = trimesh.load(os.path.join(OUT, fn), force="mesh")
    meshes_colors.append((m, col))

render(meshes_colors, os.path.join(os.path.dirname(__file__), "..", "preview", "assembly_v01.png"),
       title="TomatoStar v0.1 - assembled (4 parts)")

# Exploded: shift parts outward along their insertion axes.
explode = [(0, 0, 0), (0, 22, 0), (0, 20, 0), (0, 0, 26)]
meshes_colors_x = []
for (m, col), off in zip(meshes_colors, explode):
    mm = m.copy()
    mm.apply_translation(off)
    meshes_colors_x.append((mm, col))
render(meshes_colors_x, os.path.join(os.path.dirname(__file__), "..", "preview", "exploded_v01.png"),
       title="TomatoStar v0.1 - exploded")
print("done")
