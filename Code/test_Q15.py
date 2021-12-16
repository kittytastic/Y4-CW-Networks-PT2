import unittest
from Int_Nets_routing_qwrx21 import *

def assert2DListEqual(self, list_a, list_b):
   self.assertEqual(len(list_a), len(list_b))
   for a,b in zip(list_a, list_b):
      self.assertListEqual(a,b)

class TestRemapNode(unittest.TestCase):
   def test_remap_1(self):
      in_n = [0,1,2,3,4]
      mapper = [4,3,2,1,0]
      expected = [4,3,2,1,0]
      self.assertEqual(expected, remap_node(in_n, mapper))
    
   def test_remap_2(self):
      in_n = [2,1,0,4,3]
      mapper = [0,3,4,1,2]
      expected = [4,3,0,2,1]
      self.assertEqual(expected, remap_node(in_n, mapper))
    
class TestGenMap(unittest.TestCase):
   def test_gen_1(self):
      n=5
      in_node = [0,1,2,3,4]
      
      expected_to = [0,1,2,3,4]
      expected_from = [0,1,2,3,4]

      res_to, res_from = generate_mappers(n, in_node)
      self.assertEqual(expected_to, res_to)
      self.assertEqual(expected_from, res_from)
    
   def test_gen_2(self):
      n=5
      in_node = [0,3,4,1,2]
      
      expected_to = [0,3,4,1,2]
      expected_from = [0,3,4,1,2]

      res_to, res_from = generate_mappers(n, in_node)
      self.assertEqual(expected_to, res_to)
      self.assertEqual(expected_from, res_from)
   
   def test_combi_1(self):
      n=5
      in_node = [0,3,4,1,2]
      expected_out = [0,1,2,3,4]
      

      res_to, res_from = generate_mappers(n, in_node)
      self.assertEqual(expected_out, remap_node(in_node, res_to))
      self.assertEqual(in_node, remap_node(remap_node(in_node, res_to), res_from))

class TestBubbleSort(unittest.TestCase):
   def test_sort_1(self):
      n=5
      in_node = [0,1,2,3,4]      
      expected = [[0,1,2,3,4]]
      self.assertEqual(expected, bubble_sort(n, in_node))
   
   def test_sort_2(self):
      n=5
      in_node = [0,1,3,2,4]      
      expected = [[0,1,3,2,4],
                  [0,1,2,3,4]]
      self.assertListEqual(expected, bubble_sort(n, in_node))
   
   def test_sort_2(self):
      n=5
      in_node = [4,3,2,1,0]      
      expected = [[4,3,2,1,0],
                  [3,4,2,1,0],
                  [3,2,4,1,0],
                  [3,2,1,4,0],
                  [3,2,1,0,4],
                  [2,3,1,0,4],
                  [2,1,3,0,4],
                  [2,1,0,3,4],
                  [1,2,0,3,4],
                  [1,0,2,3,4],
                  [0,1,2,3,4]
                  ]

      assert2DListEqual(self, expected, bubble_sort(n, in_node))

class TestRouting(unittest.TestCase):
   def test_routing_1(self):
      n=5
      in_node = [4,1,2,3,0]
      target = [3,2,4,1,0]

      path = bubblesort_routing(5, in_node, target)
      self.assertListEqual(path[0], in_node)
      self.assertListEqual(path[-1], target)
   
  
   
   def test_sort_2(self):
      n=5
      in_node = [3,2,1,0,4]
      target = [4,1,0,2,3]      
      expected = [
         [3, 2, 1, 0, 4],
         [2, 3, 1, 0, 4],
         [2, 1, 3, 0, 4],
         [2, 1, 0, 3, 4],
         [2, 1, 0, 4, 3],
         [1, 2, 0, 4, 3],
         [1, 0, 2, 4, 3],
         [1, 0, 4, 2, 3],
         [1, 4, 0, 2, 3],
         [4, 1, 0, 2, 3]
                  ]

      path = bubblesort_routing(5, in_node, target)
      self.assertListEqual(path[0], in_node)
      self.assertListEqual(path[-1], target)

      assert2DListEqual(self, path, expected)


if __name__ == '__main__':
    unittest.main()