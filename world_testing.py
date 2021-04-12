# Portal 2D - a 2D Python game inspired by the Portal series

import os
import pygame
import Sprites as sp
import Objects as ob

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

# game logic
TILE_SIZE = 64
TILES_X, TILES_Y = WIDTH/TILE_SIZE, HEIGHT/TILE_SIZE # number of tiles in each direction (18 x 11)
PLAYER_WIDTH, PLAYER_HEIGHT =  TILE_SIZE//2, TILE_SIZE*2
VEL = 8
JUMP_VEL = 30

# maps for world textures and sprite collisions
world_map = []
collision_map = []

# assets
BLOCK_IMG = pygame.image.load(os.path.join('assets', 'ground_texture_1.png'))
BLOCK_RECT = pygame.transform.scale(BLOCK_IMG, (TILE_SIZE, TILE_SIZE))

SLUDGE_IMG = pygame.image.load(os.path.join('assets', 'sludge.png'))
SLUDGE_RECT = pygame.transform.scale(SLUDGE_IMG, (TILE_SIZE, TILE_SIZE))

PORTAL_WALL_IMG = pygame.image.load(os.path.join('assets', 'portal_wall.png'))
PORTAL_WALL_RECT = pygame.transform.scale(PORTAL_WALL_IMG, (TILE_SIZE, TILE_SIZE))
# ------------------------------------------


# loads the world and collision maps
def load_maps():
    file_location = os.path.join('maps', '1.txt')
    f = open(file_location)

    # Loop thru file, load text into 2D List
    for line in f:
        elements = line.split(' ')
        world_map.append(elements)
    f.close()

    # Needed seperate loop for collision map, 
    # I THINK python was treating collision_map and world_map as
    # pointers to the same thing when appending in same loop :\
    f = open(file_location)
    for line in f:
        elements = line.split(' ')
        collision_map.append(elements)
    f.close()

    # Set any non 0 or 2 block to be 1
    i = 0
    for line in collision_map:
        j = 0
        for element in line:
            # if element isn't empty, or a sludge block
            if element != '0' and element != '2':
                collision_map[i][j] = '1'
            j += 1
        i += 1

# Detect if player is colliding with a portal
def portal_collision(portal, x, y):
    # If character is colliding with portal
    if x >= portal.rect.left and x <= portal.rect.right and y >= portal.rect.top and y <= portal.rect.bottom:
            return True
    else:
        return False

# check if the player collided with any blocks in x axis (O(1))
def block_x_collision(x, y):
    # top, middle, bottom of player
    x = x // TILE_SIZE
    y1 = y // TILE_SIZE
    y2 = (y+PLAYER_HEIGHT//2) // TILE_SIZE
    y3 = (y+PLAYER_HEIGHT-1) // TILE_SIZE

    # Check if left, middle, or right points of player is colliding
    # the ifs prevents crashing from map list index out of range error
    if y1 < 0:
        y1 = 0
    if y3 > TILES_Y-1:
        y3 = TILES_Y-1
    if collision_map[y1][x] == '1' or collision_map[y2][x] == '1' or collision_map[y3][x] == '1':
        return True
    else:
        return False

# check if the player collided with any blocks in y axis
def block_y_collision(x, y):
    # left, middle, and right of player
    x1 = x // TILE_SIZE
    x2 = (x+PLAYER_WIDTH//2) // TILE_SIZE
    x3 = (x+PLAYER_WIDTH-1) // TILE_SIZE
    y = y // TILE_SIZE

    # Check if left, middle, or right points of player is colliding
    # the ifs prevents crashing from map list index out of range error
    if x1 < 0:
        x1 = 0
    if x3 > TILES_X-1:
        x3 = TILES_X-1
    if collision_map[y][x1] == '1' or collision_map[y][x2] == '1' or collision_map[y][x3] == '1':
        return True
    else:
        return False

# move the player in the x and y directions
def move_player(keys_pressed, player, blue, orange):
    # Left movement
    if keys_pressed[pygame.K_a] and player.rect.x  > 0:
        # flip player if needed
        if player.direction == 1:
            player.flip()

        # check if player collided with blue/orange portals
        if portal_collision(blue, player.rect.left-1, player.rect.centery+1):
            player.teleport(orange)
        if portal_collision(orange, player.rect.left-1, player.rect.centery+1):
            player.teleport(blue)

        # if not colliding with blocks, move player
        if not block_x_collision(player.rect.x -1, player.rect.y):
            player.move(-VEL, 0)
        
    # Right movement
    if keys_pressed[pygame.K_d] and player.rect.x+PLAYER_WIDTH < WIDTH:
        # flip player right if needed
        if player.direction == 0:
            player.flip()  

        # check if player collided with blue/orange portals
        if portal_collision(blue, player.rect.right+1, player.rect.centery+1):
            player.teleport(orange)
        if portal_collision(orange, player.rect.right+1, player.rect.centery+1):
            player.teleport(blue)

        # if not colliding with blocks, move player
        if not block_x_collision(player.rect.right, player.rect.y):
            player.move(VEL, 0)
        
    # UP and DOWN will be gone soon, once jump implemented
    if keys_pressed[pygame.K_w] and player.rect.y > 0:
        # check if player collided with blue/orange portals
        if portal_collision(blue, player.rect.centerx, player.rect.top-1):
            player.teleport(orange)
        if portal_collision(orange, player.rect.centerx, player.rect.top-1):
            player.teleport(blue)

        # if not colliding with blocks, move player
        if not block_y_collision(player.rect.x, player.rect.y-1):
            player.move(0, -VEL)
            player.is_falling = True
       
    if keys_pressed[pygame.K_s] and player.rect.y+PLAYER_HEIGHT < HEIGHT:
        # check if player collided with blue/orange portals
        if portal_collision(blue, player.rect.centerx, player.rect.bottom+1):
            player.teleport(orange)
        if portal_collision(orange, player.rect.centerx, player.rect.bottom+1):
            player.teleport(blue)

        # if not colliding with blocks, move player
        if not block_y_collision(player.rect.x , player.rect.bottom):
            player.move(0, VEL)

# the player wants to jump
def jump(player):
    global JUMP_VEL
    if not block_y_collision(player.rect.x, player.rect.top+JUMP_VEL):
        player.rect.y -= JUMP_VEL
        JUMP_VEL -= 5
    if JUMP_VEL == 0:
        JUMP_VEL = 30
        player.is_jumping = False
        player.is_falling = True

# should any objects be falling?
# something in here causing some COLLISIONNNNNN issues
def check_gravity(sprite):
    # if y is not colliding with world_map in the y direction, decrement height
    y = sprite.rect.bottom
    if y < HEIGHT and block_y_collision(sprite.rect.x, y):
        sprite.is_falling = False
    if y+2 < HEIGHT and not block_y_collision(sprite.rect.x, y+2):
        sprite.is_falling = True
        sprite.rect.y += 2

# draws the map
def draw_map():
    WIN.fill(BLUE_BACK)
    row_count = 0
    for row in world_map:
        col_count = 0
        for col in row:
            if col == '1':
                block_rect = pygame.Rect(col_count*TILE_SIZE, row_count*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                WIN.blit(BLOCK_RECT, (block_rect.x, block_rect.y))
            elif col == '2':
                block_rect = pygame.Rect(col_count*TILE_SIZE, row_count*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                WIN.blit(SLUDGE_RECT, (block_rect.x, block_rect.y))
            elif col == '3' or col == '4':
                block_rect = pygame.Rect(col_count*TILE_SIZE, row_count*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                WIN.blit(PORTAL_WALL_RECT, (block_rect.x, block_rect.y))
            col_count += 1
        row_count += 1

# draw necessary things to the screen
def draw_window(player, blue, orange, button, cube):
    draw_map()
    pygame.draw.rect(WIN, BLUE, blue)
    pygame.draw.rect(WIN, ORANGE, orange)
    WIN.blit(button.surface, (button.rect.x, button.rect.y))
    WIN.blit(cube.surface, (cube.rect.topleft))
    WIN.blit(player.surface, (player.rect.x , player.rect.y))
    pygame.display.update()

def debug(player, blue, orange):
    # Draw a grid over the screen
    i = 0
    while i < TILES_Y:
        x = i * TILES_Y
        grid_line = pygame.Rect(x, 0, 10, 10)
        pygame.draw.rect(WIN, WHITE, grid_line)
        i += 1

def main():
    # Init maps
    load_maps()

    # Init Sprites
    player = sp.Player()
    cube = sp.Cube(TILE_SIZE*3, TILE_SIZE*3)

    # Init Objects
    blue = ob.Portal(0, 0)
    orange = ob.Portal(0, 120)
    button = ob.Button(TILE_SIZE*2, TILE_SIZE*9)
    
    # game loop
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        # Check for individual events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
                pygame.quit()
            
            # move portals if player clicks mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                mx = mouse_pos[0] // TILE_SIZE
                my = mouse_pos[1] // TILE_SIZE
                # Portal placed on wall
                if world_map[my][mx] == '3':
                    if mouse_click[0]: # left mouse button
                        blue.move(mouse_pos, 0)
                    if mouse_click[2]: # right mouse button
                        orange.move(mouse_pos, 0)
                # Portal placed on floor
                if world_map[my][mx] == '4':
                    if mouse_click[0]: # left mouse button
                        blue.move(mouse_pos, 1)
                    if mouse_click[2]: # right mouse button
                        orange.move(mouse_pos, 1)

            # Player grabs cube 
            cube_x_distance = abs(player.rect.centerx - cube.rect.centerx)
            cube_y_distance = abs(player.rect.centery - cube.rect.centery)
            if keys_pressed[pygame.K_e] and cube_x_distance < 100 and cube_y_distance < 100:
                if cube.held == True:
                    cube.held = False
                else:
                    cube.held = True
 
            # If the player jumps
            if keys_pressed[pygame.K_SPACE]:
                player.is_jumping = True
                player.is_falling = False 

        # if player.is_jumping == True:
        #     jump(player)
        # if player.is_falling == True:
        #     check_gravity(player)
        move_player(keys_pressed, player, blue, orange)
        if cube.held:
            cube.move(player)
        draw_window(player, blue, orange, button, cube)
        
if __name__ == "__main__":
    main()