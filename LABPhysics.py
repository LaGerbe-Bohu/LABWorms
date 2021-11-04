import sys
import pygame
import math

gravity = -9.8


def setGravity(grav):
    gravity = grav;


# position X0 Y0 angle et force du tir
def simulate(X, Y, angle,Force):

    time = pygame.time.get_ticks()/200
    print(time)
    V = Force * math.cos(math.radians(angle))
    W = Force * math.sin(math.radians(angle))
    return [V * time + X, -1 / 2 * gravity * time ** 2 + W * time + Y]
