import numpy as np

def fixed_priority_values(n_pop, function, value = 0.1):
    """
    Initialize a population with uniform distribution

    parameter
    ----------
    n_pop: int
      population size
    (priority) function: 
      name of the function used for resource allocation
    

    return
    ----------
    1D-Array
      an array of fixed values for resource allocation
    """
    if(function == "fix_random"):
        X = fix_random(n_pop, value)
    return X

def fix_random(n_pop, value = 0.1):
    """
    Initialize a population with uniform distribution

    parameter
    ----------
    n_pop: int
      population size
    (priority) function: 
      name of the function used for resource allocation
    value: float
      fix value for selecting part of the population
    

    return
    ----------
    1D-Array
      an array of fixed values for resource allocation
    """
    X = np.full(n_pop, value)

    return X