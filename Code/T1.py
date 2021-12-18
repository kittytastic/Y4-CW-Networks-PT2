from typing import List, Optional, Tuple, Set, Dict, Union

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
    return visited


def calc_set_weight(nodes: Set[int], weight_dict: Dict[int,int]):
    ws = [weight_dict[n] for n in nodes]
    return sum(ws)

def find_largest_k(g: Graph, weight_dict: Dict[int,int])->Set[int]:
    largest_k = set()
    largest_w = 0

    i=0
    for k, ns in g.items():
        if i%1000 == 0 and i>1:
            print(f"{i}/{len(g)}  ({i*100/len(g):.1f})")
        intersection = set(ns)
        for n in ns:
            intersection = intersection.intersection(g[n])

        set_w = calc_set_weight(intersection, weight_dict)
        if set_w>largest_w:
            largest_k = intersection
            largest_w = set_w
        
        i+=1

    return largest_k

def generate__largest_connected_components(graph: Graph, weight_dict: Dict[int,int])->Set[int]:
    cg = create_connection_graph(graph)
    print("P1")
    ucg = tf_g_to_undirected(cg)
    print("P2")
    return find_largest_k(ucg, weight_dict) 

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


def dfs_one(n:int, visited:Set[int], stack: List[int], g:Graph):
    visited.add(n)

    for m in g[n]:
        if m not in visited:
            dfs_one(m, visited, stack, g)
    
    stack.append(n)
    return stack

def graph_transpose(g:Graph)->Graph:
    tg = {k:set() for k in g.keys()}
    
    for k, v in g.items():
        for n in v:
            tg[n].add(k)

    return tg

def dfs_two(n: int, visited:Set[int], cc:Set[int], g:Graph):
    visited.add(n)
    cc.add(n)
    for m in g[n]:
        if m not in visited:
            dfs_two(m, visited, cc, g)

    return cc

def find_strong_componets(g: Graph):
    stack=[]
    visited=set()

    for v in g.keys():
        if v not in visited:
            dfs_one(v, visited, stack, g)

    g_t = graph_transpose(g)

    visited = set()
    strong_components = []

    while len(stack)>0:
        v = stack.pop()
        if v not in visited:
            strong_components.append(dfs_two(v, visited, set(), g_t)) 

    return strong_components

def merge_nodes(g:Graph, merge_sets: List[Set[int]])-> Tuple[Graph, Dict[int, int]]:
    new_g = {k:v for k,v in g.items()}
    weight_dict = {k:1 for k,v in g.items()}    


    for cs in merge_sets:
        cs_iter = iter(cs)
        new_node = next(cs_iter)
        for n in cs_iter:
            new_g[new_node].union(g[n])
            new_g.pop(n, None)

            weight_dict[new_node] += 1
            weight_dict.pop(n)

            for i in new_g.keys():
                if n in new_g[i]:
                    new_g[i].remove(n)
                    new_g[i].add(new_node)

    return new_g, weight_dict


def longest_path_dfs(n:int, visited:Set[int], longest_pl:Dict[int, int], longest_pl_bt:Dict[int, Union[int, None]], g:Graph):
    visited.add(n)

    for m in g[n]:
        if m not in visited:
            longest_path_dfs(m, visited, longest_pl, longest_pl_bt, g)
        
        if longest_pl[n]<longest_pl[m]+1:
            longest_pl[n] = longest_pl[m]+1
            longest_pl_bt[n] = m
    
def rebuild_path(n: int, longest_pl_bt, route: List[int]):
    route.append(n)
    m = longest_pl_bt[n]
    if m is None:
        return
    else:
        rebuild_path(m, longest_pl_bt, route)

def longest_path(g:Graph):
    visited=set()
    longest_pl = {k:1 for k in g.keys()} # TODO weight
    longest_pl_bt = {k:None for k in g.keys()}

    for v in g.keys():
        if v not in visited:
            longest_path_dfs(v, visited, longest_pl, longest_pl_bt, g)

    max_pl = 0
    max_p_start = None
    for  n, w in longest_pl.items():
        if max_pl<w:
            max_pl = w
            max_p_start = longest_pl_bt[n]

    max_p = []
    rebuild_path(max_p_start, longest_pl_bt, max_p)
    return max_p


def remove_self_cycles(g:Graph)->Graph:
    for n in g.keys():
        g[n].discard(n)
    
    return g


if __name__=="__main__":
    g= load_graph("./Datasets/alg_phys-cite.txt")
    '''
    g ={ 
         1: {2,3,4},
         2: {1,3,4},
         3: {2},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
    '''

    sc = find_strong_componets(g)
    total_combine = 0
    for c in sc:
        if len(c)>1:
            total_combine += len(c)-1
            #print(len(c)) 

    print(f"Can combine: {total_combine}   ({len(g)} -> {len(g)-total_combine})")
    mg,weight_dict = merge_nodes(g, sc)
    print(len(mg))
    mg = remove_self_cycles(mg)
    #check_if_acyclic(mg)
    #ck = generate__largest_connected_components(mg, weight_dict)
    lp = longest_path(mg)
    print(f"Weight of largest component: {calc_set_weight(lp, weight_dict)}")
    print(f"Largest connected component: {len(lp)}")