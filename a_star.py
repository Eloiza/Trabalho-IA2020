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
        tup = (self.city, self.node_cost)
        return str(tup)

def print_nodelist(n_list):
    for i in n_list:
        print(i)

def find_node(node_name, node_list):
    for n in node_list:
        if(n.city == node_name):
            return 1

    return 0

def a_star(problem):
    print("Resolvendo entrada: %s" %(problem))


    # open_nodes = PriorityQueue() #nos vistos mas nao visitados

    open_nodes = []
    closed_nodes = []   #nos vistos e visitados
    
    #obtem estado inicial
    current_state = problem.get_start_state()

    print("estado inicial:", current_state)

    #cria primeiro nó com o estado inicial
    node = Node(state=(0,), path_cost=0, heuristic_cost=problem.get_heuristic(current_state), city=0, parent_node=0)

    #inicializa lista de nos vistos com o no inicial
    # open_nodes.put(node)
    open_nodes.append(node)
    while(len(open_nodes) > 0):
        #recebe proximo no a ser visitado - no de menor custo
        open_nodes.sort()   #fazer sort pelo custo
        node = open_nodes.pop(0)
        closed_nodes.append(node)
        # node = open_nodes.get()

        print("Explorando nó: %i - custo: %i" %(node.city, node.node_cost))

        if(problem.is_goal_state(node.state)):
            print("Solução encontrada")
            break;

        #visita vizinhos do estado atual
        next_states = problem.get_next_states(node.state)
        print("next_states: ", next_states) 

        children = []
        for state in next_states:
            new_node = Node(state=state[0], path_cost=state[2], heuristic_cost=problem.get_heuristic(state[0]), city=state[1], parent_node=node.city)
            children.append(new_node)

        for child in children:
            if(find_node(child, closed_nodes)):
                 continue

            if(find_node(child, open_nodes)):
                new_g = node.path_cost + child.path_cost
                if(child.path_cost > node.path_cost):
                    child.path_cost = new_g
                    child.parent_node

            else:
                child.path_cost = node.path_cost + child.path_cost
                open_nodes.append(child)


        print( )
        print("Lista nós fechados:")
        print_nodelist(closed_nodes)
        print("Lista nós abertos:")
        print_nodelist(open_nodes)

    print("Solução encontrada: ", node.state)

    print("nos fechados")
    for i in closed_nodes:
        print(i.city)

    path = []
    path.append(node.city)
    while(node.city != 0 and node != None):
        #node recebe valor de seu nodo pai
        for n in closed_nodes:
            if(n.city == node.parent_node):
                path.append(n.city)
                node = n 

        # node = next((n for n in closed_nodes if n.city == node.parent_node), None)
        # path.append(node.city)

    print("Caminho encontrado: ", path)

if __name__ == "__main__":
    problem = TSP('instances/berlin4.tsp')
    path = a_star(problem)
    # print(path, problem.evaluate(path))
