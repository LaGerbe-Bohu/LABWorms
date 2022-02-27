import sys
import pygame
import math

def scalaire(A, B, C):
    return (B[0] - A[0]) * (C[0] - A[0]) + (B[1] - A[1]) * (C[1] - A[1])


def normalise(vec):
    return math.sqrt((vec[0] * vec[0]) + (vec[1] * vec[1]))


def normalized(vec):
    normal = normalise(vec)
    return [vec[0] / normal, vec[1] / normal]

def lerp(a,b,c):
    return (c*a) + ((1-c) * b)

def clamp(current,_min,_max):
    return max(min(_max,current),_min)



def getAngle(A, B):
    AB = [B[0] - A[0], B[1] - A[1]]
    norme = math.sqrt((AB[0] * AB[0]) + (AB[1] * AB[1]))

    ABnorm = [AB[0] / norme, AB[1] / norme]
    norme = math.sqrt((ABnorm[0] * ABnorm[0]) + (ABnorm[1] * ABnorm[1]))

    C = [A[0] + ABnorm[0], A[1] + ABnorm[1]]
    B = [A[0] + 1, A[1]]
    scl = scalaire(A, B, C)
    return (math.acos(scl / (norme)) * 180 / math.pi)


class body:
    gravity = -9.8

    # getters/setters

    def setGravity(self, grav):
        self.gravity = grav

    def Setvelocity(self, x, y):
        self.velocity[0] = x
        self.velocity[1] = y

    def getVelocity(self):
        return self.velocity

    def setWind(self,x,y):
        self.wind[0] = x
        self.wind[1] = y

    def getPosition(self):
        return self.currentPosition;

    def Addvelocity(self, x, y):
        self.velocity[0] = x
        self.velocity[1] = y

    # constructeur

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = body.gravity
        self.currentPosition = [x, y]
        self.pivot = [0, 0]
        self.velocity = [0, 0]
        self.pas = 0
        self.angle = 0
        self.Force = 0
        self.oldPosition = self.currentPosition
        self.vitesse = [0, 0]
        self.simulationSpeed = 0.1
        self.wind = [0,0]

    def addForce(self, angle, Force):
        self.angle = angle
        self.Force = Force

    def simulate(self):
        self.pas += self.simulationSpeed

        V = (self.Force * math.cos(math.radians(self.angle))) + self.velocity[0] + self.wind[0]
        W = ((-self.gravity *self.pas) + self.Force * math.sin(math.radians(self.angle)) ) + self.velocity[1] + self.wind[1]
        self.vitesse = [V, W]
        self.currentPosition = [V * self.pas + (self.x),
                                (-1 / 2 * self.gravity * self.pas ** 2) +( W * self.pas) + (self.y)]

        return self.currentPosition

    def collision(self, decore, decorerect, coefRebond):
        x = int(max(0, min(decorerect.width - 1, self.currentPosition[0] + self.pivot[0])))
        y = int(max(0, min(decorerect.height - 1, self.currentPosition[1] + self.pivot[1])))

        color = decore.get_at((x, y))

        if color[3] > 0 :

            pos = self.findSurface(decore, decorerect, self.currentPosition[0], self.currentPosition[1]);
            self.x = self.currentPosition[0]
            self.currentPosition[1] = pos[1]
            self.y =  self.currentPosition[1]
            self.pas = 0

            A = self.currentPosition
            B = [A[0] + 1, A[1]]
            C = [A[0] + self.vitesse[0], A[1] + self.vitesse[1]]
            normeAB = normalise([B[0] - A[0], B[1] - A[1]])
            normalizedAB = normalized([B[0] - A[0], B[1] - A[1]])
            scl = scalaire(A, B, C)
            normeAH = scl / (normeAB)
            projection = [A[0] + normeAH * normalizedAB[0], A[1] + normeAH * normalizedAB[1]]
            symetrie = [2 * projection[0] - C[0], 2 * projection[1] - C[1]]

            Force = normalise([symetrie[0] - A[0], symetrie[1] - A[1]])
            Force = Force

            self.addForce(0,0)

            if(Force > 1):
                self.addForce(-getAngle(A,symetrie),((Force)) * coefRebond)
            return True;
        return False;

    def findSurface(self, decore, decorerect, x_, y_):

        trouver = False;
        y = int(y_)
        x = int(x_)
        while (trouver == False):

            y = int(max(0, min(decorerect.height - 1, y)))
            x = int(max(0, min(decorerect.width - 1, x)))

            color = decore.get_at((x, y + self.pivot[1]))

            if color[3] > 0:
                y = y - 1
            else:
                trouver = True

        return [x, y + 1 ]


class Collider(body):

    def __init__(self, x, y, image, rect):
        body.__init__(self, x, y)
        self.image = image
        self.rect = rect
        self.pivot = [self.rect.width / 2, self.rect.height]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.x = self.currentPosition[0];
        self.rect.y = self.currentPosition[1]

    def __str__(self):
        return str(self.x) + "/" + str(self.y)

    def debuggerBounds(self):
        x =int(max(0, min(self.rect.width - 1, self.pivot[0])))
        y = int(max(0, min(self.rect.height - 1, self.pivot[1])))

        self.image.set_at((x, y), (255, 0, 0, 255))


class Worms(Collider):

    MaxHitDammage = 80
    MinDistanceHit = 100

    def __init__(self, x, y, image, rect, Equipe):
        Collider.__init__(self, x, y, image, rect)
        self.Equipe = Equipe
        self.flip = False
        self.Arrow = image
        self.Angle = 0
        self.tir = Collider(0, 0, image, rect)
        self.life = 100
        self.lifebar = pygame.Surface((100, 10), pygame.SRCALPHA)






    def calculedommage(self,x,y):
        vector = [self.currentPosition[0] - x,self.currentPosition[1] - y]
        distance = normalise(vector)
        value = distance/Worms.MinDistanceHit;
        value = clamp(value,0,1)
        dammage = lerp(0,Worms.MaxHitDammage,abs(value))

        self.life = self.life - dammage

        if(self.life < 0):
            self.life  = 0;





    def Viser(self, Arrow, screen):

        self.Arrow = Arrow

        A = [self.currentPosition[0] + self.pivot[0], self.currentPosition[1]];
        Mouse = pygame.mouse.get_pos()

        self.Angle = getAngle(A, Mouse)

        if (Mouse[1] > A[1]):
            self.Angle = -self.Angle

        self.Arrow = pygame.transform.rotate(self.Arrow, self.Angle - 90)
        ABnorm = normalized([Mouse[0] - A[0], Mouse[1] - A[1]])
        screen.blit(self.Arrow, [A[0] + ABnorm[0] * 50 - self.Arrow.get_rect().width / 2,
                                 A[1] + ABnorm[1] * 50 - self.Arrow.get_rect().height / 2])

        return A  + [self.Angle]

    def getLife(self):
        return self.life;

    def get_Equipe(self):
        return self.Equipe;

    def draw(self, screen, font):
        Collider.draw(self, screen)

        textsurface = font.render(self.Equipe.get_nom(), False, (0,0, 0))

        if self.velocity[0] > 0 and not self.flip:
            self.flip = True;
            self.debuggerBounds()
            self.image = pygame.transform.flip(self.image, True, False)

        if self.velocity[0] < 0 and self.flip:
            self.flip = False
            self.image = pygame.transform.flip(self.image, True, False)


        for i in range(0,(int(self.lifebar.get_rect().width))):
            for j in range(0, self.lifebar.get_rect().height):
                self.lifebar.set_at((int(i),int(j)),(0,0,0,0))

        for i in range(0,(int(self.life))):
            for j in range(0, self.lifebar.get_rect().height):
                self.lifebar.set_at((int(i),int(j)),self.Equipe.get_Couleur())

        screen.blit(self.lifebar, (self.currentPosition[0] - (self.lifebar.get_rect().width/2) + self.pivot[0], self.currentPosition[1] - 20))
        screen.blit(textsurface, (self.currentPosition[0] - (textsurface.get_rect().width/2) + self.pivot[0], self.currentPosition[1] - 40))

    def move(self):
        keys = pygame.key.get_pressed()
        self.Setvelocity(0, 0)

        if (keys[pygame.K_RIGHT]):
            self.Setvelocity(5, 0)

        if (keys[pygame.K_LEFT]):
            self.Setvelocity(-5, 0)


class balistic(body):


    def __init__(self,x,y,simulationspeed,angle,force,couleur):
        body.__init__(self,x,y)
        self.simulationSpeed = simulationspeed;
        self.arrayOfPos = []
        self.Force = force;
        self.Angle = angle;
        self.rayTex = pygame.Surface((10, 10), pygame.SRCALPHA)

        for i in range(0, (int(self.rayTex.get_rect().width))):
            for j in range(0, self.rayTex.get_rect().height):
                dst = math.sqrt((i - 5) ** 2 + (j - 5) ** 2)
                if(dst < 2):
                    self.rayTex.set_at((int(i), int(j)), couleur)


    def line(self,decore,coefrebond):
        x = 0
        body.addForce(self,self.Angle,self.Force)
        while( x < 1000):
            body.simulate(self)
            body.collision(self,decore,decore.get_rect(),coefrebond)
            self.arrayOfPos.append((self.currentPosition[0],self.currentPosition[1]))
            x+=1

    def draw(self,screen):
        for i in self.arrayOfPos:
            screen.blit(self.rayTex, (i))