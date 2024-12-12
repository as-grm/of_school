#!/bin/bash 
#SBATCH --export=ALL,LD_PRELOAD=
#SBATCH --partition=rome 
#SBATCH --mem=0
#SBATCH --ntasks 8
#SBATCH --ntasks-per-node=8

# Needed to load OpenFOAM env on the HPC nodes
module purge
module load OpenFOAM
source $FOAM_BASH

# run parallel
echo "Start foamRun in parallel. Log is written in case/slurm-ID.log!"
srun --mpi=pmix foamRun -parallel

# Check the running process with: tail -f case/slurm-ID.log
