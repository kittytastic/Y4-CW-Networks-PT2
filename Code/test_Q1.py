import unittest
from T1 import *

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
      self.assertEqual(expected, largest_unilateral_strong_component(in_g))
   
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
      self.assertEqual(expected, largest_unilateral_strong_component(in_g))

   def test_dfs_3(self):
      in_g = {
         1: {2},
         2: {1},
         3: set(),
         4: set(),
      } 
      expected = {1,2}
      self.assertEqual(expected, largest_unilateral_strong_component(in_g))


class TestLargestCCDirected(unittest.TestCase):
   def test_lccd_1(self):
      in_g = {
         1: set(),
         2: {1},
         3: {2,4},
         4: set(),
      } 
      expected = {1,2,3}
      self.assertEqual(expected, largest_unilateral_strong_component(in_g))

class TestFSC(unittest.TestCase):
   def test_fsc_1(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      expected = [{5,6,7}, {1,2,3,4}]
      self.assertEqual(expected, find_strong_componets(in_g))


class TestMergeNodes(unittest.TestCase):
   def test_mn_1(self):
      in_g = {
         1: {2,3,4},
         2: {1,3,4},
         3: {1,2,4},
         4: {1,2,3},
         5: {6,7},
         6: {5,7},
         7: {5,6}
      } 
      mn = [{5,6,7}, {1,2,3,4}]
      expected_n = {1:{1}, 5:{5}}
      expected_w = {1: 4, 5:3}
      self.assertEqual((expected_n, expected_w), merge_nodes(in_g, mn))

class TestRemoveSelfCycles(unittest.TestCase):
   def test_rsc_1(self):
      in_g = {
         1: {1},
         5: {5},
      } 
      expected_n = {1:set(), 5:set()}
      self.assertEqual(expected_n, remove_self_cycles(in_g))

class TestLongestPath(unittest.TestCase):
   def test_lp_1(self):
      in_g = {
         1: set(),
         5: set(),
      }
      in_w = {
         1:4,
         5:3
      }

      expected = [1]
      self.assertEqual(expected, longest_path(in_g, in_w))

if __name__ == '__main__':
    unittest.main()