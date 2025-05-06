import pyxel

class GameState:
    def __init__(self, game):
        self.game = game

    def update(self):
        self.game.update_player()
        self.game.update_monsters()
        self.game.check_collisions()

    def draw(self):
        self.game.draw_maze()
        self.game.draw_entities()