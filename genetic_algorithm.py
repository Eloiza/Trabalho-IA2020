from tsp import TSP
import random
import copy

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

#calcula porção da roleta para cada individuo da população
def roulette_wheel(population):
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

    return population

#seleciona dois pontos de corte aleatórios para o crossover
def select_random_cut(genome_size):
    cut1 = 0
    cut2 = 0

    #garante que cortes serão diferentes
    while(cut1 == cut2):
        cut1 = random.randint(1,int(genome_size/2))
        cut2 = random.randint(int(genome_size/2), genome_size - 1)

    return cut1, cut2

#testa se um genoma é valido - sem repetições de cidades
def is_valid_genome(genome):
    for g in genome:
        count = 0 
        
        for h in genome:
            if(g == h):
                count += 1

        if(count > 1):
            return False

    return True

def map_genome(cut_indexes, genome, map_from, map_to):

    for i in range(len(genome)):
        #caso estiver nos indexes que ocorreram o corte pula
        if(i in cut_indexes):
            continue

        #caso o alelo já estiver na área que ocorreu o corte
        if(genome[i] in map_from):
            map_index = map_from.index(genome[i])   #busca o indice da região conservada p/ mapeamento
            genome[i] = map_to[map_index]           #substitui alelo pelo correpondente da outra regiao conservada

    return genome


def crossover(parents):
    #(x x x |4 5 6| x x)
    cut1, cut2 = select_random_cut(len(parents[0].permutation))
    
    children = []
    for p in parents:
        children.append(copy.deepcopy(p.permutation))

    children[0][cut1:cut2] = copy.deepcopy(parents[1][cut1:cut2])
    children[1][cut1:cut2] = copy.deepcopy(parents[0][cut1:cut2])
   

####################################################################
    p1_genome = parents[0].permutation
    p2_genome = parents[1].permutation

    print("p1_genome", p1_genome)
    print("p2_genome", p2_genome)

    cut1, cut2 = select_random_cut(len(parents[0].permutation))
    print("crossover:  cut1: %i, cut2: %i" %(cut1, cut2))

    child1 = copy.deepcopy(parents[0].permutation)
    child2 = copy.deepcopy(parents[1].permutation)

    child1[cut1:cut2] = copy.deepcopy(p2_genome[cut1:cut2])
    child2[cut1:cut2] = copy.deepcopy(p1_genome[cut1:cut2])

    print("child1", child1)
    print("child2", child2)

    #salva parte herdada do pai
    cut_section_c1 = p2_genome[cut1:cut2]
    cut_section_c2 = p1_genome[cut1:cut2]

    print("cut_section_c1", cut_section_c1)
    print("cut_section_c2", cut_section_c2)

    section_indexes = range(cut1,cut2)
    while(not is_valid_genome(child1)):
        child1 = map_genome(cut_indexes=section_indexes, genome=child1, map_from=cut_section_c1, map_to=cut_section_c2)
        print(child1)

    while(not is_valid_genome(child1)):
        child1 = map_genome(cut_indexes=section_indexes, genome=child1, map_from=cut_section_c1, map_to=cut_section_c2)
        print(child1)

    return child1
#original pop_size=50 e max_gen=2000
def genetic_algorithm(problem, pop_size=5, max_gen=10):
    mutation_chance = 0.10
    population = random_population(problem, pop_size)
    fitness_history = []
    best_permutation = None

    #-------------------Seleção de pais ---------------------
    #                       roleta 
    population = roulette_wheel(population)

    parents = []
    new_population = []
    while(len(new_population) < pop_size):
        #seleciona dois pais
        for i in range(2):
            rand_num = random.random()  #gera número aleatorio entre 0 e 1
            print("Numero random", rand_num)
            for individual in population:
                print("select_prob[0]: ", individual.select_prob[0])
                print("select_prob[1]: ", individual.select_prob[1])
                print()

                if(individual.select_prob[0] <= rand_num and individual.select_prob[1] <=rand_num):
                    parents.append(individual)

        #-------------------Cruzamento------------------------
        #                    crossover
        print("Pais selecionados")
        print("p1:", parents[0].permutation)
        print("p2:", parents[1].permutation)

        offspring = crossover(parents)

        #--------------------Mutação---------------------------
        #                     troca
        # rand_num = random.random()
        # #caso num prox a taxa de mutacao realiza troca de cromossomos
        # if(rand_num <= mutation_chance):

        #     #a troca vai ocorrer entre o index 1 e 2 escolhidos randomicamente
        #     index1 = random.randint(0, len(offspring.permutation))
        #     index2 = random.randint(0, len(offspring.permutation))

        #     #faz com que os indexes realmente sejam diferentes
        #     while(index1 == index2):
        #         index1 = random.randint(0, len(offspring.permutation))

        #     aux = offspring.permutation[index1]

        #     #alg de troca
        #     offspring.permutation[index1] = offspring.permutation[index2]
        #     offspring.permutation[index2] = aux
            #ter certeza que o cruzamento rendeu um filho valido para o problema

        new_population.append(offspring)
    #Seleção de individuos para a prox geracao 
        #- geracional, uniforme, competição, elitismo

    return best_permutation, fitness_history


if __name__ == "__main__":
    problem = TSP('instances/berlin4.tsp')
    best_solution, fitness_history = genetic_algorithm(problem)
    # print(best_solution, problem.evaluate(best_solution))
