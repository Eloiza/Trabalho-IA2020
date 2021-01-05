from tsp import TSP
import random

random.seed(42)

class Individual():
    def __init__(self, permutation, fitness):
        self.permutation = permutation
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness


def random_population(problem, pop_size):
    population = []
    for _ in range(pop_size):
        permutation = problem.random_path()
        fitness = problem.evaluate(permutation)
        population.append(Individual(permutation, fitness))
    return population


def genetic_algorithm(problem, pop_size=50, max_gen=2000):
    population = random_population(problem, pop_size)
    fitness_history = []
    best_permutation = None
    #SUA IMPLEMENTACAO AQUI

    return best_permutation, fitness_history


if __name__ == "__main__":
    problem = TSP('instances/berlin52.tsp')
    best_solution, fitness_history = genetic_algorithm(problem)
    print(best_solution, problem.evaluate(best_solution))
