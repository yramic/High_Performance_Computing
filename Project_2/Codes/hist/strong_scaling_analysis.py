import numpy as np
import os
import matplotlib.pyplot as plt

######################## DATA ############################

# Since it's only one file I decided to read out the data manually!

# Results for the omp (total time)
# t_omp = [1684.3, 789.63, 422.157, 190.186, 89.7582, 52.6643]
t_omp = [2.60583, 1.47105, 0.843258, 0.468622, 0.340959, 0.290979]

# Number of threads
threads = [1, 2, 4, 8, 16, 32]

# Result for the sequential implementation (without omp)
t_seq = 2.65926

######################## STRONG SCALING ANALYSIS - SPEEDUP ############################

# Formula for the speed up: S = T_serial / T_parallel

S = []

for i in range(len(threads)):
    S.append(t_seq / t_omp[i])

# Now I want to get the ideal line!
S_ideal = []

for i in range(len(threads)):
    S_ideal.append( t_seq / (t_seq / threads[i]))

######################## PLOTS ############################

# plot the Speed up
plt.figure(dpi=200)
plt.title("Parallel Speedup")
plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.grid()
plt.plot(threads[:], S[:], marker="x", label="omp result")
plt.plot(threads[:], S_ideal[:], marker="x", label="ideal")
plt.legend()
plt.show()

# plt.savefig('parallel_speedup.png')