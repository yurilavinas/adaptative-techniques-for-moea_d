import os
import argparse
import yaml
import random
import numpy as np
from scipy.special import comb
import itertools

from Factory import set_problem
from WeightVector import das_dennis, determine_neighbor
from Population import init_pop, eval_pop, eval_all_solutions
from ReferencePoint import init_ref_point, update_ref_point
from Mutation import lf_mutation, poly_mutation, fix_bound, de_mutation
from Decomposition import tchebycheff
from PriorityFunctions import priority, get_mask


###################
#  MOP to solve   #
###################
from pymoo.factory import get_problem
from platypus.problems import UF9
###################
# parse arguments #
###################

parser = argparse.ArgumentParser()
parser.add_argument('params', type=argparse.FileType('r'))
parser.add_argument('seed', type=int)
args = parser.parse_args()

##################
# set parameters #
##################

params = yaml.safe_load(args.params)                                # read config file

random.seed(args.seed)
np.random.seed(args.seed)

output = params['output']                                           # set output of record in this run

n_obj = params['n_obj']                                             # set number of objectives
n_var = params['n_var']                                             # set number of variables
xl = params['xl']                                                   # set boundary of variables
xu = params['xu']

prob_name = params['prob_name']
if (prob_name == "dtlz7"): 
    problem = get_problem(prob_name)							# set optimization problem
    problem.n_var = n_var
    problem.n_obj = n_obj
    problem.xu = np.repeat(xu, n_var)
    problem.xl = np.repeat(xl, n_var)
else:
    problem = set_problem(prob_name)                                     # set optimization problem
    



n_eval = params['n_eval']                                           # set maximum number of evaluation
n_pop = params['n_pop']							                    # get population size

T = params['T']                                                     # set neighbor size
delta = params['delta']                                             # set probability to select parent from neighbor
nr = params['nr']                                                   # set maximum update counts for one offspring

F = params['F']
etam = params['etam']                                               # set index parameter of polynomial mutation

priority_function = params['priority_function']                     # name of the priority function for resource allocation
fix_value = params['fix_value']                                     # set index parameter of priority functions for resource allocation
number_solutions = params['number_solutions']                       # number of solution to receive resources given the priority function


#################
# start program #
#################

os.makedirs(f'./{output}', exist_ok=True)                           # create a folder to include running results
os.makedirs(f'./{output}/history/', exist_ok=True)
os.makedirs(f'./{output}/final/', exist_ok=True)
os.makedirs(f'./{output}/history/{prob_name}_{args.seed}', exist_ok=True)

W = np.zeros(shape=(n_pop,n_obj))
with open("/home/yclavinas/MOEADr/SOBOL-"+str(n_obj)+"objs-500wei.ws") as file_in:
    lines = []
    i = 0
    for line in file_in:
    	data = line.split(" ")
    	for e in range(n_obj):
    		W[i,e] = float(data[e])
    	i += 1	


boundaries = list(itertools.permutations(np.append(np.zeros(n_obj-1), 1)))
idx_boundary = np.zeros(n_obj)
for i in range(n_obj):
	idx_boundary[i] = np.where((W == boundaries[i]).all(axis=1))[0]

B = determine_neighbor(W, T)                                        # determine neighbor
X = init_pop(n_pop, n_var, xl, xu)                                  # initialize a population

if (prob_name == "dtlz7"):
    Y = eval_pop(X, problem)                                                  # evaluate fitness
else:
    Y = eval_all_solutions(X, problem)                                                  # evaluate fitness

z = init_ref_point(Y)                                               # determine a reference point

n_fe = n_pop

if(priority_function == "fix_random"):
    dt_X = X
    dt_Y = Y
    priority_values = priority(n_pop, X, dt_X, Y, dt_Y, priority_function, fix_value) # generate an array of values for resource allocation based on priority_function named function
else:
    priority_values = np.zeros(n_pop) + 1	
bigZ = np.zeros(n_pop)


c_gen = 1
while n_fe < n_eval:												# start main loop
    result = np.hstack([Y])                                      # record objective values and decision variables
    np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_paretos.csv', result)

    info_gen = np.hstack([n_fe, c_gen])                                      # record information (n_fe and c_gen) about the current generation
    np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_info_gen.csv', info_gen)

    dt_X = X.copy()
    dt_Y = Y.copy()
    dt_bigZ = bigZ.copy()
    mask_priority = get_mask(n_pop, number_solutions, priority_values, idx_boundary) # mask for RA

    for i in np.random.permutation(n_pop):                          # traverse the population; randomly permuting solutions in the population set
    	
    	if (mask_priority[i] == 1):									# if 1 we give resources for solutions	

            n_fe += 1
            xi, fi = X[i, :], Y[i, :]                                   # get current individual and its fitness value						
            if random.random() < delta:                                 # determine selection pool by probability
                pool = B[i, :]                                          # neighbor as the pool
            else:
                pool = np.arange(n_pop)                                 # population as the pool

            j = np.random.choice(pool)                                  # select a random individual from pool
            xj, fj = X[j, :], Y[j, :]

            
            xi_ = fix_bound( de_mutation(xi, X, n_pop, i, F), xl, xu ) # differential evolution mutation
            xi_ = fix_bound( poly_mutation(xi_, etam, xl, xu), xl, xu ) # polynomial mutation
            X[i] = xi_
            if (prob_name == "dtlz7"):
                fi_ = problem.evaluate(xi_)                                                # evaluate offspring
            else:
                fi_ = problem(xi_)                                          # evaluate offspring

            z = update_ref_point(z, fi_)                                # update reference point

            bigZ[i] = tchebycheff(fi_, W[i, :], z)

            nc = 0                                                      # initialize the update counter
            for k in np.random.permutation(len(pool)):                  # traverse the selection pool

                fk = Y[k, :]                                            # get k-th individual fitness
                wk = W[k, :]                                            # get k-th weight vector

                tch_ = tchebycheff(fi_, wk, z)                          # compute tchebycheff cost of offspring
                tchk = tchebycheff(fk, wk, z)                           # compute tchebycheff cost of parent

                if tch_ <= tchk:                                        # compare tchebycheff cost of offspring and parent
                    X[k] = xi_                                          # update parent
                    Y[k] = fi_
                    nc += 1                                             # cumulate the counter

                if nc >= nr: break                                      # break if counter arrive the upper limit
    		
    c_gen += 1
    priority_values = priority(n_pop, X, dt_X, bigZ, dt_bigZ, priority_function, fix_value) # generate an array of values for resource allocation based on priority_function named function
    dt_bigZ = bigZ.copy()

info_gen = np.hstack([n_fe, c_gen])                                      # record information (n_fe and c_gen) about the current generation
result = np.hstack([Y])                                          # record objective values and decision variables

np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_info_gen.csv', info_gen)
np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_paretos.csv', result)

np.savetxt(f'./{output}/final/{prob_name}_{args.seed}_paretos.csv', result)
np.savetxt(f'./{output}/final/{prob_name}_{args.seed}_info_gen.csv', info_gen)






