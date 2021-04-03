# Portal 2D - a 2D Python game inspired by the Portal series

import os
import pygame

# ---- CONSTANTS ------------------------
# window
# for some god DAMN reason this causes out of range errors in collision
# when the width/height starts with an odd number...
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Portal 2D: World Testing")
FPS = 60

# colors
WHITE = (255, 255, 255)
BLUE_BACK = (54, 81, 94)
BLUE = (0, 91, 255)
ORANGE = (255, 127, 80)

# game logic
PLAYER_WIDTH, PLAYER_HEIGHT =  WIDTH//20, HEIGHT//5
TILE_SIZE = WIDTH//10
PORTAL_WIDTH, PORTAL_HEIGHT = 9, TILE_SIZE*2
VEL = 10
player_direction = 1 # 0 == left, 1 == right

# assets
PLAYER_IMG = pygame.image.load(os.path.join('assets', 'sven.png'))
PLAYER_SURF = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))
BLOCK_IMG = pygame.image.load(os.path.join('assets', 'ground_texture_1.png'))
BLOCK_RECT = pygame.transform.scale(BLOCK_IMG, (TILE_SIZE, TILE_SIZE))
BLUE_RECT = pygame.Rect(0, 0, PORTAL_WIDTH, PORTAL_HEIGHT)
ORG_RECT = pygame.Rect(0, 120, PORTAL_WIDTH, PORTAL_HEIGHT)
# ------------------------ CONSTANTS ----

# loads the world map
def load_map():
    # can later add a level selector, each map just named its level
    # number, easy to create a string to find file name i.txt
    file_location = os.path.join('maps', 'test_map.txt')
    f = open(file_location)

    world_map = []
    for line in f:
        # maps are 10x10 (0-9)
        elements = line.split(' ')
        world_map.append(elements)
    return world_map

# check if the player is going through the blue portal
def blue_collision(player):
    # checks the midpoint of the player
    char_mid_x = player.x + PLAYER_WIDTH/2
    char_mid_y = player.y + PLAYER_HEIGHT/2

    # is character colliding with blue portal
    if char_mid_x >= BLUE_RECT.x and char_mid_x <= BLUE_RECT.x+PORTAL_WIDTH and char_mid_y >= BLUE_RECT.y and char_mid_y <= BLUE_RECT.y+PORTAL_HEIGHT:
        return True
    else:
        return False

# check if the player is going through the orange portal
def orange_collision(player):
    # checks the midpoint of the player
    char_mid_x = player.x + PLAYER_WIDTH/2
    char_mid_y = player.y + PLAYER_HEIGHT/2

    # is the character colliding with orange portal
    if char_mid_x >= ORG_RECT.x and char_mid_x <= ORG_RECT.x+PORTAL_WIDTH and char_mid_y >= ORG_RECT.y and char_mid_y <= ORG_RECT.y+PORTAL_HEIGHT:
        return True
    else:
        return False

# check if the player collided with any blocks in x axis (O(1))
def block_x_collision(world_map, x, y):
    # top, middle, bottom of player
    if x > WIDTH:
        x = WIDTH
    x = x // TILE_SIZE
    y1 = y // TILE_SIZE
    y2 = (y+PLAYER_HEIGHT//2) // TILE_SIZE
    y3 = (y+PLAYER_HEIGHT-1) // TILE_SIZE

    # Check if left, middle, or right points of player is colliding
    # after going thru portal cords get wacky, this this prevents list index out of range error
    if y1 < 0:
        y1 = 0
    if y3 > 9:
        y3 = 9
    if world_map[y1][x] == '1' or world_map[y2][x] == '1' or world_map[y3][x] == '1':
        return True
    else:
        return False

# check if the player collided with any blocks in y axis
def block_y_collision(world_map, x, y):
    # left, middle, and right of player
    x1 = x // TILE_SIZE
    x2 = (x+PLAYER_WIDTH//2) // TILE_SIZE
    x3 = (x+PLAYER_WIDTH-1) // TILE_SIZE
    y = y // TILE_SIZE

    # Check if left, middle, or right points of player is colliding
    # after going thru portal cords get wacky, this prevents list index out of range error
    if x1 < 0:
        x1 = 0
    if x3 > 9:
        x3 = 9
    if world_map[y][x1] == '1' or world_map[y][x2] == '1' or world_map[y][x3] == '1':
        return True
    else:
        return False

# move the player in the x and y directions
def move_player(keys_pressed, world_map, player):
    # might need to assign global vars new values
    global player_direction
    global PLAYER_SURF

    # some quick bounds checking, won't need if I can find the glitch
    if player.x < 0:
        player.x = 0
    if player.x+PLAYER_WIDTH > WIDTH:
        player.x = WIDTH-PLAYER_WIDTH

    if keys_pressed[pygame.K_LEFT] and player.x > 0:
        # flip player left if needed
        if player_direction == 1:
            PLAYER_SURF = pygame.transform.flip(PLAYER_SURF, True, False)
            player_direction = 0
        # if not colliding with blocks, move player
        if not block_x_collision(world_map, player.x-1, player.y):
            player.x -= VEL
        # check if the player collided with portals
        if blue_collision(player):
            player.x = ORG_RECT.x - PLAYER_WIDTH
            player.y = ORG_RECT.y
        if orange_collision(player):
            player.x = BLUE_RECT.x - PLAYER_WIDTH
            player.y = BLUE_RECT.y
        
    if keys_pressed[pygame.K_RIGHT] and player.x+PLAYER_WIDTH < WIDTH:
        # flip player right if needed
        if player_direction == 0:
            PLAYER_SURF = pygame.transform.flip(PLAYER_SURF, True, False)
            player_direction = 1
        # if not colliding with blocks, move player
        if not block_x_collision(world_map, player.x+PLAYER_WIDTH, player.y):
            player.x += VEL
        # check if player collided with portals
        if blue_collision(player):
            player.x = ORG_RECT.x + PORTAL_WIDTH
            player.y = ORG_RECT.y
        if orange_collision(player):
            player.x = BLUE_RECT.x + PORTAL_WIDTH
            player.y = BLUE_RECT.y
        
    if keys_pressed[pygame.K_UP] and player.y > 0:
        # if not colliding with blocks, move player
        if not block_y_collision(world_map, player.x, player.y-1):
            player.y -= VEL
       
    if keys_pressed[pygame.K_DOWN] and player.y+PLAYER_HEIGHT < HEIGHT:
        # if not colliding with blocks, move player
        if not block_y_collision(world_map, player.x, player.y+PLAYER_HEIGHT):
            player.y += VEL

# draws the map
def draw_map(world_map):
    WIN.fill(BLUE_BACK)
    row_count = 0
    for row in world_map:
        col_count = 0
        for tile in row:
            if tile == '1':
                block_rect = pygame.Rect(col_count*TILE_SIZE, row_count*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                WIN.blit(BLOCK_RECT, (block_rect.x, block_rect.y))
            col_count += 1
        row_count += 1

# draw necessary things to the screen
def draw_window(player, world_map):
    draw_map(world_map)
    pygame.draw.rect(WIN, BLUE, BLUE_RECT)
    pygame.draw.rect(WIN, ORANGE, ORG_RECT)
    WIN.blit(PLAYER_SURF, (player.x, player.y))
    pygame.display.update()

def main():
    # world_map = load_map()
    world_map = [
        [ '0', '1', '1', '1', '1', '1', '1', '0', '0', '1'],
        [ '0', '0', '1', '0', '1', '1', '1', '0', '0', '1'],
        [ '1', '0', '1', '0', '0', '0', '0', '0', '0', '1'],
        [ '0', '0', '0', '0', '0', '0', '0', '1', '0', '1'],
        [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        [ '1', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
        [ '1', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
        [ '1', '0', '1', '0', '0', '0', '0', '0', '1', '1'],
        [ '1', '1', '1', '1', '0', '0', '1', '1', '1', '1']
    ]
    
    # Rect(x, y, width, height)
    player = pygame.Rect(WIDTH/2, HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)

    # game loop
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # move portals if player clicks mouse button
            # need to implement feature that only allows portals on edge of walls
            # maybe if x = mouse_pos//60, world_map[x][x] == '1', then place portal
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_click[0]: # left mouse button
                    BLUE_RECT.x = mouse_pos[0]-5
                    BLUE_RECT.y = mouse_pos[1]-PORTAL_WIDTH//2
                if mouse_click[2]: # right mouse button
                    ORG_RECT.x = mouse_pos[0]-5
                    ORG_RECT.y = mouse_pos[1]-PORTAL_WIDTH//2
        
        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed, world_map, player)

        # DEBUG
        if keys_pressed[pygame.K_h]:
            print("-------------------------------------------------")
            print("top.x, top.y == ", player.x, ", ", player.y)
            print("right.x, bottom.y == ", player.x+PLAYER_WIDTH, ", ", player.y+PLAYER_HEIGHT)
            print("blue.x, blue.y == ", BLUE_RECT.x, BLUE_RECT.y)
            print("orange.x, orange.y == ", ORG_RECT.x, ORG_RECT.y) 
            print("-------------------------------------------------")

        draw_window(player, world_map)

if __name__ == "__main__":
    main()

# NOTES
# for some reason after I teleport through a portal, my x cords get messed up,
# causing me to clip into blocks and get stuck. Potentially due to portals
# coords, maybe set them to only sit on intervals of TILE_SIZE. Then maybe
# I could set player to only ever spawn on the tops of blocks.