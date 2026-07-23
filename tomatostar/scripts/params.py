"""Shared dimensions so every part's mating features line up.

Slip-fit clearance: the CA-glue assembly plan. Sockets are cut CLEARANCE mm
larger (per side) than the matching peg/plate so parts drop in with a thin glue
gap. Tighten toward 0.1 for a snap-ish fit once you've calibrated your printer.
"""
CLEARANCE = 0.20  # mm per side, slip fit for CA glue

# ---- overall ----
TOTAL_HEIGHT = 100.0  # mm, tip of calyx to floor (target)

# ---- body ----
BODY_RX = 33.0   # half-width  (X)
BODY_RY = 30.0   # half-depth  (Y, front/back)
BODY_RZ = 40.0   # half-height (Z)
BODY_CZ = 44.0   # centre height of the main body ellipsoid

# ---- face recess / faceplate ----
FACE_CZ = 58.0            # centre height of the face
FACE_HALF_W = 19.0        # oval half width
FACE_HALF_H = 14.0        # oval half height
FACE_DEPTH = 5.0          # how deep the pocket is cut into the body
FACEPLATE_THICK = 5.5     # faceplate total thickness (sits proud slightly)

# ---- badge recess / logo badge ----
BADGE_CZ = 26.0
BADGE_HALF_W = 12.0
BADGE_HALF_H = 8.5
BADGE_DEPTH = 3.0
BADGE_THICK = 3.5

# ---- calyx socket / stem peg ----
STEM_R = 5.0              # nominal stem peg radius
STEM_DEPTH = 11.0         # socket depth
BODY_TOP_Z = BODY_CZ + BODY_RZ  # ~84, top of body before calyx

# ---- arms & wheels ----
ARM_R = 8.0
WHEEL_R = 11.0
