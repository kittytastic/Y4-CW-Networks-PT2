from typing import Set
from graph_types import *
import random
from Utils import plot_degree

class PATrial:
    def __init__(self, num_nodes:int):
        self._num_nodes = num_nodes 
        self._node_ballot = [node for node in range(num_nodes) for _ in range(num_nodes)]
        self._out_ballot = {n:num_nodes for n in range(num_nodes)}

    def run_trial(self, num_nodes:int)->Set[int]:
        num_nodes = random.choice(list(self._out_ballot.values()))

        new_neighbors:Set[Node] = set()
        for _ in range(num_nodes):
            nn = random.choice(self._node_ballot)
            if nn not in new_neighbors:
                self._out_ballot[nn]+=1
            new_neighbors.add(nn)
               
        self._node_ballot.extend(list(new_neighbors))
        self._node_ballot.append(self._num_nodes)
        self._out_ballot[self._num_nodes] = 0 

        self._num_nodes += 1
        return new_neighbors
    
def make_complete_graph(num_nodes:int)->Graph:   
    complete_graph = {
        v: 
        set([j for j in range(num_nodes) if j != v]) 
        for v in range(num_nodes)
        }
   
    return complete_graph
    
def make_PA_Graph(total_nodes:int, out_degree:int)->Graph:
   
    PA_graph = make_complete_graph(out_degree)
    trial = PATrial(out_degree)
    
    for v in range(out_degree, total_nodes):
        PA_graph[v] = trial.run_trial(out_degree)
    
    return PA_graph


if __name__=="__main__":
    g = make_PA_Graph(7000,10)
    plot_degree(g, 'Q2')

