import numpy as np

def fixed_priority_values(n_pop, value = 0.1):
    """
    Initialize a population with uniform distribution

    parameter
    ----------
    n_pop: int
      population size
    

    return
    ----------
    1D-Array
      an array of fixed values for resource allocation
    """
    X = np.full(n_pop, value)
    return X