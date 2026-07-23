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


def rounded_rect_prism(w, h, depth, fillet, center=(0, 0, 0), axis="y"):
    """A rounded-rectangle profile (in the plane perpendicular to `axis`)
    extruded `depth` along `axis`. Profile is w (first in-plane) x h (second)."""
    import shapely.geometry as sg

    fillet = min(fillet, w / 2 - 0.01, h / 2 - 0.01)
    poly = sg.box(-w / 2, -h / 2, w / 2, h / 2).buffer(-0.0)
    poly = sg.box(-w / 2 + fillet, -h / 2 + fillet, w / 2 - fillet, h / 2 - fillet).buffer(fillet, join_style=1)
    m = trimesh.creation.extrude_polygon(poly, height=depth)
    m.apply_translation((0, 0, -depth / 2))  # centre on extrusion axis (local Z)
    if axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    elif axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation(center)
    return m


def tapered_pin(d_base, d_tip, length, center=(0, 0, 0), axis="y"):
    """A slightly tapered locating pin (truncated cone) with a rounded tip."""
    m = trimesh.creation.cone(radius=d_base / 2, height=length, sections=32)
    # cone tip is sharp; blend it. Use a frustum via two-radius cylinder instead.
    m = _frustum(d_base / 2, d_tip / 2, length, sections=32)
    if axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    elif axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation(center)
    return m


def _frustum(r0, r1, h, sections=32):
    ang = np.linspace(0, 2 * np.pi, sections, endpoint=False)
    bot = np.c_[r0 * np.cos(ang), r0 * np.sin(ang), np.zeros(sections)]
    top = np.c_[r1 * np.cos(ang), r1 * np.sin(ang), np.full(sections, h)]
    verts = np.vstack([bot, top, [0, 0, 0], [0, 0, h]])
    n = sections
    cb, ct = 2 * n, 2 * n + 1
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces += [[i, j, n + j], [i, n + j, n + i]]        # side
        faces += [[cb, j, i]]                               # bottom
        faces += [[ct, n + i, n + j]]                       # top
    return trimesh.Trimesh(vertices=verts, faces=np.array(faces), process=True)


def cross_key(major, arm, height, center=(0, 0, 0), axis="z", clearance=0.0):
    """A '+' cross-section keyed peg/socket, extruded along `axis`.
    `major` = overall span, `arm` = thickness of each bar."""
    import shapely.geometry as sg

    a = sg.box(-major / 2, -arm / 2, major / 2, arm / 2)
    b = sg.box(-arm / 2, -major / 2, arm / 2, major / 2)
    poly = a.union(b)
    if clearance:
        poly = poly.buffer(clearance, join_style=2)
    m = trimesh.creation.extrude_polygon(poly, height=height)
    m.apply_translation((0, 0, -height / 2))
    if axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    elif axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation(center)
    return m


def box(extents, center=(0, 0, 0)):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    return m


def torus(major_r, minor_r, center=(0, 0, 0), axis="z", sections=48):
    m = trimesh.creation.torus(major_radius=major_r, minor_radius=minor_r,
                               major_sections=sections, minor_sections=24)
    if axis == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    elif axis == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation(center)
    return m


def segment(p0, p1, radius, sections=24):
    """A capsule spanning from point p0 to point p1."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    length = np.linalg.norm(p1 - p0)
    m = trimesh.creation.capsule(radius=radius, height=length, count=[sections, sections])
    # capsule is built along +Z from origin; align its axis to (p1-p0) and move.
    z = np.array([0, 0, 1.0])
    d = (p1 - p0) / length
    axis = np.cross(z, d)
    if np.linalg.norm(axis) < 1e-9:
        R = np.eye(4) if d[2] > 0 else trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
    else:
        angle = np.arccos(np.clip(z @ d, -1, 1))
        R = trimesh.transformations.rotation_matrix(angle, axis / np.linalg.norm(axis))
    m.apply_transform(R)
    m.apply_translation(p0)
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
