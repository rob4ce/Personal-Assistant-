"""Headless multi-view preview renderer (matplotlib, Lambert shading).

Usage: python3 render.py <mesh.stl_or_3mf> <out.png> [--color R,G,B] [--views]
Renders a few angles into one PNG so geometry can be sanity-checked.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh


def shade(mesh, base_rgb, elev, azim):
    tris = mesh.triangles  # (n,3,3)
    normals = mesh.face_normals
    # Light from the camera position (so whatever we look at is lit), lifted up.
    a, e = np.deg2rad(azim), np.deg2rad(elev + 20)
    cam = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    light = cam / np.linalg.norm(cam)
    intensity = np.clip(normals @ light, 0, 1) * 0.75 + 0.25
    base = np.array(base_rgb) / 255.0
    colors = np.clip(intensity[:, None] * base[None, :], 0, 1)
    return tris, colors


def render(meshes_colors, out, title=""):
    views = [("front", 8, 90), ("three-quarter", 18, 55), ("right", 5, 0)]
    fig = plt.figure(figsize=(13, 5.2))
    fig.patch.set_facecolor("#f4f4f4")
    for i, (name, elev, azim) in enumerate(views):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        allpts = []
        for mesh, color in meshes_colors:
            tris, colors = shade(mesh, color, elev, azim)
            pc = Poly3DCollection(tris, facecolors=colors, edgecolors="none")
            ax.add_collection3d(pc)
            allpts.append(mesh.vertices)
        pts = np.vstack(allpts)
        c = pts.mean(0)
        r = (pts.max(0) - pts.min(0)).max() / 2 * 1.05
        ax.set_xlim(c[0] - r, c[0] + r)
        ax.set_ylim(c[1] - r, c[1] + r)
        ax.set_zlim(c[2] - r, c[2] + r)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
        ax.set_title(name, fontsize=11, color="#333")
    if title:
        fig.suptitle(title, fontsize=14, color="#1a5", weight="bold")
    plt.tight_layout()
    fig.savefig(out, dpi=90, facecolor=fig.get_facecolor())
    print("wrote", out)


if __name__ == "__main__":
    path = sys.argv[1]
    out = sys.argv[2]
    color = [214, 40, 40]
    if "--color" in sys.argv:
        color = [int(x) for x in sys.argv[sys.argv.index("--color") + 1].split(",")]
    mesh = trimesh.load(path, force="mesh")
    render([(mesh, color)], out, title=os.path.basename(path))
