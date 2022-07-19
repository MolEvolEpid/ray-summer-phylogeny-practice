from scipy.optimize import minimize
from tree_likelihood import tree_likelihood
from time_tree import TimeTree
from population_models import *


treefile = open("linear-latest.tre")
t = TimeTree(treefile.readline())
treefile.close()

def fun(params):
    N0, b = params
    res = -tree_likelihood(t, lin_population, lin_probability, {"N0": N0, "b": b})
    print(params, res)
    return res

def optimize_linear(tree):
    res = minimize(fun, (100, 1), method="Nelder-Mead")
    return res

if __name__ == "__main__":
    best_params = optimize_linear(t)
    print(best_params)

# Okay, current issue is this:
#     If I use BFGS, I get a failed optimization due to "precision loss"
#     If I use Nelder-Mead with no special params, I get
#     N0 = 1.874 and b = 1.875. How can that get past the filter?
#     
#     If I run tree_likelihood with those params, I get that the 
#     log likelihood is 61.68. Does that mean something? Is it wrong?
#     I don't get what it's doing wrong here. Shouldn't both of them 
#     be significantly higher than it predicts?
