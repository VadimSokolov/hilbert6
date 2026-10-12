#!/bin/bash
#SBATCH --job-name=gbc_cover2
#SBATCH --partition=normal
#SBATCH --constraint=intel
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --array=1-20
#SBATCH --output=logs/cover2_%a.out
#SBATCH --error=logs/cover2_%a.err

cd /scratch/vsokolov/gbc_cover2
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
python3 -u exp_cover2.py --rep $SLURM_ARRAY_TASK_ID --reps_per_task 15 \
    --out results/cover2_rep${SLURM_ARRAY_TASK_ID}.json
