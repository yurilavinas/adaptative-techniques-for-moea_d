import numpy as np

def init_pop(n_pop, n_var, xl, xu):
    """
    Initialize a population with uniform distribution

    parameter
    ----------
    n_pop: int
      population size
    n_var: int
      number of decision variables
    xl, xu: float
      lower and upper boundary of decision variables

    return
    ----------
    2D-Array
      a matrix showing the population where each row is an individual
    """
    X = np.random.uniform(xl, xu, (n_pop, n_var))
    return X

def eval_pop(X, problem, problem_name):
    """
    Evaluate a population with the given objectives
    parameter
    -----------
    X: 2D-Array
      population matrix where each row is an individual
    problem: method
      objective function which returns fitness values of a input individual
    
    return
    -----------
    2D-Array
      fitness value matrix where each row is the fitness values of an individual
    """
    # F = []]
    benchmark_name = ''.join(i for i in problem_name if not i.isdigit())

    if (benchmark_name == "dtlz" or benchmark_name == "DTLZ"):
        F = problem(X)
    elif (benchmark_name == "uf" or benchmark_name == "UF"):
        F = []
        for x in X:
            F.append(problem(x))
    
    return np.array(F)