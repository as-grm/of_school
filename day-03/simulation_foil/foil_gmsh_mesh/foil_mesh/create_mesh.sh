#!/bin/bash
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

thickness=0.12
num_pts=100
angle=$1
gmsh_geo="naca_profile.geo"
gmsh_msh="naca_profile.msh"

# Python script to create GMSH geo file for foil geometry
python3 exterior_flow_NACA_profile.py -t $thickness -N $num_pts -a $angle

if [[ $angle -le 15 ]]; then
    echo " a <= 15"
    sed \
    -e s/"w_bb_ib = 0.05;"/"w_bb_ib = 0.035;"/g \
    -e s/"Field\[1\].Size = 0.005;"/"Field\[1\].Size = 0.004;"/g \
    $gmsh_geo > temp.$$
    mv temp.$$ $gmsh_geo
else
    echo " a > 15"
    sed \
    -e s/"w_bb_ib = 0.035;"/"w_bb_ib = 0.05;"/g \
    -e s/"Field\[1\].Size = 0.004;"/"Field\[1\].Size = 0.005;"/g \
    $gmsh_geo > temp.$$
    mv temp.$$ $gmsh_geo
fi

gmsh -3 -format msh2 -o $gmsh_msh $gmsh_geo

rm -rf constant/polyMesh
gmshToFoam $gmsh_msh
python3 correct_boundary.py > temp.$$
mv temp.$$ constant/polyMesh/boundary

#------------------------------------------------------------------------------ 
