#!/bin/bash
#SBATCH --job-name=gbc_study2
#SBATCH --partition=normal
#SBATCH --constraint=intel
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --array=1-40
#SBATCH --output=logs/study2_%A_%a.log

cd /scratch/vsokolov/gbc_study2
export OMP_NUM_THREADS=4
python3 -u exp_study2.py --rep $SLURM_ARRAY_TASK_ID \
        --out results/study2_rep${SLURM_ARRAY_TASK_ID}.json
