from numpy import exp
from scipy.stats import expon

def validate_params(params, expected_params):
    """
    Raise an exception if any of the expected_params are not a key in params.

    Parameters:
      params (dict): Dictionary containing any named parameters.
      expected (list): List containing the keys of each expected param.

    Returns:
      Nothing, but may throw an Exception.
    """
    if any(map(lambda s: s not in params, expected_params)):
        raise Exception(f"Please check params. Expected {expected_params}, given {list(params.keys())}")
    return [params[k] for k in expected_params]

def con_population(params, t):
    """
    Return a constant population. Params and T are not necessary, they just exist so it is easier
    to swap constant population with linear and exponential.

    Parameters:
      params (dict): Description of population size. Kept in a dictionary
      to match linear and exponential inputs.
        N (float): Population size
        I (float): Time of infection
      t (float): Time since infection

    Returns:
      population (float): Effective population size at specified time
    """
    N, I = validate_params(params, ['N', 'I'])
    return N

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
    a, b, I = validate_params(params, ['a', 'b', 'I'])
    return a + (I-t)*b

def con_probability(params, start, z):
    """
    The proabaility of a coalescence at time z with constant population

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        N (float): Population size
        I (float): Time of infection
      start (float): Start of the window for the coalescence event (where the previous event ended)
      z (float): Time until the coalescence event (from start)

    Returns:
      probability (float): Probability of a coalescence event happening
      exactly at the specified time
    """
    k, N, I = validate_params(params, ['k', 'N', 'I'])

    lmd = k*(k - 1)/(2*N)
    return lmd * exp(-lmd*z)

def lin_probability(params, start, z):
    """
    The proabaility of a coalescence at time z with linear population

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        a (float): Population at time of infection
        b (float): Linear rate of effective population increase (per generation)
        I (float): Time of infection
      start (float): Start of the window for the coalescence event (where the previous event ended)
      z (float): Time until the coalescence event (from start)

    Returns:
      probability (float): Probability of a coalescence event happening
      exactly at the specified time
    """
    k, a, b, I = validate_params(params, ['k', 'a', 'b', 'I'])

    lmd = k*(k-1)/2
    start_pop = a + (b*(I-start-z))
    end_pop = a + (b * (I-start))
    return lmd * (1 / start_pop) * (end_pop / start_pop) ** (-lmd / b)

def con_nocoal_probability(params, start, z):
    """
    The probability of no coalescence happening from start for z time
    with constant population.

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        N (float): Population size
        I (float): Time of infection
      start (float): Start of the window for the coalescence event (where the previous event ended)
      z (float): Time until the coalescence event (from start)

    Returns:
      probability (float): Probability of no coalescence happening across the
      specified time.
    """
    k, N, I = validate_params(params, ['k', 'N', 'I'])

    scale = (2*N) / (k*(k-1))
    dist = expon(scale=scale)

    return 1 - dist.cdf(z)

def lin_nocoal_probability(params, start, z):
    """
    The probability of no coalescence happening from start for z time
    with linear population.

    Parameters:
      params (dict): Parameters specifying the state of the tree at a certain point in time.
        k (int): Number of sequences
        a (float): Population at time of infection
        b (float): Linear rate of effective population increase (per generation)
        I (float): Time of infection
      start (float): Start of the window for the coalescence event (where the previous event ended)
      z (float): Time until the coalescence event (from start)

    Returns:
      probability (float): Probability of no coalescence happening across the
      specified time.
    """
    k, a, b, I = validate_params(params, ['k', 'a', 'b', 'I'])

    lmb = k*(k-1) / (2*b)
    start_pop = a + (b*(I-start-z))
    end_pop = a + (b * (I-start))

    return (end_pop ** -lmb) * (start_pop ** lmb)
