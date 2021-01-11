from tsp import TSP
import random

random.seed(42)

class Individual():

    def __init__(self, permutation, fitness):
        self.permutation = permutation
        self.fitness = fitness
        self.select_prob = 0 #representa probabilidade de ser selecionado

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __str__(self):
        return str(self.permutation) + " " + str(self.fitness) 

def random_population(problem, pop_size):
    population = []
    for _ in range(pop_size):
        permutation = problem.random_path()
        fitness = problem.evaluate(permutation)
        population.append(Individual(permutation, fitness))
    return population


#original pop_size=50 e max_gen=2000
def genetic_algorithm(problem, pop_size=5, max_gen=10):
    population = random_population(problem, pop_size)
    fitness_history = []
    best_permutation = None

    for individual in population:
        print(individual)

    #-------------------Seleção de pais ---------------------
    #                       roleta 

    #calcula soma total da fitness da população
    fitness_sum = 0
    for individual in population:
        fitness_sum += individual.fitness

    #calculando tamanho da seção para cada individuo
    prob_sum = 0 
    for individual in population:
        #calcula fitness com relacao aos demais individuos
        fitness_ratio = individual.fitness / fitness_sum

        #recebe intervalo da roleta em que pode ser escolhido (min, max)
        individual.select_prob = (prob_sum, prob_sum + fitness_ratio)

        #atualiza soma de probabilidades para setar o inicio da prox seção
        prob_sum += fitness_ratio

        print(individual.select_prob)

    # selected_pop = []
    parents = []
    while(len(new_population) < pop_size):
        #select two parents
        for i in range(2):
            rand_num = random.random()  #gera número aleatorio entre 0 e 1
            for individual in population:
                if(individual.select_prob[0] >= rand_num and individual.select_prob[1] <=rand_num):
                    parents.append(individual)

        #-------------------Cruzamento------------------------
        #                    crossover

        new_population.append(Individual())
    #Cruzamento
        #order crossover, order based, position based, partially mapped cycle
    #Mutação
        #- inserção ou troca
    #Seleção de individuos para a prox geracao 
        #- geracional, uniforme, competição, elitismo

    return best_permutation, fitness_history


if __name__ == "__main__":
    problem = TSP('instances/berlin4.tsp')
    best_solution, fitness_history = genetic_algorithm(problem)
    # print(best_solution, problem.evaluate(best_solution))
