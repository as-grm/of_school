#!/bin/bash

# run it with flags:
#$> run_case.sh -c {transient, steady} -p {not, local, hpc}

path=$(pwd)

usage()
{
    echo "usage: run_case.sh -c {transient, steady} -p {not, local, hpc}"
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

if [ -z "${case}" ] || [ -z "${parallel}" ]; then
    usage
    exit 1
fi


# Load modules in HPC system

#module purge
#module load OpenFOAM
#source $FOAM_BASH

# Clean old simulations
bash $path/clean_all.sh

echo "Prepare case: $case";

# Prepare Mesh
cd $path/foil_mesh
bash ./Allrun
cd $path

# Set mesh and initial conditions to case
cp -rf $path/$case/0.org $path/$case/0
cp -r $path/foil_mesh/constant/polyMesh $path/$case/constant
cp $path/foil_mesh/0.org/U $path/$case/0

echo "Run case: $case";

# can run in three different modes
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
