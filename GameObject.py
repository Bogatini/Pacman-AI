from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import Pos

from GameDefs import globals


class GameObject:
    gameObjects = []

    def __init__(self, p, t):
        self.startPos = p
        self.position = p
        self.type = t
        GameObject.gameObjects.append(self)

    def move(self):
        return Direction.NONE

    def checkCollisions(o):
        for go in GameObject.gameObjects:

            if go.position.x == o.x and go.position.y == o.y:
                return go.type
        return SpriteType.EMPTY

    def checkCollision(self, other):
        return self.position.x == other.position.x and self.position.y == other.position.y

    def hide(self):
        self.position = Pos(-1, -1)

    def reset(self):
        self.position = self.startPos

    def update(self):
        # Basic movement logic
        direction = self.move()

        if direction != Direction.NONE:
            newPos = Pos(self.position.x, self.position.y)
            if direction & Direction.LEFT:
                newPos.x -= 1
            if direction & Direction.RIGHT:
                newPos.x += 1
            if direction & Direction.UP:
                newPos.y -= 1
            if direction & Direction.DOWN:
                newPos.y += 1

            # Wrap around logic for the game boundaries
            newPos.x = (newPos.x + globals.gameSize) % globals.gameSize
            newPos.y = (newPos.y + globals.gameSize) % globals.gameSize

            # Check if the new position is not a wall before moving
            if globals.game.check_position(newPos) != SpriteType.WALL:
                self.position = newPos

