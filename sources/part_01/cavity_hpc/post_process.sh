#!/bin/bash

module purge
module load OpenFOAM/10-foss-2022a
source $FOAM_BASH

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions


# refined mesh case
caseName="cavityFine"
cd $caseName
runApplication reconstructPar -latestTime

paraFoam
