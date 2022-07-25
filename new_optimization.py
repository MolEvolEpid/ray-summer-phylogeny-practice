from scipy.optimize import minimize
from tree_likelihood import tree_likelihood
from time_tree import TimeTree
from population_models import *
import numpy as np

def optimize_b(tree, a, b0, I):
    fun = lambda x: -tree_likelihood(tree, lin_population, lin_probability, {"a": a, "b": b0, "I": I})
    res = minimize(fun, b0, method="Nelder-Mead")
    return res

def optimize_a_b(tree, p0, I):
    fun = lambda x: -tree_likelihood(tree, lin_population, lin_probability, {"a": x[0], "b": x[1], "I": I})
    res = minimize(fun, p0, method="Nelder-Mead")
    return res

def simple_gridsearch(tree, a_range, b_range, I):
    values = np.zeros((len(a_range), len(b_range)))
    # b along rows, N0 down columns
    for i, b in enumerate(b_range):
        for j, N0 in enumerate(a_range):
            val = tree_likelihood(tree, lin_population, lin_probability, {"a": N0, "b": b, "I": I})
            values[j][i] = val
    return values

