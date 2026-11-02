import os
os.environ['PYGAME_BLEND_ALPHA_SDL2'] = '1'

import pygame
import sys
from pygame.locals import *

from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from data.config import *
from gfx.gfx import Renderer, Cube
from camera import Camera

pygame.init()
pygame.display.set_caption('CYBERPUNK City')

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode(WISZ) # pygame.FULLSCREEN | pygame.SCALED
        self.dis = pygame.Surface(DISZ)
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.c = Cube((0, 0, 50), (15, 15, 15), 0, 90)
        self.ren = Renderer(self)
        self.cam = Camera(self)


    def run(self):
        while 1:
            self.dt = self.clock.tick(10_000) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.cam.move()
            self.ren.vertex_proc()

            self.dis.fill((0, 0, 0))

            self.ren.render()

            self.win.blit(
                pygame.transform.scale(self.dis, WISZ), (0, 0)
            )
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
