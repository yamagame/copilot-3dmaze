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

        # Draw a big red monster face
        face_width = screen_width * 0.8
        face_height = screen_height * 0.7
        face_x = (screen_width - face_width) // 2
        face_y = (screen_height - face_height) // 2

        # Monster body (red rectangle)
        pyxel.rect(0, 0, screen_width, screen_height, 8)

        # Eyes
        eye_width = face_width * 0.2
        eye_height = face_height * 0.15
        left_eye_x = face_x + face_width * 0.25 - eye_width / 2
        right_eye_x = face_x + face_width * 0.75 - eye_width / 2
        eyes_y = face_y + face_height * 0.3
        pyxel.rect(left_eye_x, eyes_y, eye_width, eye_height, 0)  # Left eye
        pyxel.rect(right_eye_x, eyes_y, eye_width, eye_height, 0)  # Right eye

        # Angry eyebrows
        eyebrow_width = eye_width * 1.5
        eyebrow_height = eye_height * 0.4
        pyxel.rect(left_eye_x - eyebrow_width * 0.25, eyes_y - eyebrow_height * 1.5, eyebrow_width, eyebrow_height, 0)
        pyxel.rect(right_eye_x - eyebrow_width * 0.25, eyes_y - eyebrow_height * 1.5, eyebrow_width, eyebrow_height, 0)

        # Mouth
        mouth_width = face_width * 0.6
        mouth_height = face_height * 0.1
        mouth_x = face_x + (face_width - mouth_width) / 2
        mouth_y = face_y + face_height * 0.7
        pyxel.rect(mouth_x, mouth_y, mouth_width, mouth_height, 0)

        # Teeth
        teeth_count = 4
        teeth_width = mouth_width / (teeth_count * 2)
        for i in range(teeth_count):
            tooth_x = mouth_x + i * teeth_width * 2
            pyxel.rect(tooth_x, mouth_y, teeth_width, mouth_height // 2, 7)

        pyxel.text(text_game_over_x, text_game_over_y, text_game_over, 7)
        pyxel.text(text_restart_x, text_restart_y, text_restart, 7)
