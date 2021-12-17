from Node import Node


class Maze:
    def __init__(self, size):
        self.explored = []
        self.size = size
        self.isInitialized = True
        self.start = None
        self.goal = None
        self.walls = None
        self.currentState = None
        self.frontier = None
        self.initial_node = None

    def init(self, start, goal, walls, frontier):
        self.start = start
        self.goal = goal
        self.walls = walls
        self.currentState = self.start
        self.frontier = frontier
        self.initial_node = Node(pos=self.start, parent=None, level=None, cost=0)
        starting_nodes = self.neighbours(self.initial_node)
        for node in starting_nodes:
            self.frontier.add(node)

    def restart(self):
        self.isInitialized = False
        self.explored = []

    def calculateNodeLevel(self, pos, parent):
        goal_distance = 0
        goal_distance += abs(pos[0] - self.goal[0])
        goal_distance += abs(pos[1] - self.goal[1])

        return goal_distance + parent.cost + 1

    def solve(self):  # return the state (done or searching) and all the positions of :
        # (if searching) -> the positions explored
        # (if done) -> the shortest path to the goal

        state = "searching"  # or done
        solution = []

        if self.frontier.isEmpty():
            raise Exception("No solution!")
        else:
            if self.frontier.contains(self.goal):
                node = self.frontier.contains(self.goal)
                self.frontier.frontier.remove(self.goal)
            else:
                node = self.frontier.remove()

            if node.pos == self.goal:
                state = "done"
                while node.parent:
                    solution.append(node.pos)
                    node = node.parent
            else:
                self.explored.append(node.pos)
                neighbours = self.neighbours(node)
                for neighbour in neighbours:
                    self.frontier.add(neighbour)

        if not solution == []:
            solution.remove(self.goal)
        return state, self.explored, solution

    def neighbours(self, node):
        row, column = node.pos
        possible_neighbours = [
            [row + 1, column],
            [row - 1, column],
            [row, column + 1],
            [row, column - 1]
        ]
        neighbours = []
        for neighbour in possible_neighbours:
            is_in_frontier = False
            for frontier_node in self.frontier.frontier:
                if frontier_node.pos == neighbour:
                    is_in_frontier = True
            if 0 < neighbour[0] <= self.size and 0 < neighbour[1] <= self.size and \
                    neighbour not in self.explored and neighbour not in self.walls and \
                    not neighbour == self.initial_node.pos and not is_in_frontier:
                level = self.calculateNodeLevel(neighbour, node)
                neighbours.append(Node(pos=neighbour, parent=node, level=level, cost=(node.cost+1)))

        return neighbours
