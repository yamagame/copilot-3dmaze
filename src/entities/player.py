import math

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def move(self, maze, speed):
        new_x = self.x + math.cos(self.angle) * speed
        new_y = self.y + math.sin(self.angle) * speed

        if maze[int(new_y)][int(self.x)] == 0:
            self.y = new_y
        if maze[int(self.y)][int(new_x)] == 0:
            self.x = new_x