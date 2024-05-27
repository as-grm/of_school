#!/bin/bash

#module purge
#module load OpenFOAM
#source $FOAM_BASH

cp -r 0.org 0
blockMesh

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# decompose the case (number of decompositions is equal to --ntasks)
runApplication decomposePar


