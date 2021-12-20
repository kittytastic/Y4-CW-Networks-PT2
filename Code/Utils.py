

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