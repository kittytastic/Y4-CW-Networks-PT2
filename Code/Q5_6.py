
from typing import Callable, List, Optional, Tuple, Set, Dict, TypeVar, Union, Any
from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from Utils import graph_subset
from Q4 import closeness_centrality
from graph_types import *
import time

Population = Dict['State', Set[Node]]
Transitions = Dict[Tuple['State', 'State'], float]
Metrics = Dict['State', List[int]]
VaccinationStrategy = Callable[[Graph, Population, int], Set[Node]]
_T = TypeVar("_T")
_S = TypeVar("_S")

class State(Enum):
    S = 1
    I = 2
    R = 3
    V = 4
    VI = 5

def verify_prob_dict(t: Transitions):
    REQUIRED_KEYS = {
            (State.I, State.S),
            (State.I, State.V),
            (State.VI, State.S),
            (State.VI, State.V)
        }

    if set(t.keys())!=REQUIRED_KEYS:
        raise Exception(f"Prob dict doesn't contain required keys\nRequired: {REQUIRED_KEYS}\nObserved: {set(t)}")

def add_to_metrics(m: Metrics, pop: Population)->Metrics:
    for s in State:
        m[s].append(len(pop[s]))
    
    return m

def _take_best(in_l: List[_T], key: Callable[[_T], Union[int, float]], val: Callable[[_T], _S], num: int, largest:bool = True)->List[_S]:
    sorted_l = sorted(in_l, key=key, reverse=largest)
    top_l = sorted_l[:min(len(sorted_l), num)]
    return [val(n) for n in top_l]

def random_vaccine(_: Graph, pop: Population, num: int)->Set[Node]:
    return set(random.sample(tuple(pop[State.S]), min(num, len(pop[State.S]))))

def global_most_at_risk(g: Graph, pop: Population, num: int)->Set[Node]:
    degree = [(n, len(g[n])) for n in pop[State.S]]
    return set(_take_best(degree, lambda x: x[1], lambda x: x[0], num))

def local_most_at_risk(g: Graph, pop: Population, num:int)->Set[Node]:
    i_neighbours = {n:0 for n in pop[State.S]}
    for i in pop[State.S]:
        for n in g[i]:
            if n in pop[State.I] or n in pop[State.VI]:
                i_neighbours[i]+=1

    i_neighbours_l = list(i_neighbours.items())
    return set(_take_best(i_neighbours_l, lambda x: x[1], lambda x: x[0], num))
    
def closeness_of_susceptible(g: Graph, pop: Population, num: int)->Set[Node]:
    sub_graph = graph_subset(g, pop[State.S])
    closeness = closeness_centrality(sub_graph)
    closeness_l = list(closeness.items())
    return set(_take_best(closeness_l, lambda x: x[1], lambda x:x[0], num))

def local_most_at_risk2(g: Graph, pop: Population, num:int)->Set[Node]:
    i_neighbours = {n:0 for n in pop[State.S]}
    all_infected = pop[State.I].union(pop[State.VI])
    for i in all_infected:
        #sn = g[i].intersection(pop[State.S])
        #for n in sn:
        #    i_neighbours[n]+=1
        for n in g[i]:
            if n in pop[State.S]:
                i_neighbours[n]+=1

    i_neighbours_l = list(i_neighbours.items())
    return set(_take_best(i_neighbours_l, lambda x: x[1], lambda x: x[0], num))


def simulate(
    g:Graph,
    t: Transitions,
    ti: int, 
    vaccine_strategy:VaccinationStrategy = random_vaccine, 
    vaccines_start:int=50,
    start_infected:int=5,
    rand_seed:int = 42
    )->Metrics:
    verify_prob_dict(t)
    random.seed(rand_seed)
    start_t = time.time()
    start_v = None

    metrics:Metrics = {s:[] for s in State} 

    all_people = tuple(g.keys())
    initial_infected = random.sample(all_people, start_infected)
    pop: Population = {
        State.S: set(all_people)-set(initial_infected),
        State.I: set(initial_infected),
        State.V:set(), State.VI: set(), State.R: set()
    }
    infection_tracker:Dict[Node,int] = {p: ti for p in initial_infected}
    metrics = add_to_metrics(metrics, pop)

    time_c=1
    print("Day 1")
    while len(pop[State.I])>0 or len(pop[State.VI])>0:
        if time_c%30==0:
            print(f"Day: {time_c}")

        # Deal with new vaccines
        if time_c>vaccines_start:
            if start_v == None:
                start_v = time.time()  
            to_vaccinate = vaccine_strategy(g, pop, 400)
            assert(len(to_vaccinate)<=400)
            pop[State.S]-=to_vaccinate
            pop[State.V] = pop[State.V].union(to_vaccinate)

        # Work out new infections
        new_I:Set[Node] = set()
        new_VI:Set[Node] = set()

        all_infections = pop[State.I].union(pop[State.VI])
        for i in all_infections:
            i_state = State.I if i in pop[State.I] else State.VI
            
            for n in g[i]:
                r = random.random()
                
                if n in pop[State.S]:
                    if r<t[(i_state, State.S)]:
                        new_I.add(n)
            
                if n in pop[State.V]:
                    if r<t[(i_state, State.V)]:
                        new_VI.add(n)

        # Update current infected
        new_R:Set[Node] = set()
        for p in infection_tracker.keys():
            infection_tracker[p]-=1

            if infection_tracker[p]==0:
                new_R.add(p)
        
        for r in new_R:
            infection_tracker.pop(r)
        
        pop[State.VI]-=new_R
        pop[State.I]-=new_R
        pop[State.R] = pop[State.R].union(new_R)

        # Add new infected
        pop[State.S]-=new_I
        pop[State.I] = pop[State.I].union(new_I)
        
        pop[State.V]-=new_VI
        pop[State.VI] = pop[State.VI].union(new_VI)
        
        for i in new_VI.union(new_I):
            infection_tracker[i] = ti

        metrics = add_to_metrics(metrics, pop)
        time_c += 1


    end_t = time.time()
    dt = end_t-start_t
    if start_v:
        v_rt = end_t-start_v
    else:
        v_rt = -1.0

    print(f"Final day: {time_c}")
    print(f"Runtime: {dt:.1f}s   ({v_rt:.1f}s in vaccine days)")
    print(f"Rate: {1000*(dt)/time_c:.2f} ms/day    ({1000*v_rt/(time_c-vaccines_start):.1f} ms/day in vaccine days)")

    return metrics

def poisson(n: int, m: int)->List[int]:
    dist:Any = np.zeros(n, dtype='int') #type:ignore

    filled = 0
    while filled!=n:
        new_dist:Any = np.random.poisson(m,n-filled) #type:ignore
        new_dist = new_dist[new_dist>0]
        dist[filled:filled+len(new_dist)] = new_dist # type:ignore
        filled+=len(new_dist)

    return list(dist)

def is_anticlockwise(num_nodes:Node, cur_node:Node, query_node: Node):
    cn_shift = cur_node+num_nodes
    qn_shift = query_node+num_nodes
    lb = cn_shift-num_nodes//2

    return (qn_shift>lb and qn_shift<cn_shift) or (query_node>lb and query_node<cn_shift)

def VDWS(n: int, m: int, rewire_prob: float, seed:Optional[int] = None)->Graph:
    if seed is None:
        seed = random.randrange(2**32 - 1)
    rng = random.Random(seed)
    np.random.seed(seed)

    g:Graph = {i:set() for i in range(n)}
    local_degrees = poisson(n,m)
    #print(f"Max local degree: {max(local_degrees)}")

    edges_c = 0
    for i in range(n):
        for j in range(i-local_degrees[i], i+local_degrees[i]+1):
            v = j % n
            if v==i:
                continue
            edges_c +=1
            g[i].add(v)
            g[v].add(i)

    rewire_c  = 0
    rewire_skip = 0
    rewired_edges:Set[Tuple[Node, Node]] = set()
    for i in range(n):
        for j in g[i]:
            if (i,j) in rewired_edges or is_anticlockwise(n, i, j):
                continue
                
            p = rng.random()
            if p < rewire_prob:
                v = rng.randint(0,n-1)
                if v!=i and v not in g[i]:
                    g[i].remove(j)
                    g[j].remove(i) 
                    g[i].add(v)
                    g[v].add(i)
                    rewired_edges.add((i,v))
                    rewired_edges.add((v,i))
                    rewire_c +=1
                else:
                    rewire_skip +=1
    
    #print(f"Edges: {edges_c}  Rewire: {rewire_c} Rewire Skip: {rewire_skip}  ({100*rewire_c/edges_c:.4f})  p:{100*rewire_prob}")
    #degrees = [len(v) for v in g.values()]
    #print(f"Max degree: {max(degrees)}")
    #print(f"Min degree: {min(degrees)}")
    #print(f"Mean degree: {100*sum(degrees)/len(degrees):.1f}")

    return g

def graph_metrics(metrics:Metrics, name:str="tmp-T3", scale:str='linear'):
    total_I = [metrics[State.I][i]+metrics[State.VI][i] for i in range(len(metrics[State.I]))]

    fig, axs = plt.subplots(2, 3, sharex=True, sharey='row')
    axs[0, 0].plot(metrics[State.S], 'tab:blue')
    axs[0, 0].set_title('Susceptible (S)')
    axs[0, 1].plot(metrics[State.V], 'tab:orange')
    axs[0, 1].set_title('Vaccinated (V)')
    axs[0, 2].plot(metrics[State.R], 'tab:green')
    axs[0, 2].set_title('Recovered (R)')
    
    axs[1, 0].plot(metrics[State.I], 'tab:red')
    axs[1, 0].set_title('Infected (I)')
    axs[1, 1].plot(metrics[State.VI], 'tab:red')
    axs[1, 1].set_title('Vac. & Infected (VI)')
    axs[1, 2].plot(total_I, 'tab:red')
    axs[1, 2].set_title('Total Infected (I+VI)')
    
    for ax in axs.flat:
        ax.set_yscale(scale)

    fig.supxlabel('Simulation Steps')
    fig.supylabel('Number of People')

    plt.savefig(f'Artifacts/{name}.png')


def seed_thrash():
    to = 1000000
    step = to/100
    for i in range(to):
        if i%step==0:
            print(f"{i}/{to} ({i*100/to}%)")
        
        _ = VDWS(10, 1, 0.01)


def test_diffrent_strategy(g:Graph):
    transmition_p:Transitions = {
            (State.I, State.S):0.01,
            (State.I, State.V):0.005,
            (State.VI, State.S):0.005,
            (State.VI, State.V):0.005
    }

    t_i = 3
    
    strats = [(random_vaccine, "Random"), (global_most_at_risk, "Global"), (local_most_at_risk2, "Local 2"), (local_most_at_risk, "Local")]

    for s, name in strats:
        print(f"------  {name}  ------")
        metrics = simulate(g, transmition_p, t_i, rand_seed=random.randint(0, int(10e6)), vaccine_strategy=s)
        graph_metrics(metrics, name=f'Q6-{name}-lin')
        graph_metrics(metrics, name=f'Q6-{name}-log', scale='log')

if __name__ == "__main__":
    transmition_p:Transitions = {
            (State.I, State.S):0.01,
            (State.I, State.V):0.01,
            (State.VI, State.S):0.01,
            (State.VI, State.V):0.01
    }

    t_i = 3

    g = VDWS(200000, 25, 0.01)
    #metrics = simulate(g, transmition_p, t_i, rand_seed=random.randint(0, int(10e6)))
    #graph_metrics(metrics)
    #graph_metrics(metrics, name='tmp-T3-log', scale='log')
    
    test_diffrent_strategy(g)

    exit()
    import Utils
    
    #sc = Utils.find_strong_componets(g)
    
    #for s in sc:
    #    print(f"Set of size: {len(s)}")

    import Q4
    nm = {k:f"N{k}" for k in g.keys()}
    dc = Q4.degree_centrality(g)

    print(f"Largest Degree: {Q4.get_best(dc, nm, top_count=5)}")
    print(f"Smallest Degree: {Q4.get_best(dc, nm,smallest=True, top_count=5)}")
   


