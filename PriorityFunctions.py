import numpy as np
import random 

def weighted_choice(objects, weights):
    """ 
    returns randomly an element from the sequence of 'objects', 
        the likelihood of the objects is weighted according 
        to the sequence of 'weights', i.e. percentages.
        code from https://www.python-course.eu/weighted_choice_and_sample.php
    """

    weights = np.array(weights, dtype=np.float64)
    sum_of_weights = weights.sum()
    # standardization:
    np.multiply(weights, 1 / sum_of_weights, weights)
    weights = weights.cumsum()
    x = random.random()
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]

def weighted_sample(population, weights, k, epsilon = 1e-50):
    """ 
    This function draws a random sample (without repeats) 
    of length k     from the sequence 'population' according 
    to the list of weights

    code from https://www.python-course.eu/weighted_choice_and_sample.php
    """
    sample = set()
    population = list(population)
    weights += epsilon
    weights = list(weights) 
    while len(sample) < k:
        choice = weighted_choice(population, weights)
        sample.add(choice)
        index = population.index(choice)
        weights.pop(index)
        population.remove(choice)
        weights = [ x / sum(weights) for x in weights]
    return list(sample)

def priority(n_pop, X, dt_X, Y, dt_Y, function, value = 0.1):
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
    elif(function == "ds_norm"):
        X = ds_norm(X, dt_X)
    elif(function == "RI"):
        X = RI(Y, dt_Y)
    return X

def fix_random(n_pop, value = 0.1):
    """
    define fix values for random resource allocation

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
      an array of fixed values per solution for resource allocation
    """
    p = np.full(n_pop, value)
    # p /= p.sum() # scaling values to avoid problems with numpy choice

    return p

def ds_norm(X, dt_X, epsilon = 1e-50): 
    """
    define values for resource allocation based on the euclidian distance

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
      an array of fixed values per solution for resource allocation
    """
    p = np.linalg.norm(X - dt_X, axis = 1, ord = 2)
    p = (p - min(p)) / ((max(p) - min(p) + epsilon))
    return p

def RI(bigZ, dt_bigZ, epsilon = 1e-50): 
    """
    define values for resource allocation based on the euclidian distance

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
      an array of fixed values per solution for resource allocation
    """
    p = (dt_bigZ - bigZ) / ( dt_bigZ+ epsilon)
    if max(p) == 0:
        p = np.zeros(len(p)) + 1
    else:
        p = (p - min(p)) / ((max(p) - min(p) + epsilon))
    return p


def get_mask(n_pop, number_solutions, priority_values, idx_boundary):
    """
    Generate a mask of which solutions of a population will receive resources

    parameter
    ----------
    n_pop: int
      population size
    number_solutions: int
      number of solutions to receive resources
    priority_values: 1D-Array float
      an array of values per solution for resource allocation
    idx_boundary: 1D-Array int
      an array of where the boundary weight vectors are

    return
    ----------
    1D-Array
      a mask for selecting solutions for resource allocation (1 means that the solution will get resources; otherwise, 0)
    """
 
    no_boundaries = np.arange(0, n_pop) 
    no_boundaries = np.delete(no_boundaries, idx_boundary)
    priority_values = np.delete(priority_values, idx_boundary)

    idx_select_solutions = weighted_sample(no_boundaries, priority_values, number_solutions)
    mask_priority = np.zeros(n_pop)
    mask_priority[idx_select_solutions] = 1

    for e in idx_boundary:
        mask_priority[int(e)] = 1    

    return mask_priority


