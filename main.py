# les libs
import math
import sys
import time
import pygame
import LibPhx
from random import randrange

class Equipe:
    def __init__(self,nom,couleur):
        self.nom = nom;
        self.couleur = couleur;

    def get_Couleur(self):
        return self.couleur;

    def get_nom(self):
        return self.nom;



# initialisation de pygame :
pygame.init()
size = width, height = 1440, 900
black = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
myfont2 = pygame.font.SysFont('Comic Sans MS', 25)

# le décor
decore =  pygame.Surface((1440, 900), pygame.SRCALPHA)
lifebarEquipe =  pygame.Surface((100, 30), pygame.SRCALPHA)
arrow = pygame.image.load("Images/Arrow.png")
arrowRocket = pygame.image.load("Images/ArrowRocket.png")
arrowWind = pygame.image.load("Images/ArrowWind.png")
fond = pygame.image.load("Images/fond.png")
decorerect = decore.get_rect()





nbWormsEquipe = 1

QueuePlay = []
Equipes = [Equipe('Equipe 1',(255,0,0,255)),Equipe('Equipe 2',(0,0,255,255)),Equipe('Equipe 3',(255,255,0,255))]


listOfWorms = []
EquipeIdx = 0
for i in range(0,nbWormsEquipe*len(Equipes)):
    EquipeIdx+=1
    worms = pygame.image.load("Images/worms.png")
    wormsrect = worms.get_rect()

    listOfWorms.append( LibPhx.Worms(randrange(0,screen.get_width()) , 500 ,worms,wormsrect,Equipes[ EquipeIdx % len(Equipes)]) )

for i in listOfWorms:
    QueuePlay.append(i)

currentWorms = QueuePlay.pop()
QueuePlay.append(currentWorms)

Clock = pygame.time.Clock()
AngleWind = randrange(float(0),float(360));

arrowWind = pygame.transform.rotate(arrowWind, -AngleWind - 90)

windForce=5;

viser = True
InfoTir = [0,0,0]
grenade = None
rocket = None

timerGranade = 100
timerRocket = 0

selectRocket = False;
selectGrenade = True;

pressed = False;
killed = False;

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

def findWorms(_currentWorms):
    _currentWorms.Setvelocity(0, 0)
    _currentWorms = QueuePlay.pop(0)
    QueuePlay.append(_currentWorms)

    return _currentWorms



while 1:
    # pour fermer la fenêtre
    Clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                pass
                #pressed = True;

            if event.key == pygame.K_g:
                selectGrenade = True;
                selectRocket = False\

            if event.key ==  pygame.K_r:
                selectRocket = True;
                selectGrenade = False;


        if event.type == pygame.MOUSEBUTTONDOWN:
            viser = False
            if(selectRocket):
                imgrocket = pygame.image.load("Images/rocket.png");
                imgrocket = pygame.transform.rotate(imgrocket, InfoTir[2] )
                rocket = LibPhx.Collider(InfoTir[0],InfoTir[1], imgrocket,imgrocket.get_rect());
                rocket.addForce(-InfoTir[2], 300)
                counter = timerRocket

            if(selectGrenade):
                grenade = LibPhx.Collider(InfoTir[0],InfoTir[1], pygame.image.load("Images/W4_Grenade.png"),pygame.image.load("Images/W4_Grenade.png").get_rect())
                grenade.addForce(-InfoTir[2],100)
                counter = timerGranade


    screen.fill(black)




    screen.blit(fond, fond.get_rect())
    screen.blit(decore, decorerect)
    k = 0
    for i in Equipes:

        life = 0;
        for j in listOfWorms:
            if (i == j.get_Equipe()):
                life = life + j.getLife()
        textsurface = myfont2.render(i.get_nom() + " :" + str(int(life)), False, i.get_Couleur())

        screen.blit(textsurface, ( 0,50 * k))
        k+=1


    if rocket != None:
        rocket.draw(screen)
        rocket.simulate()
        val = rocket.collision(decore, decorerect, 0.8)
        rocket.setWind(5 * math.cos(AngleWind),5 * math.sin(AngleWind))

        if(val ):
            pos = rocket.getPosition()
            destroyDecor(int(pos[0]), int(pos[1]))
            rocket = None
            pressed = True;
            for i in listOfWorms:
                i.calculedommage(pos[0], pos[1])




    if grenade != None:
        grenade.draw(screen)
        grenade.simulate()
        grenade.collision(decore, decorerect, 0.8)

        counter -= 1

        grenade.setWind(5 * math.cos(AngleWind), 5 * math.sin(AngleWind))

        if(counter < 0):
            pos = grenade.getPosition()
            destroyDecor(int(pos[0]),int(pos[1]))
            grenade = None
            pressed = True;
            for i in listOfWorms:
                i.calculedommage(pos[0],pos[1])


    for i in listOfWorms:

        if( i == currentWorms and i.getLife()<= 0):
            killed = True;

        if(i.getLife() > 0):
            i.draw(screen, myfont)
            i.simulate();
            i.collision(decore, decorerect, 0.8)

            if(i == currentWorms ):
                    i.move()
                    i.debuggerBounds()

                    if viser:

                        if(selectGrenade):
                            balistic = LibPhx.balistic(InfoTir[0], InfoTir[1], 0.01, -InfoTir[2], 100, currentWorms.get_Equipe().get_Couleur());
                            balistic.setWind(windForce * math.cos(AngleWind), windForce * math.sin(AngleWind))
                            balistic.line(decore, 0.8)
                            balistic.draw(screen)

                            InfoTir = i.Viser(arrow, screen)
                        elif(selectRocket) :
                            balistic = LibPhx.balistic(InfoTir[0], InfoTir[1], 0.01, -InfoTir[2], 300, currentWorms.get_Equipe().get_Couleur());
                            balistic.setWind(windForce * math.cos(AngleWind), windForce * math.sin(AngleWind))
                            balistic.line(decore, 0)
                            balistic.draw(screen)

                            InfoTir = i.Viser(arrowRocket, screen)


    if(pressed or killed):
        currentEquipe = currentWorms.get_Equipe().get_nom()
        currentWorms = findWorms(currentWorms)

        if (currentWorms.getLife() <= 0 ):
            currentWorms = findWorms(currentWorms)

        viser = True
        pressed = False;
        killed = False;

    screen.blit(arrowWind, (screen.get_width()-80,25))

    pygame.display.flip()

