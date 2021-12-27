from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *

class SimulatorGraph():
    def __init__(self, graphAlgo: GraphAlgoInterface):
        self._algo = graphAlgo
        self._x = []
        self._y = []

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


    def draw(self):
        pygame.init()

        stop = False
        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True

            fig, ax = plt.subplots()
            self.setTheNodesEdges(ax)
            ax.scatter(self._x, self._y)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.buffer_rgba()
            width, height = canvas.get_width_height()

            pygame.init()
            window = pygame.display.set_mode((width + 150, height + 10), DOUBLEBUF)
            screen = pygame.display.get_surface()

            size = canvas.get_width_height()
            surf = pygame.image.frombuffer(raw_data, size, "RGBA")
            bg_color = (255, 255, 255)  # fill red as background color
            screen.fill(bg_color)
            screen.blit(surf, (100, 5))  # x, y position on screen
            pygame.display.flip()
            pygame.time.Clock().tick(30)  # Avoid 100% CPU usage

