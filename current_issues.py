import matplotlib.pyplot as plt
import numpy as np

from new_optimization import *

# Create a few trees from files
# All trees were generated with Erik's simulator and scaled by my script
with open("eric-sim/b5/tree02_rescaled.txt") as f:
    t_b3_normal = TimeTree(f.readline())
with open("eric-sim/b5/tree01_rescaled.txt") as f:
    t_b3_broken = TimeTree(f.readline())

# Gridsearch
# For some trees, the gridsearch reveals a hard edge to the valid values.
# This is not present for other trees.
def plot_gridsearch(t, a_bounds, b_bounds, title):
    a_min, a_max = a_bounds
    b_min, b_max = b_bounds
    a_range = np.linspace(a_min, a_max, 100)
    b_range = np.linspace(b_min, b_max, 100)

    values = simple_gridsearch(t, a_range, b_range, 2*(365/1.5))

    fig, ax = plt.subplots()
    cax = ax.imshow(values, origin="lower")
    cbar = fig.colorbar(cax)

    ax.set_title(title)
    ax.set_xlabel("Beta")
    ax.set_ylabel("Alpha")
    ax.set_xticks((0, 20, 40, 60, 80, 100)) # Set to known values so it's easy to relabel
    ax.set_yticks((0, 20, 40, 60, 80, 100))
    ax.set_xticklabels(np.round(np.linspace(b_min, b_max, 6), 1))
    ax.set_yticklabels(np.round(np.linspace(a_min, a_max, 6), 1))
    plt.show()

#plot_gridsearch(t_b3_normal, (0, 10), (1, 10), "Expected behavior")

# I think the warning I implemented that the end of the tree passes
# over the infection time helps solve this issue.
plot_gridsearch(t_b3_broken, (0, 10), (1, 10), "Confusing behavior")

