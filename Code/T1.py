from typing import List, Optional, Tuple, Set, Dict

Graph = Dict[int, Set[int]]

def load_graph(graph_txt)->Graph:
    """
    Loads a graph from a text file.
    Then returns the graph as a dictionary.
    """
    graph = open(graph_txt)
    
    answer_graph = {}
    nodes = 0
    for line in graph:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))
        nodes += 1
    print ("Loaded graph with", nodes, "nodes")
    
    return answer_graph


def tf_g_to_undirected(d_graph:Graph)->Graph:
    u_graph = {k:set() for k in d_graph.keys()}

    for k, ns in d_graph.items():
        for n in ns:
            u_graph[k].add(n)
            u_graph[n].add(k)

    return u_graph


def connected_dfs(cur_node:int, visited:Set[int], graph: Graph):
    visited.add(cur_node)
    for n in graph[cur_node]:
        if n not in visited:
            connected_dfs(n, visited, graph)
    return visited

def generate__largest_connected_components(graph: Graph)->Set[int]:
    nodes_to_visit = set(graph.keys())
    largest_component = set()

    while len(nodes_to_visit)>0:
        n = next(iter(nodes_to_visit))
        cc = connected_dfs(n, set(), graph)

        if len(cc)>len(largest_component):
            largest_component = cc

        nodes_to_visit-=cc
        print(f"Found CC len: {len(cc)}  Updated to visit: {len(nodes_to_visit)}")

    return largest_component 

def create_connection_graph(d_graph:Graph)->Graph:    
    out_dict = {}
    keys = list(d_graph.keys())
    for i in range(len(keys)):
        if i%1000==0 and i>0:
            print(f"{i}/{len(keys)}  ({i*100/len(keys):.1f})")
        k = keys[i]
        out_dict[k]=connected_dfs(k, set(), d_graph)
        
    
    #return {k:connected_dfs(k, set(), d_graph) for k in d_graph.keys()}
    return out_dict

if __name__=="__main__":
    g= load_graph("./Datasets/alg_phys-cite.txt")
    #create_connection_graph(g)
    p1 = create_connection_graph(g)
    print("Fin P1")
    c_g = tf_g_to_undirected(p1)
    print(len(generate__largest_connected_components(g)))