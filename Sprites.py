import os
import pygame

# window
WIDTH, HEIGHT = 1152, 704 #  must be multiples of 64

# game logic
TILE_SIZE = 64
VEL = 8
JUMP_VEL = 24

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE * 2
        image = pygame.image.load(os.path.join('assets', 'sven.png'))
        self.surface = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        # Game logic of player
        self.direction = 1 # 0 == Left, 1 == Right
        self.is_jumping = False
        self.just_teleported = False

    # Control player movement
    def move(self, x_vel, y_vel):
        self.rect.x += x_vel
        self.rect.y += y_vel

    # Drag player down
    def gravity(self):
        self.rect.bottom += VEL

    # the player wants to jump
    def jump(self):
        self.rect.top -= JUMP_VEL

    # Teleport player to specified portal
    def teleport(self, portal):
        if portal.direction == 0:
            self.rect.topright = (portal.rect.left, portal.rect.top)
        if portal.direction == 1:
            self.rect.topleft = (portal.rect.right, portal.rect.top)
        if portal.direction == 2:
            self.rect.centerx = portal.rect.centerx
            self.rect.bottom = portal.rect.top
        if portal.direction == 3:
            self.rect.centerx = portal.rect.centerx
            self.rect.top = portal.rect.bottom
    
    # Change which direction the player is looking
    def flip(self):
        self.surface = pygame.transform.flip(self.surface, True, False)
        if self.direction == 0:
            self.direction = 1
        else:
            self.direction = 0


class Cube():
    def __init__(self, x, y):
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.image.load(os.path.join('assets', 'cube.png'))
        self.surface = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (x, y)
        self.held = False
        self.is_falling = False
        self.on_button = False

    # Move the cube with the player
    def move(self, player):
        # if player facing left
        if player.direction == 0:
            self.rect.right = player.rect.left
            self.rect.centery = player.rect.centery
        # if player facing right
        if player.direction == 1:
            self.rect.left = player.rect.right
            self.rect.centery = player.rect.centery

    # Drag sprite down
    def gravity(self):
        self.rect.bottom += VEL

    # Teleport cube to specified portal
    def teleport(self, portal):
        if portal.direction == 0:
            self.rect.topright = (portal.rect.left, portal.rect.top)
        if portal.direction == 1:
            self.rect.topleft = (portal.rect.right, portal.rect.top)
        if portal.direction == 2:
            self.rect.centerx = portal.rect.centerx
            self.rect.bottom = portal.rect.top
        if portal.direction == 3:
            self.rect.centerx = portal.rect.centerx
            self.rect.top = portal.rect.bottom

    # Set the cube to appear directly on top of the button
    def snap_to_button(self, button):
        self.rect.centerx = button.rect.centerx
        self.rect.bottom = button.rect.centery