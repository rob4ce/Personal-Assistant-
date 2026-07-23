PROJECT MATER v1.5 - ENGINEERING REFERENCE PACKAGE

Purpose
-------
This package is intended to let your R&D/CAD team build the real parametric model.
The included turnaround image is concept art, not dimensionally authoritative.
Use the dimension schedule and engineering brief as the starting source of truth.

Files
-----
- Mater_v1_5_Engineering_Brief.pdf
- Mater_v1_5_Dimension_Schedule.csv
- Mater_FDM_Fit_Coupon.scad
- Morning_Star_Tomato_Reference.png
- Mater_v1_5_Turnaround_Concept.png

Recommended CAD structure
-------------------------
1. 01_Body_Red
2. 02_Faceplate_Black
3. 03_Logo_Badge_White
4. 04_Calyx_Green
5. Mater_v1_5_Assembly

Critical process
----------------
1. Build nominal geometry.
2. Print the fit coupon on the same printer/material/profile planned for Mater.
3. Pick the best clearance.
4. Apply that measured clearance to faceplate, badge, and calyx joints.
5. Print Prototype A at 100 mm tall.
6. Mark fit issues and revise by 0.05-0.10 mm increments.
7. Freeze Release 1 only after a full dry-fit and glue test.

Logo note
---------
The supplied logo image is a visual reference. For a crisp badge, your CAD/graphics
team should obtain the original vector artwork (SVG, EPS, AI, or PDF) from Morning Star.
