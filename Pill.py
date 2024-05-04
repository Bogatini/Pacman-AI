from GameObject import GameObject
from GameDefs import SpriteType


class Pill(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PILL)
        self.timer = 0

    def eaten(self):
        self.timer = 15
        self.hide()

    def isActive(self):
        return self.timer > 0

    def update(self):
        if self.timer > 0:
            self.timer -= 1