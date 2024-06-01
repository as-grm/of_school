Mesh.RecombineAll=1;//blossom
Mesh.RecombinationAlgorithm=1;//blossom
	
Point(1) = {-1.25, -.5, 0, 1.1};
Point(2) = {-1.25, 1.25, 0, 1.1};
Point(3) = {1.25, -.5, 0, 1.1};
Point(4) = {1.25, 1.25, 0, 1.1};
Line(1) = {1, 2};
Line(2) = {2, 4};
Line(3) = {4, 3};
Line(4) = {3, 1};
Line Loop(4) = {1,2, 3, 4};
Plane Surface(100) = {4};
	
Physical Line(1000)={1,2,3,4};
Physical Surface(100)={100};
	
Field[1] = MathEval;
Field[1].F = "0.01*(1.0+30.*(y-x*x)*(y-x*x) + (1-x)*(1-x))";
Background Field = 1;
