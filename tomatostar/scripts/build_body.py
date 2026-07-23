"""Part 1 - BODY (red): head+body+arms+wheels, with face recess, badge recess
and calyx socket. Printability-first stylised interpretation."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def build_body():
    # --- main rounded body/head (one chibi blob) ---
    body = c.ellipsoid((p.BODY_RX, p.BODY_RY, p.BODY_RZ), center=(0, 0, p.BODY_CZ), subdiv=5)

    # subtle cheek widening low down for a friendlier squat silhouette
    belly = c.ellipsoid((p.BODY_RX * 1.02, p.BODY_RY * 1.05, p.BODY_RZ * 0.5),
                        center=(0, 2, p.BODY_CZ - 14), subdiv=5)
    body = c.union([body, belly])

    # --- arms: stubby capsules tucked down against the sides (no supports) ---
    arm_l = c.capsule(p.ARM_R, 20, center=(-p.BODY_RX + 2, 6, 34), axis="z")
    arm_r = c.capsule(p.ARM_R, 20, center=(p.BODY_RX - 2, 6, 34), axis="z")
    # tilt them slightly outward at the bottom
    for arm, s in ((arm_l, -1), (arm_r, 1)):
        arm.apply_transform(trimesh.transformations.rotation_matrix(
            s * np.deg2rad(12), [0, 1, 0], point=(s * (p.BODY_RX - 2), 6, 44)))
    # little rounded hands
    hand_l = c.sphere(p.ARM_R * 1.05, center=(-p.BODY_RX - 1, 8, 26))
    hand_r = c.sphere(p.ARM_R * 1.05, center=(p.BODY_RX + 1, 8, 26))

    # --- wheels/feet: flattened rounded feet giving a stable base ---
    foot_l = c.ellipsoid((p.WHEEL_R, p.WHEEL_R * 1.25, p.WHEEL_R * 0.9), center=(-15, 6, 9))
    foot_r = c.ellipsoid((p.WHEEL_R, p.WHEEL_R * 1.25, p.WHEEL_R * 0.9), center=(15, 6, 9))

    body = c.union([body, arm_l, arm_r, hand_l, hand_r, foot_l, foot_r])

    # --- flatten the very bottom for a clean first layer on the print bed ---
    floor_cut = trimesh.creation.box(extents=(200, 200, 20))
    floor_cut.apply_translation((0, 0, -10 + 3.0))  # keep floor at z=3
    body = c.difference(body, floor_cut)

    # --- face recess (oval pocket on the upper front) ---
    face_pocket = c.ellipsoid((p.FACE_HALF_W, p.FACE_DEPTH * 2.2, p.FACE_HALF_H),
                              center=(0, p.BODY_RY + p.FACE_DEPTH * 1.4, p.FACE_CZ), subdiv=5)
    body = c.difference(body, face_pocket)

    # --- badge recess (smaller oval on the belly) ---
    badge_pocket = c.ellipsoid((p.BADGE_HALF_W, p.BADGE_DEPTH * 2.0, p.BADGE_HALF_H),
                               center=(0, p.BODY_RY + p.BADGE_DEPTH * 0.7, p.BADGE_CZ), subdiv=5)
    body = c.difference(body, badge_pocket)

    # --- calyx socket on top (blind cylindrical hole for the stem peg) ---
    socket = c.cylinder(p.STEM_R + p.CLEARANCE, p.STEM_DEPTH * 2,
                        center=(0, 0, p.BODY_TOP_Z - 2), axis="z")
    body = c.difference(body, socket)

    c.set_color(body, c.RED)
    return body


if __name__ == "__main__":
    body = build_body()
    print("watertight:", body.is_watertight, "| volume(cm^3):", round(body.volume / 1000, 1))
    print("bounds:", np.round(body.bounds, 1).tolist())
    os.makedirs(OUT, exist_ok=True)
    body.export(os.path.join(OUT, "1_body_red.3mf"))
    body.export(os.path.join(OUT, "1_body_red.stl"))
    print("exported 1_body_red.3mf / .stl")
