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
    for k, ns in d_graph.items():
        for n in ns:
            d_graph[n].add(k)

    return d_graph 


def connected_dfs(cur_node:int, visited:Set[int], graph: Graph):
    visited.add(cur_node)
    for n in graph[cur_node]:
        if n not in visited:
            connected_dfs(n, visited, graph)
        else:
            print("Cycle")
    return visited

def find_largest_k(g: Graph)->Set[int]:
    largest_k = set()

    for k, ns in g.items():
        #if k%1000 == 0 and k>1:
        print(f"{k}/{len(g)}  ({k*100/len(g):.1f})")
        intersection = set(ns)
        for n in ns:
            intersection = intersection.intersection(g[n])

        if len(intersection)>len(largest_k):
            largest_k = intersection

    return largest_k

def generate__largest_connected_components(graph: Graph)->Set[int]:
    cg = create_connection_graph(graph)
    print("P1")
    ucg = tf_g_to_undirected(cg)
    print("P2")
    return find_largest_k(ucg) 

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

def check_if_acyclic_r(cur_node:int, g: Graph, visited: Set[int], cs: List[int]):
    lcs = list(cs)
    lcs.append(cur_node)
    visited.add(cur_node)
    for n in g[cur_node]:
        if n in lcs:
            print(f"Cycle: {lcs[lcs.index(n):]}->{cur_node}->{n}")

        if n not in visited:
            check_if_acyclic_r(n, g, visited, lcs)
        
    return visited

def check_if_acyclic(graph:Graph):    
    keys = list(graph.keys())
    for i in range(len(keys)):
        if i%1000==0 and i>0:
            print(f"{i}/{len(keys)}  ({i*100/len(keys):.1f})")
        k = keys[i]
        check_if_acyclic_r(k, graph, set(), [])

if __name__=="__main__":
    g= load_graph("./Datasets/alg_phys-cite.txt")
    check_if_acyclic(g)
    #ck = generate__largest_connected_components(g)
    #print(f"Largest connected component: {len(ck)}")