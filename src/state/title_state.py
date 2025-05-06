import pyxel
from .game_state import GameState

class TitleState:
    def __init__(self, game):
        self.game = game

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game.reset_game()
            self.game.state = GameState(self.game)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(80, 100, "MAZE ADVENTURE", pyxel.frame_count % 16)
        pyxel.text(60, 140, "PRESS SPACE TO START", 7)