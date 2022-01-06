import unittest
from unittest.mock import MagicMock
import numpy as np
from Q5_6 import *
from Utils import edge_count

class TestPoision(unittest.TestCase):
    def test_p_1(self):
        np.random.seed(42)
        n = 5 
        m = 10

        x = poisson(n,m)
        self.assertEqual(len(x), n)
    
    def test_p_2(self):
        np.random.seed(42)
        n = 1000000 
        m = 10

        x = poisson(n,m)
        self.assertEqual(len(x), n)
        self.assertTrue(np.all(x!=0)) #type:ignore

class TestVDWS(unittest.TestCase):
    def test_p_1(self):
        n = 10 
        m = 1
        p = 0.01
        seed = 239781413

        VDWS(n,m, p, rnd_seed=seed)

    def test_p_2(self):
        n = 10 
        m = 3
        p = 0.01
        seed = 3902944517

        VDWS(n,m, p, rnd_seed=seed)
    
    def test_p_3(self):
        n = 20 
        m = 10
        p = 0.01
        seed = 1045711233

        VDWS(n,m, p, rnd_seed=seed)
    
    def test_p_4(self):
        n = 2000 
        m = 25
        p = 0.01
        seed = 1868584733 

        VDWS(n,m, p, rnd_seed=seed)
    
    def test_p_5(self):
        n = 10
        m = 1
        p = 0.01
        seed = 2540674012 

        VDWS(n,m, p, rnd_seed=seed)
    
    def test_p_6(self):
        n = 10
        m = 1
        p = 1
        seed = 2540674012 

        VDWS(n,m, p, rnd_seed=seed)
    
    def test_1(self):
        VDWS(7, 1, 1.0, rnd_seed=3567099385)
    
    def test_2(self):
        VDWS(200_000, 25, 0.01)

class TestSIM(unittest.TestCase):
    def xtest_sim_1(self):
        transmition_p:Transitions = {
            (State.I, State.S):0.00,
            (State.I, State.V):0.00,
            (State.VI, State.S):0.00,
            (State.VI, State.V):0.00
        }   

        t_i = 2
        g = VDWS(20, 5, 0.01, rnd_seed=42)

        metrics = simulate(g, transmition_p, t_i)
        self.assertEqual(len(metrics[State.I]), 2)
    
    def test_sim_2(self):
        transmition_p:Transitions = {
            (State.I, State.S):1.00,
            (State.I, State.V):0.00,
            (State.VI, State.S):0.00,
            (State.VI, State.V):0.00
        }   

        t_i = 2
        g = VDWS(20, 5, 0.01, rnd_seed=42)

        metrics = simulate(g, transmition_p, t_i)
        self.assertEqual(metrics[State.R][-1], 20)


class TestGlobalMostAtRisk(unittest.TestCase):
   def test_gmar_1(self):
      in_g = {
         1: {3,4},
         2: {3,4},
         3: {1,2,4},
         4: {1,2,3,5},
         5: {6,7,4},
         6: {5,7},
         7: {5,6}
      } 
      in_pop = {State.S: {1,2,3,5,6,7}}
      expected = {3,5}

      self.assertEqual(expected, global_most_at_risk(in_g, in_pop, 2))

class TestLocalMostAtRisk(unittest.TestCase):
    def test_lmar_1(self):
      in_g = {
         1: {3,4},
         2: {3,4},
         3: {1,2,4},
         4: {1,2,3,5},
         5: {6,7,4},
         6: {5,7},
         7: {5,6}
      } 
      in_pop = {State.S: {1,3,5,6,7}, State.I:{4}, State.VI:{2}}
      expected = {1,3,5}

      self.assertEqual(expected, local_most_at_risk(in_g, in_pop, 3))
    
    def test_lmar_2(self):
      in_g = {
         1: {3,4},
         2: {3,4},
         3: {1,2,4},
         4: {1,2,3,5},
         5: {6,7,4},
         6: {5,7},
         7: {5,6}
      } 
      in_pop:Population = {State.S: {1,2,3,4,5,7}, State.I:{6}, State.VI:set()}
      expected = {5,7}

      self.assertEqual(expected, local_most_at_risk(in_g, in_pop, 2))

class TestLocalMostAtRiskWeighted(unittest.TestCase):
    def test_lmar_1(self):
      in_g = {
         1: {3,4},
         2: {3,4},
         3: {1,2,4},
         4: {1,2,3,5},
         5: {6,7,4},
         6: {5,7},
         7: {5,6}
      } 
      in_pop = {State.S: {1,3,5,6,7}, State.I:{4}, State.VI:{2}}
      expected = {1,3,5}

      self.assertEqual(expected, local_most_at_risk(in_g, in_pop, 3))
    
    def test_lmar_2(self):
      in_g = {
         1: {3,4},
         2: {3,4},
         3: {1,2,4},
         4: {1,2,3,5},
         5: {6,7,4},
         6: {5,7},
         7: {5,6}
      } 
      in_pop:Population = {State.S: {1,2,3,4,5,7}, State.I:{6}, State.VI:set()}
      expected = {5,7}

      self.assertEqual(expected, local_most_at_risk(in_g, in_pop, 2))

class TestVDWSBase(unittest.TestCase):
    def test_1(self):
        n = 5
        ld = [1,1,1,1,1]

        excpected = {0: {4,1}, 1:{0,2}, 2:{1,3}, 3:{2,4}, 4:{3,0}}
        self.assertEqual(excpected, VDWS_base(n, ld))
    
    def test_2(self):
        n = 6
        ld = [1,1,2,1,1,1]

        excpected = {0: {5,1,2}, 1:{0,2}, 2:{0,1,3,4}, 3:{2,4}, 4:{2,3,5}, 5:{4,0}}
        self.assertEqual(excpected, VDWS_base(n, ld))
    
    def test_3(self):
        n = 7
        ld = [3,1,1,1,1,1,1]

        excpected = {0: {4,5,6,1,2,3}, 1:{0,2}, 2:{0,1,3}, 3:{0,2,4}, 4:{0,3,5}, 5:{0,4,6}, 6:{0,5,0}}
        self.assertEqual(excpected, VDWS_base(n, ld))


YES = 0.4
NO = 0.6
P = 0.5

class TestVDWSRewire(unittest.TestCase):
    def base_test(self, n:int, ld:List[int], p_rand:List[float], int_rand:List[int], excpected:Graph):
        rng:random.Random = MagicMock(spec=random.Random)
        rng.random.side_effect = p_rand #type:ignore
        rng.randint.side_effect = int_rand #type: ignore
      
        g = VDWS_base(n, ld)

        return_g, _ = VDWS_rewire(g, n, P, ld, rng)
        self.assertEqual(excpected, return_g)
        self.assertEqual(edge_count(g), edge_count(return_g))
        self.assertEqual(rng.random.call_count, edge_count(g)//2) #type:ignore
        self.assertEqual(rng.randint.call_count, p_rand.count(YES)) #type:ignore

    def test_1_do_nothing(self):
        n = 100
        ld = [1]*n
        p_trial = [NO]*n 
        int_trial:list[int] = [] 

        excpected = VDWS_base(n,ld)

        self.base_test(n,ld,p_trial,int_trial,excpected)
    
    def test_2(self):
        n = 100
        ld = [i for _ in range(n//5) for i in [1,1,3,1,1]]
        excpected = VDWS_base(n,ld)
        p_trial = [NO]*edge_count(excpected) 
        int_trial:list[int] = [] 

        self.base_test(n,ld,p_trial,int_trial,excpected)
    
    def test_3(self):
        n = 6
        ld = [1,1,2,1,1,1]
        p_trials = [NO, NO, NO, YES, NO, NO, NO, NO, NO]
        int_trials:list[int] = [3]
        
        excpected = {0:{5,1,2}, 1:{0,2}, 2:{0,1,4,5}, 3:{4}, 4:{2,3,5}, 5:{2,4,0}}
        
        self.base_test(n, ld, p_trials, int_trials, excpected)
    
    def test_4(self):
        n = 6
        ld = [1,1,2,1,1,1]
        p_trials = [NO, NO, NO, YES, NO, NO, NO, NO, NO]
        int_trials:list[int] = [2]
        
        excpected = VDWS_base(n,ld) 
        
        self.base_test(n, ld, p_trials, int_trials, excpected)

    def test_5(self):
        n = 7
        ld = [1,1,2,1,1,1,1]
        p_trials = [NO, NO, YES, NO, NO, NO, NO, NO, NO]
        int_trials:list[int] = [-3]
        
        excpected = {0:{6,1}, 1:{0,2}, 2:{6,1,3,4}, 3:{2,4}, 4:{2,3,5}, 5:{4,6}, 6:{5,0,2}}
        
        self.base_test(n, ld, p_trials, int_trials, excpected)

    def test_6(self):
        n = 7
        ld = [1,1,2,1,1,1,1]
        p_trials = [NO, NO, NO, YES, YES, NO, NO, NO, NO]
        int_trials:list[int] = [3,3]
        
        excpected = {0:{6,1,2}, 1:{0,2}, 2:{0,1,4,5}, 3:{4}, 4:{2,3,5}, 5:{2,4,6}, 6:{5,0}}
        
        self.base_test(n, ld, p_trials, int_trials, excpected)


if __name__ == '__main__':
    unittest.main()