import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

######################## DATA EXTRACTION ############################
# Folder where the data files are stored:
folder_path = 'Output_Data/'

# Define a list of column names
columns_1 = ['pi', 'N', 'threads', 'time']
# For the serial file there is no number of threads!
columns_2 = ['pi', 'N', 'time']

# Create DataFrame for slurm_job_pi_critical:
with open(folder_path + 'slurm_job_pi_critical.txt', 'r') as file:
    lines = file.readlines()

df_critical = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_1)

df_critical['pi'] = df_critical['pi'].astype(float)
df_critical['N'] = df_critical['N'].astype(int)
df_critical['threads'] = df_critical['threads'].astype(int)
df_critical['time'] = df_critical['time'].astype(float)

# Same thing now for the reduction text file:
with open(folder_path + 'slurm_job_pi_reduction.txt', 'r') as file:
    lines = file.readlines()

df_reduction = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_1)

df_reduction['pi'] = df_reduction['pi'].astype(float)
df_reduction['N'] = df_reduction['N'].astype(int)
df_reduction['threads'] = df_reduction['threads'].astype(int)
df_reduction['time'] = df_reduction['time'].astype(float)

# Same thing now for the serial text file:
with open(folder_path + 'slurm_job_pi_serial.txt', 'r') as file:
    lines = file.readlines()

df_serial = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_2)

df_serial['pi'] = df_serial['pi'].astype(float)
df_serial['N'] = df_serial['N'].astype(int)
df_serial['time'] = df_serial['time'].astype(float)

# Now I want to have all Unique values:
N_values = df_critical['N'].iloc[:]
N_unique = N_values.unique()

threads_values = df_critical['threads'].iloc[:]
threads_unique = threads_values.unique()


######################## STRONG SCALING ANALYSIS ############################

# Formula for the speed up: S = T_serial / T_parallel
# Formula for the efficiency: E = 1 / (S * p) with: p ... number of threads
S_critical_strong = []
E_critical_strong = []
# Note that I will do the calculations only for N = 1,000,000:
# df_filtered = df_critical[df_critical['N'] == 1000000]
# for i in range(len(df_filtered)):
for i in range(len(df_critical['N'])):
    idx = i // 5 # Integer division!
    S_critical_strong.append(df_serial['time'].loc[idx] / df_critical['time'].loc[i])
    E_critical_strong.append( 1/ (S_critical_strong[i] * df_critical['threads'].loc[i]) )


S_reduction_strong = []
E_reduction_strong = []

for i in range(len(df_reduction['N'])):
    idx = i // 5 # Integer division!
    S_reduction_strong.append(df_serial['time'].loc[idx] / df_reduction['time'].loc[i])
    E_reduction_strong.append( 1/ (S_reduction_strong[i] * df_reduction['threads'].loc[i]) )

# Now I want to get the ideal line!
S_ideal_strong = []

for i in range(len(df_critical['N'])):
    idx = i // 5 # Integer division!
    S_ideal_strong.append( df_serial['time'].loc[idx] / (df_serial['time'].loc[idx] / df_critical['threads'].loc[i]) )


######################## WEAK SCALING ANALYSIS ############################

# Formula for the speed up: S = p * (T_serial / T_parallel)
# Forula for the efficiency: E = T_serial / T_parallel
    
S_critical_weak = []
E_critical_weak = []
# Note that I will do the calculations only for N = 1,000,000:
# df_filtered = df_critical[df_critical['N'] == 1000000]
# for i in range(len(df_filtered)):
for i in range(len(df_critical['N'])):
    idx = i // 5 # Integer division!
    S_critical_weak.append( df_critical['threads'].loc[i] * (df_serial['time'].loc[idx] / df_critical['time'].loc[i]) )
    E_critical_weak.append( df_serial['time'].loc[idx] / df_critical['time'].loc[i] )


S_reduction_weak = []
E_reduction_weak = []

for i in range(len(df_reduction['N'])):
    idx = i // 5 # Integer division!
    S_critical_weak.append( df_reduction['threads'].loc[i] * (df_serial['time'].loc[idx] / df_reduction['time'].loc[i]) )
    E_critical_weak.append( df_serial['time'].loc[idx] / df_reduction['time'].loc[i] )

######################## PLOTS ############################

# plot the Speed up
plt.figure(dpi=200)
plt.title("Parallel Speedup")
plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.grid()
plt.plot(threads_unique[:], S_critical_strong[0:5], marker="x", label="critical")
plt.plot(threads_unique[:], S_reduction_strong[0:5], marker="x", label="reduction")
plt.plot(threads_unique[:], S_ideal_strong[0:5], marker="x", label="ideal")
plt.xlim(1, threads_unique[-1] + 1)
plt.legend()
plt.show()

# # plt.savefig('parallel_speedup.png')

# # plot parallel efficiency
plt.figure(dpi=200)
plt.title("Parallel Efficiency")
plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.grid()
plt.plot(threads_unique[:], E_critical_strong[0:5], marker="x", label="critical")
plt.plot(threads_unique[:], E_reduction_strong[0:5], marker="x", label="reduction")
# plt.plot(threads_unique[:], E_ideal_strong[0:5], marker="x", label="ideal")
plt.xlim(1, threads_unique[-1] + 1)
plt.legend()
plt.show()

# # plt.savefig('parallel_efficiency.png')