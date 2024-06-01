// ***************************************
// *** GMSH exterior flow mesh example ***
// ***************************************

// General settings
General.ExpertMode = 1;

// *** geometry parameters ***
R     = \VAR{R};
tb1_y1 = \VAR{tb1_y1};
tb1_y2 = \VAR{tb1_y2};
fr1_x = \VAR{fr1_x};
ba1_x = \VAR{ba1_x};
tb2_y1 = \VAR{tb2_y1};
tb2_y2 = \VAR{tb2_y2};
fr2_x = \VAR{fr2_x};
ba2_x1 = \VAR{ba2_x1};
ba2_x2 = \VAR{ba2_x2};

// *** grading parameters ***
g1_fr = \VAR{g1_fr}; // outer boundary front grading
g1_ba = \VAR{g1_ba}; // outer boundary back grading
g2_fr = \VAR{g2_fr}; // inner front boundary grading
g2_ba = \VAR{g2_ba}; // inner back boundary grading
gC    = \VAR{gC};    // cylinder boundary grading

// *** Outer square points ***
Point(1) = {-fr1_x, -tb1_y1, 0, g1_fr};
Point(2) = { ba1_x, -tb1_y2, 0, g1_ba};
Point(3) = { ba1_x,  tb1_y2, 0, g1_ba};
Point(4) = {-fr1_x,  tb1_y1, 0, g1_fr};

// *** Inner square points ***
Point(5)  = {-fr2_x,  -tb2_y1, 0, g2_fr};
Point(6)  = { ba2_x1, -tb2_y1, 0, g2_fr};
Point(7)  = { ba2_x2, -tb2_y2, 0, g2_ba};
Point(8)  = { ba2_x2,  tb2_y2, 0, g2_ba};
Point(9)  = { ba2_x1,  tb2_y1, 0, g2_fr};
Point(10) = {-fr2_x,   tb2_y1, 0, g2_fr};

// *** Cylinder construction points ***
Point(20) = { 0, 0,0, gC};
Point(21) = { R, 0,0, gC};
Point(22) = { 0, R,0, gC};
Point(23) = {-R, 0,0, gC};
Point(24) = { 0,-R,0, gC};

// *** Edges ***
// outer square
Line(1) = {4,1}; // left
Line(2) = {2,3}; // right
Line(3) = {1,2}; // bottom
Line(4) = {3,4}; // top
// inner square
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {10,5};
// cylinder
Circle(20) = {21, 20, 22};
Circle(21) = {22, 20, 23};
Circle(22) = {23, 20, 24};
Circle(23) = {24, 20, 21};

Line Loop(10) = {1:4};   // outer square line
Line Loop(11) = {5:10};  // inner square line
Line Loop(12) = {20:23}; // hole line

// *** Surfaces ***
Plane Surface(100) = { 10, 11 };
Plane Surface(200) = { 11, 12 };
Recombine Surface {100, 200};

//Extrude surface to obtain 3D geometry
Extrude {0, 0, \VAR{zEf}} {
	 Surface {100, 200};
	 Layers{1};
	 Recombine;
}
//Define physical surfaces - numeric designations from GUI
Physical Surface("top") = {227};
Physical Surface("bottom") = {219};
Physical Surface("inlet") = {215};
Physical Surface("outlet") = {223};
Physical Surface("cylinder") = {291,295,299,303};

//Define physical volumes - numeric designations from GUI
Physical Volume("internal") = {1,2};

//Define Boundary Layer
Field[1] = BoundaryLayer;
Field[1].CurvesList = {23,22,21,20};
Field[1].Size = \VAR{bl_h1};
Field[1].Thickness = \VAR{bl_H};
Field[1].Ratio = \VAR{bl_sf};
Field[1].Quads = 1;
BoundaryLayer Field = 1;
