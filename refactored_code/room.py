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

    def move(self, keys, obstacles, items, invisibleObstacle, screen_width, screen_height):
        """
        Handles player movement while avoiding obstacles and collecting items.

        Parameters:
        - keys: Pressed keys from pygame.key.get_pressed()
        - obstacles: List of obstacle objects to check for collision
        - items: List of item objects to check for collection
        """
        # Check if player can move without colliding with obstacles
        if (
            keys[pygame.K_LEFT]
            and self.x > 0
            and self.can_move(
                self.x - self.vel, self.y, obstacles, invisibleObstacle, screen_width, screen_height
            )
        ):
            self.x -= self.vel  # Move left
        if (
            keys[pygame.K_RIGHT]
            and self.x < screen_width - self.width
            and self.can_move(
                self.x + self.vel, self.y, obstacles, invisibleObstacle, screen_width, screen_height
            )
        ):
            self.x += self.vel  # Move right
        if (
            keys[pygame.K_UP]
            and self.y > 0
            and self.can_move(
                self.x, self.y - self.vel, obstacles, invisibleObstacle, screen_width, screen_height
            )
        ):
            self.y -= self.vel  # Move up
        if (
            keys[pygame.K_DOWN]
            and self.y < screen_height - self.height
            and self.can_move(
                self.x, self.y + self.vel, obstacles, invisibleObstacle, screen_width, screen_height
            )
        ):
            self.y += self.vel  # Move down

        self.collect_items(items)  # Check if player collects any items

    def can_move(self, new_x, new_y, obstacles, invisibleObstacle, screen_width, screen_height):
        """
        Checks if the player can move to the new position without colliding.

        Parameters:
        - new_x, new_y: The new position the player wants to move to
        - obstacles: List of obstacles to check against

        Returns:
        - True if the move is allowed, False if it collides
        """

        # Check for obstacles
        for obstacle in obstacles:
            if obstacle.collides_with(new_x, new_y, self.width, self.height):
                return False  # Block movement if collision detected with obstacle

        # Check for invisible obstacles (loop through the list)
        for inv_obs in invisibleObstacle:  # Loop through the list of InvisibleObstacle objects
            if inv_obs.collides_with(new_x, new_y, self.width, self.height):
                return False  # Block movement if collision detected with invisible obstacle

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
        pygame.draw.rect(
            screen, (255, 0, 0), (self.x, self.y, self.width, self.height)
        )  # Red color


class InvisibleObstacle:
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        """
        Initializes an obstacle.

        Parameters:
        - x, y: Position of the obstacle
        - width, height: Size of the obstacle
        - color: Color of the obstacle (default is black)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color  # New color parameter

    def draw(self, screen):
        """
        Draws the obstacle on the screen.

        Parameters:
        - screen: The game screen where the obstacle will be drawn
        """
        pygame.draw.rect(
            screen, self.color, (self.x, self.y, self.width, self.height)
        )  # Use the color


    def collides_with(self, x, y, width, height):
        """
        Checks if a given rectangle (player) collides with this obstacle.

        Parameters:
        - x, y: Position of the rectangle
        - width, height: Size of the rectangle

        Returns:
        - True if there's a collision, False otherwise
        """
        return (
            x < self.x + self.width
            and x + width > self.x
            and y < self.y + self.height
            and y + height > self.y
        )


class Obstacle:
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        """
        Initializes an obstacle.

        Parameters:
        - x, y: Position of the obstacle
        - width, height: Size of the obstacle
        - color: Color of the obstacle (default is black)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color  # New color parameter

    def draw(self, screen):
        """
        Draws the obstacle on the screen.

        Parameters:
        - screen: The game screen where the obstacle will be drawn
        """
        pygame.draw.rect(
            screen, self.color, (self.x, self.y, self.width, self.height)
        )  # Use the color

    def collides_with(self, x, y, width, height):
        """
        Checks if a given rectangle (player) collides with this obstacle.

        Parameters:
        - x, y: Position of the rectangle
        - width, height: Size of the rectangle

        Returns:
        - True if there's a collision, False otherwise
        """
        return (
            x < self.x + self.width
            and x + width > self.x
            and y < self.y + self.height
            and y + height > self.y
        )


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
        pygame.draw.circle(
            screen,
            (255, 223, 0),
            (self.x + self.width // 2, self.y + self.height // 2),
            self.width // 2,
        )  # Gold color

    def collides_with(self, x, y, width, height):
        """
        Checks if a given rectangle (player) collides with this item.

        Parameters:
        - x, y: Position of the rectangle
        - width, height: Size of the rectangle

        Returns:
        - True if there's a collision, False otherwise
        """
        return (
            x < self.x + self.width
            and x + width > self.x
            and y < self.y + self.height
            and y + height > self.y
        )


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))  # Reduced height to 800
        pygame.display.set_caption("HEIST Game")

        # Player moved to top-left as far as possible
        self.player = Player(31, 31, 29, 29, 5)  # Player positioned at (15, 15)

        # Define levels with obstacle colors and invisible obstacles
        self.levels = [
            {
                "obstacles": [
                    Obstacle(0, 0, 1000, 30),
                    Obstacle(0, 0, 30, 800),
                    Obstacle(0, 770, 1000, 30),
                    Obstacle(970, 0, 30, 800),
                    Obstacle(323, 0, 30, 100),
                    Obstacle(323, 150, 30, 650),
                    Obstacle(646, 0, 30, 100),
                    Obstacle(646, 150, 30, 650),
                    Obstacle(0, 385, 150, 30),
                    Obstacle(200, 385, 200, 30),
                    Obstacle(900, 385, 150, 30),
                    Obstacle(450, 385, 400, 30),
                ],
                "invisibleObstacle": [
                    InvisibleObstacle(70, 150, 60, 120),
                    InvisibleObstacle(120, 180, 110, 60),
                    InvisibleObstacle(225, 150, 50, 120),
                    InvisibleObstacle(427, 178, 176, 150),
                    InvisibleObstacle(400, 215, 20, 20),
                    InvisibleObstacle(400, 275, 20, 20),
                    InvisibleObstacle(460, 330, 190, 60),
                    InvisibleObstacle(450, 150, 120, 20),
                    InvisibleObstacle(600, 210, 40, 180),
                    InvisibleObstacle(675, 300, 25, 90),
                    InvisibleObstacle(775, 30, 100, 150),
                    InvisibleObstacle(750, 67, 20, 20),
                    InvisibleObstacle(880, 67, 20, 20),
                    InvisibleObstacle(950, 100, 25, 90),
                    InvisibleObstacle(150, 590, 50, 90),
                    InvisibleObstacle(350, 476, 25, 90),
                    InvisibleObstacle(375, 625, 52, 120),
                    InvisibleObstacle(575, 475, 52, 120),
                    InvisibleObstacle(430, 715, 20, 20),
                    InvisibleObstacle(550, 560, 20, 20),
                    InvisibleObstacle(550, 740, 76, 30)
                ],
                "items": [],
            },
            {
                "obstacles": [
                    Obstacle(0, 0, 1000, 20),
                    Obstacle(0, 0, 20, 800),
                    Obstacle(0, 780, 1000, 20),
                    Obstacle(980, 0, 20, 800),
                    Obstacle(295, 0, 20, 85),
                    Obstacle(295, 150, 20, 260),
                    Obstacle(295, 450, 20, 205),
                    Obstacle(530, 0, 20, 85),
                    Obstacle(530, 150, 20, 500),
                    Obstacle(390, 650, 20, 140),
                    Obstacle(510, 650, 20, 140),
                    Obstacle(855, 167, 20, 47),
                    Obstacle(855, 245, 20, 89),
                    Obstacle(855, 365, 20, 89),
                    Obstacle(855, 485, 20, 89)
                ],
                "invisibleObstacle": [
                    
                ],
                "items": [],
            },
            {
                "obstacles": [
                    Obstacle(100, 100, 300, 100, (255, 0, 255)),
                    Obstacle(500, 500, 100, 100, (0, 128, 0)),
                ],
                "invisibleObstacle": [
                    InvisibleObstacle(150, 200, 80, 80),
                    InvisibleObstacle(600, 350, 90, 100),
                ],
                "items": [],
            },
        ]

        # Now, generate items for each level, using level data
        for i in range(len(self.levels)):
            self.levels[i]["items"] = self.generate_items(30, 20, self.levels[i])

        self.font = pygame.font.SysFont("Arial", 24)
        self.current_level = 0
        self.run = True

        # Load the background images for each level
        self.background_images = [
            pygame.image.load("refactored_code/lvl1.png"),
            pygame.image.load("refactored_code/lvl2.png"), 
            pygame.image.load("refactored_code/lvl3.png") 
        ]

        # Scale the images to match the screen size
        self.background_images = [pygame.transform.scale(image, (self.screen.get_width(), self.screen.get_height())) for image in self.background_images]

        # Load the instruction screen image
        self.instruction_screen_image = pygame.image.load("chess.png")
        self.instruction_screen_image = pygame.transform.scale(
            self.instruction_screen_image, (self.screen.get_width(), self.screen.get_height())
        )

        # Flag to check if we are showing the instruction screen
        self.show_instructions = True


    def check_obstacle_collision(self, x, y, width, height, obstacles):
        for obstacle in obstacles:
            if obstacle.collides_with(x, y, width, height):
                return True  # If the item collides with any obstacle
        return False

    def generate_items(self, num_items, size, level_data):
        items = []
        obstacles = level_data.get("obstacles", [])
        invisible_obstacles = level_data.get("invisibleObstacle", [])
        
        for _ in range(num_items):
            valid_position = False
            while not valid_position:
                # Randomly place item within the valid bounds
                x = random.randint(50, 950)
                y = random.randint(50, 750)

                # Check if the item collides with any regular obstacle
                if self.check_obstacle_collision(x, y, size, size, obstacles):
                    continue

                # Check if the item collides with any invisible obstacle
                if self.check_obstacle_collision(x, y, size, size, invisible_obstacles):
                    continue

                valid_position = True  # Valid position found
                items.append(Item(x, y, size, size))  # Add item to the list
                
        return items


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.show_instructions:
                # When user clicks on instruction screen, start the game.
                self.show_instructions = False

    def update(self):
        if self.show_instructions:
            return  # Don't update the game if we're showing the instruction screen.

        keys = pygame.key.get_pressed()
        current_level_data = self.levels[self.current_level]
        self.player.move(
            keys,
            current_level_data["obstacles"],
            current_level_data["items"],
            current_level_data["invisibleObstacle"],
            self.screen.get_width(),
            self.screen.get_height(),
        )

        # if len(current_level_data["items"]) == 0:
        #     print(f"Level {self.current_level + 1} completed!")
        #     if self.current_level < len(self.levels) - 1:
        #         self.current_level += 1
        #         self.player.inventory.clear()
        if self.current_level == 0:  # Check if it's Level 1
            self.current_level = 1  # Skip directly to Level 2 for testing

    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.show_instructions:
            # Draw the instruction screen (image)
            self.screen.blit(self.instruction_screen_image, (0, 0))
        else:
            # Draw the background image based on the current level
            self.screen.blit(self.background_images[self.current_level], (0, 0))

            current_level_data = self.levels[self.current_level]
            for obstacle in current_level_data["obstacles"]:
                obstacle.draw(self.screen)
            for item in current_level_data["items"]:
                item.draw(self.screen)
            self.player.draw(self.screen)

        pygame.display.update()

    def run_game(self):
        while self.run:
            pygame.time.delay(10)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()
