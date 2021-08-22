# Select a level to play for Portal 2D

import os
import pygame
import world_testing as wt

# ---- GLOBAL STUFF ------------------------
# window
WIDTH, HEIGHT = 1152, 704 #  must be multiples of 64
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Portal 2D: World Testing")
FPS = 60

# colors
WHITE = (255, 255, 255)
BLUE_BACK = (54, 81, 94)
BLUE = (0, 91, 255)
ORANGE = (255, 127, 80)

# Tile sizes for button placement
TILE_SIZE = 64
TILES_X, TILES_Y = WIDTH/TILE_SIZE, HEIGHT/TILE_SIZE # number of tiles in each direction (18 x 11)

# Assets
LOGO = pygame.image.load("logo.png")
LOGO_RECT = LOGO.get_rect();
LOGO_RECT.centerx = WIDTH // 2
LOGO_RECT.y = TILE_SIZE

# Left x coordinate of buttons
B1_L = TILE_SIZE*4
B2_L = TILE_SIZE*8
B3_L = TILE_SIZE*12
# Top y coordinate of buttons
BT = TILE_SIZE*4
# Width and Height of buttons
BW, BH = TILE_SIZE*2, TILE_SIZE*2
# ------------------------------------------

# Select a level based on the level selection
def select_level(level):
    # There's probably a better way to do this, but when there's only 3 levels, this is probably faster
    if level == 1:
        wt.level_1()
    if level == 2:
        wt.level_2()
    if level == 3:
        wt.level_3();

# Check which level user has selected based on mouse coordinates
def check_selection():  
    mouse_pos = pygame.mouse.get_pos()
    mx = mouse_pos[0]
    my = mouse_pos[1]

    # Check if mouse position is inside a button
    if mx >= B1_L and mx <= B1_L+BW and my >= BT and my <= BT+BH:
        select_level(1)
    if mx >= B2_L and mx <= B2_L+BW and my >= BT and my <= BT+BH:
        select_level(2)
    if mx >= B3_L and mx <= B3_L+BW and my >= BT and my <= BT+BH:
        select_level(3)

# Draw necessary things to the screen
def draw_window():
    WIN.fill((0,0,255))
    # Logo
    WIN.blit(LOGO, (LOGO_RECT.x, LOGO_RECT.y))

    # Buttons
    pygame.draw.rect(WIN, BLUE, (B1_L, BT, BW, BH)) # rect == (LEFT, TOP, WIDTH, HEIGHT)
    pygame.draw.rect(WIN, BLUE, (B2_L, BT, BW, BH))
    pygame.draw.rect(WIN, BLUE, (B3_L, BT, BW, BH))
    pygame.display.update()

# First function that is run in the execution of Portal 2D
def main():
    # Run the level selector
    while True:
        # Game Loop
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            keys_pressed = pygame.key.get_pressed()

            # Check for individual events
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                    pygame.quit()
                
                # Move portals if player clicks mouse button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    check_selection()

            draw_window()

if __name__ == "__main__":
    main()