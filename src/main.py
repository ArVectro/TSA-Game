import pygame
import random


class Screen:
    def __init__(self):
        # Initialize pygame and the screen
        pygame.init()


        # Game state variables
        self.show_first_screen = True  # Flag to track if the first screen should be shown
        self.show_instructions = False  # Flag to track if the instruction screen should be shown
        self.show_game_screen = False  # Flag to track if the game screen should be shown

        # Instruction screen image (you can replace this with your own image)
        self.instruction_screen_image = pygame.image.load("instruction_screen.png")  
        self.instruction_screen_image.fill((0, 255, 0))  # Green background for instructions
        
        # First screen image (you can replace this with your own image)
        self.first_screen_image = pygame.image.load("chess.png")
        self.first_screen_image.fill((255, 0, 0))  # Red background for first screen
        
        # Background image for main game (replace this with your game background)
        self.background_image = pygame.Surface((800, 600))
        self.background_image.fill((255, 255, 255))  # White background for the game

        # Initialize other game elements
        self.player = None  # Initialize player object (replace with actual player object)
        
    def restart_level(self):
        """
        Restart the current level by resetting the player's position and clearing the inventory.
        """
        print("Restarting level...")
        self.player.x, self.player.y = 40, 680  # Reset player position
        self.player.inventory.clear()  # Clear inventory

    def draw(self):
        """
        Draw the current screen based on game state.
        """
        if self.show_first_screen:
            # Draw the first screen (e.g., title or splash screen)
            self.screen.blit(self.first_screen_image, (0, 0))
        elif self.show_instructions:
            # Draw the instruction screen
            self.screen.blit(self.instruction_screen_image, (0, 0))
        elif self.show_game_screen:
            # Draw the main game screen
            self.screen.blit(self.background_image, (0, 0))
            # Add logic to draw your game elements, e.g., obstacles, player, items
            self.player.draw(self.screen)  # Assuming your player object has a draw method
        pygame.display.flip()

    def handle_events(self):
        """
        Handle all events including mouse clicks.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_first_screen:
                    # When the first screen is clicked, show the instruction screen
                    self.show_first_screen = False
                    self.show_instructions = True
                elif self.show_instructions:
                    # When the instruction screen is clicked, hide it and show the game
                    self.show_instructions = False
                    self.show_game_screen = True

    def game_loop(self):
        """
        Main game loop.
        """
        while True:
            self.handle_events()
            self.draw()  # Draw the screen based on the current state
            self.clock.tick(60)  # Maintain 60 FPS

class Player:
    def __init__(self, x, y, width, height, vel, image_path):
        """
        Initializes the player with an image.

        Parameters:
        - x, y: Initial position of the player
        - width, height: Size of the player
        - vel: Movement speed of the player
        - image_path: Path to the image to represent the player
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.inventory = []

        # Load the player image
        self.image = pygame.image.load(image_path)

        # Scale the image to fit the player's size (optional, based on your game's design)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self, keys, obstacles, items, invisibleObstacle, screen_width, screen_height):
        """
        Handles player movement while avoiding obstacles and collecting items.
        """
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
        Draws the player image on the screen.

        Parameters:
        - screen: The game screen where the player will be drawn
        """
        screen.blit(self.image, (self.x, self.y))  # Draw the player image at (x, y)


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


class Laser:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        """
        Initializes a laser.

        Parameters:
        - x, y: Position of the laser
        - width, height: Size of the laser (can be a thin rectangle)
        - color: Color of the laser (default is red)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        """
        Draws the laser on the screen.

        Parameters:
        - screen: The game screen where the laser will be drawn
        """
        pygame.draw.rect(
            screen, self.color, (self.x, self.y, self.width, self.height)
        )  # Use the color

    def collides_with(self, x, y, width, height):
        """
        Checks if a given rectangle (player) collides with this laser.

        Parameters:
        - x, y: Position of the rectangle (player)
        - width, height: Size of the rectangle (player)

        Returns:
        - True if there's a collision, False otherwise
        """
        return (
            x < self.x + self.width
            and x + width > self.x
            and y < self.y + self.height
            and y + height > self.y
        )
    def laser_sound(self, sound_path):
        sound = pygame.mixer.Sound("src/assets/laser.mp3")
        sound.play()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Load sound effects
        # self.coin_pickup_sound = pygame.mixer.Sound("src/assets/coin_pickup_sound.wav")
        # self.laser_hit_sound = pygame.mixer.Sound("src/assets/laser.mp3")
        # self.game_over_sound = pygame.mixer.Sound("src/assets/game_over_sound.wav")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 800))  # Reduced height to 800
        pygame.display.set_caption("HEIST Game")

        # Add image_path parameter for the player image
        self.player = Player(40, 680, 28.4, 32, 2.5, "src/assets/standing_robber.png")  # Example path to the image

        # Define levels with obstacle colors and invisible obstacles
        self.levels = [
            {
                "obstacles": [
                    Obstacle(0, 0, 520, 415),
                    Obstacle(0, 0, 40, 800),
                    Obstacle(0, 0, 1000, 40),
                    Obstacle(960, 0, 40, 800),
                    Obstacle(0, 770, 1000, 30),
                    Obstacle(520, 385, 260, 30),
                    Obstacle(855, 385, 145, 30),
                    Obstacle(485, 415, 30, 65),
                    Obstacle(485, 530, 30, 270),
                ],
                "invisibleObstacle": [
                    InvisibleObstacle(110, 740, 150, 40),
                    InvisibleObstacle(445, 680, 30, 120),
                    InvisibleObstacle(175, 565, 40, 30),
                    InvisibleObstacle(260, 500, 40, 30),
                    InvisibleObstacle(260, 630, 40, 30),
                    InvisibleObstacle(345, 565, 40, 30),
                    InvisibleObstacle(225, 535, 110, 90),
                    InvisibleObstacle(805, 645, 80, 60),
                    InvisibleObstacle(760, 670, 40, 30),
                    InvisibleObstacle(815, 610, 40, 30),
                    InvisibleObstacle(830, 710, 40, 30),
                    InvisibleObstacle(890, 650, 40, 30),
                    InvisibleObstacle(520, 415, 230, 65),
                    InvisibleObstacle(520, 565, 225, 235),
                    InvisibleObstacle(890, 415, 75, 180),
                    InvisibleObstacle(925, 235, 35, 150),
                    InvisibleObstacle(560, 80, 75, 120),
                    InvisibleObstacle(855, 80, 75, 120),
                    InvisibleObstacle(555, 300, 150, 90),
                    InvisibleObstacle(640, 170, 30, 25),
                    InvisibleObstacle(670, 270, 30, 25),
                    InvisibleObstacle(815, 170, 30, 25),
                    InvisibleObstacle(755, 705, 70, 40)

                ],
                "items": [],
                "lasers": [
                    Laser(80, 415, 5, 100),
                    Laser(390, 660, 5, 110)
                ]
            },

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
                "lasers": []
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
                    Obstacle(855, 167, 20, 44),
                    Obstacle(855, 245, 20, 86),
                    Obstacle(855, 365, 20, 86),
                    Obstacle(855, 485, 20, 86),
                    Obstacle(855, 605, 20, 40),
                    Obstacle(0, 230, 40, 20),
                    Obstacle(120, 230, 290, 20),
                    Obstacle(500, 230, 40, 20),
                    Obstacle(0, 505, 160, 20),
                    Obstacle(225, 505, 90, 20),
                    Obstacle(295, 635, 125, 20),
                    Obstacle(550, 160, 325, 20),
                    Obstacle(550, 280, 325, 20),
                    Obstacle(550, 405, 325, 20),
                    Obstacle(550, 520, 325, 20),
                    Obstacle(520, 635, 385, 20),
                    Obstacle(970, 635, 30, 20)
                ],
                "invisibleObstacle": [
                    InvisibleObstacle(350, 60, 150, 35),
                    InvisibleObstacle(35, 560, 105, 65),
                    InvisibleObstacle(320, 285, 70, 90),
                    InvisibleObstacle(340, 460, 50, 90),
                    InvisibleObstacle(550, 180, 85, 105),
                    InvisibleObstacle(550, 305, 85, 105),
                    InvisibleObstacle(550, 430, 85, 105),
                    InvisibleObstacle(550, 555, 85, 105),
                    InvisibleObstacle(575, 700, 300, 100),
                    InvisibleObstacle(110, 440, 70, 70)
                ],
                "items": [],
                "lasers": []
            }
        ]

        # Now, generate items for each level, using level data
        for i in range(len(self.levels)):
            self.levels[i]["items"] = self.generate_items(50, 20, self.levels[i])

        self.font = pygame.font.SysFont("Arial", 24)
        self.current_level = 0
        self.run = True

        # Load the background images for each level
        self.background_images = [
            pygame.image.load("src/assets/lvl1.png"),
            pygame.image.load("src/assets/lvl2.png"), 
            pygame.image.load("src/assets/lvl3.png") 
        ]
        # Scale the images to match the screen size
        self.background_images = [pygame.transform.scale(image, (self.screen.get_width(), self.screen.get_height())) for image in self.background_images]
 #       end_screen_image = pygame.transform.scale(end_screen_image, (self.screen.get_width(), self.screen.get_height()))
        # Load the instruction screen image and end screen
        self.instruction_screen_image = pygame.image.load("src/assets/instruction_screen.png")
        self.instruction_screen_image = pygame.transform.scale(self.instruction_screen_image, (self.screen.get_width(), self.screen.get_height()))
        self.first_screen_image = pygame.image.load("src/assets/chess.png")
        self.first_screen_image = pygame.transform.scale(self.first_screen_image, (self.screen.get_width(), self.screen.get_height()))

        self.end_screen_image = pygame.image.load("src/assets/game_over.png")
        self.end_screen_image = pygame.transform.scale(self.end_screen_image, (self.screen.get_width(), self.screen.get_height()))
        # self.instruction_screen_image2 = pygame.image.load("src/assets/instruction_screen.png")
        # self.instruction_screen_image2 = pygame.transform.scale(self.instruction_screen_image2, (self.screen.get_width(), self.screen.get_height()))
        # Flag to check if we are showing the instruction screen
        self.show_instructions = False
        self.show_first_screen = True
        self.show_game_screen = False

         # Play background music on loop
        pygame.mixer.music.load("src/assets/Rev.mp3")  # Replace with your music file path
        pygame.mixer.music.set_volume(0.5)  # Optional: Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # The -1 means loop forever


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
                break
            if event.type == pygame.MOUSEBUTTONDOWN and self.show_first_screen:
                # When user clicks on instruction screen, start the game.
                self.show_instructions = True
                self.show_first_screen = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and self.show_instructions:
                self.show_instructions = False
                self.show_game_screen = True
                break       

    def update(self):
        if self.show_instructions:
            return  # Don't update the game if we're showing the instruction screen.

        if self.show_first_screen:
            return
        
        keys = pygame.key.get_pressed()
        current_level_data = self.levels[self.current_level]

        # Move the player
        self.player.move(
            keys,
            current_level_data["obstacles"],
            current_level_data["items"],
            current_level_data["invisibleObstacle"],
            self.screen.get_width(),
            self.screen.get_height(),
        )

        # Check for collisions with lasers
        for laser in current_level_data.get("lasers", []):
            if laser.collides_with(self.player.x, self.player.y, self.player.width, self.player.height):
                print("Player hit a laser! Restarting level.")
                
                self.restart_level()

        # Check if all items are collected
        if len(current_level_data["items"]) == 0:
            print(f"Level {self.current_level + 1} completed!")
            if self.current_level < len(self.levels) - 1:
                self.current_level += 1
                self.player.inventory.clear()  # Optionally clear the player's inventory when moving to the next level
                self.player.x, self.player.y = 40, 680  # Reset player position

    def restart_level(self):
        """
        Restart the current level by resetting the player's position and clearing the inventory.
        """
        print("Restarting level...")
        self.player.x, self.player.y = 40, 680  # Reset player position
        self.player.inventory.clear()  # Clear inventory
        
    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.show_first_screen:
            self.screen.blit(self.first_screen_image, (0, 0))
        elif self.show_instructions:
            self.screen.blit(self.instruction_screen_image, (0, 0))
        else:
            self.screen.blit(self.background_images[self.current_level], (0, 0))

            current_level_data = self.levels[self.current_level]
            for obstacle in current_level_data["obstacles"]:
                obstacle.draw(self.screen)
            for item in current_level_data["items"]:
                item.draw(self.screen)
            for laser in current_level_data.get("lasers", []):
                laser.draw(self.screen)
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
