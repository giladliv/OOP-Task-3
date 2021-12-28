from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo

class TestDiGraph(TestCase):

    def test_v_size(self):
        g_algo = GraphAlgo()
        file1 = '../data/A0.json'
        g_algo.load_from_json(file1)
        self.assertEqual(g_algo.get_graph().v_size(), 11)

    def test_e_size(self):
        graph = DiGraph()
        graph.add_node(0, (4., 5, 3))
        graph.add_node(1, (1, 5, 0))
        graph.add_node(2, (2, 7, 0))
        graph.add_node(3, (8, 4, 0))
        graph.add_edge(0, 3, 5)
        graph.add_edge(1, 3, 3)
        graph.add_edge(0, 2, 9)
        graph.add_edge(3, 2, 10)
        self.assertEqual(graph.e_size(),4)

    def test_add_edge(self):
        graph = DiGraph()
        graph.add_node(0, (4.22, 5, 33))
        graph.add_node(1, (2, 3, 0))
        graph.add_node(2, (5, 6, 0))
        self.assertEqual(graph.add_edge(0, 1, 5), True)
        self.assertEqual(graph.add_edge(1, 2, 3), True)
        self.assertEqual(graph.add_edge(0, 2, 9), True)
        self.assertEqual(graph.add_edge(8, 2, 9), False)
        self.assertEqual(graph.add_edge(2, 8, 9), False)
        self.assertEqual(graph.add_edge(9, 8, 9), False)
        self.assertEqual(graph.all_in_edges_of_node(0), {})
        self.assertEqual(graph.all_out_edges_of_node(0), {1: 5, 2: 9})
        self.assertEqual(graph.all_in_edges_of_node(1), {0: 5})
        self.assertEqual(graph.all_out_edges_of_node(1), {2: 3})
        self.assertEqual(graph.all_in_edges_of_node(2), {0: 9, 1: 3})
        self.assertEqual(graph.all_out_edges_of_node(2), {})
        self.assertEqual(graph.e_size(), 3)

    def test_add_node(self):
        graph = DiGraph()
        self.assertEqual(graph.add_node(0, (4.22, 5, 33)), True)
        nodes = {0: (4.22, 5, 33)}
        self.assertEqual(graph.get_all_v(), nodes)
        self.assertEqual(graph.add_node(1, (2, 3, 0)), True)
        self.assertEqual(graph.add_node(2, (5, 6, 0)), True)
        self.assertEqual(graph.add_node(2, (1, 2, 0)), False)
        nodes = {0: (4.22, 5, 33), 1: (2, 3, 0), 2: (5, 6, 0)}
        self.assertEqual(graph.get_all_v(), nodes)

    def test_remove_node(self):
        g_algo = GraphAlgo()
        file1 = '../data/A0.json'
        g_algo.load_from_json(file1)
        graph = g_algo.get_graph()
        nodes = graph.get_all_v()
        self.assertTrue(0 in nodes)
        self.assertTrue(1 in nodes)
        self.assertTrue(graph.remove_node(0))
        self.assertTrue(graph.remove_node(1))
        self.assertEqual(graph.v_size(),9)
        nodes = graph.get_all_v()
        self.assertTrue(0 not in nodes)
        self.assertTrue(1 not in nodes)

    def test_remove_edge(self):
        graph = DiGraph()
        i = 0
        while i < 4:
            graph.add_node(i)
            i += 1
        graph.add_edge(0, 1, 4.8)
        graph.add_edge(0, 2, 5.0)
        graph.add_edge(1, 3, 4.1)
        graph.add_edge(1, 0, 4.0)
        graph.add_edge(2, 3, 3.8)
        graph.add_edge(3, 2, 5.0)
        graph.add_edge(0, 1, 1.8)
        graph.remove_edge(2, 1)
        self.assertTrue(graph.e_size() == 6)
        graph.remove_edge(2, 3)
        self.assertTrue(3 not in graph.all_out_edges_of_node(2))
        self.assertTrue(2 not in graph.all_in_edges_of_node(3))
        self.assertTrue(graph.e_size() == 5)
        graph.remove_edge(1, 2)
        self.assertTrue(graph.e_size() == 5)