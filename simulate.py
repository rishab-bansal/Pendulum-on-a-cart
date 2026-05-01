import pygame
import pandas as pd
import math
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
ppm = 100       # Pixels per meter

# Initial positions
l = 1*ppm
xc = df.at[0,"xp"]*ppm
theta = df.at[0, "angle"]*math.pi/180
xp = xc - l*math.sin(theta)
yp = l*math.cos(theta)
# Defining the objects on screen
# Cart
cart_pos = pygame.Vector2(screen.get_width()/ 2 + xc, screen.get_height() / 2)
pen_pos = pygame.Vector2(screen.get_width()/2 + xp, screen.get_height()/2 + yp)
ref = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def mark(x,y,c):
    r = pygame.Vector2(screen.get_width() / 2 + x, screen.get_height() / 2 + y)
    pygame.draw.circle(screen, c, r, 4)


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
    pygame.draw.line(screen, "black", [0, screen.get_height() / 2 + 20], [screen.get_width(),screen.get_height() / 2 + 20], width=2)
    pygame.draw.circle(screen, "red", cart_pos, 20)
    pygame.draw.circle(screen, "purple", pen_pos,10)
    pygame.draw.line(screen, "black", cart_pos, pen_pos)
    # Putting the markers
    mark(0,0,"green")
    for i in range(1,10):
        mark(ppm*i,0, "blue")
        mark(-ppm*i, 0, "blue")


    if count < N:
        cart_pos.x = screen.get_width() / 2 + df.at[count, "xp"]*ppm
        
        th = df.at[count,"angle"]
        pen_pos.x = cart_pos.x - l*math.sin(th)
        pen_pos.y = cart_pos.y - l*math.cos(th)
    pygame.display.flip()

    # dt is the change in time every frame
    # dt is used for discrete time system
    count += 1
    dt = clock.tick(100)/1000 # Limits the fps to 60



pygame.quit()