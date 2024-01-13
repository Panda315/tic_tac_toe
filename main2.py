import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sin, cos
import sys

# Initialize Pygame
pygame.init()

# Set the window dimensions
width, height = 600, 600

# to control the loop in show_result
called = False

# Initialize the Pygame window
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Font
font = pygame.font.Font(None, 36)

grid = [['', '', ''],
        ['', '', ''],
        ['', '', '']]

def draw_message(message, result_button, new_game_button):
    print(message)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    screen = pygame.display.set_mode((width, height))
    glOrtho(0, width, 0, height, -1, 1)
    screen.fill(white)

    # Display the message
    text = font.render(message, True, black)
    text_rect = text.get_rect(center=(width // 2, height // 3))
    screen.blit(text, text_rect)

    # Draw the "View Result" button
    pygame.draw.rect(screen, green, result_button)
    result_text = font.render('View Result', True, white)
    result_text_rect = result_text.get_rect(center=(result_button.centerx, result_button.centery))
    screen.blit(result_text, result_text_rect)

    # Draw the "New Game" button
    pygame.draw.rect(screen, red, new_game_button)
    new_game_text = font.render('New Game', True, white)
    new_game_text_rect = new_game_text.get_rect(center=(new_game_button.centerx, new_game_button.centery))
    screen.blit(new_game_text, new_game_text_rect)

    pygame.display.flip()
    pygame.time.wait(2000)

def draw_grid():
    glColor3f(1.0, 1.0, 1.0)
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
    glColor3f(1.0, 1.0, 1.0)
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
    glColor3f(1.0, 1.0, 1.0)
    for i in range(100):
        angle = 2.0 * 3.1415926 * i / 100
        glVertex2f(x + width / 6 + radius * cos(angle), y + height / 6 + radius * sin(angle))
    glEnd()

def draw_board(grid):
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 'X':
                draw_X(col * width / 3, row * height / 3)
            elif grid[row][col] == 'O':
                draw_O(col * width / 3, row * height / 3)

def check_winner(grid):
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != '':
            return grid[i][0]  # Row
        if grid[0][i] == grid[1][i] == grid[2][i] != '':
            return grid[0][i]  # Column

    if grid[0][0] == grid[1][1] == grid[2][2] != '':
        return grid[0][0]  # Diagonal from top-left to bottom-right
    if grid[0][2] == grid[1][1] == grid[2][0] != '':
        return grid[0][2]  # Diagonal from top-right to bottom-left

    return None  # No winner

def is_board_full(grid):
    for row in grid:
        for cell in row:
            if cell == '':
                return False
    return True

def main_game_loop():
    global width, height,grid_needed
    # Set the OpenGL orthographic projection
    glOrtho(0, width, 0, height, -1, 1)

    current_player = 'X'

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = int(x // (width / 3))
                row = 2 - int(y // (height / 3))

                if grid[row][col] == '' and not check_winner(grid):
                    grid[row][col] = current_player
                    current_player = 'O' if current_player == 'X' else 'X'

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)
        draw_grid()
        draw_board(grid)
        winner = check_winner(grid)
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
        elif is_board_full(grid):
            print("It's a draw!")
            game_over = True

        pygame.display.flip()
        pygame.time.wait(10)

    return grid

def view_result():
    # Create a new Pygame surface for the OpenGL context
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        
    # Set the OpenGL orthographic projection
    glOrtho(0, width, 0, height, -1, 1)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
        
        # Clear the OpenGL buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the grid and board
        draw_grid()
        draw_board(grid)
        # pygame.quit()
        # quit()
    
        # Update the display
        pygame.display.flip()
        pygame.time.wait(10)

def show_result(winner):
    global width, height,screen,called

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        result_button = pygame.Rect(width // 4, height // 2, width // 2, height // 8)
        new_game_button = pygame.Rect(width // 4, 2 * height // 3, width // 2, height // 8)

        draw_message(f"Player {winner} wins!", result_button, new_game_button)

        while not called:
            for event in pygame.event.get():
                if event.type == QUIT:
                    called = True
                    pygame.quit()
                    quit()

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos

                    if result_button.collidepoint(x, y):
                        view_result()
                        called = True
                        break

                    elif new_game_button.collidepoint(x, y):
                        reset_grid()
                        break
            

def reset_grid():
    global width, height, screen, grid

    # Set the window dimensions
    width, height = 600, 600

    # Reset other global variables
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    grid = [['', '', ''],
            ['', '', ''],
            ['', '', '']]

    main()


def main():
    global width, height

    game_grid = main_game_loop()
    winner = check_winner(game_grid)

    if winner:
        show_result(winner)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
