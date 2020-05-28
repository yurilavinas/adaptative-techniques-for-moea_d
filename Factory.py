import MultiObjectiveProblem as MOOP
import numpy as np
###################
#  MOP to solve   #
###################
from pymoo.factory import get_problem, get_reference_directions, get_visualization
from pymoo.util.plotting import plot

def set_problem(prob_name, n_var = 0, n_obj = 0, xu = 0, xl = 0):

	benchmark_name = ''.join(i for i in prob_name if not i.isdigit())

	if benchmark_name == 'dtlz' or benchmark_name == 'DTLZ':
		return (dtlz_benchmark(prob_name, n_var, n_obj, xu, xl))

	elif benchmark_name == 'uf' or benchmark_name == 'UF':
		return (uf_benchmark(prob_name))

	elif prob_name == "sch" or prob_name == "SCH":
		return MOOP.SCH
	
	else:
		return False

def dtlz_benchmark(prob_name, n_var = 0, n_obj = 0, xu = 0, xl = 0):

	problem = get_problem(prob_name, n_var, n_obj)                                            # set optimization problem
	problem.n_var = n_var
	problem.n_obj = n_obj

	return problem.evaluate

def uf_benchmark(prob_name):
	if prob_name == "uf1" or prob_name == "UF1":
		return MOOP.UF1

	elif prob_name == "uf2" or prob_name == "UF2":
		return MOOP.UF2

	elif prob_name == "uf3" or prob_name == "UF3":
		return MOOP.UF3

	elif prob_name == "uf4" or prob_name == "UF4":
		return MOOP.UF4

	elif prob_name == "uf5" or prob_name == "UF5":
		return MOOP.UF5

	elif prob_name == "uf6" or prob_name == "UF6":
		return MOOP.UF6

	elif prob_name == "uf7" or prob_name == "UF7":
		return MOOP.UF7

	elif prob_name == "uf8" or prob_name == "UF8":
		return MOOP.UF8

	elif prob_name == "uf9" or prob_name == "UF9":
		return MOOP.UF9

	elif prob_name == "uf10" or prob_name == "UF10":
		return MOOP.UF10
	
	else:
		return False