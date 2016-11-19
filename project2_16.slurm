#!/bin/bash
#SBATCH --job-name=project2
#SBATCH --output results_16_thread.txt
#SBATCH --error slurm.err
#SBATCH --partition=batch
#SBATCH --qos=short
#SBATCH --constraint=hpcf2013
#SBATCH --exclusive
#SBATCH --cpus-per-task=16
#SBATCH --ntasks=1

export KMP_AFFINITY="verbose,compact"
export OMP_NUM_THREADS=16
srun ./project2
