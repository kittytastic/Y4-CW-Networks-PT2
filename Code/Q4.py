from typing import List, Optional, Tuple, Set, Dict, Union
from Utils import Graph, find_strong_componets
import heapq

def load_london(file_name)->Graph:
    g = {}
    station_id_map = {}
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

def load_roget(file_name: str)->Graph:
    g = {}
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

def load_ccsb_y2h(file_name:str)->Graph:
    g = {}
    name_id_map = {}
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

                
def dijkstras(start_node:int, g:Graph)->Dict[int, int]:
    out_dict = {}
    possible_weights: List[Tuple(int, int)] = [(0, start_node)]
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

def closeness_centrality(g:Graph)->Dict[int, float]:
    min_path = min_path_dict(g)
    return {n: 1/sum(min_path[n].values()) for n in g.keys()}

def nearness_centrality(g: Graph)->Dict[int, float]:
    min_path = min_path_dict(g)
    return {
            n: sum([1/d for d in min_path[n].values() if d!=0])
            for n in g.keys()
        }

def degree_centrality(g: Graph)->Dict[int, int]:
    return {n: len(v) for n,v in g.items()}

def adjacency_centrality(g: Graph)->Dict[int, int]:
    d = degree_centrality(g)
    out_dir = {}
    for j in g.keys():
        x = sum([(d[j]-d[i])/(d[j]+d[i]) for i in g[j] if i!=j])
        x *= 1/d[j]
        out_dir[j]=x

    return out_dir


def strip_graph(g:Graph, nodes:Set[int])->Graph:
    return {n: g[n].intersection(nodes) for n in nodes}


def strip_to_largest_connected(g: Graph)->Graph:
    sc = find_strong_componets(g)
    largest_set = set()
    for s in sc:
        if len(s)>len(largest_set):
            largest_set = s

    return strip_graph(g, largest_set)    


if __name__ == "__main__":
    lg, lg_map = load_london("Datasets/london_transport_raw.edges.txt")
    lg = strip_to_largest_connected(lg)
    print(f"Loaded London dataset: {len(g)} nodes")
    print(f"London (strip) {len(lg)}")
    
    exit()
    rg, rg_map = load_roget("Datasets/Roget.txt")
    rg = strip_to_largest_connected(rg)
    print(f"Loaded Roget dataset: {len(g)} nodes")
    print(f"Roget (strip) {len(rg)}")
    cg, cg_map = load_ccsb_y2h("Datasets/CCSB-Y2H.txt")
    cg = strip_to_largest_connected(cg)
    print(f"Loaded CCSB-Y2H: {len(g)} nodes")
    print(f"CCSB-Y2H (strip) {len(cg)}")

