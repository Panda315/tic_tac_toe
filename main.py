import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Initializing Pygame
pygame.init()

# setting the window dimension
width , height = 600,600

# Initialize the pygame window
pygame.display.set_mode((width,height),DOUBLEBUF | OPENGL)
glOrtho(0,width,0,height,-1,1)

# set up the game grid
grid = [['','',''],
        ['','',''],
        ['','','']]

# variable to keep track of the current player ('X' or 'O')
current_player = 'X'

def draw_grid():
    for i in range(1,3):
        glBegin(GL_LINES)
        glVertex2f(i*width/3,0)
        glVertex2f(i*width/3,height)
        glEnd()

        glBegin(GL_LINES)
        glVertex2f(0,i*height/3)
        glVertex2f(width, i*height/3)
        glEnd()

def main():
    global current_player

if __name__ == "__main__":
    main()
