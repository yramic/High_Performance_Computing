import numpy as np
import os
import matplotlib.pyplot as plt

######################## DATA ############################

# Since it's only one file I decided to read out the data manually!

# Results for the omp (total time)
# size = 10000000
t_omp_1 = [2.343903, 1.195091, 0.6066376, 0.5392190, 0.6830470, 0.9954015]
# size = 20000000
t_omp_2 = [2.877877, 1.937033, 1.38269, 0.9329812, 1.159151, 1.858519]
# size = 40000000
t_omp_3 = [5.542243, 3.742279, 2.550562, 1.538046, 1.721030, 1.186206]
# size = 80000000
t_omp_4 = [11.55358, 6.683268, 4.438704, 3.967884, 3.645958, 5.972143]
# size = 160000000
t_omp_5 = [24.25635, 12.97314, 8.261791, 6.008415, 6.590894, 9.855544]
# size = 320000000 
t_omp_6 = [72.22869, 30.66898, 16.95288, 11.47378, 11.62033, 17.64139]

# Summary Problem Size:
size = [10000000, 20000000, 40000000, 80000000, 160000000, 320000000]

# Number of threads
threads = [1, 2, 4, 8, 16, 32]

# Result for the sequential implementation (without omp)
t_seq = [2.182783, 3.224260, 5.726701, 10.74196, 22.36872, 46.31199]

######################## STRONG SCALING ANALYSIS - SPEEDUP ############################

# Formula for the speed up: S = T_serial / T_parallel

S_1 = []
S_2 = []
S_3 = []
S_4 = []
S_5 = []
S_6 = []

# for i in range(len(threads)):
#     S_1.append(t_seq[0] / t_omp_1[i])
#     S_1.append(t_seq[1] / t_omp_2[i])
#     S_1.append(t_seq[2] / t_omp_3[i])
#     S_1.append(t_seq[3] / t_omp_4[i])
#     S_1.append(t_seq[4] / t_omp_5[i])
#     S_1.append(t_seq[5] / t_omp_6[i])

S_1 = [t_seq[0] / t_omp_1[i] for i in range(len(threads))]
S_2 = [t_seq[1] / t_omp_2[i] for i in range(len(threads))]
S_3 = [t_seq[2] / t_omp_3[i] for i in range(len(threads))]
S_4 = [t_seq[3] / t_omp_4[i] for i in range(len(threads))]
S_5 = [t_seq[4] / t_omp_5[i] for i in range(len(threads))]
S_6 = [t_seq[5] / t_omp_6[i] for i in range(len(threads))]

# Now I want to get the ideal line!
S_ideal = []

for i in range(len(threads)):
    S_ideal.append( t_seq[0] / (t_seq[0] / threads[i]))

######################## PLOTS ############################

# plot the Speed up
plt.figure(dpi=200)
plt.title("Parallel Speedup")
plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.grid()
plt.plot(threads, S_ideal, marker="x", label="ideal")
plt.plot(threads, S_1, marker="x", label="omp result: 10M")
plt.plot(threads, S_2, marker="x", label="omp result: 20M")
plt.plot(threads, S_3, marker="x", label="omp result: 40M")
plt.plot(threads, S_4, marker="x", label="omp result: 80M")
plt.plot(threads, S_5, marker="x", label="omp result: 160M")
plt.plot(threads, S_6, marker="x", label="omp result: 320M")
plt.legend()
# plt.show()

plt.savefig('qicksort_speedup_plot.png')