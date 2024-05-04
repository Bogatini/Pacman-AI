from GameObject import GameObject

from GameDefs import globals
from GameDefs import SpriteType

from GameDefs import Pos
from Pill import Pill
from PacMan import PacMan
from Ghost import Ghost




class Game:

    gameTime = 0
    addWalls = False



    def __init__(self):
        # Initialize game elements
        self.pacman = PacMan(Pos(15, 15))
        self.ghost = Ghost(Pos(1, 1))
        self.pill = Pill(Pos(15, 3))
        self.score = 0
        self.grid = [[None for x in range(globals.gameSize)] for y in range(globals.gameSize)]

        globals.pacman = self.pacman
        globals.ghost = self.ghost
        globals.pill = self.pill



        for i in range(globals.gameSize):
            GameObject(Pos(i, 0), SpriteType.WALL)
            GameObject(Pos(i, globals.gameSize - 1), SpriteType.WALL)
            GameObject(Pos(0, i), SpriteType.WALL)
            GameObject(Pos(globals.gameSize - 1, i), SpriteType.WALL)

        if Game.addWalls:

            for i in range(globals.gameSize  // 2 - 3):
                GameObject(Pos(i + globals.gameSize  // 4 + 2, globals.gameSize  // 4), SpriteType.WALL)
                GameObject(Pos(i + globals.gameSize  // 4 + 2, globals.gameSize  * 3 // 4), SpriteType.WALL)

                GameObject(Pos(globals.gameSize  // 4, i + globals.gameSize  // 4 + 2), SpriteType.WALL)
                GameObject(Pos(globals.gameSize  * 3 // 4, i + globals.gameSize  // 4 + 2), SpriteType.WALL)
        for i in range(globals.gameSize):
            for j in range(globals.gameSize):
                if GameObject.checkCollisions(Pos(i, j)) == SpriteType.EMPTY:
                    self.grid[i][j] = GameObject(Pos(i, j), SpriteType.DOT)

    def update(self):
        Game.gameTime += 1



        if self.grid[self.pacman.position.x][self.pacman.position.y] != None:
            self.grid[self.pacman.position.x][self.pacman.position.y].hide()
            self.grid[self.pacman.position.x][self.pacman.position.y] = None
            self.score += 1

        # Update game elements
        self.pacman.update()
        self.ghost.update()
        self.pill.update()

        ## PILL STUFF ***
        # corrected this like to have NOT in it
        if (not self.pill.isActive()) and self.pacman.checkCollision(self.pill):
            self.pill.eaten()

        if self.pacman.checkCollision(self.ghost):
            if self.pill.isActive():
                self.ghost.hide()
                self.score += 100
            else:
                print("Score: " + str(self.score))
                return True

        if Game.gameTime >= 1000:
            return True

        return False

    @staticmethod
    def check_position(p):
        for obj in GameObject.gameObjects:
            if obj.position.x == p.x and obj.position.y == p.y:
                return obj.type
        return SpriteType.EMPTY

