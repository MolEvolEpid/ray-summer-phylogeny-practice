import matplotlib.pyplot as plt
import numpy as np

from new_optimization import *

# Create a few trees from files
# All trees were generated with Erik's simulator and scaled by my script
with open("eric-sim/b3/tree01_rescaled.txt") as f:
    t_b3_normal = TimeTree(f.readline())
with open("eric-sim/b3/tree02_rescaled.txt") as f:
    t_b3_broken = TimeTree(f.readline())

# Gridsearch
# For some trees, the gridsearch reveals a hard edge to the valid values.
# This is not present for other trees.
def plot_gridsearch(t, a_bounds, b_bounds):
    a_min, a_max = a_bounds
    b_min, b_max = b_bounds
    a_range = np.linspace(a_min, a_max, 100)
    b_range = np.linspace(b_min, b_max, 100)

    values = simple_gridsearch(t, a_range, b_range, 2*(365/1.5))

    fig, ax = plt.subplots()
    cax = ax.imshow(values, origin="lower")
    cbar = fig.colorbar(cax)

    ax.set_xlabel("Beta")
    ax.set_ylabel("Alpha")
    ax.set_xticks((0, 100))
    ax.set_yticks((0, 100))
    ax.set_xticklabels((b_min, b_max))
    ax.set_yticklabels((a_min, a_max))
    plt.show()

plot_gridsearch(t_b3_normal, (1, 200), (1, 200))
plot_gridsearch(t_b3_broken, (1, 200), (1, 200))

# Optimization
# With the trees with
t1 = optimize_a_b(t_b3_normal, (1, 1), 2*(365/1.5))
t2 = optimize_a_b(t_b3_normal, (2, 2), 2*(365/1.5))
t3 = optimize_a_b(t_b3_normal, (1, 3), 2*(365/1.5))
t4 = optimize_a_b(t_b3_normal, (3, 1), 2*(365/1.5))
t5 = optimize_a_b(t_b3_normal, (5, 5), 2*(365/1.5))
t6 = optimize_a_b(t_b3_normal, (5, 3), 2*(365/1.5))
