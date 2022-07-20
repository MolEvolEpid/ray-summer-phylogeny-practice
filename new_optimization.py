from scipy.optimize import minimize
from tree_likelihood import tree_likelihood
from time_tree import TimeTree
from population_models import *
import random

def optimize_linear(tree, x0):
    fun = lambda x: -tree_likelihood(tree, lin_population, lin_probability, {"N0": N0, "b": b})
    res = minimize(fun, x0, method="Nelder-Mead")
    return res

def optimize_worse(tree, N0):
    fm = lambda x: -tree_likelihood(tree, lin_population, lin_probability, {"N0": x, "b": 1095})
    res = minimize(fm, N0, method="BFGS")
    return res

def different_cold_starts(tree, starts):
    for x0 in starts:
        res = optimize_linear(tree, x0)
        print(x0, res.x, res.success)
    
def random_startpoint_list(n, low, high):
    return [(random.randint(low, high), random.randint(low, high)) for _ in range(n)]

def simple_gridsearch(tree, N0_range, b_range):
    values = np.zeros((len(N0_range), len(b_range)))
    # b along rows, N0 down columns
    for i, b in enumerate(b_range):
        for j, N0 in enumerate(N0_range):
            val = tree_likelihood(tree, lin_population, lin_probability, {"N0": N0, "b": b})
            values[j][i] = val
    return values

import matplotlib.pyplot as plt

if __name__ == "__main__":
    treefile = open("linear-latest.tre")
    t = TimeTree(treefile.readline())
    treefile.close()

    #starts = [(1, 1), (300, 300), (1000, 1000), (100, 1), (1, 100), (1100, 1100)]
    #starts = random_startpoint_list(100, 1100, 2500)
    #different_cold_starts(t, starts)

    min_N0, max_N0 = (1, 5)
    min_b, max_b = (1, 5)
    N0_range = np.linspace(min_N0, max_N0, 100)
    b_range = np.linspace(min_b, max_b, 100)

    values = simple_gridsearch(t, N0_range, b_range)
    print(values)

    plt.imshow(values, origin="lower") # Flip vertically to make (0, 0) in bottom left corner
    plt.xlabel("Values of N0")
    plt.ylabel("Values of b")
    plt.colorbar()

    """
    # It probably isn't actually this hard to make the axes line up
    num_x_ticks = len(ax.get_xticklabels())
    num_y_ticks = len(ax.get_yticklabels())
    x_ticks = np.arange(min_N0, max_N0+min_N0, (max_N0 - min_N0) / num_x_ticks)
    y_ticks = np.arange(min_b, max_b+min_b, (max_b - min_b) / num_y_ticks)
    ax.set_xticklabels(x_ticks)
    ax.set_yticklabels(y_ticks)
    """

    plt.show()

