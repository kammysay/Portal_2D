# **Portal 2D**
Portal 2D is a platform based game made using Python's pygame library inspired by the Portal game series.

## **The Player**

---

The player class consists of location and game logic information and several useful methods such as move() and flip(). The player is a rectangle that moves on the screen (referred to as a sprite) and collides with the map and certain objects. The player intentionally is unable to collide with the Cubes or Buttons.

The Player class can be found in Sprites.py

## **Portal Logic**

---
The portals were troublesome to say the least. The logic itself is simple enough, when a certain point of the player collides with a portal the program checks the direction of the opposite portal (left, right, up, down) and will teleport the player to the appropriate coordinates of that portal.

The portals had to be made to only be placed on exact intervals of TILE_SIZE, else when the player teleported, the player's rect would be out of line, causing collision issues including the playing getting stuck in blocks and crashing when touching the edge of the map.

Portals can only be placed on portal wall and portal floor/ceiling (3 and 4 in world_map), and will be placed on the left, right, top or bottom of the block that is clicked depending on the position of the mouse. If the mouse is closer to the left of the block when clicked it is placed on the left and vice versa.

The Portal class can be found in Objects.py

*note: the portal system is unfinished*


## **Map System**
---
The game map system consists of two maps for two different purposes, each loaded from the same file. The maps are 2D lists of numbers. The maps are text files stored in the maps subdirectory consisting of numbers 0 - 4 and are manually typed.
### **World Map**
This is a direct copy of the file it is loaded from, and is used for texture information in the game.  Tiles are drawn based on the numbers in world_map.
* 0 - nothing / air
* 1 - standard block
* 2 - sludge / water
* 3 - portal wall (for vertical portals)
* 4 - portal floor/ceiling (for horizontal portals)
### **Collision Map**
This map is used for detecting collisions between the map and sprites. Every element in this 2D list is either a 0 (no collision) or a 1 (collision). Any block that isn't a 0 or a 2 (air or water) in world_map will be set to 1 in collision_map (something the player will collide with).

Both maps are contained directly in the world_testing.py file and are not treated as classes.

## **Companion Cube and Buttons**
---

*"The Enrichment Center reminds you that the Weighted Companion Cube will never threaten to stab you and, in fact, cannot speak."*

The Companion Cube is a Sprite that moves along the screen when held by the player and is affected by gravity. The button is implemented as a static object. When the bottom of the cube collides with the button, the button is activated and the cube snaps to position centered on top of the button.

Cube movement is handled simply; if the player is holding it, it will snap to the player's left or right edge depending on what direction the player is facing. The cube is not affected by gravity while it is being held. If it is not being held it will be affected by gravity and can collide with the collision_map.

The Cube class can be found in Sprites.py

The Button class can be found in Objects.py