#! /usr/bin/python3

from numpy import *
from numpy import linalg
import pygame

class Body:
    m = 0            # Kg
    v = array([0,0]) # m / s
    r = array([0,0]) # m
    c = (255,255,255)

    def __init__(self, mass, velocity, location):
        self.m = mass
        self.v = velocity
        self.r = location
        self.c = randomRBGColor()

def randomRBGColor():
    r = random.triangular(0,125,255)
    b = random.triangular(0,125,255)
    g = random.triangular(0,125,255)
    
    return (int(r),int(b),int(g))

def randomBody(xRange, yRange, mRange, vRange):
    m  = random.randint(mRange[0], mRange[1])
    x  = random.randint(xRange[0], xRange[1])
    y  = random.randint(yRange[0], yRange[1])
    v1 = random.randint(vRange[0], vRange[1])
    v2 = random.randint(vRange[0], vRange[1])

    b  = Body(m, array([v1,v2]), array([x,y]))
    return b
    
def randomBody2():
    return randomBody((-2*640, 2*640), (-2*480,2*480), (1,1e12), (0,4))

# Pygame initialzation
pygame.init()
xResolution = 2*640
yResolution = 2*480
surface = pygame.display.set_mode((xResolution, yResolution))
xCenter = int(xResolution / 2)
yCenter = int(yResolution / 2)
font = pygame.font.Font(None, 20)


# Simulation constants
N    = 50
dt   = 1           # s
G    = 6.67384e-11 # m³ / (kg * s²)
maxV = 4           # m / s
maxM = 1e12        # kg

# Generate random bodies
bodies = []
for i in range(0, N):
    bodies.append(randomBody((-xResolution, xResolution), (-yResolution, yResolution), (1,maxM), (0,maxV)))


# Loop timesteps forever
timestep = 0
while True:

    # Increment timestep
    timestep = timestep + 1

    # Pygame update screen
    pygame.display.update()

    surface.fill((0,0,0))

    for i in range(0, len(bodies)):
        F = 0

        # Sum force of other bodies
        for j in range(0, len(bodies)):
            if i != j:
                F += G * bodies[i].m * bodies[j].m * ((bodies[j].r - bodies[i].r) / power(linalg.norm(bodies[j].r - bodies[i].r), 3))

        # Update body position
        a           = F / bodies[i].m
        s           = ((a/2) * power(dt,2) + bodies[i].v * dt + bodies[i].r)
        bodies[i].r =  s

        # Update body velocity
        bodies[i].v = a * dt + bodies[i].v

        # Bodies out of scope will be replaced by new random ones
        if bodies[i].r[0] > xCenter or bodies[i].r[0] < -xCenter:
            bodies[i] = randomBody((-xResolution, xResolution), (-yResolution, yResolution), (1,maxM), (0,maxV))
            
        if bodies[i].r[1] > yCenter or bodies[i].r[1] < -yCenter:
            bodies[i] = randomBody((-xResolution, xResolution), (-yResolution, yResolution), (1,maxM), (0,maxV))

        # Pygame draw body
        pygame.draw.circle(surface, bodies[i].c, (xCenter + int(bodies[i].r[0]), yCenter + int(bodies[i].r[1])), 5,1)

        # Pygame write elapsed time
        text = font.render("Time: " + str(int(timestep * dt))+"s", True, (255,255,255))
        surface.blit(text,(10,10))

