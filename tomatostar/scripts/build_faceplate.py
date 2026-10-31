"""02_Faceplate_Black - Project Mater v1.5.

Curved rounded-rect face panel (58x36) that seats 2 mm into the body, with:
- recessed eyes + smile (fill white)
- 4 tapered locating pins on the back
- integrated gaming headset: ear cups, headband arc, mic boom
  (the brief puts the whole headset on the faceplate, not the red head)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def head_shell(inner, outer):
    """Shell of the head between two inward offsets (mm)."""
    return c.difference(
        c.ellipsoid((p.HEAD_RX - inner, p.HEAD_RY - inner, p.HEAD_RZ - inner), (0, 0, p.HEAD_CZ), 5),
        c.ellipsoid((p.HEAD_RX - outer, p.HEAD_RY - outer, p.HEAD_RZ - outer), (0, 0, p.HEAD_CZ), 5))


def build_faceplate():
    # --- curved face panel conforming to the head front, ~0.5 mm proud ---
    shell = head_shell(-0.5, p.FACE_SEAT_DEPTH)  # from 0.5 mm proud of surface to 2 mm in
    panel_prism = c.rounded_rect_prism(p.FACE_W - 2 * p.FACE_CLEAR, p.FACE_H - 2 * p.FACE_CLEAR,
                                       60, p.FACE_FILLET, center=(0, 30, p.FACE_CZ), axis="y")
    panel = c.intersection([shell, panel_prism])

    def surf(x, z):
        t = 1 - (x / p.HEAD_RX) ** 2 - ((z - p.HEAD_CZ) / p.HEAD_RZ) ** 2
        return p.HEAD_RY * np.sqrt(max(t, 0.01))

    # --- ear cups: discs tangent to the head sides (inner face ~ surface) ---
    # + rim-riding blobs that bridge the panel edge out to each cup on the
    # exterior, so nothing buries into the (wide) tomato head.
    parts = [panel]
    for sx in (-1, 1):
        cup = c.cylinder(10, 4, center=(sx * 33.2, 0, p.FACE_CZ), axis="x", sections=64)  # x31.2..35.2
        rim = c.cylinder(10.5, 1.2, center=(sx * 30.8, 0, p.FACE_CZ), axis="x")           # bezel
        blob = c.sphere(5.0, center=(sx * 30.5, surf(sx * 30.5, p.FACE_CZ) + 0.5, p.FACE_CZ))
        parts += [cup, rim, blob]

    # --- headband arc riding just outside the head, through the cup centres ---
    band = c.torus(32.6, 3.0, center=(0, 0, p.FACE_CZ), axis="y", sections=96)
    band = c.intersection([band, c.box((90, 40, 70), center=(0, 0, p.FACE_CZ + 18))])
    parts.append(band)

    # --- mic boom: two-segment rod rooted in the left ear cup ---
    j = (-26, 22, p.FACE_CZ - 2)
    seg1 = c.segment((-32, 3, p.FACE_CZ - 2), j, 2.1)
    seg2 = c.segment(j, (-9, 26, p.FACE_CZ - 9), 2.1)
    mic = c.sphere(2.8, center=(-9, 26, p.FACE_CZ - 9))
    parts += [seg1, seg2, mic]

    face = c.union(parts)

    # --- tapered locating pins on the back, pointing inward (-Y) ---
    def surf(x, z):
        t = 1 - (x / p.HEAD_RX) ** 2 - ((z - p.HEAD_CZ) / p.HEAD_RZ) ** 2
        return p.HEAD_RY * np.sqrt(max(t, 0.01))

    pins = []
    for sx, sz in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        cx, cz = sx * p.FACE_PIN_DX, p.FACE_CZ + sz * p.FACE_PIN_DZ
        ys = surf(cx, cz)
        L = p.FACE_PIN_ENGAGE + 1.5
        # frustum along +Z, rotated to point -Y, base anchored just inside the panel back
        pin = c._frustum(p.FACE_PIN_D / 2, p.FACE_PIN_D / 2 - 0.4, L, sections=32)
        pin.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))  # +Z -> -Y
        pin.apply_translation((cx, ys - p.FACE_SEAT_DEPTH + 0.5, cz))
        pins.append(pin)
    face = c.union([face] + pins)

    # --- recessed eyes + smile (shallow ~1 mm dishes that stay within black) ---
    def surf_y(x, z):
        t = 1 - (x / p.HEAD_RX) ** 2 - ((z - p.HEAD_CZ) / p.HEAD_RZ) ** 2
        return p.HEAD_RY * np.sqrt(max(t, 0.01))

    for sx in (-1, 1):
        x, z = sx * 9, p.FACE_CZ + 2
        eye = c.ellipsoid((4.2, p.EYE_RECESS, 6.0), center=(x, surf_y(x, z), z), subdiv=4)
        face = c.difference(face, eye)
    # smile: shallow curved dish
    z = p.FACE_CZ - 9
    smile = c.ellipsoid((8.0, p.EYE_RECESS, 3.0), center=(0, surf_y(0, z), z), subdiv=4)
    smile_cut = c.ellipsoid((10, p.EYE_RECESS, 3.2), center=(0, surf_y(0, z) + 2.0, z + 2.4), subdiv=4)
    smile = c.difference(smile, smile_cut)
    face = c.difference(face, smile)

    c.set_color(face, p.BLACK)
    return face


if __name__ == "__main__":
    m = build_faceplate()
    print("watertight:", m.is_watertight, "| ext:", [round(x, 1) for x in m.extents])
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "02_Faceplate_Black.3mf"))
    m.export(os.path.join(OUT, "02_Faceplate_Black.stl"))
    print("exported 02_Faceplate_Black")
