import numpy as np
import math

def SCH(x):
    f1 = x[0] ** 2
    f2 = (x[0] - 2) ** 2

    return np.array([f1, f2])

def UF1(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x) 

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
        
        if j % 2 == 1:
            sum1 += yj**2
            count1 += 1
        else:
            sum2 += yj**2
            count2 += 1
            
    f1 = x[0] + 2.0 * sum1 / count1
    print(x[0])
    print(math.sqrt(x[0]))
    print(2.0 * sum2 / count2)
    f2 = 1.0 - math.sqrt(x[0]) + 2.0 * sum2 / count2

    return np.array([f1, f2])

def UF2(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x) 

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    
    for j in range(2, nvars+1):
        if j % 2 == 1:
            yj = x[j-1] - 0.3*x[0]*(x[0] * math.cos(24.0*math.pi*x[0] + 4.0*j*math.pi/nvars) + 2.0)*math.cos(6.0*math.pi*x[0] + j*math.pi/nvars)
            sum1 += yj**2
            count1 += 1
        else:
            yj = x[j-1] - 0.3*x[0]*(x[0] * math.cos(24.0*math.pi*x[0] + 4.0*j*math.pi/nvars) + 2.0)*math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
            sum2 += yj**2
            count2 += 1
            
    f1 = x[0] + 2.0 * sum1 / count1
    f2 = 1.0 - math.sqrt(x[0]) + 2.0 * sum2 / count2

    return np.array([f1, f2])

def UF3(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x) 

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    prod1 = 1.0
    prod2 = 1.0
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.pow(x[0], 0.5*(1.0 + 3.0*(j - 2.0) / (nvars - 2.0)))
        pj = math.cos(20.0*yj*math.pi/math.sqrt(j))
        
        if j % 2 == 1:
            sum1 += yj**2
            prod1 *= pj
            count1 += 1
        else:
            sum2 += yj**2
            prod2 *= pj
            count2 += 1
            
    f1 = x[0] + 2.0 * (4.0*sum1 - 2.0*prod1 + 2.0) / count1
    f2 = 1.0 - math.sqrt(x[0]) + 2.0 * (4.0*sum2 - 2.0*prod2 + 2.0) / count2

    return np.array([f1, f2])


def UF4(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x) 

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
        hj = abs(yj) / (1.0 + math.exp(2.0*abs(yj)))
        
        if j % 2 == 1:
            sum1 += hj
            count1 += 1
        else:
            sum2 += hj
            count2 += 1
            
    f1 = x[0] + 2.0*sum1/count1
    f2 = 1.0 - x[0]**2 + 2.0*sum2/count2

    return np.array([f1, f2])

def UF5(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x) 

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    N = 10.0
    E = 0.1
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
        hj = 2.0*yj**2 - math.cos(4.0*math.pi*yj) + 1.0
        
        if j % 2 == 1:
            sum1 += hj
            count1 += 1
        else:
            sum2 += hj
            count2 += 1
    
    hj = (0.5/N + E) * abs(math.sin(2.0*N*math.pi*x[0]))
    f1 = x[0] + hj + 2.0*sum1/count1
    f2 = 1.0 - x[0] + hj + 2.0*sum2/count2

    return np.array([f1, f2])


def UF6(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x)  

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    N = 10.0
    E = 0.1
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
        hj = 2.0*yj**2 - math.cos(4.0*math.pi*yj) + 1.0
        
        if j % 2 == 1:
            sum1 += hj
            count1 += 1
        else:
            sum2 += hj
            count2 += 1
    
    hj = (0.5/N + E) * abs(math.sin(2.0*N*math.pi*x[0]))
    f1 = x[0] + hj + 2.0*sum1/count1
    f2 = 1.0 - x[0] + hj + 2.0*sum2/count2
    
    return np.array([f1, f2])

def UF6(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x)  

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    prod1 = 1.0
    prod2 = 1.0
    N = 2.0
    E = 0.1
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
        pj = math.cos(20.0*yj*math.pi/math.sqrt(j))
        
        if j % 2 == 1:
            sum1 += yj**2
            prod1 *= pj
            count1 += 1
        else:
            sum2 += yj**2
            prod2 *= pj
            count2 += 1
    
    hj = 2.0 * (0.5/N + E) * math.sin(2.0*N*math.pi*x[0])
    hj = max(hj, 0.0)
    
    f1 = x[0] + hj + 2.0*(4.0*sum1 - 2.0*prod1 + 2.0)/count1
    f2 = 1.0 - x[0] + hj + 2.0*(4.0*sum2 - 2.0*prod2 + 2.0)/count2
    
    return np.array([f1, f2])

def UF7(x):
    """
    adapted from
    https://github.com/Project-Platypus/Platypus/blob/master/platypus/problems.py
    """

    nvars = len(x)

    count1 = 0
    count2 = 0
    sum1 = 0.0
    sum2 = 0.0
    
    for j in range(2, nvars+1):
        yj = x[j-1] - math.sin(6.0*math.pi*x[0] + j*math.pi/nvars)
        
        if j % 2 == 1:
            sum1 += yj**2
            count1 += 1
        else:
            sum2 += yj**2
            count2 += 1
    
    yj = math.pow(x[0], 0.2)
    f1 = yj + 2.0*sum1/count1
    f2 = 1.0 - yj + 2.0*sum2/count2
    
    return np.array([f1, f2])

def UF8(x):
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
    
    f1 = math.cos(0.5*math.pi*x[0]) * math.cos(0.5*math.pi*x[1]) + 2.0*sum1/count1
    f2 = math.cos(0.5*math.pi*x[0]) * math.sin(0.5*math.pi*x[1]) + 2.0*sum2/count2
    f3 = math.sin(0.5*math.pi*x[0]) + 2.0*sum3/count3
    
    return np.array([f1, f2, f3])

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


def UF10(x):
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
    
    for j in range(3, self.nvars+1):
        yj = x[j-1] - 2.0*x[1]*math.sin(2.0*math.pi*x[0] + j*math.pi/self.nvars)
        hj = 4.0*yj**2 - math.cos(8.0*math.pi*yj) + 1.0
        
        if j % 3 == 1:
            sum1 += hj
            count1 += 1
        elif j % 3 == 2:
            sum2 += hj
            count2 += 1
        else:
            sum3 += hj
            count3 += 1
    
    f1 = math.cos(0.5*math.pi*x[0])*math.cos(0.5*math.pi*x[1]) + 2.0*sum1/count1
    f2 = math.cos(0.5*math.pi*x[0])*math.sin(0.5*math.pi*x[1]) + 2.0*sum2/count2
    f3 = math.sin(0.5*math.pi*x[0]) + 2.0*sum3/count3
    
    return np.array([f1, f2, f3])


