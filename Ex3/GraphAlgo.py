import json
from random import randint

from src.GraphAlgoInterface import *
from src.GraphInterface import GraphInterface
from DiGraph import DiGraph
from Simulator.SimulatorGraph import SimulatorGraph

class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph : GraphInterface = None):
        if graph is None:
            self._g = DiGraph()
        else:
            self._g = graph
        self._pathBest = {}
        self.allPairsW = {}
        self.allPairsPath = {}

    def get_graph(self) -> GraphInterface:
        return self._g

    def load_from_json(self, file_name: str) -> bool:
        with open(file_name) as file:
            jCont = json.load(file)
            file.close()

        self._g = DiGraph()
        nodesLen = len(jCont['Nodes'])
        for nodeData in jCont['Nodes']:
            id = nodeData['id']
            if 'pos' not in nodeData:
                pos = tuple((randint(0, nodesLen), randint(0, nodesLen), 0))
            else:
                pos = tuple(str(nodeData['pos']).split(','))
                newPos = []
                for i in range(len(pos)):
                    newPos += [float(pos[i])]
                pos = tuple(newPos)
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
        try:
            with open(file_name, 'w') as file:
                json.dump(dictJson, file)
                file.close()
                return True
        except:
            return False

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
            self.allPairsW = {}
            self.allPairsPath = {}
            for src in nodes:
                for dest in nodes:
                    w, listNodes = self.shortest_path(src, dest)
                    if w != float('inf'):
                        if src not in self.allPairsW:
                            self.allPairsW[src] = {}
                        if src not in self.allPairsPath:
                            self.allPairsPath[src] = {}
                        self.allPairsW[src][dest] = w
                        self.allPairsPath[src][dest] = listNodes

            currNodes = list()
            for city in node_lst:
                remained = list(node_lst)
                remained.remove(city)
                currNodes = list([city])
                self.setPathsList(currNodes, remained, 0)

            currNodes = ""
            w = float('inf')
            for src in self._pathBest:
                for bestNodes in self._pathBest[src]:
                    currWeight = self._pathBest[src][bestNodes]
                    if currWeight < w:
                        w = currWeight
                        currNodes = bestNodes

            currNodes = json.loads(currNodes)
            nodesRet = list()
            for num in currNodes:
                nodesRet.append(int(num))
            return nodesRet, w

    def setPathsList(self, nodes: List[int], nodesRemain: List[int], w: float):
        if len(nodesRemain) == 0:
            if nodes[0] not in self._pathBest:
                self._pathBest[nodes[0]] = {}
            self._pathBest[nodes[0]][str(nodes)] = w

        last = nodes[-1]

        for node in self.allPairsPath[last]:
            if node != last and node in nodesRemain:
                bestP = list(self.allPairsPath[last][node])
                del bestP[0]
                tempList = list(nodes)
                tempRemain = list(nodesRemain)
                tempList += bestP
                for curr in bestP:
                    if curr in tempRemain:
                        tempRemain.remove(curr)
                self.setPathsList(tempList, tempRemain, w + self.allPairsW[last][node])

    def plot_graph(self):
        sim = SimulatorGraph(self)
        sim.run()
