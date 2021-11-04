import sys
import time

import pygame


import LABPhysics

pygame.init()

size = width, height = 720*2, 450*2

speed = [0, 0]
pos = [ 0, height/2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("Intro_ball.gif")
ballrect = ball.get_rect()

ballrect.x = pos[0]
ballrect.y = pos[1]

Clock = pygame.time.Clock()

while 1 :
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    speed = LABPhysics.simulate(pos[0], pos[1], -30,120)

    ballrect.x = speed[0]
    ballrect.y = speed[1]




    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]

    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1];

    screen.fill(black)
    screen.blit(ball,ballrect)
    pygame.display.flip()

    Clock.tick_busy_loop(60)

