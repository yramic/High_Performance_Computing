#!/bin/bash
#SBATCH --job-name=slurm_mandel                 # Job name    (default: sbatch)
#SBATCH --output=slurm_job_mandel-%j.out        # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_mandel-%j.err         # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                              # Number of tasks
#SBATCH --cpus-per-task=48                      # Number of CPUs per task
#SBATCH --mem-per-cpu=1024                      # Memory per CPU
#SBATCH --time=01:00:00                         # Wall clock time limit
#SBATCH --constraint=EPYC_7763                  # Nodes with specific CPU

# load some modules & list loaded modules
module load gcc

# Compile the C++ program:
make

# run (srun: run job on cluster with provided resources/allocation)

# Strong Scaling Analysis
echo "Mandel Serial Implementation:"
srun ./mandel_seq
echo "---------------------------------------------"

echo "Mandel Parallelized with 1 Thread:"
srun ./mandel_omp 1
echo "---------------------------------------------"

echo "Mandel Parallelized with 2 Threads:"
srun ./mandel_omp 2
echo "---------------------------------------------"

echo "Mandel Parallelized with 4 Threads:"
srun ./mandel_omp 4
echo "---------------------------------------------"

echo "Mandel Parallelized with 8 Threads:"
srun ./mandel_omp 8
echo "---------------------------------------------"

echo "Mandel Parallelized with 16 Threads:"
srun ./mandel_omp 16
echo "---------------------------------------------"

echo "Mandel Parallelized with 32 Threads:"
srun ./mandel_omp 32

# Remove the first four lines from the output file
tail -n +7 slurm_job_mandel-${SLURM_JOB_ID}.out > slurm_job_mandel.txt