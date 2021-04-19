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

    # Detect if sprite is colliding with a portal
    def collision(self, x, y):
        if x >= self.rect.left and x <= self.rect.right and y >= self.rect.top and y <= self.rect.bottom:
                return True
        else:
            return False

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
        self.x = x
        self.y = y

        self.image_off = pygame.image.load(os.path.join('assets', 'button_off.png'))
        self.image_on = pygame.image.load(os.path.join('assets', 'button_on.png'))
        self.surface_off = pygame.transform.scale(self.image_off, (self.width, self.height))
        self.surface_on = pygame.transform.scale(self.image_on, (self.width, self.height))
        self.surface = self.surface_off
        self.rect = self.surface_off.get_rect()
        self.rect.bottomleft = (x, y)

        self.activated = False

    # Detect if sprite collided with button
    def collision(self, sprite):
        x = sprite.rect.centerx
        y = sprite.rect.bottom

        if x >= self.rect.left and x <= self.rect.right and y >= self.rect.top and y <= self.rect.bottom:
            return True
        else:
            return False

    # Turn button on
    def button_on(self):
        if self.activated == False:
            self.flip_state()

    # Turn button off
    def button_off(self):
        if self.activated == True:
            self.flip_state()

    # Turn button "on" or "off" (change the image and activation status)
    def flip_state(self):
        if self.activated == False:
            self.activated = True
            self.surface = self.surface_on
        else:
            self.activated = False
            self.surface = self.surface_off
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (self.x, self.y)