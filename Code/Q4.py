from Utils import Graph

def load_london(file_name)->Graph:
    g = {}
    station_id_map = {}
    id_station_map = {}
    next_station_id = 0

    with open(file_name) as f:
        lines = f.readlines()

        for l in lines:
            segments = l.split(" ")
            if len(segments)==0:
                continue

            for s in segments[1:]:
                if s not in station_id_map:
                    station_id_map[s]=next_station_id
                    id_station_map[next_station_id]=s
                    next_station_id +=1

                if s not in g:
                    g[station_id_map[s]] = set()

                            
            a, b = station_id_map[segments[1]], station_id_map[segments[2]]
            g[a].add(b)
            g[b].add(a)

    print(f"Loaded London dataset: {len(g)} nodes")
    return g, id_station_map

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
    
    print(f"Loaded Roget dataset: {len(g)} nodes")
    return g

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
                    next_id +=1

                if c not in g:
                    g[name_id_map[c]] = set()

                            
            a, b = name_id_map[segments[0]], name_id_map[segments[1]]
            g[a].add(b)
            g[b].add(a)
        
    print(f"Loaded CCSB-Y2H: {len(g)} nodes")
    return g

                



if __name__ == "__main__":
    #lg, _ = load_london("Datasets/london_transport_raw.edges.txt")
    rg = load_roget("Datasets/Roget.txt")
    cg = load_ccsb_y2h("Datasets/CCSB-Y2H.txt")


