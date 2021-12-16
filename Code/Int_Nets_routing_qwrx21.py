from typing import List, Optional, Tuple, Set

############################## Q15 #################################
Node=List[int]

def remap_node(node:Node, mapper: List[int])->Node:
    new_node = [mapper[l] for l in node]
    return new_node

def generate_mappers(n:int, renorm_node: Node)->Tuple[List[int], List[int]]:
    to_remapper = [-1]*n
    from_remapper = [-1]*n
    for i, v in enumerate(renorm_node):
        to_remapper[v]=i
        from_remapper[i]=v

    return to_remapper, from_remapper

def bubble_sort(n: int, start_l: Node)->List[Node]:

    path:List[Node] = []
    current_node = list(start_l)

    path.append(list(current_node))

    for i in range(n):
        for j in range(0, n-i-1):
            if current_node[j]>current_node[j+1]:
                current_node[j], current_node[j+1] = current_node[j+1], current_node[j]
                path.append(list(current_node))

    return path


def bubblesort_routing(n: int, source:Node, destination:Node)->List[Node]:
    prob_calc_remapper, calc_prob_remapper = generate_mappers(n, destination)
    r_source = remap_node(source, prob_calc_remapper)

    path = bubble_sort(n, r_source)    
    path = [remap_node(n, calc_prob_remapper) for n in path]

    return path

    
############################## Q16 #################################
EncodedNode = Tuple[int, ...]


def hamming_distance(node_a:Node, node_b:Node)->int:
    d = 0
    for a, b in zip(node_a, node_b):
        if a!=b:
            d+=1

    return d


def flip_bit(b: int, node:Node)->Node:
    assert b<len(node)
    new_node = list(node)
    new_node[b] = 1 if new_node[b]==0 else 0
    return new_node


def encode_node(node:Node)->EncodedNode:
    return tuple(node)


def build_dead_channel_set(n:int, faulty_node:List[Node], faulty_channels:List[Tuple[Node, Node]])->Set[Tuple[EncodedNode, EncodedNode]]:
    dc_set = set()
    
    for fc in faulty_channels:
        c = (encode_node(fc[0]), encode_node(fc[1]))
        dc_set.add(c)

    for fn in faulty_node:
       n1 = encode_node(fn)
       for i in range(n):
           n2 = flip_bit(i, fn)
           n2 = encode_node(n2)

           dc_set.add((n1, n2))
           dc_set.add((n2,n1))

    return dc_set

AStarData = Tuple[int, int, int, Node, Optional[Node]]

def select_expand_node(search_nodes: List[AStarData])->Tuple[AStarData, List[AStarData]]:
    assert len(search_nodes)>0

    f,g,_,_,_ = search_nodes[0]
    best_f = f
    best_g = g
    best_idx = 0

    for i in range(len(search_nodes)):
        f,g,_,_,_ = search_nodes[i]

        if f < best_f:
            best_f = f
            best_g = g
            best_idx = i

        if f == best_f and g>best_g:
            best_g = g
            best_idx = i

    best_data = search_nodes[best_idx]
    del search_nodes[best_idx]

    return best_data, search_nodes

def build_path(final_node:AStarData, visited_data:List[AStarData]):

    backwards_path = [final_node[3]]
    prev_node = final_node[4]

    while prev_node != None:
        backwards_path.append(prev_node)
        prev_data = None

        for vn in visited_data:
            if vn[3]==prev_node:
                prev_data = vn
                break
        assert prev_data != None
    
        prev_node = prev_data[4]

    backwards_path.reverse()
    return backwards_path




def AStarSearch(n: int, source:Node, destination: Node, dead_channels: Set[Tuple[EncodedNode, EncodedNode]])->List[Node]:

    start_data = (hamming_distance(source, destination), 0, hamming_distance(source, destination),  source, None)
    search_nodes = [start_data]
    visited_nodes = set(encode_node(source))
    visited_data = []

    arrived = False 
    while len(search_nodes)>0 and not arrived:
        curr_node, search_nodes = select_expand_node(search_nodes)
        if curr_node[3]==destination:
            arrived = True
            break

        _,g,_,node, _ = curr_node
        en = encode_node(node)

        visited_nodes.add(encode_node(node))
        visited_data.append(curr_node)

        for i in range(n):
            neighbour = flip_bit(i, node)
            enn = encode_node(neighbour)
            if (en, enn) not in dead_channels and enn not in visited_nodes:
                n_g = g+1
                n_h = hamming_distance(neighbour,destination)
                n_f = n_g+n_h
                search_nodes.append((n_f, n_g, n_h, neighbour, node))

    if not arrived:
        curr_node = start_data

    return build_path(curr_node, visited_data)


def faulty_hypercube_routing(n: int, source: Node, destination: Node, faulty_nodes: List[Node], faulty_channels: List[Tuple[Node, Node]])->List[Node]:
    dead_channels = build_dead_channel_set(n, faulty_nodes, faulty_channels)
    return AStarSearch(n, source, destination, dead_channels)