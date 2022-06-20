#!/usr/bin/env python3

import math
import random
from ete3 import TreeNode
from coalescence_time import time_until_coalescence as c_time

def generate_nodes(k):
    return [TreeNode(name=str(i)) for i in range(k)] 

def step(N, k, nodes):
    time_next = c_time(N, k)
    # then combine the nodes with that time together?

def run_constant(N, k, timesteps):
    for t in range(timesteps):
        step(N, k)

def run_linear(alpha, beta, k, timesteps):
    for t in range(timesteps):
        N = alpha + (beta * t)
        step(N, k)

def run_exponential(n0, r, k, timesteps):
    for t in range(timesteps):
        N = n0 * math.pow(math.e, r * t)
        step(N, k)
