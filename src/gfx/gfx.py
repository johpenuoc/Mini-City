import pygame
import sys
from math import cos, sin, radians, sqrt
from random import uniform


from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from data.config import *

class Renderer:
    def __init__(self):
        self.fov = 0

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

    def connect(self, p1, p2, dis):
        pygame.draw.line(dis, (255, 255, 255), (p1[0], p1[1]), (p2[0], p2[1]))

    def draw(self, p1, p2, p3):
        if p1 == None or p2 == None or p3 == None:
            return False
        else:
            return True

    def vertex_proc(self, pos, camrot, camrot2):
        points = self.obj[0]
        centre = self.obj[1]

        campos = pos
        for id, p in enumerate(points):
            perspx = campos[0] - p[0] + centre[0]
            perspy = campos[1] - p[1] + centre[1]
            perspz = campos[2] - p[2] + centre[2]

            x, z = self.yrotate(perspx, perspz, camrot)
            y, z = self.xrotate(perspy, z, camrot2)

            buf = [0, 0, (x, y, z)]

            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)

            if not z < 0:
                buf[0] = x
                buf[1] = y
                points[id][-1] = buf
            else:
                points[id][-1] = None

    def render(self, dis, campos):
        points = self.obj[0]
        centre = self.obj[1]
        points_index = self.obj[2]

        for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                p = points[p_id][-1]
                p1 = points[i1][-1]
                p2 = points[i2][-1]

                if self.draw(p, p1, p2):
                    # p_3d = p[2]
                    # p1_3d = p1[2]
                    # p2_3d = p2[2]

                    p = p[:2]
                    p1 = p1[:2]
                    p2 = p2[:2]

                    x = (abs(campos[0]) - centre[0])**2
                    y = (abs(campos[2]) - centre[2])**2
                    distance = sqrt(x + y)

                    c = 255 / (distance / 20)
                    if c > 255:
                        c = 255
                    elif c < 0:
                        c = 0

                    change = (c / 255)
                        
                    colour = [int(i * change) for i in self.obj[3]]
                    colour = tuple(colour)
                    pygame.draw.polygon(dis, colour, (p, p1, p2))

                
COLOURS = {
    0 : (0, 0, 0),
    1 : (255, 0, 0),
    2 : (0, 255, 0),
    3 : (0, 0, 255),
    4 : (255, 255, 0),
    5 : (255, 0, 255),
    6 : (0, 255, 255),
    7 : (255, 255, 255)
}
class Cube(Renderer):
    def __init__(self, centre, dim, colour):
        super().__init__()
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
            points, centre, index, COLOURS[colour]
        ]

class Floor(Renderer):
    def __init__(self, centre, dim, colour):
        super().__init__()
        self.fov = 0

        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2
        points = [
            [-width2, height2, -depth2],[width2, height2, -depth2],
            [-width2, height2, depth2], [width2, height2, depth2]
        ]
        points = [[*i, i] for i in points]

        index = [
            0, 1, 2,
            2, 1, 3
        ]

        colour = 2
        self.obj = [
            points, centre, index, COLOURS[colour]
        ]

class Sphere(Renderer):
    def __init__(self, centre, dim, colour):
        super().__init__()
        self.fov = 0

        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2
        points = [
            [0, height2, 0],                         
            [0, -height2, 0],                      
            
            [width2, 0, 0],                       
            [-width2, 0, 0],                    
            [0, 0, depth2],                        
            [0, 0, -depth2],                        
            
            [width2 * 0.7, height2 * 0.7, 0],         
            [-width2 * 0.7, height2 * 0.7, 0],      
            [0, height2 * 0.7, depth2 * 0.7],        
            [0, height2 * 0.7, -depth2 * 0.7],        
            
            [width2 * 0.7, -height2 * 0.7, 0],        
            [-width2 * 0.7, -height2 * 0.7, 0],     
            [0, -height2 * 0.7, depth2 * 0.7],       
            [0, -height2 * 0.7, -depth2 * 0.7],       
        ]

        points = [[*i, i] for i in points]

        index = [
            0, 6, 8,
            0, 8, 7,
            0, 7, 9,
            0, 9, 6,
            
            6, 2, 8,   8, 2, 4,
            8, 4, 7,   7, 4, 3,
            7, 3, 9,   9, 3, 5,
            9, 5, 6,   6, 5, 2,

            2, 10, 4,  4, 10, 12,
            4, 12, 3,  3, 12, 11,
            3, 11, 5,  5, 11, 13,
            5, 13, 2,  2, 13, 10,

            1, 8, 10,
            1, 10, 12,
            1, 12, 11,
            1, 11, 13,
            1, 13, 10
        ]

        self.obj = [
            points, centre, index, COLOURS[colour]
        ]

class Pyramid(Renderer):
    def __init__(self, centre, dim, colour):
        super().__init__()
        self.fov = 0

        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2

        points = [
            [0, height2, 0],        
            [-width2, -height2, -depth2],
            [width2, -height2, -depth2], 
            [width2, -height2, depth2], 
            [-width2, -height2, depth2]  
        ]
        
        points = [[*i, i] for i in points]

        index = [

            0, 1, 2,
            0, 2, 3,
            0, 3, 4,
            0, 4, 1,
    
            1, 4, 3,
            1, 3, 2
        ]

        self.obj = [points, centre, index, COLOURS[colour]]

class Cylinder(Renderer):
    def __init__(self, centre, dim, colour):
        super().__init__()
        self.fov = 0

        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2

        points = [
            [0, height2, 0],  
            [0, -height2, 0],   
  
            [width2, height2, 0],  
            [-width2, height2, 0],
            [0, height2, depth2],  
            [0, height2, -depth2], 
          
            [width2, -height2, 0],
            [-width2, -height2, 0],
            [0, -height2, depth2], 
            [0, -height2, -depth2] 
        ]
        
        points = [[*i, i] for i in points]

        index = [
    
            0, 4, 2,  0, 2, 5,  0, 5, 3,  0, 3, 4,
        
            1, 6, 8,  1, 8, 6,  #
            1, 9, 6,  1, 7, 9,  1, 8, 7,
     
            2, 6, 4,  4, 6, 8,
            4, 8, 3,  3, 8, 7,
            3, 7, 5,  5, 7, 9,
            5, 9, 2,  2, 9, 6
        ]

        self.obj = [points, centre, index, COLOURS[colour]]