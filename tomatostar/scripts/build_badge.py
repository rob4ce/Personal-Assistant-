"""Part 3 - LOGO BADGE (white): raised oval badge that seats in the belly
recess. Front face is a clean raised oval (apply the TomatoStar logo as a
printed sticker or a multi-colour top layer)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p
from build_faceplate import elliptical_cylinder_y

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def build_badge():
    # Curved oval disc matching body curvature, standing slightly proud (raised).
    e_out = c.ellipsoid((p.BODY_RX + 1.5, p.BODY_RY + 1.5, p.BODY_RZ + 1.5),
                        center=(0, 0, p.BODY_CZ), subdiv=5)
    e_in = c.ellipsoid((p.BODY_RX - 1, p.BODY_RY - p.BADGE_THICK, p.BODY_RZ - 1),
                       center=(0, 0, p.BODY_CZ), subdiv=5)
    shell = c.difference(e_out, e_in)

    oval = elliptical_cylinder_y(p.BADGE_HALF_W - p.CLEARANCE, p.BADGE_HALF_H - p.CLEARANCE,
                                 60, center=(0, p.BODY_RY, p.BADGE_CZ))
    badge = c.intersection([shell, oval])

    # Small locating peg on the back (drops into a hole in the body).
    peg = c.cylinder(2.4 - p.CLEARANCE, 6, center=(0, p.BODY_RY - p.BADGE_THICK - 2, p.BADGE_CZ), axis="y")
    badge = c.union([badge, peg])

    c.set_color(badge, c.WHITE)
    return badge


if __name__ == "__main__":
    m = build_badge()
    print("watertight:", m.is_watertight, "| bounds:", np.round(m.bounds, 1).tolist())
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "3_badge_white.3mf"))
    m.export(os.path.join(OUT, "3_badge_white.stl"))
    print("exported 3_badge_white")
