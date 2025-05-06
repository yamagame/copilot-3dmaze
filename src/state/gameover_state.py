import pyxel
from .title_state import TitleState

class GameOverState:
    def __init__(self, game):
        self.game = game

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.game.state = TitleState(self.game)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(100, 120, "GAME OVER", 8)
        pyxel.text(80, 140, "PRESS R TO RESTART", 7)