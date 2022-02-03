# les libs
import math
import sys
import time
import pygame
import LibPhx
from random import randrange

# initialisation de pygame :
pygame.init()
size = width, height = 1440, 900
black = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)


# le décor
decore =  pygame.Surface((1440, 900), pygame.SRCALPHA)
arrow = pygame.image.load("Images/Arrow.png")
fond = pygame.image.load("Images/fond.png")
decorerect = decore.get_rect()



nbWormsEquipe = 1

QueuePlay = []
Equipes = ['Equipe 1','Equipe 2','Equipe 3']
listOfWorms = []
EquipeIdx = 0
for i in range(0,nbWormsEquipe*len(Equipes)):
    EquipeIdx+=1
    worms = pygame.image.load("Images/worms.png")
    wormsrect = worms.get_rect()
    listOfWorms.append( LibPhx.Worms(randrange(0,screen.get_width()) , 500 ,worms,wormsrect,Equipes[ EquipeIdx % len(Equipes)])  )

for i in listOfWorms:
    QueuePlay.append(i)

currentWorms = QueuePlay.pop()
QueuePlay.append(currentWorms)

Clock = pygame.time.Clock()

viser = True
InfoTir = [0,0,0]
grenade = None

timer = 100
counter = timer

for i in range(0, decorerect.width):
    for j in range(int(decorerect.height/2), (decorerect.height)):
        x = i/ decorerect.width
        y = j/ decorerect.height
        l = (math.cos(x*30)*0.005)+0.7
        p = ((x-0.2)*(x-0.8) +7)/2

        if(y > (l*p)-1.8):
             decore.set_at((i, j), (83, 143, 68,255))


def destroyDecor(x,y):

    for i in range(x-150,x +100):
        for j in range(y-150,y + 100):

            dst = math.sqrt( (i-x)**2+(j-y)**2)

            if(dst < 100):
                decore.set_at((i,j),(255,255,255,0))


while 1:
    # pour fermer la fenêtre
    Clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                currentWorms.Setvelocity(0, 0)
                currentWorms = QueuePlay.pop(0)
                QueuePlay.append(currentWorms)
                viser = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            viser = False
            grenade = LibPhx.Collider(InfoTir[0],InfoTir[1], pygame.image.load("Images/Arrow.png"),pygame.image.load("Images/Arrow.png").get_rect())
            grenade.addForce(InfoTir[2],100)
            counter = timer


    screen.fill(black)

    screen.blit(fond, fond.get_rect())
    screen.blit(decore, decorerect)

    for i in listOfWorms:
        i.collision(decore, decorerect, 0.8)
        i.simulate();




    if grenade != None:
        grenade.draw(screen)
        grenade.collision(decore, decorerect, 0.8)
        grenade.simulate()


        counter -= 1

        if(counter < 0):
            pos = grenade.getPosition();
            destroyDecor(int(pos[0]),int(pos[1]))
            grenade = None




    for i in listOfWorms:
        i.draw(screen, myfont);
        if(i == currentWorms):
            i.move()
            i.debuggerBounds()
            if viser:
                InfoTir = i.Viser(arrow, screen)

    pygame.display.flip()
