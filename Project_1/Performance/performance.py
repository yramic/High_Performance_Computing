import numpy as np
import matplotlib.pyplot as plt

# Studying the paper provided by Williams et al. Roofline: an insightful visual performance model
# for multicore architectures, we can see how the diagramm can acutally be created!

# Roofline parameters for phase I and II respectively
# Note it's important to take only the node values!
peak_performances = np.array([5324.8, 5017.6])  # in GFlops/s

# The memory bandwidth is also relevant for both phase I and II!
memory_bandwidths = np.array([17, 27])  # in GB/s

# Performance data
# best_rate = 18000.0 / 1000  # in GB/s
avg_time = np.array([0.005233, 0.007299])  # in seconds (scale)
# For phase I and II, the copy function has the smallest avg time!

# Operational intensities (FLOPs/Byte)
ops_intensity = peak_performances / memory_bandwidths

# The labels are: 
labels = ["Phase 1", "Phase 2"]

# Create the log-log roofline plot
plt.figure(figsize=(6, 4))

# Plot roofline
for i in range(2):
    x_roofline = np.linspace(0, ops_intensity[i], 100)
    y_roofline = np.minimum(
        x_roofline * peak_performances[i], memory_bandwidths[i])
    plt.loglog(x_roofline, y_roofline, label=labels[i])

# Add labels and legend
plt.xlabel('Operational Intensity in [FLOPs/Byte]')
plt.ylabel('Performance P in [GFLOPs/s]')
plt.ylim([0.001, 40])
plt.xlim([2**(-3), 2**(7)])
plt.legend()

# Set y-axis to log base 2
plt.xscale('log', base=2)

# Show plot
plt.grid(True)
plt.tight_layout()
fname = "performance.png"
plt.savefig(fname, dpi=100)