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
PORTAL_WIDTH, PORTAL_HEIGHT = PLAYER_WIDTH//2-1, TILE_SIZE*2
VEL = 10

# assets
BLOCK_IMG = pygame.image.load(os.path.join('assets', 'ground_texture_1.png'))
BLOCK_RECT = pygame.transform.scale(BLOCK_IMG, (TILE_SIZE, TILE_SIZE))
# ------------------------ CONSTANTS ----

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        image = pygame.image.load(os.path.join('assets', 'sven.png'))
        self.surface = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        #self.rect.center = (self.width/2, self.height/2)
        # Game logic of player
        self.direction = 1 # 0 == Left, 1 == Right
        self.is_falling = True
        self.is_jumping = False
        self.just_teleported = False

    # Control player movement
    def move(self, x_vel, y_vel):
        self.rect.x += x_vel
        self.rect.y += y_vel

    # Teleport player after going through portal (not currently used)
    def teleport(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
    
    # Change which direction the player is looking
    def flip(self):
        self.surface = pygame.transform.flip(self.surface, True, False)
        if self.direction == 0:
            self.direction = 1
        else:
            self.direction = 0

# Portal class
class Portal():
    def __init__(self, x, y):
        self.width = PLAYER_WIDTH // 2
        self.height = TILE_SIZE * 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.direction = 0 # 0 == Left, 1 == Right

    # Places portal on either the left or right side of a block depending on mouse position
    def move(self, mouse_pos):
        # Floor the mouse position to the nearest even intervals of tile size
        # Portals can't be just anywhere, which causes glitches.
        L = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
        R = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE + TILE_SIZE
        H = (mouse_pos[1] // TILE_SIZE) * TILE_SIZE
        leftRange = abs(mouse_pos[0] - L)
        rightRange = abs(mouse_pos[0] - R)

        # Set portal to either left or right side of block depending on mouse proximity
        if leftRange <= rightRange:
            # move the portal to the left side of the block
            self.rect.left = L
            self.rect.top = H
            self.direction = 0
        else:
            # move the portal to the right side of the block
            self.rect.right = R
            self.rect.top = H
            self.direction = 1

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

# Detect if player is colliding with a portal
def portal_collision(portal, x, y):
    # If character is colliding with portal
    if x >= portal.rect.left and x <= portal.rect.right and y >= portal.rect.top and y <= portal.rect.bottom:
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
    # the ifs prevents crashing from list index out of range error with map
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
    # the ifs prevents crashing from list index out of range error with map
    if x1 < 0:
        x1 = 0
    if x3 > 9:
        x3 = 9
    if world_map[y][x1] == '1' or world_map[y][x2] == '1' or world_map[y][x3] == '1':
        return True
    else:
        return False

# move the player in the x and y directions
def move_player(keys_pressed, world_map, player, blue, orange):
    # Left movement
    if keys_pressed[pygame.K_a] and player.rect.x  > 0:
        # flip player if needed
        if player.direction == 1:
            player.flip()

        # check if player collided with blue/orange portals
        if portal_collision(blue, player.rect.left-1, player.rect.centery+1):
            player.rect.topright = (orange.rect.left, orange.rect.top)
        if portal_collision(orange, player.rect.left-1, player.rect.centery+1):
            player.rect.topright = (blue.rect.left, blue.rect.top)

        # if not colliding with blocks, move player
        if not block_x_collision(world_map, player.rect.x -1, player.rect.y):
            player.move(-VEL, 0)
        
    # Right movement
    if keys_pressed[pygame.K_d] and player.rect.x+PLAYER_WIDTH < WIDTH:
        # flip player right if needed
        if player.direction == 0:
            player.flip()  

        # check if player collided with blue/orange portals
        if portal_collision(blue, player.rect.right+1, player.rect.centery+1):
            player.rect.topleft = (orange.rect.right, orange.rect.top)
        if portal_collision(orange, player.rect.right+1, player.rect.centery+1):
            player.rect.topleft = (blue.rect.right, blue.rect.top)

        # if not colliding with blocks, move player
        if not block_x_collision(world_map, player.rect.x+PLAYER_WIDTH, player.rect.y):
            player.rect.x  += VEL 
        
    # UP and DOWN will be gone soon, once jump implemented
    if keys_pressed[pygame.K_w] and player.rect.y > 0:
        # if not colliding with blocks, move player
        if not block_y_collision(world_map, player.rect.x, player.rect.y-1):
            player.rect.y -= VEL
            player.is_falling = True
       
    if keys_pressed[pygame.K_s] and player.rect.y+PLAYER_HEIGHT < HEIGHT:
        # if not colliding with blocks, move player
        if not block_y_collision(world_map, player.rect.x , player.rect.y+PLAYER_HEIGHT):
            player.rect.y += VEL

# should the player be falling?
def check_gravity(world_map, player):
    # if y is not colliding with world_map in the y direction, decrement height
    y = player.rect.bottom
    if y < HEIGHT and block_y_collision(world_map, player.rect.x, y):
        player.is_falling = False
    if y < HEIGHT and not block_y_collision(world_map, player.rect.x, y):
        player.is_falling = True
        player.rect.y += VEL //2

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
def draw_window(world_map, player, blue, orange):
    draw_map(world_map)
    pygame.draw.rect(WIN, BLUE, blue)
    pygame.draw.rect(WIN, ORANGE, orange)
    WIN.blit(player.surface, (player.rect.x , player.rect.y))
    pygame.display.update()

def main():
    # world_map = load_map()
    world_map = [ # This is just a temporary testing map
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
    
    # Init Player(pygame.sprite.Sprite)
    player = Player()

    # Init Portal(x, y)
    blue = Portal(0, 0)
    orange = Portal(0, 120)


    # game loop
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # move portals if player clicks mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                mx = mouse_pos[0] // 60
                my = mouse_pos[1] // 60
                # Portal can only be placed on walls
                if world_map[my][mx] == '1':
                    print(mouse_pos)
                    if mouse_click[0]: # left mouse button
                        blue.move(mouse_pos)
                    if mouse_click[2]: # right mouse button
                        orange.move(mouse_pos)
             # DEBUG EVENT - TO BE REMOVED
            if event.type == pygame.KEYDOWN:
                kp = pygame.key.get_pressed()
                if kp[pygame.K_h]:
                    print("-- DEBUG -----------------------------------------------")
                    print("blue.x, blue.y == ", blue.rect.x, blue.rect.y)
                    print("orange.x, orange.y == ", orange.rect.x, orange.rect.y)
                    print("Player width ==", player.rect.right - player.rect.left)
                    print("Player height == ", player.rect.bottom - player.rect.top)
                    print("Player TopLeft == ", player.rect.topleft)
                    print("Player BottomRight == ", player.rect.bottomright)
                    print("--------------------------------------------------------")
            

        # if player.is_falling:
        #     check_gravity(world_map, player)
        
        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed, world_map, player, blue, orange)
        draw_window(world_map, player, blue, orange)

if __name__ == "__main__":
    main()

# NOTES
# Post-teleport Glitch: after teleporting through a portal, player improperly collides
# with blocks, gets stuck in walls and floors.
# Fixed: the post-teleport glitch was due to the location of the portals.
# Placing the portals in even intervals on the map (TILE_SIZE intervals), and spawning
# the player in similar intervals when teleporting resolves the post-teleport issue.