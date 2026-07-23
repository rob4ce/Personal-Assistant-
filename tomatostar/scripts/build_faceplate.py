"""Part 2 - FACEPLATE (black): curved oval plate that seats in the body's face
recess, with recessed eyes + smile to fill with white."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def elliptical_cylinder_y(hw, hh, length, center):
    """Cylinder along Y with elliptical cross-section (hw in X, hh in Z)."""
    m = c.cylinder(1.0, length, axis="y", sections=96)
    m.apply_scale((hw, 1.0, hh))
    m.apply_translation(center)
    return m


def build_faceplate():
    # Outer/inner surfaces share the body's curvature so the plate is conformal.
    e_out = c.ellipsoid((p.BODY_RX, p.BODY_RY, p.BODY_RZ), center=(0, 0, p.BODY_CZ), subdiv=5)
    e_in = c.ellipsoid((p.BODY_RX - 1, p.BODY_RY - p.FACEPLATE_THICK, p.BODY_RZ - 1),
                       center=(0, 0, p.BODY_CZ), subdiv=5)
    shell = c.difference(e_out, e_in)

    # Oval boundary (slip-fit: a touch smaller than the pocket).
    oval = elliptical_cylinder_y(p.FACE_HALF_W - p.CLEARANCE, p.FACE_HALF_H - p.CLEARANCE,
                                 60, center=(0, p.BODY_RY, p.FACE_CZ))
    plate = c.intersection([shell, oval])

    # --- eyes: two rounded oval pockets ---
    eye_dy = p.BODY_RY - 1.5
    for sx in (-1, 1):
        eye = c.ellipsoid((3.6, 3.5, 5.0), center=(sx * 8.0, eye_dy, p.FACE_CZ + 1.5), subdiv=4)
        plate = c.difference(plate, eye)

    # --- smile: shallow crescent (big sphere minus offset sphere) ---
    smile_c = (0, eye_dy + 0.5, p.FACE_CZ - 6.5)
    smile = c.ellipsoid((6.5, 3.0, 3.0), center=smile_c, subdiv=4)
    cut = c.ellipsoid((7.5, 4.0, 3.0), center=(0, eye_dy + 0.5, p.FACE_CZ - 4.2), subdiv=4)
    smile = c.difference(smile, cut)
    plate = c.difference(plate, smile)

    c.set_color(plate, c.BLACK)
    return plate


if __name__ == "__main__":
    m = build_faceplate()
    print("watertight:", m.is_watertight, "| bounds:", np.round(m.bounds, 1).tolist())
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "2_faceplate_black.3mf"))
    m.export(os.path.join(OUT, "2_faceplate_black.stl"))
    print("exported 2_faceplate_black")
