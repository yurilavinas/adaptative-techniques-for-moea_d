import numpy as np

def select_solutions(i, X, Y, B, params):
	
	n_pop = len(B)

	delta = params['delta']                                             # set probability to select parent from neighbor
	
	if np.random.random() < delta:                                      # determine selection pool by probability
	    pool = B[i, :]                                                  # neighbor as the pool
	else:
		pool = np.arange(n_pop)                                         # population as the pool

	j = int(np.random.choice(pool))                                          # select a random individual from pool

	xj, yj = X[j, :], Y[j, :]                                           # select the xj (solution values), and yj (function value) of the current solution (j)

	return (j, xj, yj, pool) 