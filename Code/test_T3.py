import unittest
import numpy as np
from numpy.random.mtrand import seed
from T3 import *

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

        VDWS(n,m, p, seed=seed)

    def test_p_2(self):
        n = 10 
        m = 3
        p = 0.01
        seed = 3902944517

        VDWS(n,m, p, seed=seed)
    
    def test_p_3(self):
        n = 20 
        m = 10
        p = 0.01
        seed = 1045711233

        VDWS(n,m, p, seed=seed)
    
    def test_p_4(self):
        n = 2000 
        m = 25
        p = 0.01
        seed = 1868584733 

        VDWS(n,m, p, seed=seed)
    
    def test_p_5(self):
        n = 10
        m = 1
        p = 0.01
        seed = 2540674012 

        VDWS(n,m, p, seed=seed)
    
    def test_p_6(self):
        n = 10
        m = 1
        p = 1
        seed = 2540674012 

        VDWS(n,m, p, seed=seed)

class TestSIM(unittest.TestCase):
    def xtest_sim_1(self):
        transmition_p:Transitions = {
            (State.I, State.S):0.00,
            (State.I, State.V):0.00,
            (State.VI, State.S):0.00,
            (State.VI, State.V):0.00
        }   

        t_i = 2
        g = VDWS(20, 5, 0.01, seed=42)

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
        g = VDWS(20, 5, 0.01, seed=42)

        metrics = simulate(g, transmition_p, t_i)
        self.assertEqual(metrics[State.R][-1], 20)

class TestIsAnticlockwise(unittest.TestCase):
    def test_ac_1(self):
        self.assertTrue(is_anticlockwise(8, 1, 7))
        self.assertTrue(is_anticlockwise(8, 0, 6))
        self.assertTrue(is_anticlockwise(8, 7, 5))

    def test_ac_2(self):
        self.assertFalse(is_anticlockwise(8, 7, 1))
        self.assertFalse(is_anticlockwise(8, 6, 0))
        self.assertFalse(is_anticlockwise(8, 5, 7))

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
      in_pop = {State.S: {1,2,3,4,5,7}, State.I:{6}, State.VI:set()}
      expected = {5,7}

      self.assertEqual(expected, local_most_at_risk(in_g, in_pop, 2))


if __name__ == '__main__':
    unittest.main()