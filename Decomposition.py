import numpy as np

def agg_value(agg_function, y, w, ref_point):

    if agg_function == "wt":
        scalar_value = tchebycheff(y, w, ref_point)
    
    return scalar_value


def tchebycheff(y, w, ref_point):
    """
    Compute the Tchebycheff cost

    parameter
    ----------
    y: 1D-Array
      fitness values of an individual
    w: 1D-Array
      weight vector
    ref_point: reference point

    return
    ----------
    float
      Tchebycheff cost value
    """
    return np.max( w * np.abs(y - ref_point) )