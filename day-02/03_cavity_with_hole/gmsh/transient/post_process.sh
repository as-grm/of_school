#!/bin/bash
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial clean functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# obtain data for the latest time
runApplication reconstructPar -latestTime

# generate y+ data
foamPostProcess -solver $(getSolver) -func yplus -latestTime
