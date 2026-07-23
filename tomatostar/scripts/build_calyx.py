"""04_Calyx_Green - Project Mater v1.5.

Morning-Star-style calyx: thick, smoothly-blended leaves (FDM-friendly) on a
short stem, with a KEYED cross peg (8 mm major) + shoulder stop that drops into
the body socket. Overall ~52 mm leaf-tip to tip, ~34 mm tall.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

N_LEAVES = 6


def build_calyx(z0=0.0):
    """z0 = body top surface height (socket rim). Defaults to 0 for a standalone
    part sitting on the print bed."""
    parts = []

    # Keyed cross peg (points down, -Z) with a lead-in chamfer, minus clearance.
    peg = c.cross_key(p.CALYX_KEY_MAJOR, p.CALYX_KEY_ARM, p.CALYX_ENGAGE,
                      center=(0, 0, z0 - p.CALYX_ENGAGE / 2 + 0.5), axis="z")
    # chamfer the peg tip so it self-centres
    tip_cone = c._frustum(p.CALYX_KEY_MAJOR * 0.75, p.CALYX_KEY_MAJOR * 0.3, p.CALYX_CHAMFER)
    parts.append(peg)

    # Shoulder / hub that bottoms on the head (sits just below the top surface).
    hub = c.ellipsoid((9.5, 9.5, 4.5), center=(0, 0, z0 - 1), subdiv=4)
    parts.append(hub)

    # Thick tapered leaves splaying OUT and DOWN over the tomato's crown, so the
    # calyx adds only ~8 mm of height (leaf tips droop to the head shoulders).
    for i in range(N_LEAVES):
        ang = 2 * np.pi * i / N_LEAVES
        leaf = c.ellipsoid((15, 4.2, 2.8), center=(0, 0, 0), subdiv=4)
        leaf.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(26), [0, 1, 0]))  # tip down
        leaf.apply_translation((13, 0, 0))
        leaf.apply_transform(trimesh.transformations.rotation_matrix(ang, [0, 0, 1]))
        leaf.apply_translation((0, 0, z0 - 1))
        parts.append(leaf)

    # Central stem sprig poking up (this is the only part that adds height).
    sprig = c.cylinder(2.2, 7, center=(0, 0, z0 + 2.5), axis="z", sections=32)
    knob = c.sphere(2.6, center=(0, 0, z0 + 6.5))
    parts += [sprig, knob]

    calyx = c.union(parts)
    c.set_color(calyx, p.GREEN)
    return calyx


if __name__ == "__main__":
    m = build_calyx()
    m.apply_translation((0, 0, -m.bounds[0][2]))  # drop onto the bed for a standalone part
    print("watertight:", m.is_watertight, "| ext:", [round(x, 1) for x in m.extents],
          "(target 52 wide x 34 tall)")
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "04_Calyx_Green.3mf"))
    m.export(os.path.join(OUT, "04_Calyx_Green.stl"))
    print("exported 04_Calyx_Green")
