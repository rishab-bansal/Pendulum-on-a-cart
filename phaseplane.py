import pygame
import pandas as pd
import math
import numpy as np
## Setup of pygame
pygame.init()
screen = pygame.display.set_mode((1200,800))
clock = pygame.time.Clock()
running  = True
dt = 0
pygame.display.set_caption("Pendulum on a cart")


# Extracting the data
df = pd.read_csv("data.csv")
count = 0
N = df.shape[0]
ppm = 60       # Pixels per meter

# Initial positions
x = df.at[0,"xp"]*ppm
y = df.at[0,"xv"]*ppm

point = pygame.Vector2(screen.get_width() / 2 + x, screen.get_height() / 2 - y)
ref = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
st = np.array([[point],])


################################################################################
### The loop ###################################################################
################################################################################
while running:
    # Closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe last frame
    screen.fill("white")

    # Render
    for i in st:
        print(st[0])
    
    pygame.draw.circle(screen, "red", point, 10)
    pygame.draw.circle(screen, "blue", ref, 5)
    if count < N:
        point.x = screen.get_width() / 2 + df.at[count, "xp"]*ppm
        point.y = screen.get_height() / 2 - df.at[count, "xv"]*ppm
    print(point)
    print("*****")
    pygame.display.flip()

    # dt is the change in time every frame
    # dt is used for discrete time system
    count += 1
    dt = clock.tick(100)/1000 # Limits the fps to 60



pygame.quit()