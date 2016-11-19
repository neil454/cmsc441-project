#!/bin/bash
#SBATCH --job-name=project2
#SBATCH --output results_4_thread.txt
#SBATCH --error slurm.err
#SBATCH --partition=batch
#SBATCH --qos=short
#SBATCH --constraint=hpcf2013
#SBATCH --exclusive
#SBATCH --cpus-per-task=8
#SBATCH --ntasks=1

export KMP_AFFINITY="verbose,compact"
export OMP_NUM_THREADS=4
srun ./project2
