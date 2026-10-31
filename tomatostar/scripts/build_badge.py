"""03_Logo_Badge_White - Project Mater v1.5.

White oval emblem (40x24), ~2 mm thick, printed flat-back-on-bed logo-up. Two
locating pins prevent rotation; badge sits ~0.5 mm proud of the 1.5 mm recess.
Apply the TomatoStar logo as a decal / multicolour top layer (a single-colour
white part cannot reproduce the red/green logo).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def oval_disc(w, h, thick, dome=0.0):
    """Elliptical disc of given thickness along Y, optional slight front dome."""
    disc = c.cylinder(1.0, thick, center=(0, thick / 2, 0), axis="y", sections=120)
    disc.apply_scale((w / 2, 1, h / 2))
    disc = c.union([disc])  # clean tessellation after scaling
    if dome:
        d = c.ellipsoid((w / 2, dome, h / 2), center=(0, thick, 0))
        disc = c.union([disc, d])
    return disc


def build_badge():
    # Face slightly domed for a premium emblem look.
    badge = oval_disc(p.BADGE_W - 2 * p.BADGE_CLEAR, p.BADGE_H - 2 * p.BADGE_CLEAR,
                      p.BADGE_THICK, dome=0.6)

    # Two locating pins on the flat back (y=0), pointing -Y into the chest holes.
    pins = []
    for sx in (-1, 1):
        pin = c._frustum(p.BADGE_PIN_D / 2, p.BADGE_PIN_D / 2 - 0.3, p.BADGE_PIN_ENGAGE + 1, sections=32)
        pin.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))  # +Z -> -Y
        pin.apply_translation((sx * p.BADGE_PIN_SPACING / 2, 0.5, 0))  # base just inside the disc
        pins.append(pin)
    badge = c.union([badge] + pins)

    # Orient to the chest location (so it can be dropped into an assembly render).
    badge.apply_translation((0, p.TORSO_RY - p.BADGE_RECESS, p.BADGE_CZ))
    c.set_color(badge, p.WHITE)
    return badge


if __name__ == "__main__":
    m = build_badge()
    print("watertight:", m.is_watertight, "| ext:", [round(x, 1) for x in m.extents])
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "03_Logo_Badge_White.3mf"))
    m.export(os.path.join(OUT, "03_Logo_Badge_White.stl"))
    print("exported 03_Logo_Badge_White")
