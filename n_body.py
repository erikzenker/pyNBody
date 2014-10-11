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


# Define bodies
body1  = Body(1e12, array([0,0]), array([0,0]))
body2  = Body(1e1, array([2.4,0]), array([5,5]))
body3  = Body(1e1, array([2.4,0]), array([6,6]))
body4  = Body(1e1, array([2.4,0]), array([7,7]))
body5  = Body(1e1, array([2.4,0]), array([8,8]))
body6  = Body(1e1, array([2.4,0]), array([9,9]))
body7  = Body(1e1, array([2.4,0]), array([10,10]))

# Bodies that will be simulated
bodies = []
bodies.append(body1)
bodies.append(body2)
bodies.append(body3)
bodies.append(body4)
bodies.append(body5)
bodies.append(body6) 
bodies.append(body7) 

# Simulation constants
dt     = 0.1         # s
G      = 6.67384e-11 # m³ / (kg * s²)

# Pygame initialzation
pygame.init()
xResolution = 2*640
yResolution = 2*480
surface = pygame.display.set_mode((xResolution, yResolution))
xCenter = int(xResolution / 2)
yCenter = int(yResolution / 2)
font = pygame.font.Font(None, 20)

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

        # When body outside of window
        # replace on random position

        # Pygame draw body
        pygame.draw.circle(surface, bodies[i].c, (xCenter + int(bodies[i].r[0]), yCenter + int(bodies[i].r[1])), 5,1)

        # Pygame write elapsed time
        text = font.render("Time: " + str(int(timestep * dt))+"s", True, (255,255,255))
        surface.blit(text,(10,10))

# Output plot

