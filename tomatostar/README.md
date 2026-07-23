# TomatoStar — 4-piece snap/glue 3D-print model

A printability-first, code-generated 3D model of the **TomatoStar** mascot
(V1.5 concept), split into 4 separately-printable, separately-colored parts.
All geometry is generated procedurally with `trimesh` + `manifold3d` and
exported to **3MF** (and STL) for slicing.

> **Fidelity note:** this is a *stylised* interpretation of the concept art —
> clean geometric forms built from spheres/cylinders and boolean cuts, not a
> surface-exact copy of the studio render. Printability and a recognisable
> character were the priorities.

## Parts

| # | Part | Color | File |
|---|------|-------|------|
| 1 | Body (head + body + arms + wheels, face/badge recesses, calyx socket) | Red | `output/1_body_red.3mf` |
| 2 | Faceplate (eyes + smile, recessed to fill white) | Black | `output/2_faceplate_black.3mf` |
| 3 | Logo badge (raised oval + locating peg) | White | `output/3_badge_white.3mf` |
| 4 | Calyx (leaf crown + stem peg) | Green | `output/4_calyx_green.3mf` |

Overall height ≈ 95 mm (target 100 mm).

## Assembly (CA-glue, slip-fit)

Sockets/pockets are cut **0.20 mm larger per side** than their mating part —
a thin slip fit meant for a drop of CA (super) glue. To try a snap-ish fit
instead, reduce `CLEARANCE` in `scripts/params.py` toward `0.10` and reprint
the mating part.

1. Print all 4 parts in their colors (see print settings below).
2. Seat the **faceplate** into the body's face recess — glue.
3. Seat the **badge** into the belly recess, peg into the hole — glue.
4. Drop the **calyx** stem peg into the top socket — glue.
5. Optional: fill the recessed eyes/smile with white paint pen or UV resin.

## Print settings (from the concept sheet)

- Layer height: 0.2 mm
- Infill: 15–20 %
- Supports: not needed (body cavity faces up; arms tucked in)
- Est. time: 2.5–3.5 h total for 100 mm scale

## Rebuild from source

```bash
pip install numpy trimesh manifold3d networkx lxml matplotlib
cd scripts
python3 build_body.py
python3 build_faceplate.py
python3 build_badge.py
python3 build_calyx.py
python3 render_assembly.py   # writes preview PNGs
```

Shared mating dimensions live in `scripts/params.py` — edit there to keep all
parts consistent.
