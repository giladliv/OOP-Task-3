import sys

import pygame

# Simple pygame program

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def mainWindow():
    pygame.init()
    scr = pygame.display.set_mode((1280, 720))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        scr.fill(WHITE)
        pygame.draw.circle(scr, (200, 0, 0), (250, 250), 80)
        color = (0, 0, 255)
        pygame.draw.rect(scr, color, pygame.Rect(60, 60, 100, 100))
        color = (0, 255, 0)
        pygame.draw.line(scr, color, (40, 300), (140, 380), 6)
        purple = (102, 0, 102)
        pygame.draw.polygon(scr, purple,
                            ((346, 0), (491, 106), (436, 277), (256, 277), (200, 106)))
        #pygame.draw.polygon(scr, (0, 0, 0),
        #                    ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
        pygame.draw.line(scr, BLACK, (0,0), (100,100))
        pygame.display.flip()
    pygame.quit()
    sys.exit()

mainWindow()