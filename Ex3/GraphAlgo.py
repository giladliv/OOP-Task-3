import json
import threading
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

    # load graph's details from json
    def load_from_json(self, file_name: str) -> bool:
        if not file_name.endswith(".json"):
            file_name += '.json'
        try:
            with open(file_name) as file:
                jCont = json.load(file)
                file.close()
        except:
            return False

        # collection graph data from json file
        self._g = DiGraph()
        nodesLen = len(jCont['Nodes'])
        for nodeData in jCont['Nodes']:
            id = nodeData['id']
            if 'pos' not in nodeData:
                pos = tuple((randint(0, nodesLen), randint(0, nodesLen), 0))  # generate a random pos if doesnt have a pos
            else:
                pos = tuple(str(nodeData['pos']).split(','))    # generate a position from a string
                newPos = []
                for i in range(len(pos)):
                    newPos += [float(pos[i])]
                pos = tuple(newPos)
            self._g.add_node(id, pos)
        for edgesData in jCont['Edges']:    # add all the edges
            src = edgesData['src']
            dest = edgesData['dest']
            w = float(edgesData['w'])
            self._g.add_edge(src,dest,w)
        return True

    # save to json
    def save_to_json(self, file_name: str) -> bool:
        if not file_name.endswith(".json"):
            file_name += '.json'
        nodesList = self.get_graph().get_all_v()
        nodes = []
        edges = []

        # Insert data into json file
        for node in nodesList:
            dictNode = {}
            dictNode['id'] = node
            dictNode['pos'] = nodesList[node]   # save node as id and pos dict
            nodes += [dictNode]

            outEdges = self.get_graph().all_out_edges_of_node(node) # save all the edges of some node
            for dest in outEdges:
                currOutEdges = {}
                currOutEdges['src'] = node
                currOutEdges['dest'] = dest
                currOutEdges['w'] = outEdges[dest]
        dictJson = {}
        dictJson['Nodes'] = nodes
        dictJson['Edges'] = edges

        try:
            with open(file_name, 'w') as file:  #check if no was no exception in opening
                json.dump(dictJson, file)
                file.close()
                return True
        except:
            return False

    # Dijkstra algorithm
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        Q = []
        dist = {}
        prev = {}
        # get all the nodes in the connected graph and set an initial prev and dist
        for v in self._g.get_all_v():
            dist[v] = float('inf')
            prev[v] = None
            Q.append(v)
        dist[id1] = 0

        # while there are nodes in array continue pop
        while len(Q) > 0:
            #  Node with the least distance will be selected first
            u = min(Q, key=dist.get)
            Q.remove(u)

            #if the node is the destination track the path backwards and return its w and path
            if u == id2:
                s = list()
                if prev[u] is not None or u == id1:
                    while u is not None:
                        s.insert(0, u)
                        u = prev[u]
                return dist[id2], s

            # where v is still in Q
            neighbors = self._g.all_out_edges_of_node(u)
            for v in neighbors:
                alt = dist[u] + neighbors[v]
                if alt < dist[v]:
                    dist[v] = alt   # A shorter path to v has been found
                    prev[v] = u

        return float('inf'), list()

    # find the center of the graph
    def centerPoint(self) -> (int, float):
        nodes = self.get_graph().get_all_v()
        Q = {}
        # For each node in the graph we find the shortest path for
        # each other nodes in the graph
        for src in nodes:
            pathMax = -1
            for dest in nodes:
                # The maximum path of all the shortest paths we found
                # in the graph between the nodes
                w, listNodes = self.shortest_path(src, dest)
                if w != float('inf') and pathMax < w:
                    pathMax = w
                elif w == float('inf'):
                    return None, float('inf')
            if pathMax >= 0:
                Q[src] = pathMax
        center = min(Q, key=Q.get)
        return center, Q[center]

    # helper function for thread operation to find the TSP for a group of some of the nodes
    def shortForThread(self, nodes, src):
        for dest in nodes:
            w, listNodes = self.shortest_path(src, dest)
            if w != float('inf'):
                if src not in self.allPairsW:
                    self.allPairsW[src] = {}
                if src not in self.allPairsPath:
                    self.allPairsPath[src] = {}
                self.allPairsW[src][dest] = w
                self.allPairsPath[src][dest] = listNodes    # set in dictionary

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        self.allPairsW = {}
        self.allPairsPath = {}
        threadArr = []
        for src in node_lst:
            th = threading.Thread(target=self.shortForThread, args=(node_lst, src))
            #  comute all the pairs of the src, in multithreading
            th.start()
            threadArr += [th]
        for th in threadArr:
            th.join()       # run on the threads and make sure they compleate their task fully

        #for each node select the best path that contains all of the wanted nodes
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
                if currWeight < w:              # from the best routes select the most shoirtest that contains all the wanted nodes
                    w = currWeight
                    currNodes = bestNodes

        currNodes = json.loads(currNodes)
        nodesRet = list()
        for num in currNodes:           # translte the saven path to list of int
            nodesRet.append(int(num))
        return nodesRet, w

    # by given nodes list find the and save the route that has all of the wanted nodes
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

    # present the graph in the gui system
    def plot_graph(self):
        sim = SimulatorGraph(self)
        sim.run()
