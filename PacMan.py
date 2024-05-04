from GameObject import GameObject
from GameDefs import Pos

from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals

from queue import PriorityQueue

import random

class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)
        self.directionNum = 0 # used when there is no pill or ghost to go in circles

    def heuristic(self, pos):
        # THIS IS WHERE THE DECISION MAKING HAPPENS
        # Manhattan distance heuristic   https://en.wikipedia.org/wiki/Taxicab_geometry
        # the returned value is added to the priority of a possible move
        # the higher the priority value the less likely the move is to be taken (the further back in the queue the move will be placed)
        # basically, low number here means pacman wants to take the move, high priority means he doesn't
        #
        # if pacman doesn't have the power pill, he should try and get one, unless the ghost will get in the way
        # if pacman does have the power pill AND the ghost is <16 moves away, go to is ASAP - this shoul be the only thing it cares about

        # the normal heuristic that is used for A*, added code allows for
        manhattanDistance = abs(pos[0] - globals.pill.position.x) + abs(pos[1] - globals.pill.position.y)

        # calculate the distance to the ghost and pill (pythagoras)
        ghostDistance = ((pos[0] - globals.ghost.position.x) ** 2 + (pos[1] - globals.ghost.position.y) ** 2)**0.5
        pillDistance = ((pos[0] - globals.pill.position.x) ** 2 + (pos[1] - globals.pill.position.y) ** 2)**0.5


        if globals.pill.isActive() and ghostDistance <= 15:
            # when the pill is acive go to the ghost if you know you can reach it in time (it doesn't run away like in the real game)
            return(0)

        if ghostDistance <= 10:
            # if the ghost is close, dont go nearer
            return(float("inf"))


        # if the ghost is far away and the pill isnt active, just go towards the pill
        return manhattanDistance

    def aStarSearch(self, start, end):
        # im turing the Pos(x,y) objects into Tuples (Int x,Int y) because tuples can be hashed and used in dictionaries
        startPos = (start.x, start.y)
        endPos = (end.x,end.y)

        # https://en.wikipedia.org/wiki/A*_search_algorithm
        # sorted best to worse, 0 to n, the priority queue holds all possible moves in order of how "good" they are
        openSet = PriorityQueue()
        openSet.put(startPos, 0)

        # holds all the best discovered paths (bad paths are overwritten)
        pathDict = {}
        pathDict[startPos] = None

        # holds the total "cost" or distance of a path
        totalDistanceDict = {}
        totalDistanceDict[startPos] = 0

        if endPos == (-1,-1):
            # when a ghost is eaten, it is moved to (-1,-1)
            # if we put that coordinate into the dictionary it will break
            return []

        while not openSet.empty():

            # pops the highest priority move off the queue
            currentPos = openSet.get()

            if currentPos == endPos:
                # end of the path is reached
                break

            for nextPos in self.neighbors(currentPos):
                newDistance = totalDistanceDict[currentPos] + 1

                if nextPos not in totalDistanceDict or newDistance < totalDistanceDict[nextPos]:
                    # if a better or new path is found, add the previous move that leads to current to the path dictionary

                    totalDistanceDict[nextPos] = newDistance
                    priority = newDistance + self.heuristic(nextPos) # factor in distance to ghost

                    openSet.put(nextPos, priority)
                    pathDict[nextPos] = currentPos

        # now create a path from the best moves at each position
        path = []
        currentPos = endPos # start at the end position and work your way back

        while currentPos != startPos:
            path.append(currentPos)
            currentPos = pathDict[currentPos]

        returnPath = []
        for x in range(len(path)-1, 0, -1):
            returnPath.append(path[x])

        returnPath.append(endPos) # manually add the target position to the path

        return returnPath


    def neighbors(self, pos):
        x, y = pos[0], pos[1]
        nextPositions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        validNeighbors = []

        for position in nextPositions:
            # have to turn the tuple back into a Pos(x,y) to use check_position(Pos)
            nextPos = Pos(position[0], position[1])

            if globals.game.check_position(nextPos) != SpriteType.WALL:
                validNeighbors.append((position[0], position[1]))

        return validNeighbors


    def move(self):
        direction = Direction.NONE

        # Hunt Ghost State
        if not globals.pill.isActive():
            # if the power pill is not active, go find the pill
            path = self.aStarSearch(self.position, globals.pill.position)
        # Hunt Pill State
        else:
            # if the power pill is active, go find the ghost
            path = self.aStarSearch(self.position, globals.ghost.position)

        # if there is no ghost, path = []
        if len(path) >= 1:
            next_pos = path[0]

            if next_pos[0] > self.position.x:
                direction = direction | Direction.RIGHT
            if next_pos[0] < self.position.x:
                direction = direction | Direction.LEFT

            if next_pos[1] > self.position.y:
                direction = direction | Direction.DOWN
            if next_pos[1] < self.position.y:
                direction = direction | Direction.UP

        # Collect Points State
        else:
            # there is no pill or ghost
            # just move to the edge of the map and start circling
            # pacman will wait for another pill to appear of ghost to run away from

            circleDirections = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
            direction = circleDirections[self.directionNum]

            currentPos = self.position

            # check if pacman is going to hit a wall, if he is switch direction
            if direction == Direction.RIGHT:
                nextPos = Pos(currentPos.x+1,currentPos.y)
                if globals.game.check_position(nextPos) == SpriteType.WALL:
                    self.directionNum+=1
            if direction == Direction.LEFT:
                nextPos = Pos(currentPos.x-1,currentPos.y)
                if globals.game.check_position(nextPos) == SpriteType.WALL:
                    self.directionNum+=1
            if direction == Direction.UP:
                nextPos = Pos(currentPos.x,currentPos.y-1)
                if globals.game.check_position(nextPos) == SpriteType.WALL:
                    self.directionNum+=1
            if direction == Direction.DOWN:
                nextPos = Pos(currentPos.x,currentPos.y+1)
                if globals.game.check_position(nextPos) == SpriteType.WALL:
                    self.directionNum+=1

        return direction