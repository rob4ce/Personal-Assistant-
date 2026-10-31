"""Build every part + coupon + assembly and print a validation summary.
Run from the scripts/ directory: python3 build_all.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(__file__)
STEPS = ["build_body", "build_faceplate", "build_badge", "build_calyx",
         "build_coupon", "render_assembly", "validate"]

for s in STEPS:
    print(f"\n===== {s} =====")
    r = subprocess.run([sys.executable, os.path.join(HERE, s + ".py")],
                       capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr.strip())
        sys.exit(r.returncode)
