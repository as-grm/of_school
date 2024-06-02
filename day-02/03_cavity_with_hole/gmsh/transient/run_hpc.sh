#!/bin/bash 
#SBATCH --export=ALL,LD_PRELOAD=
#SBATCH --partition=rome 
#SBATCH --mem=0
#SBATCH --ntasks 4
#SBATCH --ntasks-per-node=4

module purge
module load OpenFOAM
source $FOAM_BASH

cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# run parallel
echo "Start $(getApplication) in parallel. Log is written in case/log.$(getApplication)!"
srun --mpi=pmix  $(getApplication) -parallel 

# Check the running process with: tail -f case/log.$(getApplication)
