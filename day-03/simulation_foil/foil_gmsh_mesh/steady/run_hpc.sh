#!/bin/bash 
#SBATCH --export=ALL,LD_PRELOAD=
#SBATCH --partition=rome 
#SBATCH --mem=0
#SBATCH --ntasks 8
#SBATCH --ntasks-per-node=8

module purge
module load OpenFOAM
source $FOAM_BASH

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# decompose the case (number of decompositions is equal to --ntasks)
runApplication decomposePar

# run parallel
echo "Start $(getApplication) in parallel. Log is written in case/log.$(getApplication)!"
srun --mpi=pmix  $(getApplication) -parallel 

# Check the running process with: tail -f case/log.$(getApplication)
