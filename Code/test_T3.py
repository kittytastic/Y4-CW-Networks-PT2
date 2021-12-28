import unittest
import numpy as np
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
if __name__ == '__main__':
    unittest.main()