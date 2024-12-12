#!/bin/bash
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial clean functions
source $WM_PROJECT_DIR/bin/tools/RunFunctions

# run parallel
echo "Start $(getApplication) in parallel. Log is written in case/log.$(getApplication)!"
runParallel $(getApplication) &
