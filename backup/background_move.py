import pygame
import math
import sys

clock = pygame.time.Clock()

FrameHeight = 600
FrameWidth = 1200

# COLORS

GREEN = (0,255,0)

# PYGAME FRAME WINDOW
pygame.display.set_caption("Arrow Key Scrolling in pygame")
screen = pygame.display.set_mode((FrameWidth, FrameHeight))

bg = pygame.image.load("chess.png").convert()


# DEFINING MAIN VARIABLES IN SCROLLING
scroll_x = 0  # Horizontal scroll variable
scroll_y = 0  # Vertical scroll variable
scroll_speed = 10  # Speed of scrolling

# NUMBER OF TILES REQUIRED FOR SCROLLING
tiles_x = math.ceil(FrameWidth / bg.get_width()) + 1
tiles_y = math.ceil(FrameHeight / bg.get_height()) + 1

character = pygame.image.load("sprite.png").convert_alpha()  # Assuming character image is 'character.png'

# CHARACTER SETTINGS
char_width, char_height = character.get_width(), character.get_height()
char_x = FrameWidth // 2 - char_width // 2  # Center horizontally
char_y = FrameHeight // 2 - char_height // 2  # Center vertically

# RECT
rect = pygame.Rect(30, 30, 60, 60)

# WALLS


while True:
    pygame.draw.rect(screen,(0,0,0),((0,0),(FrameWidth,FrameHeight)))
    clock.tick(50)  # Frame rate

    # Handle keyboard events to control scrolling
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:  # Left arrow key
        scroll_x += scroll_speed
    if keys[pygame.K_RIGHT]:  # Right arrow key
        scroll_x -= scroll_speed
    if keys[pygame.K_UP]:  # Up arrow key
        scroll_y += scroll_speed
    if keys[pygame.K_DOWN]:  # Down arrow key
        scroll_y -= scroll_speed
    if keys[pygame.K_q]:    # Press q to quit
        sys.exit()

    # Drawing the background
    for i in range(tiles_x):
        for j in range(tiles_y):
            screen.blit(bg, (bg.get_width() * i + scroll_x, bg.get_height() * j + scroll_y))

     # Draw the foreground character in the center of the screen
    screen.blit(character, (char_x, char_y))

    # Draw obstacle
    pygame.draw.rect(screen, GREEN, rect)
    
    # 

    # Handle events like closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
