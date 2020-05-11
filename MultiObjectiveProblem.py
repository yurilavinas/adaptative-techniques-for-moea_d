import numpy as np
import math

def SCH(x):
    f1 = x[0] ** 2
    f2 = (x[0] - 2) ** 2
    return np.array([f1, f2])

def UF9(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """
    
    nvars = len(x)

    count1 = 0
    count2 = 0
    count3 = 0
    sum1 = 0.0
    sum2 = 0.0
    sum3 = 0.0
    E = 0.1

    for j in range(3, nvars+1):
        yj = x[j-1] - 2.0*x[1]*math.sin(2.0*math.pi*x[0] + j*math.pi/nvars)
        
        if j % 3 == 1:
            sum1 += yj**2
            count1 += 1
        elif j % 3 == 2:
            sum2 += yj**2
            count2 += 1
        else:
            sum3 += yj**2
            count3 += 1
            
    yj = (1.0 + E) * (1.0 - 4.0*(2.0*x[0] - 1.0)**2)
    yj = max(yj, 0.0)
    f1 = 0.5*(yj + 2.0*x[0])*x[1] + 2.0*sum1/count1
    f2 = 0.5*(yj - 2.0*x[0] + 2.0)*x[1] + 2.0*sum2/count2
    f3 = 1.0 - x[1] + 2.0*sum3/count3

    return np.array([f1, f2, f3])