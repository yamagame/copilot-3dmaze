# title: Copilot Adventure
# author: yamagame
# desc: Sample pyxel shooting game with GitHub Copilot
# site: https://github.com/yamagame/copilot-adventure
# license: MIT
# version: 0.1
import pyxel
import math
import random
from state.title_state import TitleState
from state.game_state import GameState
from state.clear_state import ClearState
from state.gameover_state import GameOverState
from entities.monster import Monster
from entities.player import Player
from entities.trap import Trap
from entities.maze import Maze

class AdventureGame:
    def __init__(self):
        pyxel.init(256, 240, title="Copilot 3DMaze")
        pyxel.mouse(True)

        # Initialize sound data
        self._init_sounds()

        # Define 16 shades from white to blue in pyxel.colors
        self.wallcolor = [0x000000] * 16
        def shade(min, max, step):
            return int((min*(16-i) + max*i)/16)
        for i in range(16):
            self.wallcolor[i] = shade(0xff,0x00,i)*0x10000+shade(0xff,0x00,i)*0x100+0xFF
        old_colors = pyxel.colors.to_list()
        pyxel.colors.from_list(old_colors+self.wallcolor)
        self.reset_game()
        self.state = TitleState(self)
        self.current_stage = 1  # Track the current stage
        self.total_stages = 3  # Total number of stages updated to 3
        pyxel.run(self.update, self.draw)

    def _init_sounds(self):
        """Initialize sound effects"""
        # Sound 0: モンスター移動
        pyxel.sound(0).set(
            "c1e1g1c3",
            "p",
            "4444",
            "n",
            3
        )
        
        # Sound 1: Collision with trap
        pyxel.sound(1).set(
            "f2g2a2b2a2g2f2f2g2a2b2a2g2f2",
            "p",
            "44444444444444",
            "n",
            5
        )
        
        # Sound 2: Key acquisition
        pyxel.sound(2).set(
            "f3b4",
            "p",
            "44",
            "n",
            10
        )

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()


    def reset_game(self):
        self.maze = Maze(31, 31)  # Regenerate maze using Maze class
        self.goal_x = self.maze.width - 2
        self.goal_y = self.maze.height - 2
        self.player = Player(1.5, 1.5, math.pi / 2)
        self.monsters = [Monster(self.maze.width - 3, self.maze.height - 3),
                         Monster(self.maze.width - 5, self.maze.height - 3),
                         Monster(self.maze.width - 3, self.maze.height - 5)]
        self.traps = [Trap(x, y) for x, y in self.place_traps(10)]
        self.monster_move_timer = 0
        self.key = self.place_key()
        self.has_key = False
        self.ensure_player_start_position()
        self.mouse_dragging = False  # Track mouse dragging state
        self.last_mouse_x = pyxel.mouse_x
        self.last_mouse_y = pyxel.mouse_y

    def ensure_player_start_position(self):
        self.maze.set_empty(int(self.player.x), int(self.player.y))

    def place_traps(self, num_traps):
        traps = []
        empty_cells = self.maze.get_empty_cells()
        num_traps = min(num_traps, len(empty_cells))
        for _ in range(num_traps):
            if empty_cells:
                trap_pos = random.choice(empty_cells)
                traps.append(trap_pos)
                empty_cells.remove(trap_pos)
        return traps

    def place_key(self):
        empty_cells = self.maze.get_empty_cells()
        return random.choice(empty_cells) if empty_cells else (1, 1)

    def update_monsters(self):
        if self.monster_move_timer >= 90:  # Move monsters every 90 frames (1.5 seconds at 60 FPS)
            for monster in self.monsters:
                monster.move(self.maze.grid)
            self.monster_move_timer = 0  # Reset the timer
            pyxel.play(0, 0, loop=False)  # Simple sound for monster movement
        self.monster_move_timer += 1

    def check_collision(self):
        for monster in self.monsters:
            if monster.collides_with(self.player):
                self.state = GameOverState(self)
                return

    def check_key_collision(self):
        if not self.has_key and int(self.player.x) == self.key[0] and int(self.player.y) == self.key[1]:
            self.has_key = True
            pyxel.play(2,  2, loop=False)  # Sound for collecting the key

    def check_trap_collision(self):
        for trap in self.traps:
            if trap.collides_with(self.player):
                pyxel.play(1, 1, loop=False)  # Sound for trap collision
                return True
        return False

    def move_player(self, speed):
        old_x = self.player.x
        old_y = self.player.y
        new_x = self.player.x + math.cos(self.player.angle) * speed
        new_y = self.player.y + math.sin(self.player.angle) * speed

        if not self.maze.is_wall(int(self.player.x), int(new_y)):
            self.player.y = new_y
        elif self.maze.is_wall(int(self.player.x), int(new_y)):
            self.player.x += math.cos(self.player.angle) * speed * 0.1

        if not self.maze.is_wall(int(new_x), int(self.player.y)):
            self.player.x = new_x
        elif self.maze.is_wall(int(new_x), int(self.player.y)):
            self.player.y += math.sin(self.player.angle) * speed * 0.1

        if self.maze.is_wall(int(self.player.x), int(self.player.y)):
            self.player.x = old_x
            self.player.y = old_y

    def update_player(self):
        # Handle mouse dragging for rotation
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if not self.mouse_dragging:
                self.mouse_dragging = True
                self.last_mouse_x = pyxel.mouse_x
                self.last_mouse_y = pyxel.mouse_y
            else:
                dx = pyxel.mouse_x - self.last_mouse_x
                self.player.angle += dx * 0.02
                self.last_mouse_x = pyxel.mouse_x

        else:
            self.last_mouse_x = pyxel.mouse_x
            self.last_mouse_y = pyxel.mouse_y
            self.mouse_dragging = False

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player.move = pyxel.KEY_UP
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player.move = pyxel.KEY_DOWN
        # Handle forward/backward movement based on vertical mouse drag
        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            dy = pyxel.mouse_y - self.last_mouse_y
            if abs(dy) > 4:  # Check if vertical drag exceeds 4 pixels
                self.player.move = pyxel.KEY_UP if dy < 0 else pyxel.KEY_DOWN
            else:
                self.player.move = pyxel.KEY_UNKNOWN
        else:
            self.last_mouse_y = pyxel.mouse_y  # Reset vertical drag tracking when button is released
            self.player.move = pyxel.KEY_UNKNOWN

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player.angle -= 0.1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player.angle += 0.1
        if self.player.move == pyxel.KEY_UP:
            self.move_player(0.1)
        if self.player.move == pyxel.KEY_DOWN:
            self.move_player(-0.1)

    def check_collisions(self):
        self.check_collision()
        self.check_key_collision()
        if self.check_trap_collision():
            self.maze = Maze(31, 31)  # Regenerate maze using Maze class
            self.ensure_player_start_position()
            self.traps = [Trap(x, y) for x, y in self.place_traps(10)]
            self.key = self.place_key()
            self.has_key = False
        if self.has_key and int(self.player.x) == self.goal_x and int(self.player.y) == self.goal_y:
            if self.current_stage < self.total_stages:
                self.current_stage += 1
                self.reset_game()
            else:
                self.state = ClearState(self)

    def draw_maze(self):
        # Clear the screen and draw the floor
        pyxel.cls(0)
        for ray in range(0, pyxel.width, 2):
            floor = pyxel.height / 2
            pyxel.line(ray, floor, ray, pyxel.height, 3)  # Draw the floor in color 3

        # Draw the goal in the 3D maze only if the player has the key
        if self.has_key:
            for ray in range(0, pyxel.width, 2):
                ray_angle = self.player.angle - 0.5 + (ray / pyxel.width)
                distance_to_wall = 0
                is_goal = False

                eye_x = math.cos(ray_angle)
                eye_y = math.sin(ray_angle)

                while not is_goal and distance_to_wall < 30:
                    distance_to_wall += 0.1
                    test_x = int(self.player.x + eye_x * distance_to_wall)
                    test_y = int(self.player.y + eye_y * distance_to_wall)

                    if test_x == self.goal_x and test_y == self.goal_y:
                        is_goal = True

                ceiling = int(pyxel.height / 2 - pyxel.height / distance_to_wall)
                floor = pyxel.height - ceiling

                color = 8  # Red for the goal

                if is_goal:
                    pyxel.line(ray, 0, ray, floor, color)  # Draw the goal

        # Draw the walls in the 3D maze
        for ray in range(0, pyxel.width, 2):
            ray_angle = self.player.angle - 0.5 + (ray / pyxel.width)
            distance_to_wall = 0
            hit_wall = False
            is_goal = False

            eye_x = math.cos(ray_angle)
            eye_y = math.sin(ray_angle)

            while not hit_wall and distance_to_wall < 30:
                distance_to_wall += 0.1
                test_x = int(self.player.x + eye_x * distance_to_wall)
                test_y = int(self.player.y + eye_y * distance_to_wall)

                if test_x < 0 or test_x >= self.maze.width or test_y < 0 or test_y >= self.maze.height:
                    hit_wall = True
                    distance_to_wall = 10
                elif self.maze.is_wall(test_x, test_y):
                    hit_wall = True
                elif test_x == self.goal_x and test_y == self.goal_y:
                    is_goal = True
                    hit_wall = True

            ceiling = int(pyxel.height / 2 - pyxel.height / distance_to_wall)
            floor = pyxel.height - ceiling

            if is_goal:
                color = 8  # Red for the goal
            else:
                far = 5
                if distance_to_wall > far:
                    distance_to_wall = far
                color = 16 + int((distance_to_wall / far) * 16)  # Gradient for walls

            if is_goal:
                pass  # Goal is already drawn
            elif hit_wall:
                pyxel.line(ray, ceiling, ray, floor, color)  # Draw the wall

    def draw_entities(self):
        map_scale = 4  # Doubled the size of the 2D map
        player_x = int(self.player.x)
        player_y = int(self.player.y)

        # Draw a 10x10 area around the player
        for y in range(max(0, player_y - 5), min(self.maze.height, player_y + 5)):
            for x in range(max(0, player_x - 5), min(self.maze.width, player_x + 5)):
                color = 7 if self.maze.is_wall(x, y) else 0
                pyxel.rect((x - player_x + 5) * map_scale, (y - player_y + 5) * map_scale, map_scale, map_scale, color)

        # Draw player position in the center of the 10x10 map
        pyxel.circ(5 * map_scale, 5 * map_scale, map_scale, 11)

        # Draw the key if within the 10x10 area and not yet collected
        if not self.has_key and abs(self.key[0] - player_x) <= 5 and abs(self.key[1] - player_y) <= 5:
            pyxel.circ((self.key[0] - player_x + 5) * map_scale + map_scale // 2, (self.key[1] - player_y + 5) * map_scale + map_scale // 2, map_scale // 2, 14)  # Pink for the key

        # Draw the goal if within the 10x10 area and the player has the key
        if self.has_key and abs(self.goal_x - player_x) <= 5 and abs(self.goal_y - player_y) <= 5:
            pyxel.rect((self.goal_x - player_x + 5) * map_scale, (self.goal_y - player_y + 5) * map_scale, map_scale, map_scale, 8)

        # Draw monsters if within the 10x10 area
        for monster in self.monsters:
            if abs(monster.x - player_x) <= 5 and abs(monster.y - player_y) <= 5:
                pyxel.circ((monster.x - player_x + 5) * map_scale + map_scale // 2, (monster.y - player_y + 5) * map_scale + map_scale // 2, map_scale // 2, 8)  # Red for monsters

        # Draw traps if within the 10x10 area
        for trap in self.traps:
            if abs(trap.x - player_x) <= 5 and abs(trap.y - player_y) <= 5:
                pyxel.circ((trap.x - player_x + 5) * map_scale + map_scale // 2, (trap.y - player_y + 5) * map_scale + map_scale // 2, map_scale // 2, 10)  # Yellow for traps

        # Draw a border around the 2D map
        border_x = 5 * map_scale - map_scale // 2
        border_y = 5 * map_scale - map_scale // 2
        border_size = 10 * map_scale
        pyxel.rectb(border_x - border_size // 2+2, border_y - border_size // 2+2, border_size, border_size, 7)

        # Draw the key overlay in the bottom-right corner if the player has the key
        if self.has_key:
            key_overlay_x = pyxel.width - 16  # Adjust position for a 16x16 key icon
            key_overlay_y = pyxel.height - 16
            pyxel.rect(key_overlay_x, key_overlay_y, 16, 16, 14)  # Pink background for the key
            pyxel.text(key_overlay_x + 4, key_overlay_y + 4, "Key", 7)  # 'K' to represent the key

        # Display the current stage in the top-right corner
        stage_text = f"Stage: {self.current_stage}/{self.total_stages}"
        text_width = len(stage_text) * 4  # Approximate width of the text
        pyxel.text(pyxel.width - text_width - 5, 5, stage_text, 7)

AdventureGame()
