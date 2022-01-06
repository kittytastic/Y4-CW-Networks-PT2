
from typing import Callable, List, Optional, Tuple, Set, Dict, TypeVar, Union, Any
from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from Utils import edge_count, graph_subset
from Q4 import closeness_centrality
from graph_types import *
import time

############################ Datastructures #############################
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


############################ Vaccine Strategies ##############################
def _take_best(in_l: List[_T], key: Callable[[_T], Union[int, float]], val: Callable[[_T], _S], num: int, largest:bool = True)->List[_S]:
    sorted_l = sorted(in_l, key=key, reverse=largest)
    top_l = sorted_l[:min(len(sorted_l), num)]
    return [val(n) for n in top_l]

def random_vaccine(_: Graph, pop: Population, num: int)->Set[Node]:
    return set(random.sample(tuple(pop[State.S]), min(num, len(pop[State.S]))))

def global_most_at_risk(g: Graph, pop: Population, num: int)->Set[Node]:
    degree = [(n, len(g[n])) for n in pop[State.S]]
    return set(_take_best(degree, lambda x: x[1], lambda x: x[0], num))
    
def closeness_of_susceptible(g: Graph, pop: Population, num: int)->Set[Node]:
    sub_graph = graph_subset(g, pop[State.S])
    closeness = closeness_centrality(sub_graph)
    closeness_l = list(closeness.items())
    return set(_take_best(closeness_l, lambda x: x[1], lambda x:x[0], num))

def local_most_at_risk(g: Graph, pop: Population, num:int)->Set[Node]:
    i_neighbours = {n:0 for n in pop[State.S]}
    all_infected = pop[State.I].union(pop[State.VI])
    for i in all_infected:
        for n in g[i]:
            if n in pop[State.S]:
                i_neighbours[n]+=1

    i_neighbours_l = list(i_neighbours.items())
    return set(_take_best(i_neighbours_l, lambda x: x[1], lambda x: x[0], num))

def local_most_at_risk_2_step(g: Graph, pop: Population, num:int)->Set[Node]:
    s1_risk = {n:0 for n in pop[State.S]}
    all_infected = pop[State.I].union(pop[State.VI])
    for i in all_infected:
        for n in g[i]:
            if n in pop[State.S]:
                s1_risk[n]+=1

    for p in s1_risk.keys():
        s1_risk[p]*=len(pop[State.S].intersection(g[p]))

    s1_risk = list(s1_risk.items())
    return set(_take_best(s1_risk, lambda x: x[1], lambda x: x[0], num))

########################## Simulation ##############################
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


def add_to_metrics(m: Metrics, pop: Population)->Metrics:
    for s in State:
        m[s].append(len(pop[s]))
    
    return m


########################## VDWS ##############################
def poisson(n: int, m: int)->List[int]:
    dist:Any = np.zeros(n, dtype='int') #type:ignore

    filled = 0
    while filled!=n:
        new_dist:Any = np.random.poisson(m,n-filled) #type:ignore
        new_dist = new_dist[new_dist>0]
        dist[filled:filled+len(new_dist)] = new_dist # type:ignore
        filled+=len(new_dist)

    return list(dist)

def VDWS_base(n:int, local_degrees:List[int])->Graph:
    assert(n==len(local_degrees))
    g:Graph = {i: set() for i in range(n)}
    for node in g:
        for idx in range(1, local_degrees[node]+1):
            f_neighbour = (node+idx)%n
            g[node].add(f_neighbour)
            g[f_neighbour].add(node)

            b_neighbour = (node-idx)%n
            g[node].add(b_neighbour)
            g[b_neighbour].add(node)

    return g

def rewire_trial(g: Graph, n:int, p:float, node:Node, neighbour:Node, l:int, rng:random.Random)->Tuple[Graph, bool]:
    lower_offset = (n-1)//2
    upper_offset = (n-1)-lower_offset

    rewire = False 
    #print(f"Edge {node}->{neighbour}   [{l}]")
    p_trial = rng.random()

    if p_trial<p:
        new_n_offset = rng.randint(-lower_offset, upper_offset)
        new_n = (node+new_n_offset)%n
        
        #print(f"Thinking about rewiring: {node}->{new_n} [{new_n_offset}]")
        if new_n not in g[node] and new_n!=node:
            #print(f"Valid rewiring")
            g[node].remove(neighbour)
            g[neighbour].remove(node)

            assert(node not in g[new_n])
            assert(new_n not in g[node])
            g[node].add(new_n)
            g[new_n].add(node)
            rewire = True

    return g, rewire


def VDWS_rewire(g: Graph, n:int, p: float, local_degrees:List[int], rng:random.Random)->Tuple[Graph, int]:
    rewire_c = 0
    for node in g:
        for l in range(1, local_degrees[node]+1):
            neighbour = (node-l)%n
            if local_degrees[neighbour]<l:
                #print(f"Backwards trial {node}->{neighbour}")
                g, rw = rewire_trial(g,n,p,node, neighbour, l,rng)
                rewire_c += rw
       
        for l in range(1, local_degrees[node]+1):
            neighbour = (node+l)%n
            g, rw = rewire_trial(g,n,p,node, neighbour, l,rng)
            rewire_c += rw

    return g, rewire_c


def VDWS(n:int,m:int,p:float, rnd_seed:Optional[int]=None, debug:bool = False)->Graph:
    if rnd_seed is None:
        rnd_seed = random.randrange(2**32 - 1)
    rng = random.Random(rnd_seed)
    np.random.seed(rnd_seed)
    
    ld = poisson(n,m)
    g = VDWS_base(n, ld)
    ec_1 = edge_count(g)    
    g, rewire_c = VDWS_rewire(g,n,p,ld,rng)
    ec_2 = edge_count(g)

    assert(ec_1==ec_2)
    
    if debug:
        rewire_pc = float(rewire_c)/(float(ec_2)/2)
        print(f"Edge count: {ec_2}")
        print(f"Rewired: {rewire_c}   ({rewire_pc:.3f})")
        degrees = [len(v) for v in g.values()]
        print(f"Max degree: {max(degrees)}")
        print(f"Min degree: {min(degrees)}")
        print(f"Mean degree: {sum(degrees)/len(degrees):.1f}")

    return g

########################## Trials and Metrics ##############################
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


def test_diffrent_strategy(g:Graph):
    transmition_p:Transitions = {
            (State.I, State.S):0.01,
            (State.I, State.V):0.005,
            (State.VI, State.S):0.005,
            (State.VI, State.V):0.005
    }

    t_i = 3
    
    strats = [(random_vaccine, "Random"), (global_most_at_risk, "Global"), (local_most_at_risk, "Local"), (local_most_at_risk_2_step, "Local - 2 step")]

    rs = random.randint(0, int(10e6))
    for s, name in strats:
        print(f"------  {name}  ------")
        metrics = simulate(g, transmition_p, t_i, rand_seed=rs, vaccine_strategy=s)
        graph_metrics(metrics, name=f'Q6-{name}-lin')
        graph_metrics(metrics, name=f'Q6-{name}-log', scale='log')

if __name__ == "__main__":
    g = VDWS(200_000, 25, 0.01, rnd_seed=42)
    test_diffrent_strategy(g)

   
   


