#!/bin/bash

# run it with flags:
#$> run_case.sh -c {transient, steady} -a {angle in degs} -p {not, local, hpc}

path=$(pwd)

usage()
{
    echo "usage: run_case.sh -c {transient, steady} -a {angle in [0,20]degs} -p {not, local, hpc}"
}

no_args="true"
while getopts c:a:p: flag
do
    case "${flag}" in
        c) 
            case=${OPTARG}
            if [ $case != "transient" ] &&  [ $case != "steady" ]; then
                echo "Case name can be only transient or steady!"
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
        p)
            parallel=${OPTARG}
            if [ $parallel != "local" ] &&  [ $parallel != "hpc" ] &&  [ $parallel != "not" ]; then
                echo "Parallel run can be only not, local or hpc!"
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

if [ -z "${case}" ]  || [ -z "${angle}" ] || [ -z "${parallel}" ]; then
    usage
    exit 1
fi

echo "Running case: $case";
echo "Foil angle: $angle [deg]";

# Clean all old simulations
bash $path/clean_all.sh

# prepare case
bash $path/foil_mesh/create_mesh.sh $angle
cp -rf $path/foil_mesh/constant/polyMesh $path/$case/constant
cp -rf $path/$case/0.org $path/$case/0

# run the case
cd $path/$case
if [ $parallel == "not" ]; then
    bash ./run_sequential.sh
elif [ $parallel == "local" ]; then
    bash ./run_local.sh
else
    sbatch run_hpc.sh
fi



# Check the running process with: 
# - tail -f $case/log.$case
# - foamMonitor -l $case/postProcessing/residuals/0/residuals.dat 
#       here is needed gnuplot and residuals in system/controlDict
