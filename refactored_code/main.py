import pygame

class Player:
    def __init__(self, x, y, width, height, vel):
        """
        Initializes the player.
        
        Parameters:
        - x, y: Initial position of the player
        - width, height: Size of the player
        - vel: Movement speed of the player
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel  # Speed of movement

    def move(self, keys, obstacles):
        """
        Handles player movement while avoiding obstacles.

        Parameters:
        - keys: Pressed keys from pygame.key.get_pressed()
        - obstacles: List of obstacle objects to check for collision
        """
        if keys[pygame.K_LEFT] and self.x > 0 and self.can_move(self.x - self.vel, self.y, obstacles):
            self.x -= self.vel  # Move left
        if keys[pygame.K_RIGHT] and self.x < 1000 - self.width and self.can_move(self.x + self.vel, self.y, obstacles):
            self.x += self.vel  # Move right
        if keys[pygame.K_UP] and self.y > 0 and self.can_move(self.x, self.y - self.vel, obstacles):
            self.y -= self.vel  # Move up
        if keys[pygame.K_DOWN] and self.y < 1000 - self.height and self.can_move(self.x, self.y + self.vel, obstacles):
            self.y += self.vel  # Move down

    def can_move(self, new_x, new_y, obstacles):
        """
        Checks if the player can move to the new position without colliding.

        Parameters:
        - new_x, new_y: The new position the player wants to move to
        - obstacles: List of obstacles to check against

        Returns:
        - True if the move is allowed, False if it collides
        """
        for obstacle in obstacles:
            if obstacle.collides_with(new_x, new_y, self.width, self.height):
                return False  # Block movement if collision detected
        return True

    def draw(self, screen):
        """
        Draws the player on the screen.

        Parameters:
        - screen: The game screen where the player will be drawn
        """
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Red color

class Obstacle:
    def __init__(self, x, y, width, height):
        """
        Initializes an obstacle.
        
        Parameters:
        - x, y: Position of the obstacle
        - width, height: Size of the obstacle
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        """
        Draws the obstacle on the screen.

        Parameters:
        - screen: The game screen where the obstacle will be drawn
        """
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))  # Blue color

    def collides_with(self, x, y, width, height):
        """
        Checks if a given rectangle (player) collides with this obstacle.

        Parameters:
        - x, y: Position of the rectangle
        - width, height: Size of the rectangle

        Returns:
        - True if there's a collision, False otherwise
        """
        return x < self.x + self.width and x + width > self.x and y < self.y + self.height and y + height > self.y

class Game:
    def __init__(self):
        """
        Initializes the game, including the window, player, and obstacles.
        """
        pygame.init()  # Initialize pygame
        self.screen = pygame.display.set_mode((1000, 1000))  # Create a 1000x1000 window
        pygame.display.set_caption("HEIST game")  # Set window title

        # Create the player
        self.player = Player(200, 200, 32, 32, 2.5)

        # Create multiple obstacles
        self.obstacles = [
            Obstacle(500, 500, 200, 100),  # Obstacle 1
            Obstacle(300, 300, 150, 150),  # Obstacle 2
            Obstacle(700, 200, 120, 180)   # Obstacle 3
        ]

        self.run = True  # Game loop flag

    def handle_events(self):
        """
        Handles user input events (like quitting the game).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False  # Stop game loop if window is closed

    def update(self):
        """
        Updates the game state (e.g., player movement).
        """
        keys = pygame.key.get_pressed()  # Get currently pressed keys
        self.player.move(keys, self.obstacles)  # Move the player

    def draw(self):
        """
        Draws all game elements (background, obstacles, player).
        """
        self.screen.fill((255, 255, 255))  # White background
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)  # Draw all obstacles
        self.player.draw(self.screen)  # Draw player
        pygame.display.update()  # Refresh the screen

    def run_game(self):
        """
        Main game loop. Keeps running until the player exits.
        """
        while self.run:
            pygame.time.delay(10)  # Add slight delay to control speed
            self.handle_events()  # Process user inputs
            self.update()  # Update game state
            self.draw()  # Draw everything on the screen

        pygame.quit()  # Close pygame when the loop exits

# Run the game only if this file is executed directly
if __name__ == "__main__":
    game = Game()  # Create a Game instance
    game.run_game()  # Start the game loop
