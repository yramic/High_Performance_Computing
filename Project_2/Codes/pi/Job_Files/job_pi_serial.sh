#!/bin/bash
#SBATCH --job-name=slurm_pi_serial             # Job name    (default: sbatch)
#SBATCH --output=slurm_job_pi_serial-%j.out    # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_pi_serial-%j.err     # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                             # Number of tasks
#SBATCH --cpus-per-task=1                      # Number of CPUs per task
#SBATCH --mem-per-cpu=1024                     # Memory per CPU
#SBATCH --time=01:00:00                        # Wall clock time limit
#SBATCH --constraint=EPYC_7763                 # Nodes with specific CPU

# load some modules & list loaded modules
module load gcc

# Compile the C++ program:
make

# run (srun: run job on cluster with provided resources/allocation)
srun ./pi_serial 1000000
srun ./pi_serial 500000
srun ./pi_serial 250000
srun ./pi_serial 125000
srun ./pi_serial 62500

# Remove the first four lines from the output file
# It is important to make a proper make clean before running this file, otherwise there
# will be deleted too many slides!
tail -n +8 slurm_job_pi_serial-${SLURM_JOB_ID}.out > slurm_job_pi_serial.txt