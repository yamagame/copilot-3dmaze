import random

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self._generate_maze()

    def _generate_maze(self):
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        stack = [(1, 1)]
        visited = set()

        while stack:
            x, y = stack[-1]
            visited.add((x, y))
            maze[y][x] = 0

            neighbors = []
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width-1 and 0 < ny < self.height-1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny, x + dx//2, y + dy//2))

            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                maze[wy][wx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        maze[1][1] = 0
        maze[self.height - 2][self.width - 2] = 0

        wall_count = random.randint(3,5)

        # Randomly set some walls to empty spaces
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if maze[y][x] == 1:
                    if random.randint(0,6) < wall_count:
                        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                        random.shuffle(directions)
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 < nx < self.width-1 and 0 < ny < self.height-1 and maze[ny][nx] == 1:
                                maze[ny][nx] = 0
                                break

        return maze

    def is_wall(self, x, y):
        return self.grid[y][x] == 1

    def set_empty(self, x, y):
        self.grid[y][x] = 0

    def get_empty_cells(self):
        return [(x, y) for y in range(1, self.height - 1) for x in range(1, self.width - 1) if self.grid[y][x] == 0]