from random import randint

from src.GraphInterface import *

class DiGraph(GraphInterface):
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def __repr__(self):
        return f'nodes:\t{self._nodes}\nedges:\t{self._edges}\n'

    def v_size(self) -> int:
        return len(self._nodes)

    def e_size(self) -> int:
        return len(self._edges)

    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        _retDict = {}
        for src in self._edges.keys():
            if id1 in self._edges[src]:
                _retDict[src] = self._edges[src][id1]
        return _retDict

    def all_out_edges_of_node(self, id1: int) -> dict:
        _retDict = {}
        if id1 in self._edges:
            for dst in self._edges[id1]:
                _retDict[dst] = self._edges[id1][dst]


        return _retDict

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self._nodes or id2 not in self._nodes:
            return False
        if id1 in self._edges and id2 in self._edges[id1]:
            return False

        if id1 not in self._edges:
            self._edges[id1] = {}

        self._edges[id1][id2] = weight
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes:
            return False

        if pos == None:

            pos = tuple((randint(0, 100), randint(0, 100), 0.0))

        if len(pos) > 3:
            return False

        self._nodes[node_id] = pos
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._nodes:
            return False
        del self._edges[node_id]
        for src in self.all_in_edges_of_node(node_id):
            self.remove_edge(src, node_id)
        del self._nodes[node_id]

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self._edges or node_id2 not in self._edges[node_id1]:
            return False

        del self._edges[node_id1][node_id2]
        if len(self._edges[node_id1]) == 0:
            del self._edges[node_id1]
        return True

