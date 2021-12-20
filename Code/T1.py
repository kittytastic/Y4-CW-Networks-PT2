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

def calc_set_weight(nodes: Set[int], weight_dict: Dict[int,int]):
    ws = [weight_dict[n] for n in nodes]
    return sum(ws)

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


def longest_path_dfs(n:int, visited:Set[int], longest_pl:Dict[int, int], longest_pl_bt:Dict[int, Union[int, None]], weight_dict, g:Graph):
    visited.add(n)

    for m in g[n]:
        if m not in visited:
            longest_path_dfs(m, visited, longest_pl, longest_pl_bt, weight_dict, g)
        
        if longest_pl[n]<longest_pl[m]+weight_dict[m]:
            longest_pl[n] = longest_pl[m]+weight_dict[m]
            longest_pl_bt[n] = m
    
def rebuild_path(n: int, longest_pl_bt, route: List[int]):
    route.append(n)
    m = longest_pl_bt[n]
    if m is None:
        return
    else:
        rebuild_path(m, longest_pl_bt, route)

def longest_path(g:Graph, weight_dict: Dict[int, int]):
    visited=set()
    longest_pl = {k:weight_dict[k] for k in g.keys()} # TODO weight
    longest_pl_bt = {k:None for k in g.keys()}

    for v in g.keys():
        if v not in visited:
            longest_path_dfs(v, visited, longest_pl, longest_pl_bt, weight_dict, g)

    max_pl = 0
    max_p_start = None
    for  n, w in longest_pl.items():
        if max_pl<w:
            max_pl = w
            max_p_start = n

    max_p = []
    rebuild_path(max_p_start, longest_pl_bt, max_p)
    return max_p


def remove_self_cycles(g:Graph)->Graph:
    for n in g.keys():
        g[n].discard(n)
    
    return g

def unmerge_nodes(nodes:Set[int], merged_nodes: List[Set[int]])->Set[int]:
    out_set = set()

    for n in nodes:
        out_set.add(n)

        for s in merged_nodes:
            if n in s:
                out_set = out_set.union(s)

    return out_set

def largest_unilateral_strong_component(g:Graph):
    sc = find_strong_componets(g)
    mg,weight_dict = merge_nodes(g, sc)
    mg = remove_self_cycles(mg) 
    lp = longest_path(mg, weight_dict)
    largest_set = unmerge_nodes(lp, sc)
    return largest_set


def in_degree(nodes:Set[int], g:Graph)->Dict[int,int]:
    out_dict = {n:0 for n in nodes}
    for n in nodes:
        for m in nodes:
            if n in g[m]:
                out_dict[n]+=1

    return out_dict

def out_degree(nodes: Set[int], g:Graph)->Dict[int,int]:
    return {n:len(g[n].intersection(nodes)) for n in nodes} 


def build_distribution(observed: Dict[int,int])->Dict[int,int]:
    out_dict = {}
    for c in observed.values():
        if c in out_dict:
            out_dict[c]+=1
        else:
            out_dict[c]=1

    return out_dict

def normalize_distribution(dist: Dict[int, int])->Dict[int, float]:
    total = sum(dist.values())
    return {k: v/total for k,v in dist.items()}


def Q1():
    import matplotlib.pyplot as plt
    
    g = load_graph("./Datasets/alg_phys-cite.txt")
    lc = largest_unilateral_strong_component(g)
    print(f"Largest strong component: {len(lc)} nodes")
    
    in_dist = normalize_distribution(build_distribution(in_degree(lc, g)))
    out_dist = normalize_distribution(build_distribution(out_degree(lc, g)))
    
    in_x, in_y = zip(*in_dist.items())
    out_x, out_y = zip(*out_dist.items())

    fig, axs = plt.subplots(1, 2, sharey=True)
    axs[0].loglog(in_x, in_y, marker='.', linestyle="None", color='tab:blue')
    axs[0].set_xlabel('In-Degree')
    axs[0].set_ylabel('Normalized Rate')
    axs[1].loglog(out_x, out_y, marker='.', linestyle="None", color='tab:orange')
    axs[1].set_xlabel('Out-Degree')

    fig.suptitle('Degree Distribution of Largest Connected Component In Citation Graph')
    plt.savefig('Artifacts/Q1-citations.png')

if __name__=="__main__":
    Q1()