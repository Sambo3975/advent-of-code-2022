"""Based on https://www.redblobgames.com/pathfinding/a-star/implementation.html but with some changes and
simplifications """

from numpy import array
from heapq import heappush, heappop
import load_file


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item: any, priority: int):
        heappush(self.elements, (priority, item))

    def peek(self):
        return self.elements[0][1]

    def pop(self) -> any:
        return heappop(self.elements)[1]

    def empty(self) -> bool:
        return not self.elements


GridLocation = tuple[int, int]


class WeightedGrid:
    def __init__(self, weights):
        self.weights = array(weights)
        self.rows = len(weights)
        self.cols = len(weights[0])

    @classmethod
    def from_file(cls, file_name):
        return cls(load_file.as_digit_grid(file_name))

    def in_bounds(self, location: GridLocation):
        (i, j) = location
        return 0 <= i < self.rows and 0 <= j < self.cols

    def neighbors(self, location: GridLocation):
        (i, j) = location
        neighbors = [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]
        return filter(self.in_bounds, neighbors)


def dijkstra_search(grid: WeightedGrid, start: GridLocation = (0, 0), goal: GridLocation = None):
    if goal is None:
        goal = (grid.rows - 1, grid.cols - 1)
    frontier = PriorityQueue()
    came_from: dict[GridLocation, GridLocation | None] = {}
    cost_so_far: dict[GridLocation, int] = {}
    frontier.push(start, 0)
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: GridLocation = frontier.pop()
        if current == goal:
            break
        for next_ in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.weights[next_]
            if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                cost_so_far[next_] = new_cost
                frontier.push(next_, new_cost)
                came_from[next_] = current

    return came_from, cost_so_far[goal]
