// ***************************************
// *** GMSH exterior flow mesh example ***
// ***************************************

// General settings
General.ExpertMode = 1;

// *** parameters ***
out_d = 0.05;

// *** Points ***
Point(1) = {1, -1, 0, out_d};
Point(2) = {1, 1, 0, out_d};
Point(3) = {-1, 1, 0, out_d};
Point(4) = {-1, -1, 0, out_d};

// *** Edges ***
Line(1) = {4,1}; // left
Line(2) = {2,3}; // right
Line(3) = {1,2}; // bottom
Line(4) = {3,4}; // top

// *** Boundary closed line ***
Line Loop(10) = {1:4};

// *** Surfaces ***
Plane Surface(100) = { 10 };
Recombine Surface  {100}; // transforma trinagles to quads

//Extrude surface to obtain 3D geometry
Extrude {0, 0, 0.1} {
	 Surface {100};
	 Layers{1};
	 Recombine;
}
//Define physical surfaces - numeric designations from GUI
Physical Surface("top") = {117};
Physical Surface("bottom") = {109};
Physical Surface("inlet") = {121};
Physical Surface("outlet") = {131};

//Define physical volumes - numeric designations from GUI
Physical Volume("internal") = {1};
