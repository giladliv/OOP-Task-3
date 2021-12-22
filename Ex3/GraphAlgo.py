from src.GraphAlgoInterface import *
from src.GraphInterface import GraphInterface

class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: GraphInterface):
        self._g = graph

    def get_graph(self) -> GraphInterface:
        return self._g

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        Q = []
        dist = {}
        prev = {}
        for v in self._g.get_all_v():
            dist[v] = float('inf')
            prev[v] = None
            Q.append(v)
        dist[id1] = 0

        while len(Q) > 0:
            u = min(Q, key=dist.get)
            Q.remove(u)

            if u == id2:
                s = list()
                if prev[u] is not None or u == id1:
                    while u is not None:
                        s.insert(0, u)
                        u = prev[u]
                return dist[id2], s

            neighbors = self._g.all_out_edges_of_node(u)
            for v in neighbors:
                alt = dist[u] + neighbors[v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        return float('inf'), list()