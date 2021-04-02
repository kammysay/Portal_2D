import pygame

# ---- CONSTANTS ----------------------------
# window
WIDTH, HEIGHT = 1800, 950
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Portal Testing")
FPS = 60

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
ORANGE = (255, 127, 80)

PORTAL_WIDTH, PORTAL_HEIGHT = 100, 400
CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
VEL = 10
# ---------------------------- CONSTANTS ----

# Draw the screen and objects
def draw_window(blue, orange, character):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLUE, blue) 
    pygame.draw.rect(WIN, ORANGE, orange) 
    pygame.draw.rect(WIN, BLACK, character)

    pygame.display.update()

# Move the player based on user input
def move_player(keys_pressed, character):
    if keys_pressed[pygame.K_LEFT] and character.x > 0:
        character.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and character.x < WIDTH-50:
        character.x += VEL
    if keys_pressed[pygame.K_UP] and character.y > 0:
        character.y -= VEL
    if keys_pressed[pygame.K_DOWN] and character.y < HEIGHT-50:
        character.y += VEL

# If player collides with one portal, teleport them to the other
def portal_collision(blue, orange, character):
    # The midpoint of the character in x and y directions
    CHARACTER_CENTER_X = character.x + CHARACTER_WIDTH/2
    CHARACTER_CENTER_Y = character.y + CHARACTER_HEIGHT/2

    # Check if character collided with blue portal
    if CHARACTER_CENTER_X >= blue.x and CHARACTER_CENTER_X <= blue.x + PORTAL_WIDTH and CHARACTER_CENTER_Y >= blue.y and CHARACTER_CENTER_Y <= blue.y + PORTAL_HEIGHT:
        character.x = orange.x + PORTAL_WIDTH
        character.y = orange.y + PORTAL_HEIGHT/2

     # Check if character collided with orange portal
    elif CHARACTER_CENTER_X >= orange.x and CHARACTER_CENTER_X <= orange.x + PORTAL_WIDTH and CHARACTER_CENTER_Y >= orange.y and CHARACTER_CENTER_Y <= orange.y + PORTAL_HEIGHT:
        character.x = blue.x - CHARACTER_WIDTH
        character.y = blue.y + PORTAL_HEIGHT/2


def main():
    # the portals
    # Rect(x, y, width, height)
    blue = pygame.Rect(1400, 200, PORTAL_WIDTH, PORTAL_HEIGHT)
    orange = pygame.Rect(300, 400, PORTAL_WIDTH, PORTAL_HEIGHT)

    # the "character"
    character = pygame.Rect(700, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    
    # game loop
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #Handle quit event
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
        #Move player
        keys_pressed = pygame.key.get_pressed()
        portal_collision(blue, orange, character)
        move_player(keys_pressed, character)

        draw_window(blue, orange, character)

    pygame.quit()

#Only run main if this file called it
if __name__ == "__main__":
    main()