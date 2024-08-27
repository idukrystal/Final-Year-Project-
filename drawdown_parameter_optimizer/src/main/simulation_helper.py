from numpy import e, square, pi, sqrt
from .data import test_datas, test_value_name, test_result_name
import random
from scipy.stats import norm
from src.main.solution import Solution
from src.main.simulators import Simulator
from src.main.params import solution_archive_size, q_value, parameters, e_value


total_pheromone = 0

class SimulationHelper:
    def __init__(self):
        self.solution_archive = []
        self.simulator = Simulator()
    def initialize_simulation(self):
        for i in range(solution_archive_size):
            solution = Solution()
            solution.test_data  = random.choice(test_datas)
            for variable in solution.variables:
                solution.variables[variable] = random.uniform(*parameters[variable])
            sim_result = self.simulator.simulate_test(solution)
            solution.update_pheromone(sim_result)
            global total_pheromone
            total_pheromone += solution.pheromone
            self.solution_archive.append(solution)
        self.modify_weights()
    
    def modify_weights(self):
        self.reorder_solution_archive()
        for i in range(solution_archive_size):
            solution = self.solution_archive[i]
            solution.weight = self.calculate_weight(i)

    def reorder_solution_archive(self):
        self.solution_archive.sort(reverse=True)

    def calculate_weight(self, rank):
        weight = self.get_weight(rank)
        return weight

    def print_solution_archive(self):
        for solution in self.solution_archive:
            print(solution.variables, '**', solution.weight, '**',solution.pheromone)
    def get_weight(selt, i):
        a = (1/(q_value*solution_archive_size*sqrt(2*pi)))*(e**(-(square(i-1)/(2*square(q_value*solution_archive_size)))))
        return round(a, 5)

    def update_solution_archive(self, new_solution):
        for i in range (solution_archive_size):
            if new_solution >= self.solution_archive[i]:
                self.solution_archive.insert(i, new_solution)
                self.solution_archive.pop()
                self.modify_weights()
                return True
        return False
    def calculate_sd(self, solution):
        sd = {}
        for variable in solution.variables:
            sd[variable] = calculate_sd(solution.variables[variable], [value.variables[variable] for value in self.solution_archive ])
        return sd;


def calculate_sd(x, values):
    sum = 0

    found = False

    for value in values:
        if value == x and not found:
            found = True
            continue
        sum += abs(value - x)/(solution_archive_size - 1)
    return e_value*sum
