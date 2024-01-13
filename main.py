import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sin, cos

# Initialize Pygame
pygame.init()

# Set the window dimensions
width, height = 600, 600

# Initialize the Pygame window
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
glOrtho(0, width, 0, height, -1, 1)

# Set up the game grid
grid = [['', '', ''],
        ['', '', ''],
        ['', '', '']]

# Variable to keep track of the current player ('X' or 'O')
current_player = 'X'

def draw_grid():
    for i in range(1, 3):
        glBegin(GL_LINES)
        glVertex2f(i * width / 3, 0)
        glVertex2f(i * width / 3, height)
        glEnd()

        glBegin(GL_LINES)
        glVertex2f(0, i * height / 3)
        glVertex2f(width, i * height / 3)
        glEnd()

def draw_X(x, y):
    glBegin(GL_LINES)
    glVertex2f(x + 50, y + 50)
    glVertex2f(x + 150, y + 150)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(x + 150, y + 50)
    glVertex2f(x + 50, y + 150)
    glEnd()

def draw_O(x, y):
    radius = min(width, height) // 10  

    glBegin(GL_LINE_LOOP)
    for i in range(100):
        angle = 2.0 * 3.1415926 * i / 100
        glVertex2f(x + width / 6 + radius * cos(angle), y + height / 6 + radius * sin(angle))
    glEnd()


def draw_board():
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 'X':
                draw_X(col * width / 3, row * height / 3)
            elif grid[row][col] == 'O':
                draw_O(col * width / 3, row * height / 3)

def check_winner():
    # Check rows and columns
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != '':
            return grid[i][0]  # Row
        if grid[0][i] == grid[1][i] == grid[2][i] != '':
            return grid[0][i]  # Column

    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] != '':
        return grid[0][0]  # Diagonal from top-left to bottom-right
    if grid[0][2] == grid[1][1] == grid[2][0] != '':
        return grid[0][2]  # Diagonal from top-right to bottom-left

    return None  # No winner

def is_board_full():
    for row in grid:
        for cell in row:
            if cell == '':
                return False
    return True

def main():
    global current_player

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = int(x // (width / 3))
                row = 2 - int(y // (height / 3))

                if grid[row][col] == '' and not check_winner():
                    grid[row][col] = current_player
                    current_player = 'O' if current_player == 'X' else 'X'


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        draw_board()

        winner = check_winner()
        if winner:
            print(f"Player {winner} wins!")
            pygame.quit()
            quit()
        elif is_board_full():
            print("It's a draw!")
            pygame.quit()
            quit()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
