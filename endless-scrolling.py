import pygame
import math

clock = pygame.time.Clock()

FrameHeight = 600
FrameWidth = 1200

# PYGAME FRAME WINDOW
pygame.display.set_caption("Endless Scrolling in pygame")
screen = pygame.display.set_mode((FrameWidth, FrameHeight))

bg = pygame.image.load("teal_background.jpeg").convert()

# DEFINING MAIN VARIABLES IN SCROLLING
scroll = 0
# HERE 1 IS THE CONSTATNT FOR REMOVING BUFFERING
tiles = math.ceil(FrameWidth  /bg.get_width()) + 1  

while 1:
  clock.tick(50)

  # APPENDING THE IMAGE TO THE BACK OF THE SAME IMAGE
  i=0
  while(i<tiles):
    screen.blit(bg, (bg.get_width()*i + scroll, 0))
    i+=1
  # FRAME FOR SCROLLING
  scroll -= 6

  # RESET THE SCROLL FRAME
  if abs(scroll) > bg.get_width():
    scroll = 0
  # CLOSING THE FRAME OF SCROLLING
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        quit()

  pygame.display.update()