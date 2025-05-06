import random

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, maze):
        possible_moves = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if maze[ny][nx] == 0:
                possible_moves.append((nx, ny))
        if possible_moves:
            self.x, self.y = random.choice(possible_moves)

    def collides_with(self, player):
        return int(self.x) == int(player.x) and int(self.y) == int(player.y)