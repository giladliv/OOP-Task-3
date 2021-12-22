import json

from src.GraphAlgoInterface import *
from src.GraphInterface import GraphInterface
from DiGraph import DiGraph

class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph : GraphInterface = None):
        if graph is None:
            self._g = DiGraph()
        else:
            self._g = graph

    def get_graph(self) -> GraphInterface:
        return self._g

    def load_from_json(self, file_name: str) -> bool:
        with open(file_name) as file:
            jCont = json.load(file)
            file.close()

        self._g = DiGraph()
        for nodeData in jCont['Nodes']:
            id = nodeData['id']
            if 'pos' not in nodeData:
                pos = None
            else:
                pos = tuple(str(nodeData['pos']).split(','))
            self._g.add_node(id, pos)
        for edgesData in jCont['Edges']:
            src = edgesData['src']
            dest = edgesData['dest']
            w = float(edgesData['w'])
            self._g.add_edge(src,dest,w)

    def save_to_json(self, file_name: str) -> bool:
        nodesList = self.get_graph().get_all_v()
        nodes = []
        edges = []

        for node in nodesList:
            dictNode = {}
            dictNode['id'] = node
            dictNode['pos'] = nodesList[node]
            nodes += [dictNode]

            inEdges = self.get_graph().all_in_edges_of_node(node)
            for src in inEdges:
                currInEdge = {}
                currInEdge['src'] = src
                currInEdge['dest'] = node
                currInEdge['w'] = inEdges[src]
                edges += [currInEdge]
            outEdges = self.get_graph().all_out_edges_of_node(node)
            for dest in outEdges:
                currOutEdges = {}
                currOutEdges['src'] = node
                currOutEdges['dest'] = dest
                currOutEdges['w'] = outEdges[dest]
        dictJson = {}
        dictJson['Nodes'] = nodes
        dictJson['Edges'] = edges
        if not file_name.endswith(".json"):
            file_name += '.json'
        with open(file_name, 'w') as file:
            json.dump(dictJson, file)
            file.close()

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

    def centerPoint(self) -> (int, float):
        nodes = self.get_graph().get_all_v()
        Q = {}
        for src in nodes:
            pathMax = -1
            for dest in nodes:
                w, listNodes = self.shortest_path(src, dest)
                if w != float('inf') and pathMax < w:
                    pathMax = w
            if pathMax >= 0:
                Q[src] = pathMax
                # print(str(src) + " " + str(Q[src]))
        center = min(Q, key=Q.get)
        return center, Q[center]

    def TSP(self, node_lst: List[int]) -> (List[int], float):
            nodes = self.get_graph().get_all_v()
            allPairsW = {}
            allPairsWPath = {}
            pathMin = list()
            weightMin = float('inf')
            for src in nodes:
                for dest in nodes:
                    w, listNodes = self.shortest_path(src, dest)
                    if all(node in listNodes for node in node_lst):
                        if w < weightMin:
                            weightMin = w
                            pathMin = listNodes

            return pathMin, weightMin