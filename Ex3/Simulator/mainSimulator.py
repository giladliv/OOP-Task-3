from DiGraph import DiGraph
from src.Node import Node
from GraphAlgo import GraphAlgo
import pygame
import pygame_gui
from types import SimpleNamespace
from pygame import Color, display, gfxdraw
from pygame.constants import RESIZABLE

# screen window
WIDTH, HEIGHT = 1080, 720
WIDTH = pygame.display.get_surface().get_width()
HEIGHT = pygame.display.get_surface().get_height()

_g = GraphAlgo()
graph = _g.graph()
file = '../data/A0.json'
_g.load_from_json(file)

pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

FONT = pygame.font.SysFont('Arial', 20)
black = Color(0, 0, 0)
white = Color(255, 255, 255)
gray = Color(192, 192, 192)
blue = Color(6, 187, 193)
yellow = Color(255, 255, 0)
green = Color(0, 255, 0)


def scale(data, min_screen, max_screen, min_data, max_data):
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


min_x = float(min(list(graph.nodes), key=lambda n: n.pos.x).pos.x)
min_y = float(min(list(graph.nodes), key=lambda n: n.pos.y).pos.y)
max_x = float(max(list(graph.nodes), key=lambda n: n.pos.x).pos.x)
max_y = float(max(list(graph.nodes), key=lambda n: n.pos.y).pos.y)


def GuiGraph_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


manager = pygame_gui.UIManager((WIDTH, HEIGHT))
btnLoad = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (110, 50)),
                                       text='LOAD',
                                       manager=manager)
btnSave = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110, 0), (110, 50)),
                                       text='SAVE',
                                       manager=manager)
btnShortest_Path = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 0), (110, 50)),
                                                text='Shortest_Path',
                                                manager=manager)
btnCenter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 0), (110, 50)),
                                         text='CENTER',
                                         manager=manager)
btnTSP = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((440, 0), (110, 50)),
                                      text=' TSP',
                                      manager=manager)
btnClean = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 0), (110, 50)),
                                        text=' CLEAN',
                                        manager=manager)
# button's loop

run = True
while(run):
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.update()
    clock.tick(30)

radius = 15

# draw nodes
def drawNode(n: Node, color: Color):
    for n in graph.nodes():
        x = GuiGraph_scale(n.pos.x, x=True)
        y = GuiGraph_scale(n.pos.y, y=True)
        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(green))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(white))
        id_srf = FONT.render(str(n.id), True, Color(white))
        rect = id_srf.get_rect(GraphAlgo.centerPoint(x, y))
        screen.blit(id_srf, rect)

# draw edges
def drawOneEdge(src: Node, dest: Node, color: Color):
    for e in graph.edges:
        src = next(n for n in graph.nodes if n.id == e.src)
        dest = next(n for n in graph.nodes if n.id == e.dest)
        src_x = GuiGraph_scale(src.pos.x, x=True)
        src_y = GuiGraph_scale(src.pos.y, y=True)
        dest_x = GuiGraph_scale(dest.pos.x, x=True)
        dest_y = GuiGraph_scale(dest.pos.y, y=True)
        pygame.draw.line(screen, Color(gray), (src_x, src_y), (dest_x, dest_y))

