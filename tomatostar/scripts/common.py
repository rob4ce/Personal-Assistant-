"""Shared geometry helpers for the TomatoStar model.

Conventions
-----------
- Units are millimetres.
- +Z is up, +Y is the front (the face), +X is the character's right.
- Origin (0,0,0) sits at floor level, centred under the body.

Everything is built from smooth primitives (icospheres / cylinders) combined
with manifold boolean operations. This is a stylised, printability-first
interpretation of the concept art -- clean geometric forms, not a surface-exact
copy of the studio render.
"""
import numpy as np
import trimesh

ENGINE = "manifold"


def ellipsoid(radii, center=(0, 0, 0), subdiv=4):
    """An axis-aligned ellipsoid via a scaled icosphere."""
    m = trimesh.creation.icosphere(subdivisions=subdiv, radius=1.0)
    m.apply_scale(radii)
    m.apply_translation(center)
    return m


def sphere(radius, center=(0, 0, 0), subdiv=4):
    return ellipsoid((radius, radius, radius), center, subdiv)


def cylinder(radius, height, center=(0, 0, 0), axis="z", sections=64):
    """A cylinder centred at `center`, aligned to the given axis."""
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    if axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    elif axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation(center)
    return m


def capsule(radius, length, center=(0, 0, 0), axis="z", sections=32):
    """A rounded capsule (cylinder + hemispherical caps)."""
    m = trimesh.creation.capsule(radius=radius, height=length, count=[sections, sections])
    # trimesh capsule is built along +Z starting at origin; recentre it.
    m.apply_translation((0, 0, -length / 2))
    if axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    elif axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation(center)
    return m


def union(meshes):
    return trimesh.boolean.union(meshes, engine=ENGINE)


def difference(a, b):
    return trimesh.boolean.difference([a, b], engine=ENGINE)


def intersection(meshes):
    return trimesh.boolean.intersection(meshes, engine=ENGINE)


def set_color(mesh, rgba):
    mesh.visual = trimesh.visual.ColorVisuals(mesh=mesh, face_colors=np.tile(rgba, (len(mesh.faces), 1)))
    return mesh


# Palette (RGBA 0-255) matching the concept art.
RED = [214, 40, 40, 255]
BLACK = [26, 26, 26, 255]
WHITE = [245, 245, 245, 255]
GREEN = [90, 160, 45, 255]
