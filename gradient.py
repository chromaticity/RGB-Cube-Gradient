import pygame
import pygame.gfxdraw
import random
import time
import numpy as np
from sympy import symbols, Eq, solve

background_color = 38, 38, 38
impossible_brightness_factor = 1
height = 500
width = 500
delay_seconds = 5

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Gradients")
screen.fill(background_color)
pygame.display.flip()



def draw_point(x, y, color):
    pygame.gfxdraw.pixel(screen, x, y, color)


#Gives the Point p*100% of the way from a to b.
def weighted_average(a, b, p):
    delta = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
    return (a[0]+delta[0]*p, a[1]+delta[1]*p, a[2]+delta[2]*p)



#in 3d space, p1 is the bottomleft, p2 is bottomright, p3 is topleft of the plane.
#This function gets the coordinates on a bounded plane in 3d.
def plane_coordinates(p1, p2, p3): 
    #grid[x] = xth row, 
    grid = []
    for i in range(height+1):
        p1p2 = weighted_average(p1, p2, i/height)
        row = []
        for j in range(width+1):
            row.append(weighted_average(p1p2, p3, j/width))
        grid.append(row)
    return grid
            
def points_to_rgb(points):
    rgbgrid = []
    for i in range(len(points)):
        row = []
        for j in range(len(points[i])):
            p = points[i][j]
            rgb = (round(p[0]*255), round(p[1]*255), round(p[2]*255))
            m = max(rgb)
            if m>255:
                rgb = (round(rgb[0]*impossible_brightness_factor*255/m), round(rgb[1]*255*impossible_brightness_factor/m), round(rgb[2]*255*impossible_brightness_factor/m))
            if rgb[0]<0:
                rgb = (0, rgb[1], rgb[2])
            if rgb[1]<0:
                rgb = (rgb[0], 0, rgb[2])
            if rgb[2]<0:
                rgb = (rgb[0], rgb[1], 0)
            
            row.append(rgb)
        rgbgrid.append(row)
    
    
    return rgbgrid

def draw_rgb_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            draw_point(x, y, grid[y][x])

running = True


# Function to generate a random point in 3D space
def generate_random_point():
    return np.random.rand(3)

# Function to calculate the length of a vector
def calculate_length(vector):
    return np.linalg.norm(vector)

def filtered_triplet():
    while True:
        triplet = random_triplet()
        C = triplet[2]
        if min(C)>0 and max(C)<1:
            return triplet

def random_triplet():
    # Generate random points A and B
    length_AB=0
    while length_AB<1:
        A = generate_random_point()
        B = generate_random_point()

        # Calculate vector AB
        AB = B - A

        # Calculate the length of AB
        length_AB = calculate_length(AB)

    # Generate a random vector U
    U = np.random.rand(3)

    # Calculate the cross product of AB and U to get a vector perpendicular to AB
    perpendicularVector = np.cross(AB, U)

    # Normalize the perpendicular vector and scale it to the length of AB to get AC
    AC = perpendicularVector / calculate_length(perpendicularVector) * length_AB *width/height

    # Add AC to point A to get point C
    C = A + AC

    return (tuple(A.tolist()), tuple(B.tolist()), tuple(C.tolist()))





    


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    p1,p2,p3 = filtered_triplet()
    draw_rgb_grid(points_to_rgb(plane_coordinates(p1, p2, p3)))
    pygame.display.flip()
    time.sleep(delay_seconds)
