import pygame
import sys
from math import cos, sin, tan, radians


from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from data.config import *

class Renderer:
    def __init__(self, Main):
        self.main = Main

        self.fov = 0
        self.obj = self.main.c.obj

    def translate_coord(self, x, y):
        return x + (DISZ[0] / 2), y + (DISZ[1] / 2)

    def point(self, x, y, s):
        pygame.draw.rect(self.main.dis, (255, 255, 255), (x, y, s, s))

    def translate_Z(self, x, y, z):
        return (x / z) * RENDER_SCALE, (y / z) * RENDER_SCALE,

    def yrotate(self, x, z, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _x = (x * c) - (z * s)
        _z = (x * s) + (z * c)

        return _x, _z

    def xrotate(self, y, z, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _y = (y * c) - (z * s)
        _z = (y * s) + (z * c)

        return _y, _z

    def zrotate(self, x, y, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _x = (x * c) - (y * s)
        _y = (x * s) + (y * c)

        return _x, _y

    def connect(self, p1, p2):
        pygame.draw.line(self.main.dis, (255, 255, 255), (p1[0], p1[1]), (p2[0], p2[1]))

    def vertex_proc(self):
        #self.fov += .2 * self.main.dt
        #self.obj[1] += (50 * self.main.dt) % 360
        #self.obj[2] += (50 * self.main.dt) % 360
        #self.fov += 3.5 * self.main.dt
        points = self.obj[0]
        centre = self.obj[3]
        #points_index = self.obj[3]

        for id, p in enumerate(points):
            campos = self.main.cam.pos
            perspx = campos[0] - p[0]
            perspy = campos[1] - p[1]
            perspz = campos[2] - p[2]

            x, z = self.yrotate(perspx, perspz, self.main.cam.rot)
            y, z = self.xrotate(perspy, z, -self.main.cam.rot2)
            #x, y = self.zrotate(x, y, -self.main.cam.rot)
            #y = p[1]
            
            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)
            

            #self.point(x, y, 2)
            points[id][-1] = (x, y)

    def render(self):
        points = self.obj[0]
        points_index = self.obj[4]

        # connecting each dot to actually draw the object
        for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                self.connect(points[p_id][-1], points[i1][-1])
                self.connect(points[i1][-1], points[i2][-1])
                self.connect(points[i2][-1], points[p_id][-1])

                #self.shader(points[p_id][-1], points[i1][-1], points[i2][-1])

    def triangle_area(self, p1, p2, p3):
        return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2)
    def shader(self, p1, p2, p3):
        x_list = [p1[0], p2[0], p3[0]]
        y_list = [p1[1], p2[1], p3[1]]
        minx = min(x_list)
        miny = min(y_list)
        maxx = max(x_list)
        maxy = max(y_list)
        square_prem = (
            abs(maxx - minx),
            abs(maxy - miny)
        )

        for x in range(int(square_prem[0])):
            for y in range(int(square_prem[1])):
                p = (minx + x, miny + y)

                a1 = self.triangle_area(p1, p2, p3)
                a2 = self.triangle_area(p, p1, p2)
                a3 = self.triangle_area(p, p2, p3)
                a4 = self.triangle_area(p, p1, p3)

                if int(a2 + a3 + a4) == int(a1):
                    _x, _y = self.translate_coord(p[0], p[1])
                    _x -= DISZ[0] / 2
                    _y -= DISZ[1] / 2
                    self.main.dis.set_at((_x, _y), (255, 0, 0))
                else:
                    continue

class Cube:
    def __init__(self, centre, dim, thetax, thetay):
        self.fov = 0

        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2
        points = [
            # top left                      bottom left                 top right                    bottom right
            [-width2, -height2, -depth2], [-width2, height2, -depth2], [width2, -height2, -depth2], [width2, height2, -depth2],
            [-width2, -height2, depth2], [-width2, height2, depth2], [width2, -height2, depth2], [width2, height2, depth2]
        ]
        points = [[*i, i] for i in points]

        index = [

            # back
            0, 1, 2,
            3, 2, 1,

            # top
            0, 2, 6,
            6, 4, 0,

            # front
            4, 5, 7,
            7, 6, 4,

            # bottom
            1, 3, 7,
            7, 5, 1,

            # left
            0, 1, 5,
            5, 4, 0,

            # right
            2, 3, 7,
            7, 6, 2

        ]

        self.obj = [
            points, thetax, thetay, centre, index
        ]
