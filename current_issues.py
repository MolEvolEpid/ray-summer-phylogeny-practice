import matplotlib.pyplot as plt
import numpy as np

from new_optimization import *

# Create a few trees from files
# All trees were generated with Erik's simulator and scaled by my script
with open("eric-sim/b3/tree02_rescaled.txt") as f:
    t_b3 = TimeTree(f.readline())
with open("eric-sim/b5/tree01_rescaled.txt") as f:
    t_b5 = TimeTree(f.readline())
with open("eric-sim/b10/tree01_rescaled.txt") as f:
    t_b10 = TimeTree(f.readline())

# Range to search a and b
a_min, a_max = 0, 5
b_min, b_max = 1, 5
a_range = np.linspace(a_min, a_max, 100)
b_range = np.linspace(b_min, b_max, 100)

# Plot likelihood for each of those points
# I can't get the axes to show the right values but that's neither here nor there
fig, ax = plt.subplots()

values = simple_gridsearch(t_b3, a_range, b_range, 2 * (365/1.5))

cax = ax.imshow(values, origin="lower")
ax.set_xlabel("Values of beta")
ax.set_ylabel("Values of alpha")
ax.set_xticks((0, 100))
ax.set_yticks((0, 100))
ax.set_xticklabels((b_min, b_max))
ax.set_yticklabels((a_min, a_max))
cbar = fig.colorbar(cax)

plt.show()
