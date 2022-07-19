from scipy.optimize import minimize
from tree_likelihood import tree_likelihood
from time_tree import TimeTree
from population_models import *
import random


treefile = open("linear-latest.tre")
t = TimeTree(treefile.readline())
treefile.close()

def fun(params): # TODO should be a lambda going forward but I can hardcode for now to get prints
    N0, b = params
    res = -tree_likelihood(t, lin_population, lin_probability, {"N0": N0, "b": b})
    print(params, res)
    return res

def optimize_linear(tree, x0):
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

if __name__ == "__main__":
    #starts = [(1, 1), (300, 300), (1000, 1000), (100, 1), (1, 100), (1100, 1100)]
    starts = random_startpoint_list(100, 1100, 2500)
    different_cold_starts(t, starts)

