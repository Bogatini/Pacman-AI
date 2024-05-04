from GameObject import GameObject
from GameDefs import Pos, SpriteType, Direction, globals
from queue import PriorityQueue

class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)

    def pillHeuristic(self, pos):
        # THIS IS WHERE THE DECISION MAKING HAPPENS
        # Manhattan distance heuristic   https://en.wikipedia.org/wiki/Taxicab_geometry
        # the returned value is added to the priority of a possible move
        # the higher the priority the less likely the move is to be taken
        # basically, low number here means pacman wants to take the move, high priority means he doesn't
        #
        # if pacman doesn't have the power pill, he should try and get one, unless the ghost will get in the way
        # if pacman does have the power pill AND the ghost is <16 moves away, go to is ASAP - this shoul be the only thing it cares about

        manhattanDistance = abs(pos[0] - globals.pill.position.x) + abs(pos[1] - globals.pill.position.y)

        # calculate the distance to the ghost and pill
        ghostDistance = ((pos[0] - globals.ghost.position.x) ** 2 + (pos[1] - globals.ghost.position.y) ** 2)**0.5
        pillDistance = ((pos[0] - globals.pill.position.x) ** 2 + (pos[1] - globals.pill.position.y) ** 2)**0.5




        if globals.pill.isActive() and ghostDistance <= 15:
            # when the pill is acive go to the ghost if you know you can reach it in time (it doesn't run away like in the real game)
            return(0)

        if pillDistance <= 5:
            # if the pill is close, no matter what go to it
            return(-10)

        if ghostDistance <= 10:
            # if the ghost is
            return(float("inf"))



        return manhattanDistance

    def a_star_search(self, start, end):
        start = (start.x, start.y)
        end = (end.x,end.y)
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():

            current = frontier.get()

            if current == end:
                break

            for next_pos in self.neighbors(current):
                new_cost = cost_so_far[current] + 1

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:

                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.pillHeuristic(next_pos) # factor in distance to ghost

                    frontier.put(next_pos, priority)
                    came_from[next_pos] = current

        path = []
        pillPos = globals.pill.position
        current = (pillPos.x, pillPos.y) # start at the end and work your way back

        while current != start:
            path.append(current)
            current = came_from[current]



        returnPath = []
        for x in range(len(path)-1, 0, -1):
            returnPath.append(path[x])

        returnPath.append((pillPos.x, pillPos.y))


        return returnPath





    def neighbors(self, pos):
        x, y = pos[0], pos[1]
        next_positions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
        valid_neighbors = []
        ghost_pos = (globals.ghost.position.x, globals.ghost.position.y)

        for next_pos in next_positions:
            nextPos = Pos(next_pos[0], next_pos[1])



            if globals.game.check_position(nextPos) != SpriteType.WALL and next_pos[0] != ghost_pos[0] and next_pos[0] != ghost_pos[0]:
                valid_neighbors.append((next_pos[0], next_pos[1]))

        return valid_neighbors

    def move(self):
        direction = Direction.NONE


        if not globals.pill.isActive():
            path = self.a_star_search(self.position, globals.pill.position)
            print(path)


            if len(path) >= 1:
                next_pos = path[0]

                print("current: ", self.position.x, self.position.y)
                print("pill: ", globals.pill.position.x, globals.pill.position.y)
                print("next: ", next_pos)

                if next_pos[0] > self.position.x:
                    direction = direction | Direction.RIGHT
                if next_pos[0] < self.position.x:
                    direction = direction | Direction.LEFT

                if next_pos[1] > self.position.y:
                    direction = direction | Direction.DOWN
                if next_pos[1] < self.position.y:
                    direction = direction | Direction.UP


            return direction
        else:
            print("aasdasd")