import MultiObjectiveProblem as MOOP
import numpy as np
###################
#  MOP to solve   #
###################
from pymoo.factory import get_problem

def set_problem(prob_name, n_var = 0, n_obj = 0, xu = 0, xl = 0):

	if prob_name == "sch" or prob_name == "SCH":
		return MOOP.SCH

	if prob_name == "uf9" or prob_name == "UF9":
		return MOOP.UF9

	if prob_name == "dtlz7" or prob_name == "DTLZ7":
		problem = get_problem(prob_name)                                            # set optimization problem
		problem.n_var = n_var
		problem.n_obj = n_obj
		problem.xu = np.repeat(xu, n_var)
		problem.xl = np.repeat(xl, n_var)

		return problem.evaluate

