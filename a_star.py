
from queue import PriorityQueue
from tsp import TSP

class Node():
    def __init__(self, state, path_cost, heuristic_cost, city, parent_node):
        self.state = state
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.node_cost = path_cost + heuristic_cost
        self.city = city
        self.parent_node = parent_node

    def __lt__(self, other):
        return self.node_cost < other.node_cost

    def __le__(self, other):
        return self.node_cost <= other.node_cost

    def __gt__(self, other):
        return self.node_cost > other.node_cost

    def __ge__(self, other):
        return self.node_cost >= other.node_cost

    def __str__(self):
        tup = (self.city, self.path_cost, self.heuristic_cost, self.node_cost)
        return str(tup)

def print_nodelist(n_list):
    for i in n_list:
        print(i, "de pai %i" %(i.parent_node))

def find_node(node_name, node_list):
    for n in node_list:
        if(n.city == node_name):
            return n

    return 0

def a_star(problem):
    print("Resolvendo entrada: %s" %(problem))

    open_nodes = []     #nos visto mas não visitados
    closed_nodes = []   #nos vistos e visitados
    
    #obtem estado inicial
    current_state = problem.get_start_state()

    print("estado inicial:", current_state)

    #cria primeiro nó com o estado inicial
    node = Node(state=(0,), path_cost=0, heuristic_cost=problem.get_heuristic(current_state), city=0, parent_node=None)

    #inicializa lista de nos vistos com o no inicial
    open_nodes.append(node)
    while(len(open_nodes) > 0):
        #recebe proximo no a ser visitado - no de menor custo
        open_nodes.sort()
        node = open_nodes.pop(0)
        closed_nodes.append(node)

        #caso nó tiver o estado objetivo encerra a busca
        if(problem.is_goal_state(node.state)):
            print("Solução encontrada")
            break;

        #recebe nós adjacentes ao nó atual
        next_states = problem.get_next_states(node.state)

        #criando nós filhos do nó atual
        children = []
        for state in next_states:
            new_node = Node(state=state[0], path_cost=state[2] + node.path_cost, heuristic_cost=problem.get_heuristic(state[0]), city=state[1], parent_node=node)
            children.append(new_node)

        #analisa filhos para saber melhor opcao
        for child in children:
            #se o nó filho já foi explorado segue para o prox
            if(find_node(child, closed_nodes)):
                 continue

            copy = find_node(child, open_nodes)
            if(copy):
                #se o no estiver na lista aberta e tiver custo maior que o já inserido 
                #segue para prox filho
                if(child.path_cost > copy.path_cost):
                    continue

            #se não adiciona a lista de nós abertos
            open_nodes.append(child)


    print("Estado final encontrada: ", node.state)

    #backtracking para determinar o caminho encontrado
    path = []
    ultimo_custo = node.node_cost
    while(node != None):
        path.append(node.city)
        node = node.parent_node 

    path.reverse()
    print("Caminho encontrado: ", path)
    print("Custo ultimo no: ", ultimo_custo)

    return path

if __name__ == "__main__":
    import sys
    if(len(sys.argv) != 2):
        print("Número inválido de argumentos :(\nUsage: python3 a_star.py arquivo.tsp")
        sys.exit()

    else: 
        problem = TSP(sys.argv[1])
        path = a_star(problem)
        print(path, problem.evaluate(path))