####################################
# USEAGE:
# make the directory: ./Artifacts
# install the additional packages:
#       pip install scipy tabulate    
# run: python Q4.py
####################################

from typing import Callable, List, Tuple, Set, Dict, Union, Any

from tabulate import tabulate

from Utils import find_strong_componets, graph_subset
from graph_types import *

import heapq
import math

NodeNameMap = Dict[Node, Any]

def load_london(file_name:str)->Tuple[Graph, NodeNameMap]:
    g:Graph = {}
    station_id_map:Dict[Any, Node] = {}
    next_station_id = 0

    with open(file_name) as f:
        lines = f.readlines()

        for l in lines:
            segments = l.split()
            if len(segments)==0:
                continue

            for s in segments[1:]:
                if s not in station_id_map:
                    station_id_map[s]=next_station_id
                    g[next_station_id] = set()
                    next_station_id +=1

                            
            a, b = station_id_map[segments[1]], station_id_map[segments[2]]
            g[a].add(b)
            g[b].add(a)

    return g, {v:k for k,v in station_id_map.items()}

def load_roget(file_name: str)->Tuple[Graph,NodeNameMap]:
    g:Graph = {}
    with open(file_name) as f: 
        lines = f.readlines()

        edges_start = None
        for i, l in enumerate(lines):
            if l == "*Arcslist\n":
                edges_start = i+1
                break

        edge_lines = lines[edges_start:]

        for l in edge_lines:
            nodes = [int(n) for n in l.split()]

            for n in nodes:
                if n not in g:
                    g[n] = set()

            for n in nodes:
                for m in nodes:
                    if n!= m:
                        g[n].add(m)
                        g[m].add(n)            
    
    return g, {k:k for k in g.keys()}

def load_ccsb_y2h(file_name:str)->Tuple[Graph,NodeNameMap]:
    g:Graph = {}
    name_id_map:Dict[Any, Node] = {}
    next_id = 0
    
    with open(file_name) as f:
        lines = f.readlines()
        lines = lines[1:]
        for l in lines:
            segments = l.split()

            for c in segments[:2]:
                if c not in name_id_map:
                    name_id_map[c]=next_id
                    g[next_id] = set()
                    next_id +=1 

                            
            a, b = name_id_map[segments[0]], name_id_map[segments[1]]
            g[a].add(b)
            g[b].add(a)
        
    return g, {v:k for k,v in name_id_map.items()}

                
def dijkstras(start_node:Node, g:Graph)->Dict[Node, int]:
    out_dict:Dict[Node, int] = {}
    possible_weights: List[Tuple[int, Node]] = [(0, start_node)]
    left_to_visit = set(g.keys())

    while len(left_to_visit)>0:
        if len(possible_weights)==0:
            raise Exception("Graph is not connected")

        node_d, next_node = heapq.heappop(possible_weights)

        if next_node not in left_to_visit:
            continue
        
        left_to_visit.remove(next_node)
        out_dict[next_node] = node_d

        neighbors = [(node_d+1, n) for n in g[next_node] if n in left_to_visit]
        for n in neighbors:
            heapq.heappush(possible_weights, n)
        
    return out_dict

def min_path_dict(g:Graph)->Dict[int, Dict[int,int]]:
    return {n: dijkstras(n,g) for n in g.keys()}

def closeness_centrality(g:Graph)->Dict[Node, float]:
    min_path = min_path_dict(g)
    return {n: 1/sum(min_path[n].values()) for n in g.keys()}

def nearness_centrality(g: Graph)->Dict[Node, float]:
    min_path = min_path_dict(g)
    return {
            n: sum([1/d for d in min_path[n].values() if d!=0])
            for n in g.keys()
        }

def degree_centrality(g: Graph)->Dict[Node, int]:
    return {n: len(v) for n,v in g.items()}

def adjacency_centrality(g: Graph)->Dict[Node, float]:
    d = degree_centrality(g)
    out_dir:Dict[Node, float] = {}
    for j in g.keys():
        x = sum([(d[j]-d[i])/(d[j]+d[i]) for i in g[j] if i!=j])
        x *= 1/d[j]
        out_dir[j]=x

    return out_dir


def strip_to_largest_connected(g: Graph)->Graph:
    sc = find_strong_componets(g)
    largest_set:Set[Node] = set()
    for s in sc:
        if len(s)>len(largest_set):
            largest_set = s

    return graph_subset(g, largest_set)    

def get_best(d: Union[Dict[Node, float], Dict[Node, int]], name_map: Dict[int, Any],  top_count:int=20, smallest:bool=False)->List[Tuple[Any, Union[float,int]]]:
    to_sort = [(name_map[k], v) for k,v in d.items()]
    sorted_l = sorted(to_sort, key=lambda x: x[1], reverse=(not smallest))

    top_part = sorted_l[:top_count]
    last_v = top_part[-1][1]
    for i in range(top_count, len(to_sort)):
        if math.isclose(sorted_l[i][1], last_v):
            top_part.append(sorted_l[i])
        else:
            break

    return top_part 

def flatten(t: List[List[Tuple[Any, Union[float,int]]]])->List[Tuple[Any, ...]]:
    width = len(t)
    max_table_l = max([len(x) for x in t])

    out_t:List[Tuple[Any, ...]] = []
    for i in range(max_table_l):
        row:List[Any] = []
        for j in range(width):
            sec = t[j]
            if i<len(sec):
                row.append(sec[i][0])
                row.append(sec[i][1])
            else:
                row.append(None)
                row.append(None)

        out_t.append(tuple(row))
    
    return out_t



def generate_table(g: Graph, g_map: Dict[int, Any])->str:
    from tabulate import tabulate
    metrics:List[Union[Callable[[Graph], Dict[Node,float]], Callable[[Graph], Dict[Node,int]], ]] = [closeness_centrality, nearness_centrality, degree_centrality, adjacency_centrality]

    table = [get_best(m(g), g_map, top_count=20) for m in metrics]
    table=flatten(table)
    return tabulate(table, floatfmt=".3g", tablefmt="latex", headers=["Node", "Closeness", "Node", "Near.", "Node", "Deg.", "Node", "Adj."])

def center_table(tab:str)->str:
    return f'''\\begin{{center}}\n{tab}\n\\end{{center}}'''

def allow_wide_table(tab:str, margin_adjust:str="-1.2in")->str:
    return f'\\begin{{adjustwidth}}{{{margin_adjust}}}{{{margin_adjust}}}{tab}\\end{{adjustwidth}}'

def Q3():
    g = {
         1: {4},
         2: {4},
         3: {4},
         4: {1,2,3,5,6},
         5: {4},
         6: {4,7,8,9,10, 11},
         7: {6, 8, 11},
         8: {6, 7, 9, 11},
         9: {6,8,10},
         10: {6, 9, 11, 12},
         11: {6, 7, 8, 10},
         12: {10}
    }
    nodes = sorted(list(g.keys()))
    a = closeness_centrality(g)
    b = nearness_centrality(g)
    c = degree_centrality(g)
    d = adjacency_centrality(g)

    tab:List[Tuple[Any, ...]] = [(i, a[i], b[i], c[i], d[i]) for i in nodes]


    with open("Artifacts/Q3.tex", "w+") as f:
        f.write(
            center_table(
                tabulate(tab, floatfmt=".3g", tablefmt="latex", headers=['Node', 'Closeness', 'Nearness', 'Degree', 'Adjacency'])))


def Q4():
    lg, lg_map = load_london("Datasets/london_transport_raw.edges.txt")
    lg = strip_to_largest_connected(lg)
    print(f"Loaded London dataset: {len(lg)} nodes")
    print(f"London (strip) {len(lg)}")
    london_tab = generate_table(lg, lg_map)
    
    
    rg, rg_map = load_roget("Datasets/Roget.txt")
    rg = strip_to_largest_connected(rg)
    print(f"Loaded Roget dataset: {len(rg)} nodes")
    print(f"Roget (strip) {len(rg)}")
    rg_tab = generate_table(rg, rg_map)
    
    cg, cg_map = load_ccsb_y2h("Datasets/CCSB-Y2H.txt")
    cg = strip_to_largest_connected(cg)
    print(f"Loaded CCSB-Y2H: {len(cg)} nodes")
    print(f"CCSB-Y2H (strip) {len(cg)}")
    cg_tab = generate_table(cg, cg_map)

    with open("Artifacts/Q4.tex", "w+") as f:
        f.write(f"\\subsection*{{London}}\n")
        f.write(allow_wide_table(center_table(london_tab), margin_adjust="-1.3in"))
        f.write(f"\n\\subsection*{{Rodget}}\n")
        f.write(center_table(rg_tab))
        f.write(f"\n\\subsection*{{CCSB Y2H}}\n")
        f.write(allow_wide_table(center_table(cg_tab)))

def rank(d: Dict[Node, Union[int, float]])->Dict[Node, int]:
    l = list(d.items())
    sorted_l = sorted(l, key=lambda x: x[1])
    return {v[0]:idx+1 for idx, v in enumerate(sorted_l)}

def spear_rank(a: Dict[Node, Union[int, float]], b: Dict[Node, Union[int, float]])->float:
    from scipy.stats import spearmanr # type: ignore
    a_rank_map = rank(a)
    b_rank_map = rank(b)
    nodes = list(a.keys())
    a_ranked = [a_rank_map[n] for n in nodes]
    b_ranked = [b_rank_map[n] for n in nodes]

    return spearmanr(a_ranked, b_ranked)[0] # type: ignore


def Q4_additional():
    lg, _ = load_london("Datasets/london_transport_raw.edges.txt")
    lg = strip_to_largest_connected(lg)
    rg, _ = load_roget("Datasets/Roget.txt")
    rg = strip_to_largest_connected(rg)    
    cg, _ = load_ccsb_y2h("Datasets/CCSB-Y2H.txt")
    cg = strip_to_largest_connected(cg)
    
    ds = [("London", lg), ("Roget", rg), ("CCSB Y2H", cg)]
    tab:List[Tuple[Any, ...]] = []
    for name, g in ds:
        
        cl = closeness_centrality(g)
        near = nearness_centrality(g)
        cor1 = spear_rank(cl, near)

        deg = degree_centrality(g)
        adj = adjacency_centrality(g)
        cor2 = spear_rank(deg, adj) # type: ignore
        tab.append((name, cor1, cor2))

    with open("Artifacts/Q4-additional.tex", "w+") as f:
        f.write(center_table(tabulate(tab, headers=["Dataset", "Closness & Nearness", "Degree & Adjacency"], tablefmt='latex')))

if __name__ == "__main__":
    Q3()
    Q4()
    print("Calculating additional Info...")
    Q4_additional()

