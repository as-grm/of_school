#!/bin/bash 
#SBATCH --export=ALL,LD_PRELOAD=
#SBATCH --partition=rome 
#SBATCH --mem=0
#SBATCH --ntasks 4
#SBATCH --ntasks-per-node=4

module purge
module load OpenFOAM
source $FOAM_BASH

# run parallel
echo "Start $(getApplication) in parallel. Log is written in case/log.$(getApplication)!"
srun --mpi=pmix foamRun -parallel > log.foamRun

# Check the running process with: tail -f case/log.$(getApplication)
