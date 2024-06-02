#!/bin/bash

path=$(pwd)

usage()
{
    echo "usage: run_case.sh  -c {steady, transient} -p {not, local, hpc} -u {real number} -r {real number} -y {real number}"
}

no_args="true"
while getopts c:p:u:r:y: flag
do
    case "${flag}" in
        c)
            case=${OPTARG}
            if [ $case != "steady" ] &&  [ $case != "transient" ]; then
                echo "Case can be only steady or transient!"
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
        u)
            vel=${OPTARG}
            cmp_1=$(echo "$vel <= 10" | bc) # use bc to compare float numbers
            cmp_2=$(echo "$vel > 0" | bc)
            if [[ $cmp_1 -ne 1 ]] ||  [[ $cmp_2 -ne 1 ]]; then
                echo "Velocity should be in interval [0,10] m!"
                exit 1
            fi
            ;;
        r)
            radius=${OPTARG}
            cmp_1=$(echo "$radius <= 1" | bc) # use bc to compare float numbers
            cmp_2=$(echo "$radius > 0" | bc)
            if [[ $cmp_1 -ne 1 ]] ||  [[ $cmp_2 -ne 1 ]]; then
                echo "Radius should be in interval [0,1] m!"
                exit 1
            fi
            ;;
        y)
            yplus=${OPTARG}
            cmp_1=$(echo "$yplus <= 500" | bc) # use bc to compare float numbers
            cmp_2=$(echo "$yplus > 0" | bc)
            if [[ $cmp_1 -ne 1 ]] ||  [[ $cmp_2 -ne 1 ]]; then
                echo "Y+ should be in interval [0,500]!"
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

if [ -z "${case}" ] || [ -z "${parallel}" ] || [ -z "${vel}" ] || [ -z "${radius}" ] || [ -z "${yplus}" ]; then
    usage
    exit 1
fi

echo
echo "Running case: **$case**";
echo

# Clean all old simulations
bash $path/clean_all.sh

# prepare case
bash $path/cylinder_mesh/Allrun $vel $radius $yplus
cp -rf $path/cylinder_mesh/constant/polyMesh $path/$case/constant
cp -rf $path/cylinder_mesh/0.org $path/$case/0
rm -rf $path/$case/0/U_*

# run the case
if [ $parallel == "not" ]; then
    bash $path/$case/run_sequential.sh
elif [ $parallel == "local" ]; then
    bash $path/$case/run_local.sh
else
    sbatch $path/$case/run_hpc.sh
fi



# Check the running process with: 
# - tail -f $case/log.$case
# - foamMonitor -l $case/postProcessing/residuals/0/residuals.dat 
#       here is needed gnuplot and residuals in system/controlDict
