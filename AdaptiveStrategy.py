import numpy as np
from Mutation import levy, fix_bound

def evolve(P, P_parent, P_offspring, I, I_parent, I_offspring, B,
           c_gen, n_step, betal, betau, alpha_for_param, beta_for_param):
    """
    Evolve parameters

    parameter
    ----------
    !TODO write documentation
    return
    ----------
    !TODO write documentation
    """
    n_pop = len(P)
    if c_gen % (2 * n_step) == n_step:
        P_parent = P[:]
        I_parent = I[:]
        P = fix_bound( P + levy(alpha_for_param, beta_for_param, n_pop), betal, betau)
        I = I * 0

    if c_gen % (2 * n_step) == 0:
        P_offspring = P[:]
        I_offspring = I[:]
        for i in np.random.permutation(n_pop):
            j = int(np.random.choice(B[i]))
            pi_ = P_offspring[i]
            Ii_ = I_offspring[i]
            pj = P_parent[j]
            Ij = I_parent[j]
            if Ii_ > Ij:
                P[i] = pi_
            else:
                P[i] = pj
    return P, P_parent, P_offspring, I, I_parent, I_offspring