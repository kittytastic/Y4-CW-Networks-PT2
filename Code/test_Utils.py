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
   

class TestInDegree(unittest.TestCase):
   def test_id_1(self):
      in_g = {
         1: {1,3,4},
         2: {1},
         3: {1},
         4: {1},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      n = {1,2,  5,7}
      expected = {1:2, 2:0, 5:1, 7:1}
      self.assertEqual(expected, in_degree(n, in_g))

class TestOutDegree(unittest.TestCase):
   def test_od_1(self):
      in_g = {
         1: {1,3,4},
         2: {1,3},
         3: {1},
         4: {1},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      n = {1,2,  5,7}
      expected = {1:1, 2:1, 5:1, 7:1}
      self.assertEqual(expected, out_degree(n, in_g))


class TestBuildDist(unittest.TestCase):
   def test_bd_1(self):
      in_d = {
         1: 5,
         2: 3,
         3: 5,
         4: 1,
         5: 2,
         6: 5,
         7: 12
      } 
      expected = {1:1, 2:1, 3:1, 5:3, 12:1}
      self.assertEqual(expected, build_distribution(in_d))

class TestNormalizeDist(unittest.TestCase):
   def test_bd_1(self):
      in_d = {1:1, 2:2, 3:1, 5:3, 12:3} 
      expected = {1:0.1, 2:0.2, 3:0.1, 5:0.3, 12:0.3}
      self.assertEqual(expected, normalize_distribution(in_d))

if __name__ == '__main__':
    unittest.main()