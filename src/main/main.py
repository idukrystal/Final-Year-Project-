from numpy import e, square, pi, sqrt
from data import test_datas, test_value_name, test_result_name
import random
from scipy.stats import norm
from simulator import Simulator
from solution import Solution

## simulation 
parameters = {"a":(1, 5), "b":(1, 10)}
solution_archive_size = 5 * len(parameters)
algorithm_q  = 0.5
solution_archive = []
simulator = Simulator()

def initialize_simulation():
    for i in range(solution_archive_size):
        solution = Solution()
        solution.test_data  = random.choice(test_datas)
        for parameter in parameters:
            solution.variables[parameter] = random.uniform(*parameters[parameter])
        sim_result = simulator.simulate_test(solution)
        solution.update_pheromone(sim_result)
        solution_archive.append(solution)
        modify_weights()

def modify_weights():
    reorder_solution_archive()
    for i in range(len(solution_archive)):
        solution_archive[i].weight = calculate_weight(i)

def reorder_solution_archive():
    solution_archive.sort(reverse=True)

def calculate_weight(rank):
    weight = get_weight(rank)
    return weight

def print_solution_archive():
    for solution in solution_archive:
        print(solution.variables, solution.weight, solution.pheromone)
def get_weight(i):
    a = (1/(algorithm_q*solution_archive_size*sqrt(2*pi)))*(e**(-(square(i-1)/(2*square(algorithm_q*solution_archive_size)))))
    return a

initialize_simulation()
print_solution_archive()
