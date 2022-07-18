#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from population_models import *
from tree_likelihood import *

def plot():
    x = np.linspace(0, 10, 1000)

    con_params = {"N0": 2000, "k": 30}
    lin_params = {"N0": 4000, "k": 30, "b": 400}

    con_pop = [con_population(con_params, t) for t in x]
    lin_pop = [lin_population(lin_params, t) for t in x]

    con_prob = [con_probability(con_params, z) for z in x]
    lin_prob = [lin_probability(lin_params, z) for z in x]

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(-x, con_pop, color="#1C5D99", linewidth=3)
    ax1.plot(-x, lin_pop, color="#639FAB", linewidth=3)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel("Time (t)")
    ax1.set_ylabel("Population size (N)")

    ax2.plot(x, con_prob, color="#1C5D99", linewidth=3)
    ax2.plot(x, lin_prob, color="#639FAB", linewidth=3)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xlabel("Time until coalescence (z)")
    ax2.set_ylabel("Coalescence PDF (l)")

    plt.show()

if __name__ == "__main__":
    plot()
