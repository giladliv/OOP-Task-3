from time import time
from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo

class TestGraphAlgo(TestCase):
    def test_A0(self):
        g_algo = GraphAlgo()
        file = '../data/A0'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(3,5))
        print(g_algo.TSP([1, 3, 5]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(3, 5), (3.374437071805205, [3, 4, 5]))
        self.assertEqual(g_algo.TSP([1, 3, 5]), ([5, 4, 3, 2, 1], 5.765835269343382))
        self.assertEqual(g_algo.centerPoint(), (7, 6.806805834715163))

    def test_A1(self):
        g_algo = GraphAlgo()
        file = '../data/A1'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(3, 5))
        print(g_algo.TSP([1, 3, 5]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(3, 5), (2.3961649908752305, [3, 4, 5]))
        self.assertEqual(g_algo.TSP([1, 3, 5]), ([1, 2, 3, 4, 5], 5.2609209067274225))
        self.assertEqual(g_algo.centerPoint(), (8, 9.925289024973141))

    def test_A2(self):
        g_algo = GraphAlgo()
        file = '../data/A2'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(4, 15))
        print(g_algo.TSP([1, 3, 16]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(4, 15), (9.60409118484029, [4, 3, 2, 1, 0, 16, 15]))
        self.assertEqual(g_algo.TSP([1, 3, 16]), ([16, 0, 1, 2, 3], 5.53859518705698))
        self.assertEqual(g_algo.centerPoint(), (0, 7.819910602212574))

    def test_A3(self):
        g_algo = GraphAlgo()
        file = '../data/A3'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(4, 44))
        print(g_algo.TSP([2, 16, 40, 1]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(4, 44), (5.039772151960074, [4, 5, 6, 7, 44]))
        self.assertEqual(g_algo.TSP([2, 16, 40, 1]), ([40, 39, 15, 16, 0, 1, 2], 8.352068159448587))
        self.assertEqual(g_algo.centerPoint(), (2, 8.182236568942237))

    def test_A4(self):
        g_algo = GraphAlgo()
        file = '../data/A4'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(22, 18))
        print(g_algo.TSP([1, 2, 3, 5, 8, 13]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(22, 18), (6.366786655701585, [22, 21, 20, 19, 18]))
        self.assertEqual(g_algo.TSP([1, 2, 3, 5, 8, 13]), ([1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 15, 14, 13], 18.719296299845354))
        self.assertEqual(g_algo.centerPoint(), (6, 8.071366078651435))

    def test_A5(self):
        g_algo = GraphAlgo()
        file = '../data/A5'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(8, 19))
        print(g_algo.TSP([1, 2, 3, 5, 8, 13]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(8, 19), (12.64509246680214, [8, 10, 11, 13, 14, 29, 30, 31, 23, 22, 19]))
        self.assertEqual(g_algo.TSP([1, 2, 3, 5, 8, 13]), ([8, 1, 9, 2, 3, 13, 5], 5.596709442364163))
        self.assertEqual(g_algo.centerPoint(), (40, 9.291743173960954))

    def test_T0(self):
        g_algo = GraphAlgo()
        file = '../data/T0'
        self.assertTrue(g_algo.load_from_json(file))
        print(g_algo.shortest_path(1,0))
        print(g_algo.TSP([1, 0]))
        print(g_algo.centerPoint())
        self.assertEqual(g_algo.shortest_path(1,0), (1.1, [1, 0]))
        self.assertEqual(g_algo.TSP([1, 0]), ([0, 1], 1.0))
        self.assertEqual(g_algo.centerPoint(), (None, float('inf')))

    def test_1K(self):
        g_algo = GraphAlgo()
        file = '../data/1000Nodes.json'
        self.assertTrue(g_algo.load_from_json(file))
        diff = time()
        g_algo.TSP([1, 20, 300, 150, 11])
        diff = time() - diff
        print(diff)

    def test_10K(self):
        g_algo = GraphAlgo()
        file = '../data/10000Nodes.json'
        self.assertTrue(g_algo.load_from_json(file))
        diff = time()
        g_algo.TSP([1, 20, 300, 150, 11])
        diff = time() - diff
        print(diff)

    def test_100K(self):
        g_algo = GraphAlgo()
        file = '../data/100000.json'
        self.assertTrue(g_algo.load_from_json(file))
        diff = time()
        g_algo.TSP([1, 20, 300, 150, 11])
        diff = time() - diff
        print(diff)
