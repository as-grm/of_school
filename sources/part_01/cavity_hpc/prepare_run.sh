#!/bin/bash

module purge
module load OpenFOAM/10-foss-2022a
source $FOAM_BASH

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

runMapFieldsConsistent()
{
    echo "Running mapFields from $1 to $2"
    mapFields $1 -case $2 -sourceTime latestTime -consistent > $2/log.mapFields 2>&1
}

setCavityFine()
{
    blockMeshDict="$caseName/system/blockMeshDict"
    controlDict="$caseName/system/controlDict"
    sed s/"20 20 1"/"500 500 1"/g $blockMeshDict > temp.$$
    mv temp.$$ $blockMeshDict
    sed \
    -e s/"\(deltaT[ \t]*\) 0.005;"/"\1 0.00005;"/g \
    -e s/"\(writeControl[ \t]*\) timeStep;"/"\1 runTime;"/g \
    -e s/"\(writeInterval[ \t]*\) 20;"/"\1 0.005;"/g \
    -e s/"\(endTime[ \t]*\) 0.5;"/"\1 0.01;"/g \
    $controlDict > temp.$$
    mv temp.$$ $controlDict

#    -e s/"\(startTime[ \t]*\) 0;"/"\1 0.5;"/g \
#    -e s/"\(endTime[ \t]*\) 0.5;"/"\1 0.7;"/g \
}

# run start case "cavity"
caseName="cavity"
cd $caseName
runApplication blockMesh
cd ..

# refine mesh
caseName="cavityFine"
cloneCase cavity cavityFine
setCavityFine
cd $caseName
runApplication blockMesh
