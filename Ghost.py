from GameObject import GameObject
from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals

class Ghost(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.GHOST)

    def move(self):
        direction = Direction.NONE
        if globals.pacman.position.y > self.position.y:
            direction = direction | Direction.DOWN
        if globals.pacman.position.y < self.position.y:
            direction = direction | Direction.UP
        if globals.pacman.position.x > self.position.x:
            direction = direction | Direction.RIGHT
        if globals.pacman.position.x < self.position.x:
            direction = direction | Direction.LEFT

        return direction
