#!/usr/bin/env python3

import math
import random
import numpy as np
from plot_coalescence_time import probability_overlay, side_by_side

#
# Effective population size over time for constant, linear, and exponential models
#

def con_population(params, T):
    """
    Return a constant population. Params and T are not necessary, they just exist so it is easier
    to swap constant population with linear and exponential.

    Parameters:
      params (dict): Description of population size. Kept in a dictionary
      to match linear and exponential inputs.
        N (float): Population size
      T (float): Time since infection

    Returns:
      population (float): Effective population size at specified time
    """
    if "N" not in params:
        raise Exception(f"Check params, given {params}")
    return params["N"]

def lin_population(params, t): # {"a": 1, "b": 3, "Dinf": 200} new param vector, Dinf is provided additionally (not from tree) 
    """
    Return the effective population T time units after infection
    using a linear model.

    Parameters:
      params (dict): Parameters describing the population dynamics
        a (float): Population at the time of infection
        b (float): Linear rate of population change (per generation)
      t (float): 

    Returns:
      population (float): Effective population size at specified time
    """
    if "a" not in params:
        raise Exception(f"Check params, given {params}")
    a = params["a"]
    b = params["b"]
    inf_time = params["inf_time"]
    return a + (inf_time-t)*b

#
# Probability of a coalescence event occuring for each population model
#

def con_probability(params, z):
    """
    The proabaility of a coalescence at time z with constant population

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        N (float): Population size
      z (float): Time until the coalescence event (from the current point in the tree)

    Returns:
      probability (float): Probability of a coalescence event happening
      exactly at the specified time
    """
    k = params["k"]
    N = params["N"]
    lmd = k*(k - 1)/(2*N)
    return lmd * math.exp(-lmd*z)

def lin_probability(params, now, z):
    """
    The proabaility of a coalescence at time z with constant population

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        a (float): Population at time of infection
        b (float): Linear rate of effective population increase (per generation)
        inf_time (float): TODO WHAT IS THIS
      z (float): Time until the coalescence event (forward from T)

    Returns:
      probability (float): Probability of a coalescence event happening
      exactly at the specified time
    """
    k = params["k"]
    b = params["b"]
    return (k*(k-1)/(2*(pop_T - b*z))) * (pop_T / (pop_T - b*z))**(-k*(k-1)/(2*b))

