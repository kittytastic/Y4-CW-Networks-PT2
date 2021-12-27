
from typing import Callable, Iterable, List, Optional, Tuple, Set, Dict, Union, Any
from enum import Enum
import random
import numpy as np
from numpy.random.mtrand import rand


Node = int
Population = Dict['State', Set[Node]]
Transitions = Dict[Tuple['State', 'State'], float]
Graph = Dict[Node, Set[Node]]
Metrics = Dict['State', List[int]]
VaccinationStrategy = Callable[[Graph, Population, int], Set[Node]]

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

def random_vaccine(_: Graph, pop: Population, num: int)->Set[Node]:
    return set(random.sample(tuple(pop[State.S]), num))

def simulate(g:Graph, t: Transitions, ti: int, vaccine_strat:VaccinationStrategy = random_vaccine, rand_seed:int = 42, start_infected:int=5)->Metrics:
    random.seed(rand_seed)

    metrics:Metrics = {s:[] for s in State} 

    all_people = tuple(g.keys())
    initial_infected = random.sample(all_people, start_infected)
    pop: Population = {
        State.S: set(all_people),
        State.I: set(initial_infected),
        State.V:set(), State.VI: set(), State.R: set()
    }
    infection_tracker:Dict[Node,int] = {p: ti for p in initial_infected}
    metrics = add_to_metrics(metrics, pop)

    while len(pop[State.S])>0 or len(pop[State.I])>0 or len(pop[State.VI])>0:
        # Deal with new vaccines
        to_vaccinate = vaccine_strat(g, pop, 400)
        pop[State.S]-=to_vaccinate
        pop[State.V] = pop[State.V].union(to_vaccinate)

        # Work out new infections
        new_I:Set[Node] = set()
        new_VI:Set[Node] = set()

        all_infections = pop[State.I].union(pop[State.VI])
        for i in all_infections:
            i_state = State.I if all_infections in pop[State.I] else State.VI
            
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
        
        for r in infection_tracker.keys():
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


def VDWS(n: int, m: int, rewire_prob: float)->Graph:
    g:Graph = {i:set() for i in range(n)}
    local_degrees = poisson(n,m)

    for i in range(n):
        for j in range(-local_degrees[i], local_degrees[i]+1):
            v = j % n
            g[i].add(v)
            g[v].add(i)

    rewired_edges:Set[Tuple[Node, Node]] = set()
    for i in range(n):
        for j in g[i]:
            if (i,j) in rewired_edges:
                continue
                
            p = random.random()
            if p < rewire_prob:
                v = random.randint(0,n-1)
                if v!=i and v not in g[i]:
                    g[i].remove(j)
                    g[j].remove(i)
                    g[i].add(v)
                    g[v].add(i)
                    rewired_edges.add((i,v))
                    rewired_edges.add((v,i))
                
    return g


if __name__ == "__main__":
    transmition_p:Transitions = {
            (State.I, State.S):0.01,
            (State.I, State.V):0.01,
            (State.VI, State.S):0.01,
            (State.VI, State.V):0.01
    }

    t_i = 2

    print()
   
    
    verify_prob_dict(transmition_p)


