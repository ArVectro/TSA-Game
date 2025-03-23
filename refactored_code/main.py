import pygame
import random

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
        self.vel = vel
        self.inventory = []

    def move(self, keys, obstacles, items):
        """
        Handles player movement while avoiding obstacles and collecting items.

        Parameters:
        - keys: Pressed keys from pygame.key.get_pressed()
        - obstacles: List of obstacle objects to check for collision
        - items: List of item objects to check for collection
        """
        if keys[pygame.K_LEFT] and self.x > 0 and self.can_move(self.x - self.vel, self.y, obstacles):
            self.x -= self.vel  # Move left
        if keys[pygame.K_RIGHT] and self.x < 1000 - self.width and self.can_move(self.x + self.vel, self.y, obstacles):
            self.x += self.vel  # Move right
        if keys[pygame.K_UP] and self.y > 0 and self.can_move(self.x, self.y - self.vel, obstacles):
            self.y -= self.vel  # Move up
        if keys[pygame.K_DOWN] and self.y < 1000 - self.height and self.can_move(self.x, self.y + self.vel, obstacles):
            self.y += self.vel  # Move down
        
        self.collect_items(items)  # Check if player collects any items

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

    def collect_items(self, items):
        """
        Checks if the player collides with any items and collects them.

        Parameters:
        - items: List of item objects to check for collection
        """
        for item in items[:]:
            if item.collides_with(self.x, self.y, self.width, self.height):
                self.inventory.append(item)  # Add the item to player's inventory
                items.remove(item)  # Remove item from the game
                print(f"Money collected! Inventory: {len(self.inventory)} items.")  # Feedback

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

class Item:
    def __init__(self, x, y, width, height):
        """
        Initializes an item to be collected (looks like a coin).
        
        Parameters:
        - x, y: Position of the item
        - width, height: Size of the item (for a coin, width == height)
        """
        self.x = x
        self.y = y
        self.width = width  # Diameter of the coin (same for both width and height)
        self.height = height  # Diameter of the coin (same for both width and height)

    def draw(self, screen):
        """
        Draws the item (money) on the screen as a coin.

        Parameters:
        - screen: The game screen where the item will be drawn
        """
        # Draw a coin-like shape (circle) to represent money
        pygame.draw.circle(screen, (255, 223, 0), (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)  # Gold color

    def collides_with(self, x, y, width, height):
        """
        Checks if a given rectangle (player) collides with this item.

        Parameters:
        - x, y: Position of the rectangle
        - width, height: Size of the rectangle

        Returns:
        - True if there's a collision, False otherwise
        """
        return x < self.x + self.width and x + width > self.x and y < self.y + self.height and y + height > self.y

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("HEIST Game")

        self.player = Player(200, 200, 32, 32, 2.5)

        # Define level configurations with more coins (items)
  # Initialize empty levels first
        self.levels = []

        # Define levels with obstacles and then generate items
        level_1 = {
            "obstacles": [
                Obstacle(500, 500, 200, 100),
                Obstacle(200, 300, 150, 150),
                Obstacle(700, 200, 120, 180)
            ],
            "items": self.generate_items(30, 20)  # Now this works
        }

        level_2 = {
            "obstacles": [
                Obstacle(100, 100, 150, 100),
                Obstacle(600, 600, 200, 200),
                Obstacle(300, 400, 100, 100)
            ],
            "items": self.generate_items(50, 20)
        }

        level_3 = {
            "obstacles": [
                Obstacle(100, 100, 300, 100),
                Obstacle(500, 500, 100, 100)
            ],
            "items": self.generate_items(70, 20)
        }

        # Add the levels to the levels list
        self.levels.append(level_1)
        self.levels.append(level_2)
        self.levels.append(level_3),

        self.font = pygame.font.SysFont('Arial', 24)
        self.current_level = 0
        self.run = True

    def generate_items(self, num_items, size):
        """
        Generates a list of items (coins) at random positions with a fixed size.

        Parameters:
        - num_items: Number of items (coins) to generate
        - size: Size (diameter) of each coin

        Returns:
        - List of Item objects
        """
        items = []
        for _ in range(num_items):
            x = random.randint(50, 950)
            y = random.randint(50, 950)
            items.append(Item(x, y, size, size))  # All coins will be the same size
        return items

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        keys = pygame.key.get_pressed()
        current_level_data = self.levels[self.current_level]
        self.player.move(keys, current_level_data["obstacles"], current_level_data["items"])

        # Check if the player has collected all items
        if len(current_level_data["items"]) == 0:
            print(f"Level {self.current_level + 1} completed!")
            if self.current_level < len(self.levels) - 1:
                self.current_level += 1  # Move to next level
                self.player.inventory.clear()  # Clear inventory when moving to a new level

    def draw(self):
        self.screen.fill((255, 255, 255))
        current_level_data = self.levels[self.current_level]

        # Draw obstacles and items for the current level
        for obstacle in current_level_data["obstacles"]:
            obstacle.draw(self.screen)
        for item in current_level_data["items"]:
            item.draw(self.screen)

        self.player.draw(self.screen)

        pygame.display.update()

        # Display inventory and level info
        inventory_text = f"Inventory: {len(self.player.inventory)} items"
        level_text = f"Level {self.current_level + 1}"
        text_surface = self.font.render(inventory_text, True, (0, 0, 0))
        level_surface = self.font.render(level_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        self.screen.blit(level_surface, (10, 40))

    def run_game(self):
        while self.run:
            pygame.time.delay(10)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

# Run the game only if this file is executed directly
if __name__ == "__main__":
    game = Game()
    game.run_game()
