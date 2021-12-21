from typing import Set
from Utils import *
import random

class PATrial:
    def __init__(self, num_nodes:int):
        self._num_nodes = num_nodes 
        self._node_ballot = [node for node in range(num_nodes) for _ in range(num_nodes)]

    def run_trial(self, num_nodes:int)->Set[int]:

        new_neighbors = set()
        for _ in range(num_nodes):
            new_neighbors.add(random.choice(self._node_ballot))
       
        self._node_ballot.extend(list(new_neighbors))
        self._node_ballot.append(self._num_nodes)

        self._num_nodes += 1
        return new_neighbors
    
def make_complete_graph(num_nodes:int)->Graph:   
    complete_graph = {
        v: 
        set([j for j in range(num_nodes) if j != v]) 
        for v in range(num_nodes)
        }
   
    return complete_graph
    
def make_PA_Graph(total_nodes, out_degree:int)->Graph:
   
    PA_graph = make_complete_graph(out_degree)
    trial = PATrial(out_degree)
    
    for v in range(out_degree, total_nodes):
        PA_graph[v] = trial.run_trial(out_degree)
    
    return PA_graph


if __name__=="__main__":
    g = make_PA_Graph(7000,50)
    plot_degree(g, 'Q2')

