import pyxel
from .title_state import TitleState

class ClearState:
    def __init__(self, game):
        self.game = game

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.game.state = TitleState(self.game)

    def draw(self):
        pyxel.cls(0)
        # Calculate the position to center the clear text (4 dots per character)
        clear_text = "CONGRATULATIONS!"
        reached_text = "YOU REACHED THE GOAL!"
        clear_x = (pyxel.width - len(clear_text) * pyxel.FONT_WIDTH) // 2
        reached_x = (pyxel.width - len(reached_text) * pyxel.FONT_WIDTH) // 2
        pyxel.text(clear_x, 120, clear_text, 10)
        pyxel.text(reached_x, 140, reached_text, 7)