import pygame

class Player:
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.inventory = []

    def move(self, keys, obstacles, items):
        if keys[pygame.K_LEFT] and self.x > 0 and self.can_move(self.x - self.vel, self.y, obstacles):
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < 1000 - self.width and self.can_move(self.x + self.vel, self.y, obstacles):
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > 0 and self.can_move(self.x, self.y - self.vel, obstacles):
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < 1000 - self.height and self.can_move(self.x, self.y + self.vel, obstacles):
            self.y += self.vel
        self.collect_items(items)

    def can_move(self, new_x, new_y, obstacles):
        for obstacle in obstacles:
            if obstacle.collides_with(new_x, new_y, self.width, self.height):
                return False
        return True

    def collect_items(self, items):
        for item in items[:]:
            if item.collides_with(self.x, self.y, self.width, self.height):
                self.inventory.append(item)
                items.remove(item)
                print(f"Money collected! Inventory: {len(self.inventory)} items.")

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def collides_with(self, x, y, width, height):
        return x < self.x + self.width and x + width > self.x and y < self.y + self.height and y + height > self.y

class Item:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def collides_with(self, x, y, width, height):
        return x < self.x + self.width and x + width > self.x and y < self.y + self.height and y + height > self.y

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("HEIST Game")

        self.player = Player(200, 200, 32, 32, 2.5)

        # Define level configurations
        self.levels = [
            {
                "obstacles": [
                    Obstacle(500, 500, 200, 100),
                    Obstacle(200, 300, 150, 150),
                    Obstacle(700, 200, 120, 180)
                ],
                "items": [
                    Item(400, 400, 20, 20),
                    Item(600, 300, 20, 20),
                    Item(800, 600, 20, 20)
                ]
            },
            {
                "obstacles": [
                    Obstacle(100, 100, 150, 100),
                    Obstacle(600, 600, 200, 200),
                    Obstacle(300, 400, 100, 100)
                ],
                "items": [
                    Item(500, 500, 20, 20),
                    Item(700, 700, 20, 20)
                ]
            },
            {
                "obstacles": [
                    Obstacle(100, 100, 300, 100),
                    Obstacle(500, 500, 100, 100)
                ],
                "items": [
                    Item(800, 300, 20, 20)
                ]
            }
        ]

        self.font = pygame.font.SysFont('Arial', 24)
        self.current_level = 0
        self.run = True

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
