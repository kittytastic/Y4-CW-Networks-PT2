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

if __name__ == '__main__':
    unittest.main()