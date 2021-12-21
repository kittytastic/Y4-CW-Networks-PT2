from typing import List, Optional, Tuple, Set, Dict, Union
Graph = Dict[int, Set[int]]

def _check_if_acyclic_r(cur_node:int, g: Graph, visited: Set[int], cs: List[int]):
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
        _check_if_acyclic_r(k, graph, set(), [])


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

def plot_degree(g, file_name, title="Unnamed", node_subset = None):
    import matplotlib.pyplot as plt
    
    if node_subset is None:
        node_subset = set(g.keys())
    
    in_dist = normalize_distribution(build_distribution(in_degree(node_subset, g)))
    out_dist = normalize_distribution(build_distribution(out_degree(node_subset, g)))
    
    in_x, in_y = zip(*in_dist.items())
    out_x, out_y = zip(*out_dist.items())

    fig, axs = plt.subplots(1, 2, sharey=True)
    axs[0].loglog(in_x, in_y, marker='.', linestyle="None", color='tab:blue')
    axs[0].set_xlabel('In-Degree')
    axs[0].set_ylabel('Normalized Rate')
    axs[1].loglog(out_x, out_y, marker='.', linestyle="None", color='tab:orange')
    axs[1].set_xlabel('Out-Degree')

    fig.suptitle(title)
    plt.savefig(f'Artifacts/{file_name}.png')