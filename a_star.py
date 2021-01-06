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


def a_star(problem):
    print("Resolvendo entrada: %s" %(problem))
    random_path = problem.random_path()
    start = problem.get_start_state()
    next_state = problem.get_next_states(start) #((prox estado), prox cidade, distancia atual ate prox)
    new_state = next_state[0][0]


    open_nodes = PriorityQueue() #nos vistos mas nao visitados
    closed_nodes = PriorityQueue() #nos vistos e visitados
    
    #obtem estado inicial
    current_state = problem.get_start_state()

    #cria primeiro nó com o estado inicial
	node = Node(initial_state=current_state[0], 
				path_cost=current_state[2], 
				heuristic_cost=problem.get_heuristic(current_state[0]), 
				city=current_state[1],
				parent_node=current_state[0][-2])

	#inicializa lista de nos vistos com o no inicial
	open_nodes.put(node)
  	while(len(open_nodes) > 0 or not problem.is_goal_state(node.initial_state)):
  		#recebe proximo no a ser visitado - no de menor custo
  		node = open_nodes.get()

  		#visita vizinhos do estado atual
  		next_states = problem.get_next_states(node.initial_state)

	  	#visita nós vizinhos
	  	for state in next_states:
	  		new_node = Node(initial_state=state[0], 
	  						path_cost=state[2], 
	  						heuristic_cost=problem.get_heuristic(state[0]), 
	  						city=state[1],
	  						parent_node=state[0][-2])

	  		open_nodes.put(new_node)

	  	#fecha no que teve seus vizinhos visitados
	  	closed_nodes.put(node)

	  	#recebe proximo nó a ser visitado - nó de menor heuristica
	  	node = open_nodes.get()

    print("Melhor estado", best)
    	
if __name__ == "__main__":
    problem = TSP('instances/berlin15.tsp')
    path = a_star(problem)
    # print(path, problem.evaluate(path))