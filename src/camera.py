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

        self.fov = [0, 0]
        self.pos = [0, 0, 0]
        self.rot = 0
        self.rot2 = 0

    def move(self):
        keys = pygame.key.get_pressed()
        dt = self.main.dt

        new_rot = keys[pygame.K_d] - keys[pygame.K_a]
        fb = keys[pygame.K_w] - keys[pygame.K_s]

        mrel = pygame.mouse.get_rel()
        self.rot += mrel[0] * 120 * dt
        self.rot2 += mrel[1] * 120 * dt

        #self.rot += new_rot * 10 * dt
        self.pos[0] += cos(radians(self.rot)) * 5 * fb * dt
        #self.pos[1] += sin(radians(self.rot)) * 5 * fb * dt
        self.pos[2] += sin(radians(self.rot)) * 5 * fb * dt

        #self.rot %= 360