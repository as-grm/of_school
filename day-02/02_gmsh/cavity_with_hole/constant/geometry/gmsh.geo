// ***************************************
// *** GMSH exterior flow mesh example ***
// ***************************************

// General settings
General.ExpertMode = 1;

// *** parameters ***
out_d = 0.05;
inn_d = 0.01;
R = 0.2;

// *** Points ***
Point(1) = {1, -1, 0, out_d};
Point(2) = {1, 1, 0, out_d};
Point(3) = {-1, 1, 0, out_d};
Point(4) = {-1, -1, 0, out_d};

Point(10) = {0,0,0, inn_d};
Point(11) = {R,0,0, inn_d};
Point(12) = {0,R,0, inn_d};
Point(13) = {-R,0,0, inn_d};
Point(14) = {0,-R,0, inn_d};

// *** Edges ***
// SetFactory("OpenCASCADE");
Line(1) = {4,1}; // left
Line(2) = {2,3}; // right
Line(3) = {1,2}; // bottom
Line(4) = {3,4}; // top

Circle(5) = {11, 10, 12};
Circle(6) = {12, 10, 13};
Circle(7) = {13, 10, 14};
Circle(8) = {14, 10, 11};

Line Loop(10) = {1:4}; // outer line
Line Loop(11) = {5:8}; // hole line

// *** Surfaces ***
Plane Surface(100) = { 10, 11 };

//Extrude surface to obtain 3D geometry
Extrude {0, 0, 0.1} {
	 Surface {100};
	 Layers{1};
	 Recombine;
}
//Define physical surfaces - numeric designations from GUI
Physical Surface("top") = {121};
Physical Surface("bottom") = {113};
Physical Surface("inlet") = {125};
Physical Surface("outlet") = {117};
Physical Surface("cylinder") = {129,133,137,141};

//Define physical volumes - numeric designations from GUI
Physical Volume("internal") = {1};

//Define Boundary Layer
Field[1] = BoundaryLayer;
Field[1].CurvesList = {5,6,7,8};
//Field[1].FanPointsList = {1};
//Field[1].FanPointsSizesList = {7};
Field[1].Size = 0.005;
Field[1].Thickness = 0.05;
Field[1].Ratio = 1.1;
//Field[1].AnisoMax = 5;
Field[1].Quads = 1;
//Field[1].IntersectMetrics = 10;
BoundaryLayer Field = 1;
