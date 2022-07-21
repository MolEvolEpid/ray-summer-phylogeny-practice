#!/usr/bin/env python3

from math import exp

def check_params_exist(params, expected_params):
    """
    Raise an exception if any of the expected_params are not in params.

    Parameters:
      params (dict): Dictionary containing any named parameters.
      expected (list): List containing the keys of each expected param.

    Returns:
      Nothing, but may throw an Exception.
    """
    if any(map(lambda s: s not in params, expected_params)):
        raise Exception(f"Please check params. Expected {expected_params}, given {list(params.keys())}")

def con_population(params, t):
    """
    Return a constant population. Params and T are not necessary, they just exist so it is easier
    to swap constant population with linear and exponential.

    Parameters:
      params (dict): Description of population size. Kept in a dictionary
      to match linear and exponential inputs.
        N (float): Population size
      t (float): Time since infection

    Returns:
      population (float): Effective population size at specified time
    """
    check_params_exist(params, ['N'])
    return params["N"]

def lin_population(params, t):
    """
    Return the effective population T time units after infection
    using a linear model.

    Parameters:
      params (dict): Parameters describing the population dynamics
        a (float): Population at the time of infection
        b (float): Linear rate of population change (per generation)
        I (float): Time of infection
      t (float): Time since infection

    Returns:
      population (float): Effective population size at specified time
    """
    check_params_exist(params, ['a', 'b', 'I'])
    a = params["a"]
    b = params["b"]
    I = params["I"]
    return a + (I-t)*b


# TODO Come up with a better way to talk about the `start` value. Maybe rename it too.
def con_probability(params, start, z):
    """
    The proabaility of a coalescence at time z with constant population

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        N (float): Population size
      start (float): Position of the start of the current tree segment
      z (float): Time until the coalescence event (from start)

    Returns:
      probability (float): Probability of a coalescence event happening
      exactly at the specified time
    """
    check_params_exist(params, ['k', 'N'])
    k = params["k"]
    N = params["N"]
    lmd = k*(k - 1)/(2*N)
    return lmd * np.exp(-lmd*z)

def lin_probability(params, start, z):
    """
    The proabaility of a coalescence at time z with linear population

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        a (float): Population at time of infection
        b (float): Linear rate of effective population increase (per generation)
        I (float): Time of infection
      start (float): Position of the start of the current tree segment 
      z (float): Time until the coalescence event (from start)

    Returns:
      probability (float): Probability of a coalescence event happening
      exactly at the specified time
    """
    check_params_exist(params, ['k', 'a', 'b', 'I'])
    k = params["k"]
    a = params["a"]
    b = params["b"]
    I = params["I"]
    return (k*(k-1) / 2) * (1 / (a+(b*(I-start-z)))) * ((a+(b*(I-start))) / (a+(b*(I-start-z)))) ** (-k*(k-1)/(2*b))

