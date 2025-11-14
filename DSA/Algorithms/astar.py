# Algorithms/astar.py
from heapq import heappush, heappop
import itertools

def astar(grid):
    start = grid.get_cell(*grid.start)
    end = grid.get_cell(*grid.end)

    came_from = {start: None}
    g_score = {start: 0}
    visited = set()

    open_set = []
    counter = itertools.count()  # tie-breaker
    heappush(open_set, (0, next(counter), start))  

    def heuristic(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y) 

    while open_set:
        _, _, current = heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        
        current.explored = True
        yield (current.x, current.y)

        if current == end:
            break

        for neighbor in grid.get_neighbors(current.x, current.y):
            if neighbor.blocked or neighbor in visited:
                continue
            tentative_g = g_score[current] + neighbor.cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, end)
                heappush(open_set, (f_score, next(counter), neighbor))

    path = []
    cur = end
    while cur in came_from and cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path
