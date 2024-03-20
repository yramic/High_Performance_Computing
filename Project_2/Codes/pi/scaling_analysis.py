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

# Create DataFrame for slurm_job_pi_critical_strong:
with open(folder_path + 'slurm_job_pi_critical_strong.txt', 'r') as file:
    lines = file.readlines()

df_critical_strong = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_1)

df_critical_strong['pi'] = df_critical_strong['pi'].astype(float)
df_critical_strong['N'] = df_critical_strong['N'].astype(int)
df_critical_strong['threads'] = df_critical_strong['threads'].astype(int)
df_critical_strong['time'] = df_critical_strong['time'].astype(float)

# Same thing now for the reduction_strong text file:
with open(folder_path + 'slurm_job_pi_reduction_strong.txt', 'r') as file:
    lines = file.readlines()

df_reduction_strong = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_1)

df_reduction_strong['pi'] = df_reduction_strong['pi'].astype(float)
df_reduction_strong['N'] = df_reduction_strong['N'].astype(int)
df_reduction_strong['threads'] = df_reduction_strong['threads'].astype(int)
df_reduction_strong['time'] = df_reduction_strong['time'].astype(float)

# Create DataFrame for slurm_job_pi_critical_weak:
with open(folder_path + 'slurm_job_pi_critical_weak.txt', 'r') as file:
    lines = file.readlines()

df_critical_weak = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_1)

df_critical_weak['pi'] = df_critical_weak['pi'].astype(float)
df_critical_weak['N'] = df_critical_weak['N'].astype(int)
df_critical_weak['threads'] = df_critical_weak['threads'].astype(int)
df_critical_weak['time'] = df_critical_weak['time'].astype(float)

# Create DataFrame for slurm_job_pi_reduction_weak:
with open(folder_path + 'slurm_job_pi_reduction_weak.txt', 'r') as file:
    lines = file.readlines()

df_reduction_weak = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_1)

df_reduction_weak['pi'] = df_reduction_weak['pi'].astype(float)
df_reduction_weak['N'] = df_reduction_weak['N'].astype(int)
df_reduction_weak['threads'] = df_reduction_weak['threads'].astype(int)
df_reduction_weak['time'] = df_reduction_weak['time'].astype(float)

# Same thing now for the serial text file:
with open(folder_path + 'slurm_job_pi_serial.txt', 'r') as file:
    lines = file.readlines()

df_serial = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_2)

df_serial['pi'] = df_serial['pi'].astype(float)
df_serial['N'] = df_serial['N'].astype(int)
df_serial['time'] = df_serial['time'].astype(float)

# Same thing now for the serial text file:
with open(folder_path + 'slurm_job_pi_serial_strong.txt', 'r') as file:
    lines = file.readlines()

df_serial_strong = pd.DataFrame([line.strip().split(',') for line in lines],
                  columns=columns_2)

df_serial_strong['pi'] = df_serial_strong['pi'].astype(float)
df_serial_strong['N'] = df_serial_strong['N'].astype(int)
df_serial_strong['time'] = df_serial_strong['time'].astype(float)


######################## STRONG SCALING ANALYSIS - SPEEDUP ############################

# Formula for the speed up: S = T_serial / T_parallel

S_critical_strong = []

for i in range(len(df_critical_strong['N'])):
    S_critical_strong.append(df_serial_strong['time'].loc[0] / df_critical_strong['time'].loc[i])


S_reduction_strong = []

for i in range(len(df_reduction_strong['N'])):
    S_reduction_strong.append(df_serial_strong['time'].loc[0] / df_reduction_strong['time'].loc[i])

# Now I want to get the ideal line!
S_ideal_strong = []

for i in range(len(df_critical_strong['N'])):
    S_ideal_strong.append( df_serial_strong['time'].loc[0] / (df_serial_strong['time'].loc[0] / df_critical_strong['threads'].loc[i]) )


######################## WEAK SCALING ANALYSIS - EFFICIENCY ############################

# Forula for the efficiency: E = T_serial / (T_parallel * p)
    
E_critical_weak = []

for i in range(len(df_critical_weak['N'])):
    E_critical_weak.append(df_serial['time'].loc[i] / (df_critical_weak['time'].loc[i] * df_critical_weak['threads'].loc[i] ))

E_reduction_weak = []

for i in range(len(df_reduction_weak['N'])):
    E_reduction_weak.append( df_serial['time'].loc[i] / (df_reduction_weak['time'].loc[i] * df_reduction_weak['threads'].loc[i] ) )

######################## PLOTS ############################

# plot the Speed up
plt.figure(dpi=200)
plt.title("Parallel Speedup")
plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.grid()
plt.plot(df_critical_strong['threads'].loc[:], S_critical_strong[:], marker="x", label="critical")
plt.plot(df_reduction_strong['threads'].loc[:], S_reduction_strong[:], marker="x", label="reduction")
plt.plot(df_critical_strong['threads'].loc[:], S_ideal_strong[:], marker="x", label="ideal")
plt.legend()
plt.show()

# plt.savefig('parallel_speedup.png')

# # plot parallel efficiency
plt.figure(dpi=200)
plt.title("Parallel Efficiency")
plt.xlabel("Number of Threads")
plt.ylabel("Efficiency")
plt.grid()
plt.plot(df_critical_weak['threads'].loc[:], E_critical_weak[:], marker="x", label="critical")
plt.plot(df_reduction_weak['threads'].loc[:], E_reduction_weak[:], marker="x", label="reduction")
plt.plot(df_reduction_weak['threads'].loc[:], np.ones(len(df_critical_weak['N'])), marker="x", label="ideal")
plt.legend()
plt.show()

# plt.savefig('parallel_efficiency.png')