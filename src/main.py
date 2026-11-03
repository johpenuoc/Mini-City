import os
os.environ['PYGAME_BLEND_ALPHA_SDL2'] = '1'

import pygame
import sys
from pygame.locals import *
from math import sqrt
from random import randint

from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from data.config import *
from gfx.gfx import Cube, Floor, Sphere, Pyramid, Cylinder
from camera import Camera

pygame.init()
pygame.display.set_caption('CYBERPUNK City')

WIDTH = 35
HEIGHT = 15
DEPTH = 35

# ai generated function simply to generate a primitive city quickly.
# i didnt want to spend ages on something pretty trivial
def generate_mega_city():
    city_map = [[[0 for y in range(HEIGHT)] for z in range(DEPTH)] for x in range(WIDTH)]

    for x in range(WIDTH):
        for z in range(DEPTH):
            city_map[x][z][0] = 1 

            is_road_x = (x % 12 == 0 or x % 12 == 1)
            is_road_z = (z % 12 == 0 or z % 12 == 1)

            if not is_road_x and not is_road_z:
                dist_from_center = ((x - 100)**2 + (z - 100)**2)**0.5

                if dist_from_center < 35:
                    structure_type = 5 if (x + z) % 3 == 0 else 2
                    bldg_height = randint(25, 45)
                elif dist_from_center < 70:
                    structure_type = 4 if (x * z) % 7 == 0 else 2
                    bldg_height = randint(10, 25)
                else:
                    structure_type = 3 if (x % 24 == 0 and z % 24 == 0) else 2
                    bldg_height = randint(2, 8)

                for y in range(1, bldg_height + 1):
                    if y == bldg_height and structure_type == 2:
                        city_map[x][z][y] = 3
                    else:
                        city_map[x][z][y] = structure_type

    return city_map

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode(WISZ, FULLSCREEN | SCALED) # pygame.FULLSCREEN | pygame.SCALED
        self.dis = pygame.Surface(DISZ)
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.cubes = []
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0],
            [0, 0, 0, 2, 2, 3, 2, 2, 0, 0, 0],
            [0, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        map = generate_mega_city()
        x = 0
        y = 0
        z = 0
        tz = 15
        for xm, j in enumerate(map):
            for zm, row in enumerate(j):
                for ym, i in enumerate(row):
                    if i == 0:
                        continue

                    xw = x + (xm * tz)
                    yw = -(y + (ym * tz)) + (tz )
                    zw = z + (zm * tz)

                    if i == 1:
                        self.cubes.append(
                            Floor((xw, yw, zw), (tz, tz, tz), i + 1)
                        )
                    elif i == 2:
                        self.cubes.append(
                                Cube((xw, yw, zw), (tz, tz, tz), i + 1)
                            )
                    elif i == 3:
                        self.cubes.append(
                                Sphere((xw, yw, zw), (tz, tz, tz), i + 1)
                            )
                    elif i == 4:
                        self.cubes.append(
                                Pyramid((xw, yw, zw), (tz, tz, tz), i + 1)
                            )
                    elif i == 5:
                        self.cubes.append(
                                Cylinder((xw, yw, zw), (tz, tz, tz), i + 1)
                            )


        self.cam = Camera(self)

    def run_cubes(self):
        campos = self.cam.pos
        rot = self.cam.rot
        rot2 = self.cam.rot2

        self.cubes.sort(key=lambda i: sqrt(((abs(i.obj[1][0]) - abs(campos[0]))**2) + ((abs(i.obj[1][2]) - abs(campos[2]))**2)), reverse=True)

        clen = len(self.cubes)
        for cube in self.cubes[int((clen // 2) * 1.9):]:
            cube.vertex_proc(campos, rot, rot2)

            cube.render(self.dis, campos)


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
