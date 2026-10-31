"""Project Mater v1.5 - nominal dimensions (source of truth = Engineering Brief
+ Dimension Schedule). Units: mm. Coordinate frame: Z up, +Y front, +X right,
origin (0,0,0) at the desk plane under the figure.

Fits are validated with the FDM coupon on the real printer; the values here are
the nominal starting clearances from section 4 of the brief.
"""

# ---------- overall envelope ----------
TOTAL_H = 100.0          # assembled height incl. calyx
BODY_H = 92.0            # red body height (no calyx)
WIDTH = 72.0            # wheel-to-wheel / widest
DEPTH = 60.0            # front-to-back
WALL = 2.5              # nominal cosmetic shell wall
MIN_FEATURE = 1.2       # minimum isolated feature

# ---------- hidden flat base ----------
BASE_W = 46.0           # stable flat footprint width
BASE_D = 34.0           # footprint depth
BASE_Z = 6.0            # height of the flat base pad
WHEEL_FLOAT = 0.5       # wheels sit this far above the desk (decorative)

# ---------- tomato head (oblate: wider than tall, mildly flattened) ----------
HEAD_RX = 32.0          # half width  (64 wide)
HEAD_RY = 28.0          # half depth  (56 deep)
HEAD_RZ = 29.0          # half height (58 tall) -> wider than tall
HEAD_CZ = 63.0          # head centre height (top ~92)

# ---------- torso / chest ----------
TORSO_RX = 26.0
TORSO_RY = 24.0
TORSO_RZ = 22.0
TORSO_CZ = 28.0

# ---------- face recess + faceplate joint ----------
FACE_W = 58.0           # visible faceplate width  (rounded rect)
FACE_H = 36.0           # visible faceplate height
FACE_FILLET = 12.0      # corner radius of the rounded rectangle
FACE_CZ = 64.0          # face centre height (dominates the front)
FACE_SEAT_DEPTH = 2.0   # how deep the face panel sits into the body
FACE_SHOULDER = 1.0     # perimeter shoulder that stops the panel
FACE_PIN_D = 3.0        # locating pin nominal diameter
FACE_PIN_ENGAGE = 4.0   # pin engagement depth
FACE_PIN_DX = 22.0      # pin positions (keyed: not perfectly symmetric)
FACE_PIN_DZ = 11.0
FACE_CLEAR = 0.20       # per-side clearance (0.15-0.25 range)
SHADOW_GAP = 0.25       # cosmetic perimeter shadow line

# ---------- logo badge joint ----------
BADGE_W = 40.0          # oval width
BADGE_H = 24.0          # oval height
BADGE_THICK = 2.0       # badge thickness
BADGE_RECESS = 1.5      # chest recess depth (badge proud by ~0.5)
BADGE_CZ = 30.0         # badge centre height on the chest
BADGE_PIN_D = 2.5
BADGE_PIN_SPACING = 22.0
BADGE_PIN_ENGAGE = 4.0
BADGE_CLEAR = 0.20

# ---------- calyx joint (keyed) ----------
CALYX_W = 52.0          # leaf tip to tip
CALYX_H = 34.0          # stem + crown
CALYX_KEY_MAJOR = 8.0   # keyed peg major width (cross key)
CALYX_KEY_ARM = 3.0     # cross-arm thickness
CALYX_ENGAGE = 6.0      # peg engagement depth
CALYX_CHAMFER = 1.0     # lead-in chamfer
CALYX_CLEAR = 0.25      # per-side clearance (0.20-0.30, top-facing)

# ---------- cosmetic details ----------
EYE_RECESS = 1.0        # eye/smile recess depth (fill with white)
GLUE_POCKET_DEPTH = 0.4 # relief behind cosmetic joints
EDGE_FILLET = 1.0

# ---------- colors (RGBA 0-255) ----------
RED = [225, 57, 64, 255]     # sampled Morning Star red
BLACK = [24, 24, 24, 255]
WHITE = [244, 244, 244, 255]
GREEN = [0, 105, 63, 255]     # sampled Morning Star green
