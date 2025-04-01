import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (135, 206, 250)  # Light sky blue
SWING_COLOR = (0, 255, 0)  # Green color for the rope
PLAYER_COLOR = (255, 0, 0)  # Red color for the player
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Playground Swing with Independent Player")

# Swing parameters
center_x = WIDTH // 2  # Centered horizontally
center_y = 150  # Fixed vertical position for the anchor point
swing_length = 200  # Length of the rope
angle = math.pi / 4  # Initial angle of swing
angle_velocity = 0  # Initial velocity
angle_acceleration = 0  # Initial acceleration
gravity = 0.1  # Gravitational constant

# Player parameters
player_width = 20
player_height = 40
player_x = WIDTH // 2  # Player starts in the middle horizontally
player_y = HEIGHT - 100  # Player starts at the bottom of the screen
player_speed = 5  # Player's speed for movement

# Function to draw the swing (only the rope)
def draw_swing(angle):
    # Calculate the position of the end of the rope (where it swings)
    rope_end_x = center_x + swing_length * math.sin(angle)
    rope_end_y = center_y - swing_length * math.cos(angle)

    # Draw the rope (from the center point to the end)
    pygame.draw.line(screen, SWING_COLOR, (center_x, center_y), (rope_end_x, rope_end_y), 5)

    return rope_end_x, rope_end_y

# Function to draw the player
def draw_player():
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x - player_width / 2, player_y - player_height / 2, player_width, player_height))

# Function to check for collision
def check_collision(rope_end_x, rope_end_y):
    # Check if the player is near the end of the swing (rope_end_x, rope_end_y)
    player_rect = pygame.Rect(player_x - player_width / 2, player_y - player_height / 2, player_width, player_height)
    swing_end_rect = pygame.Rect(rope_end_x - 5, rope_end_y - 5, 10, 10)  # Small collision area around the swing end

    return player_rect.colliderect(swing_end_rect)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simple physics for swinging motion
    angle_acceleration = -gravity / swing_length * math.sin(angle)
    angle_velocity += angle_acceleration
    angle += angle_velocity
    
    # No damping: the swing won't slow down over time

    # Draw the swing and get the end coordinates
    rope_end_x, rope_end_y = draw_swing(angle)

    # Control player with arrow keys (left/right/up/down)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed  # Move player left
    if keys[pygame.K_RIGHT]:
        player_x += player_speed  # Move player right
    if keys[pygame.K_UP]:
        player_y -= player_speed  # Move player up
    if keys[pygame.K_DOWN]:
        player_y += player_speed  # Move player down

    # Check if the player collides with the swing
    if check_collision(rope_end_x, rope_end_y):
        print("Game Over! Player touched the swing.")
        running = False

    # Draw the player
    draw_player()

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
