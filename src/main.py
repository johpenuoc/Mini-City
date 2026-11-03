import os
os.environ['PYGAME_BLEND_ALPHA_SDL2'] = '1'

import pygame
import sys
from pygame.locals import *
from math import sqrt

from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from data.config import *
from gfx.gfx import Cube, Floor
from camera import Camera

pygame.init()
pygame.display.set_caption('CYBERPUNK City')

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode(WISZ, FULLSCREEN | SCALED) # pygame.FULLSCREEN | pygame.SCALED
        self.dis = pygame.Surface(DISZ)
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.cubes = []
        map = [
            [1, 1, 2, 2, 2, 2, 2, 2, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [2, 2, 2, 2, 1, 2, 2, 2, 2, 2],
            [2, 2, 2, 1, 2, 1, 2, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 2, 2, 1, 1, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 2, 2, 2, 2, 2, 2, 1, 1]
        ]
        x = 0
        y = 0
        z = 0
        tz = 15
        for ym, row in enumerate(map):
            for xm, i in enumerate(row):
                if i == 1:
                    self.cubes.append(
                        Cube((x + (xm * tz), 0, z + (ym * tz)), (tz, tz, tz))
                    )
                elif i == 2:
                    self.cubes.append(
                            Floor((x + (xm * tz), 0, z + (ym * tz)), (tz, tz, tz))
                        )
                    self.cubes.append(
                            Floor((x + (xm * tz), tz, z + (ym * tz)), (tz, tz, tz))
                        )

        self.cam = Camera(self)

    def run_cubes(self):
        campos = self.cam.pos
        rot = self.cam.rot
        rot2 = self.cam.rot2

        self.cubes.sort(key=lambda i: sqrt(((abs(i.obj[1][0]) - abs(campos[0]))**2) + ((abs(i.obj[1][2]) - abs(campos[2]))**2)), reverse=True)

        for cube in self.cubes:
            cube.vertex_proc(campos, rot, rot2)

            cube.render(self.dis, campos)



        #del pixel_arr


    def run(self):
        while 1:
            self.dt = self.clock.tick(10_000) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.cam.move()

            self.dis.fill((0, 0, 0))

            self.run_cubes()

            self.win.blit(
                pygame.transform.scale(self.dis, WISZ), (0, 0)
            )
            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.run()
