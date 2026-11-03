import pygame
import sys

from math import sin, cos, radians

from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from data.config import *

class Camera:
    def __init__(self, Main):
        self.main = Main

        self.pos = [50, 0, 50]
        self.rot = 0
        self.rot2 = 0

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

    def move(self):
        mpos = pygame.mouse.get_pos()
        #if mpos[0] > (WISZ[0] * 3) / 4 or mpos[0] < WISZ[0] / 4 or mpos[1] > (WISZ[1] * 3) / 4 or mpos[1] < WISZ[1] / 4:
        #    pygame.mouse.set_pos(DISZ)
        dt = self.main.dt

        mrel = pygame.mouse.get_rel()
        self.rot += mrel[0] / 10
        self.rot2 += mrel[1] / 10

        keys = pygame.key.get_pressed()
        fb = keys[pygame.K_w] - keys[pygame.K_s]
        lr = keys[pygame.K_a] - keys[pygame.K_d]

        self.pos[0] += cos(radians(self.rot + 90)) * 25 * fb * dt
        self.pos[1] = 0 
        self.pos[2] -= sin(radians(self.rot + 90)) * 25 * fb * dt

        self.pos[0] -= cos(radians(self.rot + 180)) * 25 * lr * dt
        self.pos[1] = 0 
        self.pos[2] += sin(radians(self.rot + 180)) * 25 * lr * dt
        
        self.rot %= 360
        self.rot2 %= 360