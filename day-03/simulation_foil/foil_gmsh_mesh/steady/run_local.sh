#!/bin/bash

# Source tutorial clean functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# decompose the case (number of decompositions is equal to --ntasks)
runApplication decomposePar

# run parallel
echo "Start $(getApplication) in parallel. Log is written in case/log.$(getApplication)!"
runParallel $(getApplication) &
