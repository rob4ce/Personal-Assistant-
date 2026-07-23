"""FDM fit coupon (reimplementation of Mater_FDM_Fit_Coupon.scad).

Prints peg/hole diametral clearances (0.10-0.30) and a keyed cross-fit like the
calyx connector. Print this on the exact printer/nozzle/material/profile planned
for Mater, then pick the clearance that gives a firm hand fit and feed it back
into params.py (FACE_CLEAR / BADGE_CLEAR / CALYX_CLEAR).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c

OUT = os.path.join(os.path.dirname(__file__), "..", "output")

BASE_T = 3.0
PEG_D = 3.0
CLEARANCES = [0.10, 0.15, 0.20, 0.25, 0.30]


def build_coupon():
    parts = [c.box((90, 25, BASE_T), center=(45, 12.5, BASE_T / 2))]

    for i, clr in enumerate(CLEARANCES):
        x = i * 14.0 + 5
        # test peg
        parts.append(c.cylinder(PEG_D / 2, 6, center=(x, 4, BASE_T + 3), axis="z", sections=48))
        # matching hole block behind the peg
        block = c.box((10, 10, 9), center=(x, 17, 4.5))
        hole = c.cylinder(PEG_D / 2 + clr, 12, center=(x, 17, 4.5), axis="z", sections=48)
        parts.append(c.difference(block, hole))
        # raised clearance label bar count (i+1 small bumps) so rows are identifiable
        for k in range(i + 1):
            parts.append(c.box((1.2, 1.2, 0.6), center=(x - 3 + k * 1.6, 9.5, BASE_T + 0.3)))

    # keyed cross coupon (calyx-style), clearance 0.25
    kx = 82.0
    parts.append(c.cross_key(9, 3, 6, center=(kx, 4, BASE_T + 3), axis="z"))
    block = c.box((12, 12, 9), center=(kx, 17, 4.5))
    socket = c.cross_key(9, 3, 12, center=(kx, 17, 4.5), axis="z", clearance=0.25)
    parts.append(c.difference(block, socket))

    coupon = c.union(parts)
    c.set_color(coupon, [150, 150, 155, 255])
    return coupon


if __name__ == "__main__":
    m = build_coupon()
    print("watertight:", m.is_watertight, "| ext:", [round(x, 1) for x in m.extents])
    os.makedirs(OUT, exist_ok=True)
    m.export(os.path.join(OUT, "Mater_FDM_Fit_Coupon.3mf"))
    m.export(os.path.join(OUT, "Mater_FDM_Fit_Coupon.stl"))
    print("exported Mater_FDM_Fit_Coupon")
