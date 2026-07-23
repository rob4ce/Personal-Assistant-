"""Part 4 - CALYX (green): leaf crown + stem, with a peg that drops into the
socket on top of the body."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

N_LEAVES = 6


def build_calyx():
    top = p.BODY_TOP_Z - 2  # rim of the socket

    # Downward peg into the body socket (slip fit).
    peg = c.cylinder(p.STEM_R - p.CLEARANCE, p.STEM_DEPTH,
                     center=(0, 0, top - p.STEM_DEPTH / 2 + 1), axis="z", sections=48)

    # Central hub sitting on the body top.
    hub = c.ellipsoid((7, 7, 4), center=(0, 0, top + 2), subdiv=4)

    parts = [peg, hub]

    # Radiating leaves: flattened, tapered ellipsoids tilted up and outward.
    for i in range(N_LEAVES):
        ang = 2 * np.pi * i / N_LEAVES
        leaf = c.ellipsoid((11, 3.2, 2.2), center=(0, 0, 0), subdiv=4)   # long, flat, thin
        # taper to a point by shifting: use as-is; ellipsoid reads as a leaf
        leaf.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(-22), [0, 1, 0]))
        leaf.apply_translation((9, 0, 0))
        leaf.apply_transform(trimesh.transformations.rotation_matrix(ang, [0, 0, 1]))
        leaf.apply_translation((0, 0, top + 3))
        parts.append(leaf)

    # Little top sprig.
    sprig = c.cylinder(1.8, 8, center=(0, 0, top + 7), axis="z", sections=24)
    tip = c.sphere(2.2, center=(0, 0, top + 11))
    parts += [sprig, tip]

    calyx = c.union(parts)
    c.set_color(calyx, c.GREEN)
    return calyx


if __name__ == "__main__":
    m = build_calyx()
    print("watertight:", m.is_watertight, "| bounds:", np.round(m.bounds, 1).tolist())
    print("top of calyx z =", round(m.bounds[1][2], 1))
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "4_calyx_green.3mf"))
    m.export(os.path.join(OUT, "4_calyx_green.stl"))
    print("exported 4_calyx_green")
