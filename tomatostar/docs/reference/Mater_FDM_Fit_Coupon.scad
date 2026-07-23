
// Project Mater v1.5 - FDM Fit Coupon
// Print this before finalizing CAD. Units: mm.
// Tests peg/hole diametral clearances and a small keyed calyx-style fit.

$fn = 48;
base_t = 3;
peg_d = 3.0;
clearances = [0.10, 0.15, 0.20, 0.25, 0.30];

module label_bar(x, txt_index) {
    translate([x-4,-8,base_t]) cube([8,2,0.5]);
}

module peg_row() {
    for (i=[0:len(clearances)-1]) {
        x = i*14;
        translate([x,0,base_t]) cylinder(h=6,d=peg_d);
        // Matching hole block placed behind peg
        translate([x-5,12,0])
        difference() {
            cube([10,10,9]);
            translate([5,5,-0.1])
                cylinder(h=10,d=peg_d+2*clearances[i]);
        }
        label_bar(x,i);
    }
}

module keyed_peg() {
    // Cross-key coupon, representative of calyx connector
    translate([76,0,base_t])
    linear_extrude(height=6)
        union() {
            square([3,9],center=true);
            square([9,3],center=true);
        }

    translate([70,12,0])
    difference() {
        cube([12,12,9]);
        translate([6,6,-0.1])
        linear_extrude(height=10)
            offset(delta=0.25)
            union() {
                square([3,9],center=true);
                square([9,3],center=true);
            }
    }
}

union() {
    cube([90,25,base_t]);
    peg_row();
    keyed_peg();
}
