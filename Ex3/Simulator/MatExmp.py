import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
import pylab

# make the data
np.random.seed(3)
x = 4 + np.random.normal(0, 2, 24)
y = 4 + np.random.normal(0, 2, len(x))
# size and color:
sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))

# plot
fig, ax = plt.subplots()

ax.scatter(x, y)
ax.arrow(2, 4, 2, 2,
          head_width = 0.2,
          width = 0.01,
          ec ='green', label='w')

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.buffer_rgba()
width, height = canvas.get_width_height()

pygame.init()
window = pygame.display.set_mode((width + 150, height + 10), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()
surf = pygame.image.frombuffer (raw_data, size, "RGBA")

bg_color = (255, 255, 255)   # fill red as background color
screen.fill(bg_color)
screen.blit(surf, (100, 5)) # x, y position on screen
pygame.display.flip()

stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    pygame.time.Clock().tick(30)  # Avoid 100% CPU usage