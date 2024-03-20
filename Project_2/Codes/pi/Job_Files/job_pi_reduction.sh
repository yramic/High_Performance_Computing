#!/bin/bash
#SBATCH --job-name=slurm_pi_reduction               # Job name    (default: sbatch)
#SBATCH --output=slurm_job_pi_reduction-%j.out      # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_pi_reduction-%j.err       # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                                  # Number of tasks
#SBATCH --cpus-per-task=48                          # Number of CPUs per task
#SBATCH --mem-per-cpu=1024                          # Memory per CPU
#SBATCH --time=01:00:00                             # Wall clock time limit
#SBATCH --constraint=EPYC_7763                      # Nodes with specific CPU

# load some modules & list loaded modules
module load gcc

# Compile the C++ program:
make

# run (srun: run job on cluster with provided resources/allocation)

# Weak Scaling Analysis
# srun ./pi_omp_reduction 1000000 1
# srun ./pi_omp_reduction 2000000 2
# srun ./pi_omp_reduction 4000000 4
# srun ./pi_omp_reduction 8000000 8
# srun ./pi_omp_reduction 16000000 16
# srun ./pi_omp_reduction 32000000 32

# # Remove the first four lines from the output file
# tail -n +8 slurm_job_pi_reduction-${SLURM_JOB_ID}.out > slurm_job_pi_reduction_weak.txt

# Strong Scaling Analysis
srun ./pi_omp_reduction 10000000 2
srun ./pi_omp_reduction 10000000 7
srun ./pi_omp_reduction 10000000 12
srun ./pi_omp_reduction 10000000 17
srun ./pi_omp_reduction 10000000 22
srun ./pi_omp_reduction 10000000 27
srun ./pi_omp_reduction 10000000 32
srun ./pi_omp_reduction 10000000 37
srun ./pi_omp_reduction 10000000 42

# Remove the first four lines from the output file
tail -n +8 slurm_job_pi_reduction-${SLURM_JOB_ID}.out > slurm_job_pi_reduction_strong.txt