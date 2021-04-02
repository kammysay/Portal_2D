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
PLAYER_RECT = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))
BLOCK_IMG = pygame.image.load(os.path.join('assets', 'ground_texture_1.png'))
BLOCK_RECT = pygame.transform.scale(BLOCK_IMG, (TILE_SIZE, TILE_SIZE))
BLUE_RECT = pygame.Rect(0, 0, PORTAL_WIDTH, PORTAL_HEIGHT)
ORG_RECT = pygame.Rect(0, 120, PORTAL_WIDTH, PORTAL_HEIGHT)
# ------------------------ CONSTANTS ----

# loads the world map
def load_map():
    # can later add a level selector, each map just named its level
    # number, easy to create a string to find file name i.txt
    file_location = os.path.join('maps', '1.txt')
    f = open(file_location)

    world_map = []
    for line in f:
        # maps are 10x10 (0-9)
        elements = line.split(' ')
        world_map.append(elements)
    return world_map
 
# check for block collision in x the plane in constant time
def left_collision(world_map, player):
    # floor division, no loops
    x = (player.x-10) // TILE_SIZE
    yHi = player.y // TILE_SIZE
    yMid = (player.y+PLAYER_HEIGHT//2) // TILE_SIZE
    yLo = (player.y+PLAYER_HEIGHT-1) // TILE_SIZE
    # Check the top, middle, and low points of the player for collisions
    if world_map[yHi][x] == '1' or world_map[yMid][x] == '1' or world_map[yLo][x] == '1':
        player.x += VEL #cancel out velocity if touching block
def right_collision(world_map, player):
    x = (player.x+PLAYER_WIDTH) // TILE_SIZE
    yHi = player.y // TILE_SIZE
    yMid = (player.y+PLAYER_HEIGHT//2) // TILE_SIZE
    yLo = (player.y+PLAYER_HEIGHT-1) // TILE_SIZE
    # Check the top, middle, and low points of the player for collisions
    if world_map[yHi][x] == '1' or world_map[yMid][x] == '1' or world_map[yLo][x] == '1':
        player.x -= VEL

# check for block collisions in the y plane in constant time
def up_collision(world_map, player):
    xLeft = player.x // TILE_SIZE
    xMid = (player.x+PLAYER_WIDTH//2) // TILE_SIZE
    xRight = (player.x+PLAYER_WIDTH-1) // TILE_SIZE
    y = (player.y-10) // TILE_SIZE
    # Check the left, middle, and right points of the player for collisions
    if world_map[y][xLeft] == '1' or world_map[y][xMid] == '1' or world_map[y][xRight] == '1':
        player.y += VEL
def down_collision(world_map, player):
    xLeft = player.x // TILE_SIZE
    xMid = (player.x+PLAYER_WIDTH//2) // TILE_SIZE
    xRight = (player.x+PLAYER_WIDTH-1) // TILE_SIZE
    y = (player.y+PLAYER_HEIGHT) // TILE_SIZE
    # Check the left, middle, and right points of the player for collisions
    if world_map[y][xLeft] == '1' or world_map[y][xMid] == '1' or world_map[y][xRight] == '1':
        player.y -= VEL

# check if the player is going through the blue portal
def blue_collision(player):
    # make this easier by making a player class with a top, mid, low, etc
    char_mid_x = player.x + PLAYER_WIDTH/2
    char_mid_y = player.y + PLAYER_HEIGHT/2

    hit = False
    # is character colliding with blue portal
    if char_mid_x >= BLUE_RECT.x and char_mid_x <= BLUE_RECT.x+PORTAL_WIDTH and char_mid_y >= BLUE_RECT.y and char_mid_y <= BLUE_RECT.y+PORTAL_HEIGHT:
        hit = True
    return hit

# check if the player is going through the orange portal
def orange_collision(player):
    char_mid_x = player.x + PLAYER_WIDTH/2
    char_mid_y = player.y + PLAYER_HEIGHT/2

    hit = False
    # is the character colliding with orange portal
    if char_mid_x >= ORG_RECT.x and char_mid_x <= ORG_RECT.x+PORTAL_WIDTH and char_mid_y >= ORG_RECT.y and char_mid_y <= ORG_RECT.y+PORTAL_HEIGHT:
        hit = True
    return hit

# move the player in the x and y directions
def move_player(keys_pressed, world_map, player):
    # might need to assign global vars new values
    global player_direction
    global PLAYER_RECT

    if keys_pressed[pygame.K_LEFT] and player.x > 0:
        # flip player left if needed
        if player_direction == 1:
            print("left")
            PLAYER_RECT = pygame.transform.flip(PLAYER_RECT, True, False)
            player_direction = 0
        # check if the player collided with the walls or portals
        left_collision(world_map, player)
        if blue_collision(player):
            player.x = ORG_RECT.x - PLAYER_WIDTH
            player.y = ORG_RECT.y
        if orange_collision(player):
            player.x = BLUE_RECT.x - PLAYER_WIDTH
            player.y = BLUE_RECT.y
        # move player
        player.x -= VEL
        
    if keys_pressed[pygame.K_RIGHT] and player.x+PLAYER_WIDTH < WIDTH:
        # flip player right if needed
        if player_direction == 0:
            print("right")
            PLAYER_RECT = pygame.transform.flip(PLAYER_RECT, True, False)
            player_direction = 1
        # check if player collided with walls or portals
        right_collision(world_map, player)
        if blue_collision(player):
            player.x = ORG_RECT.x + PORTAL_WIDTH
            player.y = ORG_RECT.y
        if orange_collision(player):
            player.x = BLUE_RECT.x + PORTAL_WIDTH
            player.y = BLUE_RECT.y
        # move player
        player.x += VEL
        
    if keys_pressed[pygame.K_UP] and player.y > 0:
        up_collision(world_map, player)
        player.y -= VEL
       
    if keys_pressed[pygame.K_DOWN] and player.y+PLAYER_HEIGHT < HEIGHT:
        down_collision(world_map, player)
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
    WIN.blit(PLAYER_RECT, (player.x, player.y))
    pygame.display.update()

def main():
    # world_map = load_map()
    world_map = [
        [ '0', '1', '1', '1', '1', '1', '1', '0', '0', '1'],
        [ '0', '0', '0', '0', '1', '1', '1', '0', '0', '1'],
        [ '1', '0', '1', '0', '0', '0', '0', '0', '0', '1'],
        [ '0', '0', '1', '0', '0', '0', '0', '1', '0', '1'],
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if mouse_click[0]:
                    BLUE_RECT.x = mouse_pos[0]-5
                    BLUE_RECT.y = mouse_pos[1]-PORTAL_WIDTH/2
                if mouse_click[2]:
                    ORG_RECT.x = mouse_pos[0]-5
                    ORG_RECT.y = mouse_pos[1]-PORTAL_WIDTH/2
        
        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed, world_map, player)
        draw_window(player, world_map)

if __name__ == "__main__":
    main()