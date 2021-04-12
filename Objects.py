import os
import pygame

# window
WIDTH, HEIGHT = 1152, 704 #  must be multiples of 64

# game logic
TILE_SIZE = 64
TILES_X, TILES_Y = WIDTH/TILE_SIZE, HEIGHT/TILE_SIZE # number of tiles in each direction (18 x 11)

# Portal class
class Portal():
    def __init__(self, x, y):
        self.vert_width = TILE_SIZE // 4
        self.vert_height = TILE_SIZE * 2
        self.hor_width = TILE_SIZE * 2
        self.hor_height = TILE_SIZE // 4
        self.rect = pygame.Rect(x, y, self.vert_width, self.vert_height)
        self.direction = 0 # 0 == Left, 1 == Right, 2 = Up, 3 == Down

    # Move portal to block depending on mouse position.
    # orientation is whether or not the portal is being placed horizonatal (0) or vertical (1)
    def move(self, mouse_pos, orientation):
        mx = mouse_pos[0]
        my = mouse_pos[1]
        if orientation == 0: # vertical portal
            self.rect.width = self.vert_width
            self.rect.height = self.vert_height

            # Floor the mouse position to the nearest even intervals of tile size
            L = (mx // TILE_SIZE) * TILE_SIZE
            R = (mx // TILE_SIZE) * TILE_SIZE + TILE_SIZE
            Y = (my // TILE_SIZE) * TILE_SIZE
            leftRange = abs(mx - L)
            rightRange = abs(mx - R)

            # Set portal to either left or right side of block depending on mouse proximity
            if leftRange <= rightRange:
                # move the portal to the left side of the block
                self.rect.left = L
                self.rect.top = Y
                self.direction = 0
            else:
                # move the portal to the right side of the block
                self.rect.right = R
                self.rect.top = Y
                self.direction = 1
        else: # horizontal portal
            self.rect.width = self.hor_width
            self.rect.height = self.hor_height

            # Floor the mouse position to the nearest even intervals of tile size
            T = (my // TILE_SIZE) * TILE_SIZE
            B = (my // TILE_SIZE) * TILE_SIZE + TILE_SIZE
            X = (mx // TILE_SIZE) * TILE_SIZE
            topRange = abs(my - T)
            bottomRange = abs(my - B)

            if topRange <= bottomRange:
                # move portal to top of blocks
                self.rect.top = T
                self.rect.left = X
                self.direction = 2
            else:
                # move portal to bottom of block
                self.rect.bottom = B
                self.rect.left = X
                self.direction = 3


class Button():
    def __init__(self, x, y):
        self.width = TILE_SIZE*2
        self.height = TILE_SIZE
        self.image = pygame.image.load(os.path.join('assets', 'button.png'))
        self.surface = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (x, y)
        self.activated = False