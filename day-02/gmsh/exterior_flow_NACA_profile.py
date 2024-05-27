#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:15:24 2022

@author: sandro
"""

import sys, getopt
import math as mat
import numpy as np

def rotatePoints(pts, fi):
    # rotate points around (0,0)
    NN = pts.shape[1]
    x = np.zeros(NN)
    y = np.zeros(NN)
    
    aa = -fi/180*mat.pi
    
    for i in range(NN):
        px = pts[0,i]
        py = pts[1,i]
        cos_fi = mat.cos(aa)
        sin_fi = mat.sin(aa)
        
        x[i] = px*cos_fi - py*sin_fi
        y[i] = px*sin_fi + py*cos_fi
        
    return [x,y]

def naca00XXprofile(t,N,fi):
    # t - maximum thickness
    # N - number of control points
    # fi - angle [deg] of profile rotation around point (1,0)
    
    y = np.zeros(N)
    
    xp = np.linspace(0,1,N)
    #model = 'linear'
    model ='exp'
    
    if model == 'linear':
        x = xp
    else:
        a = 5
        x = np.flip(np.exp(a*xp)-1)
        x = x/np.max(x)
    
    # foil contour weights interval
    w_foil = 0.05
    wi = w_foil*np.ones(N) # point weights
    ww = 0.075
    w = wi*ww + x*(wi-wi*ww)

    for i in range(N):
        y[i] = 5*t*( 0.2969*mat.sqrt(x[i]) - 0.1260*x[i] - 0.3516*x[i]**2 + 0.2843*x[i]**3 - 0.1015*x[i]**4)
    y[0] = 0.0
    
    xa = np.append(x, np.flip(x)[1:-1])
    ya = np.append(y, -np.flip(y)[1:-1])
    wa = np.append(w, np.flip(w)[1:-1])
    
    yMin = np.min(ya)
    yMax = np.max(ya)
    
    [xr, yr] = rotatePoints(np.array([xa,ya]), fi)
    
    pts = np.array([xr,yr,wa])
    
    return [pts, N, yMin, yMax]

def writeMeshHeader(f):
    
    f.write('// *******************************************\n')
    f.write('// *** NACA-00XX exterior flow mesh example ***\n')
    f.write('// *******************************************\n')
    f.write('\n')
    
    f.write('// General settings\n')
    f.write('General.ExpertMode = 1;\n')
    
    f.write('\n')
    f.write('// Mesh parameters\n')
    f.write('w_bb_if = 0.05;\n')   # inner box front weights
    f.write('w_bb_ib = 0.05;\n')  # inner box back weights
    f.write('w_bb_mf = 0.075;\n')  # mid box front weights
    f.write('w_bb_mb = 0.05;\n')   # mid box back weights
    f.write('w_bb_of = 0.4;\n')    # outer box front weights
    f.write('w_bb_ob = 0.2;\n')    # outer box back weights
    f.write('a_m = 0.5;\n')      # mid box front side size
    f.write('b_m = 5;\n')        # mid box back side size
    f.write('a_o = 5;\n')        # outer box front side size
    f.write('b_o = 10;\n')       # outer box back side size
    f.write('c_o = 5;\n')        # outer box up side size
    f.write('\n')
    
def writeNACAmesh(f,naca_points, npm):
    
    NN = naca_points.shape[1]
    x = naca_points[0]
    y = naca_points[1]
    w = naca_points[2]
    LL = 10
    
    f.write('// NACA00XX foil - {:d} pts\n'.format(2*NN-1))
    for i in range(NN):
        f.write('Point({:d}) = {{ {:.8e}, {:.8e}, 0.0, {:.8e} }};\n'.format(i+1, x[i], y[i], w[i]))
        
    #f.write('Spline(1) = {{ 1:{:d},1 }};\n'.format(NN))
    f.write('Spline(1) = { 1')
    for i in range(2,npm+1):
        f.write(',{:d}'.format(i))
    f.write(' };\n')
    f.write('Spline(2) = { ')
    for i in range(npm,NN+1):
        f.write('{:d},'.format(i))
    f.write('1 };\n')
    
    f.write('Line Loop({:d}) = {{ 1,2 }};\n'.format(LL))
    
    f.write('\n')
    
    return LL
    
def writeMeshBBs(f, fi, yMin, yMax, yMinR, yMaxR, NN):
    
    NB = (mat.ceil(2*NN/100) + 1)*100
    
    # Inner bounding box
    h = yMax - yMin
    
    ix_p = [1+3*h,-h,-h,1+3*h]
    iy_p = [1.5*h,1.5*h,-1.5*h,-1.5*h]
    in_p = np.array(rotatePoints(np.array([ix_p,iy_p]), fi))
    
    yL = np.min(in_p[1]) - h
    yU = np.max(in_p[1]) + h
    
    f.write('// Inner Bounding box\n')
    f.write('Point({:d}) = {{ {:.8e}, {:.8e}, 0.0, w_bb_ib }};\n'.format(NB,in_p[0,0],in_p[1,0]))
    f.write('Point({:d}) = {{ {:.8e}, {:.8e}, 0.0, w_bb_if }};\n'.format(NB+1,in_p[0,1],in_p[1,1]))
    f.write('Point({:d}) = {{ {:.8e}, {:.8e}, 0.0, w_bb_if }};\n'.format(NB+2,in_p[0,2],in_p[1,2]))
    f.write('Point({:d}) = {{ {:.8e}, {:.8e}, 0.0, w_bb_ib }};\n'.format(NB+3,in_p[0,3],in_p[1,3]))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB, NB, NB+1))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+1, NB+1, NB+2))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+2, NB+2, NB+3))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+3, NB+3, NB))
    f.write('Line Loop({:d}) = {{ {:d}, {:d}, {:d}, {:d} }};\n'.format(NB+4, NB, NB+1, NB+2, NB+3))
    f.write('\n')
    
    f.write('// Middle Bounding box\n')
    f.write('Point({:d}) = {{ b_m, {:.5f}, 0.0, w_bb_mb}};\n'.format(NB+10,yU))
    f.write('Point({:d}) = {{ -a_m, {:.5f}, 0.0, w_bb_mf}};\n'.format(NB+11,yU))
    f.write('Point({:d}) = {{ -a_m, {:.5f}, 0.0, w_bb_mf}};\n'.format(NB+12,yL))
    f.write('Point({:d}) = {{ b_m, {:.5f}, 0.0, w_bb_mb}};\n'.format(NB+13,yL))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+10, NB+10, NB+11))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+11, NB+11, NB+12))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+12, NB+12, NB+13))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+13, NB+13, NB+10))
    f.write('Line Loop({:d}) = {{ {:d}, {:d}, {:d}, {:d} }};\n'.format(NB+14, NB+10, NB+11, NB+12, NB+13))
    f.write('\n')
    
    # Outer bounding box
    f.write('// Outer Bounding box\n')
    f.write('Point({:d}) = {{b_o, c_o, 0.0, w_bb_ob}};\n'.format(NB+20))
    f.write('Point({:d}) = {{-a_o, c_o, 0.0, w_bb_of}};\n'.format(NB+21))
    f.write('Point({:d}) = {{-a_o, -c_o, 0.0, w_bb_of}};\n'.format(NB+22))
    f.write('Point({:d}) = {{b_o, -c_o, 0.0, w_bb_ob}};\n'.format(NB+23))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+20, NB+20, NB+21))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+21, NB+21, NB+22))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+22, NB+22, NB+23))
    f.write('Line({:d}) = {{ {:d}, {:d} }};\n'.format(NB+23, NB+23, NB+20))
    f.write('Line Loop({:d}) = {{ {:d}, {:d}, {:d}, {:d} }};\n'.format(NB+24, NB+20, NB+21, NB+22, NB+23))
    
    return [NB+4, NB+14, NB+24]
    
    
def writeMeshBC(f, ll1, ll2, ll3, ll4):
    
    f.write('\n')
    f.write('//Define unstructured far field mesh zone\n')
    f.write('Plane Surface(1000) = {{ {:d}, {:d} }};\n'.format(ll1, ll2))
    f.write('Plane Surface(1001) = {{ {:d}, {:d} }};\n'.format(ll2, ll3))
    f.write('Plane Surface(1002) = {{ {:d}, {:d} }};\n'.format(ll3, ll4))
    f.write('Recombine Surface {1001, 1002};\n')
    
    f.write('\n')
    f.write('//Extrude unstructured far field mesh\n')
    f.write('Extrude {0, 0, 0.1} {\n')
    f.write('\t Surface {1000,1001,1002};\n')
    f.write('\t Layers{1};\n')
    f.write('\t Recombine;\n')
    f.write('}\n')
    
def writeMeshBL(f):
    
    f.write('//Define physical surfaces - numeric designations from GUI\n')
    #f.write('Physical Surface("back") = {1000,1001,1002};\n')
    #f.write('Physical Surface("front") = {1034,1076,1118};\n')
    f.write('Physical Surface("top") = {1117};\n')
    f.write('Physical Surface("bottom") = {1109};\n')
    f.write('Physical Surface("inlet") = {1113};\n')
    f.write('Physical Surface("outlet") = {1105};\n')
    f.write('Physical Surface("foilup") = {1013};\n')
    f.write('Physical Surface("foillow") = {1017};\n')
    
    f.write('\n')
    f.write('//Define physical volumes - numeric designations from GUI\n')
    f.write('Physical Volume("internal") = {1,2,3};\n')
    
    #// *** First algorithm - Inward extrussion ***
    #// NOTE : Create Boundaries inside the airfoil, looks not efficient for my case
    #//Extrude the boundary of the foil inwards by 0.05, with 5 layers of elements
    #//Extrude { Surface{234}; Layers{5, 0.05}; }
    
    
    #// *** Second approach - Outward extrussion ***
    #// NOTE : Create Boundaries outside the airfoil, looks much better
    f.write('\n')
    f.write('//Define Boundary Layer\n')
    f.write('Field[1] = BoundaryLayer;\n')
    f.write('Field[1].CurvesList = {1,2};\n')
    f.write('Field[1].FanPointsList = {1};\n')       # fans at geometrical vertices 1 and 11')
    f.write('Field[1].FanPointsSizesList = {7};\n')  # 7 elements in the fan for node 1')
    # For multiple fan nodes
    # Field[1].FanPointsList = {1, 100};
    # Field[1].FanPointsSizesList = {7, 3};  7 elements in the fan for node 1 and 3 for node 100')
    f.write('Field[1].Size = 0.005;\n')
    f.write('Field[1].Thickness = 0.04;\n')
    f.write('Field[1].Ratio = 1.2;\n')
    f.write('//Field[1].AnisoMax = 5;\n')
    f.write('Field[1].Quads = 1;\n')
    f.write('//Field[1].IntersectMetrics = 10;\n')
    f.write('BoundaryLayer Field = 1;\n')

def createGMSHfile(naca_points, N, geo_fn, fi, yMin, yMax):
    
    f = open(geo_fn,'w')
    
    NN = naca_points.shape[1]
    y = naca_points[1]
    yMaxR = np.max(y)
    yMinR = np.min(y)
    
    writeMeshHeader(f)
    ll1 = writeNACAmesh(f,naca_points, N)
    [ll2, ll3, ll4] = writeMeshBBs(f, fi, yMin, yMax, yMinR, yMaxR, NN)
    writeMeshBC(f, ll1, ll2, ll3, ll4)
    writeMeshBL(f)
    
    f.close()
    

def main(argv):
    
    thickness = 0.12
    numpts = 100
    angle = 5
    geo_file = 'naca_profile.geo'

    try:
        opts, args = getopt.getopt(argv,'ht:N:a:',['thickness=','numpts=', 'angle='])
    except getopt.GetoptError:
        print('exterior_flow_NACA_profile.py -t <thicknes in [0,1]> -N <number div. points> -a <angle of attack in degrees>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('exterior_flow_NACA_profile.py -t <thicknes in [0,1]> -N <number div. points> -a <angle of attack in degrees>')
            sys.exit()
        elif opt in ("-t", "--thickness"):
            thickness = float(arg)
        elif opt in ("-N", "--numpts"):
            numpts = int(arg)
        elif opt in ("-a", "--angle"):
            angle = float(arg)

    print()
    print('           Foil thickness: ', thickness)
    print('Number of division points: ', numpts)
    print('          Angle of attack: ', angle)
        
    [naca_p, N, yMin, yMax] = naca00XXprofile(thickness, numpts, angle)
    createGMSHfile(naca_p, N, geo_file, angle, yMin, yMax)
    
    print('-------------------------------------')
    print('Results written to: ', geo_file)
    print()
    
if __name__ == "__main__":
   main(sys.argv[1:])


