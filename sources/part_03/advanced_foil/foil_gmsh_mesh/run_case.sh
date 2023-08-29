#!/bin/bash

# run it with flags:
#$> run_case.sh -c {icoFoam, simpleFoam} -a {angle in degs}

path=$(pwd)

usage()
{
    echo "usage: run_case.sh -c {icoFoam, simpleFoam} -a {angle in [0,20]gdegs}"
}

no_args="true"
while getopts c:a: flag
do
    case "${flag}" in
        c) 
            case=${OPTARG}
            if [ $case != "icoFoam" ] &&  [ $case != "simpleFoam" ]; then
                echo "Case name can be only icoFoam or simpleFoam!"
                exit 1
            fi
            ;;
        a) 
            angle=${OPTARG}
            if [[ $angle -lt 0 ]] ||  [[ $angle -gt 20 ]]; then
                echo "Angle should be between 0 and 20 degrees!"
                exit 1
            fi
            ;;
        *) 
            usage
            exit 1
            ;;
    esac
    no_args="false"
done

[[ "$no_args" == "true" ]] && { usage; exit 1; }

shift $((OPTIND-1))

if [ -z "${case}" ] || [ -z "${angle}" ]; then
    usage
    exit 1
fi

echo "Running case: $case";
echo "Foil angle: $angle [deg]";

pfCase="potentialFoam"

cd $path/$pfCase
./Allclean

cd $path/$case
./Allclean

$path/foil_mesh/create_mesh.sh $angle
cp -rf $path/foil_mesh/constant/polyMesh $path/$pfCase/constant
cp -rf $path/foil_mesh/constant/polyMesh $path/$case/constant

cd $path/$pfCase
./Allrun $pfCase
cp -rf $path/$pfCase/0/p $path/$pfCase/0/U $path/$case/0

cd $path/$case
./Allrun $case

# Check the running process with: 
# - tail -f $case/log.$case
# - foamMonitor -l $case/postProcessing/residuals/0/residuals.dat 
#       here is needed gnuplot and residuals in system/controlDict
