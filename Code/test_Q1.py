import unittest
from T1 import *


class TestDFS(unittest.TestCase):
   def test_dfs_1(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      expected = {1,2,3,4}
      self.assertEqual(expected, connected_dfs(1, set(), in_g))
   
   def test_dfs_2(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {2},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      expected = {1,2,3,4}
      self.assertEqual(expected, connected_dfs(2, set(), in_g))
   
   def test_dfs_3(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      expected = {5,6,7}
      self.assertEqual(expected, connected_dfs(5, set(), in_g))
    

class TestLargestCCUndirected(unittest.TestCase):
   def test_dfs_1(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      expected = {1,2,3,4}
      self.assertEqual(expected, generate__largest_connected_components(in_g))
   
   def test_dfs_2(self):
      in_g = {
         1: {2,3,4,5},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7,1},
         6: {5,7},
         7: {5,6}
      } 
      expected = {1,2,3,4,5,6,7}
      self.assertEqual(expected, generate__largest_connected_components(in_g))

   def test_dfs_3(self):
      in_g = {
         1: {2},
         2: {1},
         3: {},
         4: {},
         5: {},
         6: {},
         7: {}
      } 
      expected = {1,2}
      self.assertEqual(expected, generate__largest_connected_components(in_g))


class TestLargestCCDirected(unittest.TestCase):
   def test_lccd_1(self):
      in_g = {
         1: {},
         2: {1},
         3: {2,4},
         4: {},
      } 
      expected = {1,2,3}
      self.assertEqual(expected, generate__largest_connected_components(in_g))

class TestTfUndirected(unittest.TestCase):
   def test_lccd_1(self):
      in_g = {
         1: set(),
         2: {1},
         3: {2,4},
         4: set(),
      } 
      expected = {
         1: {2},
         2: {1,3},
         3: {2,4},
         4: {3},
      }
      self.assertEqual(expected, tf_g_to_undirected(in_g))

class TestCCG(unittest.TestCase):
   def test_CCG_1(self):
      in_g = {
         1: set(),
         2: {1},
         3: {2,4},
         4: set(),
      } 
      expected = {
         1: {1},
         2: {1,2},
         3: {1,2,3,4},
         4: {4},
      }
      self.assertEqual(expected, create_connection_graph(in_g))

class TestFindK(unittest.TestCase):
   def test_find_k_1(self):
      in_g = {
         1: {1,2,3},
         2: {1,2,3},
         3: {1,2,3,4},
         4: {3,4},
      } 
      expected = {1,2,3}
      self.assertEqual(expected, find_largest_k(in_g))


if __name__ == '__main__':
    unittest.main()