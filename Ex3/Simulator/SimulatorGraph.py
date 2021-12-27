from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
from pygame_ui.ui_elements import *

class SimulatorGraph():
    def __init__(self, graphAlgo: GraphAlgoInterface):
        pygame.init()
        self._algo = graphAlgo
        self._x = []
        self._y = []
        self.initButtons()

    def initButtons(self):
        loadB = Button('load', (70, 25))
        loadB.add_click_listener(self.loadGraph)
        tryB = Button('try', (70, 25))
        tryB.add_click_listener(lambda : print("TODO"))
        self.toolbar = MenuBar([loadB, tryB])

    def setTheNodesEdges(self, ax):
        nodes = self._algo.get_graph().get_all_v()
        self._x = []
        self._y = []
        for id in nodes:
            self._x += [nodes[id][0]]
            self._y += [nodes[id][1]]
            idPos = nodes[id]
            for src in self._algo.get_graph().all_in_edges_of_node(id):
                srcPos = nodes[src]
                ax.annotate("", xy=(idPos[0], idPos[1]), xytext=(srcPos[0], srcPos[1]), arrowprops=dict(arrowstyle="->"))
            for dest in self._algo.get_graph().all_out_edges_of_node(id):
                destPos = nodes[dest]
                ax.annotate("", xy=(destPos[0], destPos[1]), xytext=(idPos[0], idPos[1]), arrowprops=dict(arrowstyle="->"))


    def drawGraph(self):
        fig, ax = plt.subplots()
        self.setTheNodesEdges(ax)
        ax.scatter(self._x, self._y)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        width, height = canvas.get_width_height()
        window = pygame.display.set_mode((width + 150, height + 10), DOUBLEBUF)

        size = canvas.get_width_height()
        return raw_data, size

    def loadGraph(self):
        self._algo.load_from_json("../data/A0.json")
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
