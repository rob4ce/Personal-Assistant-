"""01_Body_Red - Project Mater v1.5, built to the engineering brief.

Tomato shell + torso + arms + decorative wheels + hidden flat base, with:
- curved rounded-rect face recess (2 mm seat) + 4 locating-pin holes
- chest badge recess (1.5 mm) + 2 locating-pin holes
- keyed cross socket on top for the calyx
- glue relief pockets behind cosmetic joints
No headset geometry on the red body (it lives on the faceplate).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def head_solid(scale=0.0):
    """Head ellipsoid, optionally shrunk by `scale` mm on every radius."""
    return c.ellipsoid((p.HEAD_RX - scale, p.HEAD_RY - scale, p.HEAD_RZ - scale),
                       center=(0, 0, p.HEAD_CZ), subdiv=5)


def head_surf_y(x, z):
    """Front (+Y) surface height of the head ellipsoid at (x, z)."""
    t = 1 - (x / p.HEAD_RX) ** 2 - ((z - p.HEAD_CZ) / p.HEAD_RZ) ** 2
    return p.HEAD_RY * np.sqrt(max(t, 0.01))


def build_body():
    head = head_solid()
    torso = c.ellipsoid((p.TORSO_RX, p.TORSO_RY, p.TORSO_RZ), center=(0, 2, p.TORSO_CZ), subdiv=5)

    # hidden flat base pad (stable 46 x 34 footprint, flat bottom at z=0)
    base = c.rounded_rect_prism(p.BASE_W, p.BASE_D, p.BASE_Z, fillet=8,
                                center=(0, 2, p.BASE_Z / 2), axis="z")

    body = c.union([head, torso, base])

    # --- arms: stubby, tucked down (<=45deg overhang, no supports) ---
    arms = []
    for s in (-1, 1):
        arm = c.capsule(7.0, 16, center=(s * (p.TORSO_RX - 1), 6, 22), axis="z")
        arm.apply_transform(trimesh.transformations.rotation_matrix(
            s * np.deg2rad(14), [0, 1, 0], point=(s * (p.TORSO_RX - 1), 6, 30)))
        hand = c.sphere(7.5, center=(s * (p.TORSO_RX + 2), 9, 14))
        arms += [arm, hand]
    body = c.union([body] + arms)

    # --- 4 decorative wheels (float ~0.5 mm above the desk) + axles to the base ---
    wheels = []
    wr = 8.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            cy = sy * 14 + 2
            hub = c.cylinder(wr, 8, center=(sx * 32, cy, wr + p.WHEEL_FLOAT), axis="x")
            axle = c.segment((sx * 21, cy, 4.5), (sx * 33, cy, 4.5), 3.0)  # base -> wheel
            wheels += [hub, axle]
    body = c.union([body] + wheels)

    # --- top dimple + keyed calyx socket ---
    dimple = c.sphere(9, center=(0, 0, p.HEAD_CZ + p.HEAD_RZ + 3))
    body = c.difference(body, dimple)
    top_z = body.bounds[1][2]
    socket = c.cross_key(p.CALYX_KEY_MAJOR, p.CALYX_KEY_ARM, p.CALYX_ENGAGE * 2 + 2,
                         center=(0, 0, top_z - p.CALYX_ENGAGE + 1), axis="z",
                         clearance=p.CALYX_CLEAR)
    body = c.difference(body, socket)

    # --- curved rounded-rect FACE recess (2 mm seat, conforms to tomato) ---
    seat_shell = c.difference(head_solid(), head_solid(scale=p.FACE_SEAT_DEPTH))
    # front-only prism (spans y=0..60) so the back of the head is untouched.
    face_prism = c.rounded_rect_prism(p.FACE_W, p.FACE_H, 60, p.FACE_FILLET,
                                      center=(0, 30, p.FACE_CZ), axis="y")
    face_seat = c.intersection([seat_shell, face_prism])
    body = c.difference(body, face_seat)

    # extra blind cavity so the face reads recessed (eye depth behind panel)
    cav_shell = c.difference(head_solid(scale=p.FACE_SEAT_DEPTH), head_solid(scale=p.FACE_SEAT_DEPTH + 6))
    cav_prism = c.rounded_rect_prism(p.FACE_W - 2 * p.FACE_SHOULDER, p.FACE_H - 2 * p.FACE_SHOULDER,
                                     60, p.FACE_FILLET, center=(0, 30, p.FACE_CZ), axis="y")
    body = c.difference(body, c.intersection([cav_shell, cav_prism]))

    # --- faceplate locating-pin holes (drilled inward from the local surface) ---
    for sx, sz in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        cx, cz = sx * p.FACE_PIN_DX, p.FACE_CZ + sz * p.FACE_PIN_DZ
        ys = head_surf_y(cx, cz)
        L = p.FACE_PIN_ENGAGE + 5
        hole = c.cylinder(p.FACE_PIN_D / 2 + p.FACE_CLEAR, L,
                          center=(cx, ys + 1 - L / 2, cz), axis="y")
        body = c.difference(body, hole)

    # --- chest BADGE recess (flat-floored oval pocket, ~1.5 mm) + 2 pin holes ---
    # front surface of the torso near the badge, then cut a flat oval pocket.
    y_surf = 2 + p.TORSO_RY * np.sqrt(max(1 - ((p.BADGE_CZ - p.TORSO_CZ) / p.TORSO_RZ) ** 2, 0.01))
    puck = c.cylinder(1.0, 6.0, center=(0, y_surf - p.BADGE_RECESS + 3.0, p.BADGE_CZ), axis="y", sections=96)
    puck.apply_scale((p.BADGE_W / 2, 1, p.BADGE_H / 2))
    puck = c.union([puck])  # re-tessellate cleanly after scaling
    body = c.difference(body, puck)
    for sx in (-1, 1):
        hole = c.cylinder(p.BADGE_PIN_D / 2 + p.BADGE_CLEAR, p.BADGE_PIN_ENGAGE + 3,
                          center=(sx * p.BADGE_PIN_SPACING / 2, p.TORSO_RY - 2, p.BADGE_CZ), axis="y")
        body = c.difference(body, hole)

    # --- clean flat bottom at the desk plane ---
    body = c.difference(body, c.box((200, 200, 20), center=(0, 0, -10)))

    c.set_color(body, p.RED)
    return body


if __name__ == "__main__":
    body = build_body()
    ext = body.extents
    print("watertight:", body.is_watertight)
    print(f"W x D x H = {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm (target 72 x 60 x 92)")
    print("volume(cm^3):", round(body.volume / 1000, 1))
    os.makedirs(OUT, exist_ok=True)
    body.export(os.path.join(OUT, "01_Body_Red.3mf"))
    body.export(os.path.join(OUT, "01_Body_Red.stl"))
    print("exported 01_Body_Red")
