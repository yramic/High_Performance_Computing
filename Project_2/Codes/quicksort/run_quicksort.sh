#!/bin/bash
#SBATCH --job-name=quicksort        # Job name
#SBATCH --output=quicksort-%j.out   # Output file
#SBATCH --error=quicksort-%j.err    # Error file
#SBATCH --ntasks=1                  # Number of tasks
#SBATCH --constraint=EPYC_7763      # Select node with CPU
#SBATCH --cpus-per-task=48          # Number of CPUs per task
#SBATCH --mem-per-cpu=1024          # Memory per CPU
#SBATCH --time=00:05:00             # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Different Problem Sizes!
LIST=(10000000 20000000 40000000 80000000 160000000 320000000)
# Run the program without OMP:
for size in "${LIST[@]}"
do
  echo "Running the Sequential Program"
  echo "Problem Size = $size"
  ./quicksort $size
done

# Run the program for OMP_NUM_THREADS equal to 1, 2, 4, 8, 16, 32 -- 5
for size in "${LIST[@]}"
do
  for ((i=0; i<=2; i++))
  do
    OMP_NUM_THREADS=$((2**i))
    echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS"
    echo "Problem Size = $size"
    export OMP_NUM_THREADS
    ./quicksort_omp $size 
    done
done

# Remove the first four lines from the output file
# tail -n +7 quicksort-${SLURM_JOB_ID}.out > output_quicksort.txt