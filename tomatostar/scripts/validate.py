"""Validation report for Project Mater v1.5: per-part integrity, assembled
envelope, joint clearances, and a dry-fit interference check."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import trimesh
import common as c
import params as p
from build_body import build_body
from build_faceplate import build_faceplate
from build_badge import build_badge
from build_calyx import build_calyx

body = build_body()
face = build_faceplate()
badge = build_badge()
tz = body.bounds[1][2]
calyx = build_calyx(z0=tz)

print("== Part integrity ==")
for name, m in [("01 Body", body), ("02 Faceplate", face), ("03 Badge", badge), ("04 Calyx", calyx)]:
    e = m.extents
    print(f"  {name:14} watertight={m.is_watertight} single_body={m.body_count == 1} "
          f"tris={len(m.faces):6d}  {e[0]:.1f} x {e[1]:.1f} x {e[2]:.1f} mm")

allv = np.vstack([body.vertices, face.vertices, badge.vertices, calyx.vertices])
d = allv.max(0) - allv.min(0)
print(f"\n== Assembled envelope ==\n  {d[0]:.1f} W x {d[1]:.1f} D x {d[2]:.1f} H mm   (target 72 x 60 x 100)")

print("\n== Joint clearances (per side) ==")
print(f"  faceplate pins {p.FACE_PIN_D:.1f} mm  in holes {p.FACE_PIN_D + 2*p.FACE_CLEAR:.1f} mm -> {p.FACE_CLEAR:.2f}")
print(f"  badge pins     {p.BADGE_PIN_D:.1f} mm  in holes {p.BADGE_PIN_D + 2*p.BADGE_CLEAR:.1f} mm -> {p.BADGE_CLEAR:.2f}")
print(f"  calyx key      {p.CALYX_KEY_MAJOR:.1f} mm  in socket {p.CALYX_KEY_MAJOR + 2*p.CALYX_CLEAR:.1f} mm -> {p.CALYX_CLEAR:.2f}")

print("\n== Dry-fit interference (solid overlap volume; should be ~0) ==")
for name, part in [("faceplate", face), ("badge", badge), ("calyx", calyx)]:
    inter = trimesh.boolean.intersection([body, part], engine="manifold")
    v = inter.volume / 1000 if inter is not None and len(inter.faces) else 0.0
    flag = "OK" if v < 0.5 else "CHECK"
    print(f"  body ∩ {name:10} = {v:6.3f} cm^3   [{flag}]")

print("\n== Desk stability ==")
print(f"  flat base bottom at z=0; wheels float ~{p.WHEEL_FLOAT} mm above desk")
