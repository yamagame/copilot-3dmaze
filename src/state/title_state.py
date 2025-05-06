import pyxel
from .game_state import GameState

class TitleState:
    def __init__(self, game):
        self.game = game

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.game.reset_game()
            self.game.state = GameState(self.game)

    def draw(self):
        pyxel.cls(0)
        title_text = "Copilot 3D Maze"
        press_text = "PRESS SPACE TO START"
        title_x = (pyxel.width - len(title_text) * pyxel.FONT_WIDTH) // 2
        press_x = (pyxel.width - len(press_text) * pyxel.FONT_WIDTH) // 2
        pyxel.text(title_x, 100, title_text, pyxel.frame_count % 16)
        pyxel.text(press_x, 140, press_text, 7)