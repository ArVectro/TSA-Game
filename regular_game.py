import pygame 
from pygame import mixer
pygame.init()  # Initiates pygame
  
# Create the display surface object of specific dimension
screen = pygame.display.set_mode((1000, 1000)) 
  
# Set the pygame window name  
pygame.display.set_caption("HEIST game") 

# Object current coordinates  
x = 200
y = 200

# Dimensions of the object  
width = 32
height = 32

# Velocity / speed of movement 
vel = 2.5
  
# Rectangle (obstacle) coordinates and dimensions
obstacle_x = 500
obstacle_y = 500
obstacle_width = 200
obstacle_height = 100
  
# Indicates pygame is running 
run = True
  
# Infinite loop  
while run: 
    # Creates time delay of 10ms  
    pygame.time.delay(10) 
      
    # Iterate over the list of Event objects   
    # that was returned by pygame.event.get() method.   
    for event in pygame.event.get(): 
          
        # If event object type is QUIT, exit the program  
        if event.type == pygame.QUIT: 
            run = False

    # Stores keys pressed  
    keys = pygame.key.get_pressed() 
      
    # If left arrow key is pressed 
    if keys[pygame.K_LEFT] and x > 0: 
        # Check if moving left would overlap the obstacle
        if not (x - vel < obstacle_x + obstacle_width and x + width > obstacle_x and y + height > obstacle_y and y - vel < obstacle_y + obstacle_height):
            x -= vel
          
    # If right arrow key is pressed
    if keys[pygame.K_RIGHT] and x < 1000 - width: 
        print(f"{x - vel} <{ obstacle_x + obstacle_width } and {x + width}> {obstacle_x } and {y+height} > {obstacle_y } and {y} < {obstacle_y + obstacle_height} ")
        # Check if moving right would overlap the obstacle
        if not (x - vel < obstacle_x + obstacle_width and x + width > obstacle_x and y + height > obstacle_y and y < obstacle_y + obstacle_height):
            x += vel
         
    # If up arrow key is pressed  
    if keys[pygame.K_UP] and y > 0: 
        # Check if moving up would overlap the obstacle
        if not (x + width > obstacle_x and x < obstacle_x + obstacle_width and y - vel < obstacle_y + obstacle_height and y + height > obstacle_y):
            y -= vel
                  
    # If down arrow key is pressed    
    if keys[pygame.K_DOWN] and y < 1000 - height: 
        # Check if moving down would overlap the obstacle
        if not (x + width > obstacle_x and x < obstacle_x + obstacle_width and y - vel < obstacle_y + obstacle_height and y + height > obstacle_y):
            y += vel 

    # Background
    screen.fill((255, 255, 255)) 
    
    # Music
    # mixer.init()
    # mixer.music.load("song.mp3")
    # mixer.music.set_volume(0.7)
    # mixer.music.play()

    # Draw the obstacle (blue rectangle)
    pygame.draw.rect(screen, (0, 0, 255), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
    
    # Draw the player (red rectangle)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height)) 
    
    # Refresh the window
    pygame.display.update()  
  
pygame.quit()