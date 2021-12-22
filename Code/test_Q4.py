import unittest
from Q4 import *

example_g = {
         1: {4},
         2: {4},
         3: {4},
         4: {1,2,3,5,6},
         5: {4},
         6: {4,7,8,9,10, 11},
         7: {6, 8, 11},
         8: {6, 7, 9, 11},
         9: {6,8,10},
         10: {6, 9, 11, 12},
         11: {6, 7, 8, 10},
         12: {10}
      } 


class TestDijkstra(unittest.TestCase):
    def test_D_1(self):
        in_g = dict(example_g)
        start_node = 1

        expected = {1: 0, 2:2, 3:2, 4:1, 5:2, 6:2,7:3, 8:3, 9:3, 10:3, 11:3, 12:4}
        self.assertEqual(expected, dijkstras(start_node, in_g))
    
    def test_D_2(self):
        in_g = dict(example_g)
        start_node = 11

        expected = {1: 3, 2:3, 3:3, 4:2, 5:3, 6:1, 7:1, 8:1, 9:2, 10:1, 11:0, 12:2}
        self.assertEqual(expected, dijkstras(start_node, in_g))
    
    def test_D_3(self):
        in_g = dict(example_g)
        start_node = 7

        expected = {1: 3, 2:3, 3:3, 4:2, 5:3, 6:1, 7:0, 8:1, 9:2, 10:2, 11:1, 12:3}
        self.assertEqual(expected, dijkstras(start_node, in_g))

class TestMinPath(unittest.TestCase):
    def test_mp_1(self):
        in_g = {1: {2}, 2:{1,3}, 3: {2}}

        expected = {1: {1:0, 2:1, 3:2}, 2: {1:1, 2:0, 3:1}, 3:{1:2, 2:1, 3:0}}
        ans = min_path_dict(in_g)
        for k in ans.keys():
            self.assertEqual(ans[k], expected[k]) 
    
class TestClosnessCentrality(unittest.TestCase):
    def test_cc_1(self):
        in_g = {1: {2}, 2:{1,3}, 3: {2}}

        expected = {1: 1/3, 2: 1/2, 3:1/3}
        self.assertEqual(expected, closeness_centrality(in_g)) 

    def test_cc_2(self):
        in_g = dict(example_g) 

        expected = {1: 1/28, 2: 1/28, 3: 1/28, 4:1/18, 5:1/28, 6:1/16, 7:1/24, 8:1/23, 9:1/23, 10:1/22, 11:1/22, 12:1/32}
        self.assertEqual(expected, closeness_centrality(in_g)) 


class TestNearnessCentrality(unittest.TestCase):
    def test_nc_1(self):
        in_g = {1: {2}, 2:{1,3}, 3: {2}}

        expected = {1: 1+1/2, 2: 1+1, 3:1+1/2}
        self.assertEqual(expected, nearness_centrality(in_g)) 
    
    def test_nc_2(self):
        in_g = dict(example_g) 

        expected = {
            1: 1+ 4*1/2 +5*1/3 + 1/4,
            7: 3+3*1/2+5*1/3,
            11: 4+3*1/2+4*1/3}
        ans = nearness_centrality(in_g)

        for k in expected:
            self.assertAlmostEqual(expected[k], ans[k], msg=f"Key {k} failed") 


class TestDegreeCentrality(unittest.TestCase):
    def test_dc_1(self):
        in_g = {1: {2}, 2:{1,3}, 3: {2}}

        expected = {1: 1, 2: 2, 3:1}
        self.assertEqual(expected, degree_centrality(in_g)) 

    def test_dc_2(self):
        in_g = dict(example_g) 

        expected = {1:1, 2:1, 3:1, 4:5, 5:1, 6:6, 7:3, 8:4, 9:3, 10:4, 11:4, 12:1}
        self.assertEqual(expected, degree_centrality(in_g)) 

class TestAdjacencyCentrality(unittest.TestCase):
    def xtest_ac_1(self):
        in_g = {1: {2}, 2:{1,3}, 3: {2}}

        expected = {1: -1/3, 2: 2*1/3*1/2, 3:-1/3}
        self.assertEqual(expected, adjacency_centrality(in_g)) 
    
    def test_ac_2(self):
        in_g = dict(example_g) 

        expected = {
           4: 1/5*(4*4/6 + -1/11),
           1: -4/6
           }
        ans = adjacency_centrality(in_g)

        for k in expected:
            self.assertAlmostEqual(expected[k], ans[k], msg=f"Key {k} failed") 

if __name__ == '__main__':
    unittest.main()