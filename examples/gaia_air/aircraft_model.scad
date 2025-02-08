module point(id, x, y, z) {
    translate([x, y, z])
    sphere(r=0.2);
    translate([x, y, z])
    linear_extrude(height = 0.1, center = true, convexity = 10)
    text(text = id, size = 0.5, font = "Liberation Sans:style=Bold");
}

module connect_points(points_array) {
    for (i = [0:len(points_array)-2]) {
        p1 = points_array[i];
        p2 = points_array[i+1];
        v = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]];
        len_v = norm(v);
        if (len_v > 0) {
            cylinder(r=0.05, h=len_v, center=false);
            translate(p2)
            rotate([0, 0, atan2(v[1], v[0])])
            rotate([0, -atan2(v[2], sqrt(v[0]*v[0] + v[1]*v[1])), 0])
            cone(r1=0.08, r2=0, h=0.2, center=false);
        }
    }
}

PointData = [
["D","D-NoseTip","Nose Tip",-5.00,0.00,0.00],
["D","D-NoseBaseLower","Nose Base - Lower Profile",-2.50,1.25,-1.50],
["D","D-NoseBaseUpper","Nose Base - Upper Profile",-2.50,1.25,1.50],
["D","D-ForwardFuselageLower","Forward Fuselage - Lower Profile",2.00,1.50,-1.75],
["D","D-ForwardFuselageUpper","Forward Fuselage - Upper Profile",2.00,1.50,1.75],
["D","D-CenterFuselageLower","Center Fuselage - Lower Profile",15.00,1.75,-2.00],
["D","D-CenterFuselageUpper","Center Fuselage - Upper Profile",15.00,1.75,2.00],
["D","D-AftFuselageLower","Aft Fuselage - Lower Profile",28.00,1.50,-1.75],
["D","D-AftFuselageUpper","Aft Fuselage - Upper Profile",28.00,1.50,1.75],
["D","D-TailEnd","Tail End",33.00,0.00,0.00],
["F","F-NoseFrame","Nose Frame",-5.00,0.00,0.00],
["F","F-ForwardFrame","Forward Frame",0.00,0.00,0.00],
["F","F-CentralFrame","Central Frame",8.00,0.00,0.00],
["F","F-AftFrame","Aft Frame",23.00,0.00,0.00],
["F","F-AftmostFrame","Aftmost Frame",33.00,0.00,0.00],
["BF","BF-Forward","Belly Fairing - Forward",5.00,0.50,-2.20],
["BF","BF-Mid","Belly Fairing - Mid",15.00,0.75,-2.50],
["BF","BF-Aft","Belly Fairing - Aft",25.00,0.50,-2.20],
["W","W-RootLeadingEdge","Wing Root - Leading Edge",5.00,4.00,0.00],
["W","W-RootTrailingEdge","Wing Root - Trailing Edge",8.00,4.00,0.00],
["W","W-MidLeadingEdge","Wing Mid-Span - Leading Edge",12.00,10.00,0.50],
["W","W-MidTrailingEdge","Wing Mid-Span - Trailing Edge",16.00,10.00,0.25],
["W","W-TipLeadingEdge","Wing Tip - Leading Edge",18.00,18.00,1.00],
["W","W-TipTrailingEdge","Wing Tip - Trailing Edge",18.50,18.00,0.80],
["W","W-EngineMount","Wing Engine Mount",7.00,5.00,-0.50],
["HS","HS-RootLeadingEdge","Horizontal Stabilizer Root - Leading Edge",30.00,2.00,2.00],
["HS","HS-RootTrailingEdge","Horizontal Stabilizer Root - Trailing Edge",32.00,2.00,2.00],
["HS","HS-TipLeadingEdge","Horizontal Stabilizer Tip - Leading Edge",31.00,7.00,2.25],
["HS","HS-TipTrailingEdge","Horizontal Stabilizer Tip - Trailing Edge",32.50,7.00,2.10],
["VS","VS-RootLeadingEdge","Vertical Stabilizer Root - Leading Edge",32.00,0.00,3.00],
["VS","VS-RootTrailingEdge","Vertical Stabilizer Root - Trailing Edge",33.00,0.00,3.00],
["VS","VS-MidLeadingEdge","Vertical Stabilizer Mid-Height - Leading Edge",32.30,0.00,5.00],
["VS","VS-Tip","Vertical Stabilizer Tip",32.50,0.00,7.00],
["CKPT","CKPT-Ref","Cockpit Reference Point",-1.00,0.00,2.50]
];

module aircraft_model() {
    for (point_data = PointData) {
        series_id = point_data[0];
        point_id_str = point_data[1];
        description = point_data[2];
        x = point_data[3];
        y = point_data[4];
        z = point_data[5];

        color_val = 
            (series_id == "D") ? "blue" :
            (series_id == "F") ? "red" :
            (series_id == "W") ? "green" :
            (series_id == "HS") ? "orange" :
            (series_id == "VS") ? "purple" :
            (series_id == "BF") ? "yellow" :
            (series_id == "CKPT") ? "cyan" :
            "lightgray";

        color(color_val)
        point(point_id_str, x, y, z);
    }

    // Fuselage Profile (D-Series) Connections
    d_points = [
        PointData[0][3:6], PointData[1][3:6], PointData[2][3:6], PointData[3][3:6],
        PointData[4][3:6], PointData[5][3:6], PointData[6][3:6], PointData[7][3:6],
        PointData[8][3:6], PointData[9][3:6]
    ];
    color("blue") connect_points(d_points);

    // Fuselage Frame (F-Series) Connections
    f_points = [
        PointData[10][3:6], PointData[11][3:6], PointData[12][3:6], PointData[13][3:6],
        PointData[14][3:6]
    ];
    color("red") connect_points(f_points);

    // Belly Fairing (BF-Series) Connections
    bf_points = [
        PointData[15][3:6], PointData[16][3:6], PointData[17][3:6]
    ];
    color("yellow") connect_points(bf_points);

    // Wing (W-Series) Connections
    w_points_wing = [
        PointData[18][3:6], PointData[20][3:6], PointData[22][3:6] // Leading Edge
    ];
    color("green") connect_points(w_points_wing);
    w_points_flap = [
        PointData[19][3:6], PointData[21][3:6], PointData[23][3:6] // Trailing Edge
    ];
    color("green") connect_points(w_points_flap);
    w_points_root_box = [
        PointData[18][3:6], PointData[19][3:6] // Wing Root Box
    ];
    color("darkgreen") linear_extrude(height = 0.1) polygon(points = [w_points_root_box[0][0:2], w_points_root_box[1][0:2], [w_points_flap[0][0],w_points_flap[0][1]], [w_points_wing[0][0],w_points_wing[0][1]]]);
    w_points_mid_box = [
        PointData[20][3:6], PointData[21][3:6] // Wing Mid-Span Box
    ];
    color("darkgreen") linear_extrude(height = 0.1) polygon(points = [w_points_mid_box[0][0:2], w_points_mid_box[1][0:2], [w_points_flap[1][0],w_points_flap[1][1]], [w_points_wing[1][0],w_points_wing[1][1]]]);
        w_points_tip_box = [
        PointData[22][3:6], PointData[23][3:6] // Wing Tip Box
    ];
    color("darkgreen") linear_extrude(height = 0.1) polygon(points = [w_points_tip_box[0][0:2], w_points_tip_box[1][0:2], [w_points_flap[2][0],w_points_flap[2][1]], [w_points_wing[2][0],w_points_wing[2][1]]]);

    // Horizontal Stabilizer (HS-Series) Connections
    hs_points_le = [
        PointData[25][3:6], PointData[27][3:6] // Leading Edge
    ];
    color("orange") connect_points(hs_points_le);
    hs_points_te = [
        PointData[26][3:6], PointData[28][3:6] // Trailing Edge
    ];
    color("orange") connect_points(hs_points_te);

    // Vertical Stabilizer (VS-Series) Connections
    vs_points_le = [
        PointData[29][3:6], PointData[30][3:6], PointData[31][3:6] // Leading Edge
    ];
    color("purple") connect_points(vs_points_le);
    vs_points_vert = [
        PointData[29][3:6], PointData[32][3:6] // Vertical Span
    ];
    color("purple") connect_points(vs_points_vert);
}

aircraft_model();
