from collections import deque

def bfs(grid):
    start = grid.get_cell(*grid.start)
    end = grid.get_cell(*grid.end)

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        current.explored = True
        yield (current.x, current.y)

        if current == end:
            break

        for neighbor in grid.get_neighbors(current.x, current.y):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    path = []
    cur = end
    while cur in came_from and cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    
    return path
