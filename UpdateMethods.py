import numpy as np

def update(update_name, tch_, tchk, nc, X, Y, I):

	if update_name == 'restricted_update':
		nc, X, Y, I = restricted_update(tch_, tchk, X, Y, I)
	return nc, X, Y, I


def restricted_update(tch_, tchk, nc, X, Y, I):
	nr = params['nr']                                                               # set maximum update counts for one offspring
	if nc < nr:
		if tch_ <= tchk:                                                # compare tchebycheff cost of offspring and parent
			X[k] = xi_                                                  # update parent
			Y[k] = yi_
			nc += 1                                                     # cumulate the counter
			I[i] += np.abs(tch_ - tchk) / (tchk + 1e-50)                # cumulate the indicator
	

	return nc, X, Y, I
