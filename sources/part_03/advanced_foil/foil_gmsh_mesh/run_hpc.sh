#!/bin/bash 
#SBATCH --export=ALL,LD_PRELOAD=
#SBATCH --partition=rome 
#SBATCH --mem=0
#SBATCH --ntasks 32
#SBATCH --ntasks-per-node=16

module purge
module load OpenFOAM/10-foss-2022a
source $FOAM_BASH

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# Path to running case
#caseName="cavityFine"
#cd $caseName

# decompose the case (number of decompositions is equal to --ntasks)
#runApplication decomposePar

# run parallel
echo "Start $(getApplication) in parallel. Log is written in case/log.$(getApplication)!"
srun --mpi=pmix  $(getApplication) -parallel 
#> log.$(getApplication) 2>&1

# Check the running process with: tail -f case/log.$(getApplication)
