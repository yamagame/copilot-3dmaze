class Trap:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collides_with(self, player):
        return int(self.x) == int(player.x) and int(self.y) == int(player.y)