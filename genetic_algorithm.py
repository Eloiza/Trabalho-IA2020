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
        #calcula fitness com relacao aos demais individuos - indivuos com fitness menores são melhores neste caso 
        fitness_ratio = 1.0 - (individual.fitness / fitness_sum)     

        #recebe intervalo da roleta em que pode ser escolhido (min, max)
        individual.select_prob = (round(prob_sum, 3), round(prob_sum + fitness_ratio, 3))

        #atualiza soma de probabilidades para setar o inicio da prox seção
        prob_sum += fitness_ratio

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


def crossover(problem, parents):
    #guarda genoma dos pais
    p1_genome = parents[0].permutation
    p2_genome = parents[1].permutation

    #seleciona uma região de corte aleatória
    cut1, cut2 = select_random_cut(len(p1_genome))

    #copia genoma de um dos pais para os filhos
    child1 = copy.deepcopy(p1_genome)
    child2 = copy.deepcopy(p2_genome)

    #faz o crossover com um segmento do outro pai
    child1[cut1:cut2] = copy.deepcopy(p2_genome[cut1:cut2])
    child2[cut1:cut2] = copy.deepcopy(p1_genome[cut1:cut2])

    #salva parte principal do crossover herdada do pai
    cut_section_c1 = p2_genome[cut1:cut2]
    cut_section_c2 = p1_genome[cut1:cut2]

    section_indexes = range(cut1,cut2)

    #faz o mapeamento do genoma para obter um genoma valido
    while(not is_valid_genome(child1)):
        child1 = map_genome(cut_indexes=section_indexes, genome=child1, map_from=cut_section_c1, map_to=cut_section_c2)
        # print(child1)

    #mapeamento para o segundo filho
    while(not is_valid_genome(child2)):
        child2 = map_genome(cut_indexes=section_indexes, genome=child2, map_from=cut_section_c2, map_to=cut_section_c1)
        # print(child2)

    children = []
    children.append(Individual(permutation=child1, fitness= problem.evaluate(child1)))
    children.append(Individual(permutation=child2, fitness= problem.evaluate(child1)))

    return children

def mutation(problem, individual):

    #a troca vai ocorrer entre o index1 e index2 escolhidos randomicamente
    index1 = random.randint(0, len(individual.permutation)-1)
    index2 = random.randint(0, len(individual.permutation)-1)

    #garante indexes diferentes
    while(index1 == index2):
        index1 = random.randint(0, len(individual.permutation)-1)

    aux = individual.permutation[index1]

    #alg de troca
    individual.permutation[index1] = individual.permutation[index2]
    individual.permutation[index2] = aux

    #atualiza fitness do individuo
    individual.fitness = problem.evaluate(individual.permutation)

    return individual

def generation_review(problem, fitness_history, population, best_permutation):
    #busca melhor individuo da geracao - individuo com menor custo
    best_ind = population[0]
    for i in population:
        if(i.fitness < best_ind.fitness):
            best_ind = i

    #adiciona fitness do melhor individuo no historico
    fitness_history.append(best_ind.fitness)

    #se for maior que o registro atualiza a melhor permutacao
    if(best_ind.fitness < problem.evaluate(best_permutation)):
        best_permutation = best_ind.permutation

    return  best_permutation, fitness_history

def select_parents(population):
    parents = []
    #seleciona dois pais
    for i in range(2):
        rand_num = round(random.random(), 3)  #gera número aleatorio entre 0 e 1
        for individual in population:

            #verifica a qual setor da roleta esse valor pertence 
            if(rand_num >= individual.select_prob[0] and individual.select_prob[1] >= rand_num):
                parents.append(individual)
                break

    return parents

#original pop_size=50 e max_gen=2000
def genetic_algorithm(problem, pop_size=50, max_gen=2000):
    mutation_chance = 0.10
    population = random_population(problem, pop_size)
    fitness_history = []
    best_permutation = population[0].permutation

    #avalia primeira geração
    best_permutation, fitness_history = generation_review(problem, fitness_history, population, best_permutation)

    gen = 0 
    gen_checkpoint = int(max_gen/4) #quando 1/4 das geraçoes forem geradas é testado se há ganho de desempenho
    has_upgrade = 1                 #se tiver melhorado a melhor permutacao em 1/4 de geracoes fica 1

    while(gen < max_gen and has_upgrade):

        #-------------------Seleção de pais ---------------------
        #                       roleta 
        population = roulette_wheel(population) #inicializa valores para a roleta de seleção de pais

        new_population = []
        while(len(new_population) < pop_size):

            parents = select_parents(population) #seleciona dois pais aleatórios da população 

            #-------------------Cruzamento------------------------
            #                    crossover

            offspring = crossover(problem, parents) #faz crossover e cria dois novos individuos


            #--------------------Mutação---------------------------
            #                     troca

            rand_num = random.random()
            #caso num prox a taxa de mutacao realiza troca de cromossomos
            if(rand_num <= mutation_chance):
                #escolhe randomicamente qual dos dois será mutado
                rand_index = random.randint(0,1)
                offspring[rand_index] = mutation(problem, offspring[rand_index])


            new_population.append(copy.deepcopy(offspring[0]))
            new_population.append(copy.deepcopy(offspring[1]))

        population = new_population
        gen += 1

        #avalia nova população
        best_permutation, fitness_history = generation_review(problem, fitness_history, population, best_permutation)

    return best_permutation, fitness_history


if __name__ == "__main__":
    problem = TSP('instances/berlin15.tsp')
    best_solution, fitness_history = genetic_algorithm(problem)
    print(best_solution, problem.evaluate(best_solution))