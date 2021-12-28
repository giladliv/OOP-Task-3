import os

from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
from pygame_ui.ui_elements import *
import tkinter as tk
from tkinter import filedialog
from Simulator.EnterWindow import EnterWindow

class SimulatorGraph():
    def __init__(self, graphAlgo: GraphAlgoInterface):
        pygame.init()
        self._algo = graphAlgo
        self._x = []
        self._y = []
        self.initButtons()

    def initButtons(self):
        # buttons of algorithms
        loadB = Button('LOAD', (70, 25))
        loadB.add_click_listener(self.loadGraph)
        saveB = Button('SAVE', (70, 25))
        saveB.add_click_listener(self.saveGraph)
        spB = Button('Shortest Path', (100, 25))
        spB.add_click_listener(self.shortestPath)
        tspB = Button('TSP', (70, 25))
        tspB.add_click_listener(self.tsp)
        centerB = Button('CENTER', (70, 25))
        centerB.add_click_listener(self.center)
        cleanB = Button('Refresh', (70, 25))
        cleanB.add_click_listener(self.refreshDisplay)
        self.toolbar = MenuBar([loadB, saveB, spB, tspB, centerB, cleanB])

    def setOneNode(self, ax, nodes, id):
        self._x += [nodes[id][0]]
        self._y += [nodes[id][1]]
        idPos = nodes[id]
        for dest in self._algo.get_graph().all_out_edges_of_node(id):
            destPos = nodes[dest]
            ax.annotate("", xy=(destPos[0], destPos[1]), xytext=(idPos[0], idPos[1]), arrowprops=dict(arrowstyle="->"))
        ax.text(idPos[0], idPos[1], str(id), color='red')

    def setTheNodesEdges(self, ax):
        nodes = self._algo.get_graph().get_all_v()
        self._x = []
        self._y = []
        for id in nodes:
            self._x += [nodes[id][0]]
            self._y += [nodes[id][1]]
            idPos = nodes[id]
            for dest in self._algo.get_graph().all_out_edges_of_node(id):
                destPos = nodes[dest]
                ax.annotate("", xy=(destPos[0], destPos[1]), xytext=(idPos[0], idPos[1]), arrowprops=dict(arrowstyle="->"))
            ax.scatter(x=nodes[id][0], y=nodes[id][1], color='blue')
            ax.text(idPos[0], idPos[1], str(id), color='red')

        #ax.scatter(self._x, self._y)

    def setNodesByPath(self, ax, nodesPath: List[int]):
        nodes = self._algo.get_graph().get_all_v()
        self._x = []
        self._y = []
        lenPath = len(nodesPath)
        for i in range(lenPath):
            id = nodesPath[i]
            if id not in nodes:
                continue
            if i == 0:
                self._x += [nodes[id][0]]
                self._y += [nodes[id][1]]
                ax.text(nodes[id][0], nodes[id][1], str(id), color='red')
            if i == lenPath - 1:
                break
            idNext = nodesPath[i+1]
            if idNext not in nodes:
                continue
            self._x += [nodes[idNext][0]]
            self._y += [nodes[idNext][1]]
            ax.text(nodes[idNext][0], nodes[idNext][1], str(idNext), color='red')
            idPos = nodes[id]
            destPos = nodes[idNext]
            ax.annotate("", xytext=(idPos[0], idPos[1]), xy=(destPos[0], destPos[1]), arrowprops=dict(arrowstyle="->"))
        ax.scatter(self._x, self._y)

    def drawGraph(self, nodesPath: List[int] = None):
        fig, ax = plt.subplots()
        if nodesPath is None:
            self.setTheNodesEdges(ax)
        else:
            self.setNodesByPath(ax, nodesPath)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        width, height = canvas.get_width_height()
        window = pygame.display.set_mode((width + 150, height + 10), DOUBLEBUF)
        size = canvas.get_width_height()
        return raw_data, size

    def loadGraph(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), defaultextension=".json", filetypes=[("json", "*.json")])
        if not self._algo.load_from_json(file_path):
            return
        raw_data, size = self.drawGraph()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        bg_color = (255, 255, 255)  # fill red as background color
        self.screen.fill(bg_color)
        self.screen.blit(surf, (100, 5))

    def saveGraph(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".json", filetypes=[("json file", "*.json")])
        if not self._algo.save_to_json(file_path):
            return
        raw_data, size = self.drawGraph()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        bg_color = (255, 255, 255)  # fill red as background color
        self.screen.fill(bg_color)
        self.screen.blit(surf, (100, 5))

    def shortestPath(self):
        selectW = EnterWindow("Shortest Path", "please select start and end nodes", ["src node:", "dest node:"], "show shortest path")
        strArr = selectW.getTextArray()
        try:
            src = int(strArr[0])
            dest = int(strArr[1])
            print(str(src) + " , " + str(dest))
            #nodes = self._algo.get_graph().get_all_v()
            #if src not in
            w, path = self._algo.shortest_path(src, dest)

            raw_data, size = self.drawGraph(path)
            surf = pygame.image.frombuffer(raw_data, size, "RGBA")
            bg_color = (255, 255, 255)  # fill red as background color
            self.screen.fill(bg_color)
            self.screen.blit(surf, (100, 5))
            return True
        except:
            return False

    def tsp(self):
        selectW = EnterWindow("TSP",
                              "please select write all the nodes you wish with the charhacter ',' like this example:\n 1,2,3,4,5",
                              ["nodes:"],
                              "perform TSP")
        strArr = selectW.getTextArray()
        try:
            nodesStr = strArr[0].split(',')
            nodes = list()
            for node in nodesStr:
                nodes.append(int(node))
            path, w = self._algo.TSP(nodes)

            raw_data, size = self.drawGraph(path)
            surf = pygame.image.frombuffer(raw_data, size, "RGBA")
            bg_color = (255, 255, 255)  # fill red as background color
            self.screen.fill(bg_color)
            self.screen.blit(surf, (100, 5))
        except:
            return False

    def center(self):
        id, pos = self._algo.centerPoint()
        raw_data, size = self.drawGraph([id])
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        bg_color = (255, 255, 255)  # fill red as background color
        self.screen.fill(bg_color)
        self.screen.blit(surf, (100, 5))

    def refreshDisplay(self):
        raw_data, size = self.drawGraph()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        bg_color = (255, 255, 255)  # fill red as background color
        self.screen.fill(bg_color)
        self.screen.blit(surf, (100, 5))


    def run(self):
        pygame.init()
        raw_data, size = self.drawGraph()
        self.screen = pygame.display.get_surface()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        bg_color = (255, 255, 255)  # fill red as background color
        self.screen.fill(bg_color)
        self.screen.blit(surf, (100, 5))  # x, y position on screen


        stop = False
        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
                if event.type == MOUSEBUTTONDOWN:
                    self.toolbar.check()
            self.toolbar.render(self.screen, (0, 0))
            display.update()
            time.Clock().tick(30)  # Avoid 100% CPU usage
