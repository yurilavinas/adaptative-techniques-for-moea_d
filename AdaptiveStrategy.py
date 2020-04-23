import numpy as np
from Mutation import levy, fix_bound

def evolve(P, P_parent, P_offspring, I, I_parent, I_offspring, B,
           c_gen, n_step, betal, betau, alpha_for_param, beta_for_param):
    """
    Evolve parameters

    parameter
    ----------
    P: 1D-Array
      values of parameters of each individual in the current population
    P_parent: 1D-Array
      saved values of parameters in parameter parent population
    P_offspring: 1D-Array
      saved values of parameters in parameter offspring population
    I: 1D-Array
      indicator values of parameters of each individual in the current population
    I_parent: 1D-Array
      saved indicator values of parameters in parameter parent population
    I_offspring: 1D-Array
      saved indicator values of parameters in parameter offspring population
    B: list
      list of neighbor index information
    n_step: int
      numbers of generations to update parameters
    betal: float
      lower bound of beta, usually 0.1
    betau: float
      upper bound of beta, usually 1.9
    alpha_for_param: float
      scaling factor of levy flight used to update parameters
    beta_for_param: float
      stability factor of levy flight used to update parameters

    return
    ----------
    P: 1D-Array
      values of parameters of each individual in the current population
    P_parent: 1D-Array
      saved values of parameters in parameter parent population
    P_offspring: 1D-Array
      saved values of parameters in parameter offspring population
    I: 1D-Array
      indicator values of parameters of each individual in the current population
    I_parent: 1D-Array
      saved indicator values of parameters in parameter parent population
    I_offspring: 1D-Array
      saved indicator values of parameters in parameter offspring population
    """
    n_pop = len(P)
    if c_gen % (2 * n_step) == n_step:                                      # generate offspring parameters by levy flight
        P_parent = P[:]
        I_parent = I[:]
        P = fix_bound( P + levy(alpha_for_param, beta_for_param, n_pop),
                       betal, betau)
        I = I * 0

    if c_gen % (2 * n_step) == 0:                                           # select better parameter in a parent-offspring paremeter pair
        P_offspring = P[:]
        I_offspring = I[:]
        for i in np.random.permutation(n_pop):
            j = np.random.choice(B[i])
            pi_ = P_offspring[i]
            Ii_ = I_offspring[i]
            pj = P_parent[j]
            Ij = I_parent[j]
            if Ii_ > Ij:
                P[i] = pi_
            else:
                P[i] = pj
    return P, P_parent, P_offspring, I, I_parent, I_offspring