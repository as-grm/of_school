#!/bin/bash
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial clean functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# run sequential
echo "Start $(getApplication) in sequential. Log is written in case/log.$(getApplication)!"
runApplication $(getApplication) &



