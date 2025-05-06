import pyxel
from .title_state import TitleState

class GameOverState:
    def __init__(self, game):
        self.game = game

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.game.state = TitleState(self.game)

    def draw(self):
        pyxel.cls(0)
        screen_width = pyxel.width
        screen_height = pyxel.height
        text_game_over = "GAME OVER"
        text_restart = "PRESS SPACE TO RESTART"

        text_game_over_x = (screen_width - len(text_game_over) * pyxel.FONT_WIDTH) // 2
        text_game_over_y = screen_height // 2 - pyxel.FONT_HEIGHT
        text_restart_x = (screen_width - len(text_restart) * pyxel.FONT_WIDTH) // 2
        text_restart_y = screen_height // 2 + pyxel.FONT_HEIGHT

        pyxel.text(text_game_over_x, text_game_over_y, text_game_over, 8)
        pyxel.text(text_restart_x, text_restart_y, text_restart, 7)
