#!/usr/bin/env python3

import random
import numpy as np
import matplotlib.pyplot as plt

def time_until_coalescence(N, k):
    """
    Run a neutral coalescent model until a coalescence occurs,
    returning the total number of generations.
    """
    nodes = range(k) # ensure that all are unique in the first step (time 1)
    time = 0
    while len(nodes) == k: # TODO: Do I want >= k to be safe or is it fine?
        time += 1
        nodes = set([random.randint(1, N-1) for i in nodes])
    return time

def batch_sim(N, k, iterations):
    """
    Run many coalescence simulations and concatenate the time that each
    simulation took, keeping N and k constant.
    """
    return [time_until_coalescence(N, k) for i in range(iterations)]

def plot_coalescence_time(N, k, iterations):
    """
    Plot a histogram
    """
    times = batch_sim(N, k, iterations)
    plt.hist(times)
    plt.show()

if __name__ == "__main__":
    plot_coalescence_time(100, 2, 1000)
