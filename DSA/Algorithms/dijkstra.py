from heapq import heappush, heappop
import itertools

def dijkstra(grid):
    start = grid.get_cell(*grid.start)
    end = grid.get_cell(*grid.end)

    came_from = {start: None}
    distances = {start: 0}
    visited = set()
    heap = []
    counter = itertools.count()  # tie-breaker

    heappush(heap, (0, next(counter), start))

    while heap:
        dist, _, current = heappop(heap)
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
            new_dist = dist + neighbor.cost
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                came_from[neighbor] = current
                heappush(heap, (new_dist, next(counter), neighbor))


    path = []
    cur = end
    while cur in came_from and cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path
