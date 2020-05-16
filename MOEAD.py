import os
import argparse
import yaml
import random
import numpy as np
from scipy.special import comb

from Factory import set_problem
from WeightVector import das_dennis, determine_neighbor
from Population import init_pop, eval_pop
from ReferencePoint import init_ref_point, update_ref_point
from Mutation import lf_mutation, poly_mutation, fix_bound
from Decomposition import tchebycheff

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

params = yaml.safe_load(args.params)                                            # read config file

random.seed(args.seed)                                                          # set the seed for reproducibility purposes
np.random.seed(args.seed)                                                       # set the seed for reproducibility purposes

output = params['output']                                                       # set output of record in this run

n_obj = params['n_obj']                                                         # set number of objectives
n_var = params['n_var']                                                         # set number of variables
xl = params['xl']                                                               # set boundary of variables
xu = params['xu']                                                               # set boundary of variables

prob_name = params['prob_name']
problem = set_problem(prob_name, n_var, n_obj, xu, xl)                          # set optimization problem                                               

sld_n_part = params['sld_n_part']                                           # set number of partitions

n_eval = params['n_eval']                                           # set maximum number of evaluation
n_pop = int( comb(n_obj + sld_n_part - 1, n_obj - 1) )                  # compute population size

T = params['T']                                                     # set neighbor size
delta = params['delta']                                             # set probability to select parent from neighbor
nr = params['nr']                                                   # set maximum update counts for one offspring

alpha = params['alpha']                                             # set scaling factor of levy flight mutation
beta = params['beta']                                               # set stability parameter of levy flight mutation
etam = params['etam']                                               # set index parameter of polynomial mutation

#################
# start program #
#################

os.makedirs(f'./{output}', exist_ok=True)                           # create a folder to include running results
os.makedirs(f'./{output}/history/', exist_ok=True)
os.makedirs(f'./{output}/history/{prob_name}_{args.seed}', exist_ok=True)
os.makedirs(f'./{output}/final/', exist_ok=True)                                # create a folder to include final results

W = das_dennis(sld_n_part, n_obj)                                   # generate a set of weight vectors
B = determine_neighbor(W, T)                                        # determine neighbor
X = init_pop(n_pop, n_var, xl, xu)                                  # initialize a population

Y = eval_pop(X, problem, prob_name)                                 # evaluate fitness
z = init_ref_point(Y)                                               # determine a reference point

n_fe = n_pop

# for c_gen in range(1, n_gen):                                       # start main loop
c_gen = 1

while n_fe < n_eval:
    result = np.hstack([Y, X])                                                  # record objective values (Y) and decision variables (X)
    np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_paretos.csv', result)   # record information (Y, X) about the current generation

    info_gen = np.hstack([n_fe, c_gen])                                         # record number of function evaluations and current generation
    np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_info_gen.csv', info_gen)# record information (n_fe and c_gen) about the current generation

    
    for i in np.random.permutation(n_pop):                          # traverse the population; randomly permuting solutions in the population set

        n_fe += 1
        xi, fi = X[i, :], Y[i, :]                                   # get current individual and its fitness value

        if random.random() < delta:                                 # determine selection pool by probability
            pool = B[i, :]                                          # neighbor as the pool
        else:
            pool = np.arange(n_pop)                                 # population as the pool

        j = int(np.random.choice(pool))                                  # select a random individual from pool
        xj, fj = X[j, :], Y[j, :]

        xi_ = fix_bound( lf_mutation(xi, xj, alpha, beta), xl, xu ) # levy flight mutation
        xi_ = fix_bound( poly_mutation(xi_, etam, xl, xu), xl, xu ) # polynomial mutation
        
        fi_ = problem(xi_)                                              # evaluate offspring (new solution)

        z = update_ref_point(z, fi_)                                # update reference point


        nc = 0                                                      # initialize the update counter
        for k in np.random.permutation(len(pool)):                  # traverse the selection pool

            fk = Y[k, :]                                            # get k-th individual fitness
            wk = W[k, :]                                            # get k-th weight vector

            if tchebycheff(fi_, wk, z) <= tchebycheff(fk, wk, z):   # compare tchebycheff cost of offspring and parent

                X[k] = xi_                                          # update parent
                Y[k] = fi_
                nc += 1                                             # cumulate the counter


            if nc >= nr: break                                      # break if counter arrive the upper limit
            


            # exit()

    c_gen += 1
    # input('next gen normal moea.d')
info_gen = np.hstack([n_fe, c_gen])                                      # record information (n_fe and c_gen) about the current generation
result = np.hstack([Y, X])                                          # record objective values and decision variables

np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_info_gen.csv', info_gen)
np.savetxt(f'./{output}/history/{prob_name}_{args.seed}/{c_gen}_paretos.csv', result)

np.savetxt(f'./{output}/final/{prob_name}_{args.seed}_paretos.csv', result)
np.savetxt(f'./{output}/final/{prob_name}_{args.seed}_info_gen.csv', info_gen)

