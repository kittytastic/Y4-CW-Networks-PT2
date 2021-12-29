import unittest
from Utils import *

class TestGraphSubset(unittest.TestCase):
   def test_gsb_1(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      }
      subset = {1,2,3,7}

      expected:Graph = {1:{2,3}, 2:{1,3}, 3:{1,2}, 7:set()}
      self.assertEqual(expected, graph_subset(in_g, subset))
   

if __name__ == '__main__':
    unittest.main()