#!/bin/bash
#SBATCH --job-name=slurm_pi_critical                # Job name    (default: sbatch)
#SBATCH --output=slurm_job_pi_critical-%j.out       # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_pi_critical-%j.err        # Error file  (default: slurm-%j.out)
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
srun ./pi_omp_critical 1000000 2
srun ./pi_omp_critical 1000000 12
srun ./pi_omp_critical 1000000 22
srun ./pi_omp_critical 1000000 32
srun ./pi_omp_critical 1000000 42

srun ./pi_omp_critical 500000 2
srun ./pi_omp_critical 500000 12
srun ./pi_omp_critical 500000 22
srun ./pi_omp_critical 500000 32
srun ./pi_omp_critical 500000 42

srun ./pi_omp_critical 250000 2
srun ./pi_omp_critical 250000 12
srun ./pi_omp_critical 250000 22
srun ./pi_omp_critical 250000 32
srun ./pi_omp_critical 250000 42

srun ./pi_omp_critical 125000 2
srun ./pi_omp_critical 125000 12
srun ./pi_omp_critical 125000 22
srun ./pi_omp_critical 125000 32
srun ./pi_omp_critical 125000 42

srun ./pi_omp_critical 62500 2
srun ./pi_omp_critical 62500 12
srun ./pi_omp_critical 62500 22
srun ./pi_omp_critical 62500 32
srun ./pi_omp_critical 62500 42

# Remove the first four lines from the output file
# It is important to make a proper make clean before running this file, otherwise there
# will be deleted too many slides!
tail -n +8 slurm_job_pi_critical-${SLURM_JOB_ID}.out > slurm_job_pi_critical.txt