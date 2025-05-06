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

class AdventureGame:
    def __init__(self):
        pyxel.init(256, 240, title="Maze Adventure")
        pyxel.mouse(True)
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
        pyxel.run(self.update, self.draw)

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()

    def generate_maze(self, width, height):
        maze = [[1 for x in range(width)] for y in range(height)]
        grid_width = (width - 1) // 2
        grid_height = (height - 1) // 2
        stack = [(1, 1)]
        visited = set()

        while stack:
            x, y = stack[-1]
            visited.add((x, y))
            maze[y][x] = 0

            neighbors = []
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < width-1 and 0 < ny < height-1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny, x + dx//2, y + dy//2))

            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                maze[wy][wx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        maze[1][1] = 0
        maze[height - 2][height - 2] = 0

        for y in range(1, height-1):
            for x in range(1, width-1):
                if maze[y][x] == 0:
                    wall_count = 0
                    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        if maze[y+dy][x+dx] == 1:
                            wall_count += 1

                    if wall_count == 2 and random.random() < 0.5:
                        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                        random.shuffle(directions)
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 < nx < width-1 and 0 < ny < height-1 and maze[ny][nx] == 1:
                                maze[ny][nx] = 0
                                break

        return maze

    def reset_game(self):
        self.maze = self.generate_maze(31, 31)
        self.goal_x = len(self.maze[0]) - 2
        self.goal_y = len(self.maze) - 2
        self.player_x = 1.5
        self.player_y = 1.5
        self.player_angle = math.pi / 2
        self.player_move = pyxel.KEY_UNKNOWN
        self.monsters = [(len(self.maze[0]) - 3, len(self.maze) - 3), (len(self.maze[0]) - 5, len(self.maze) - 3), (len(self.maze[0]) - 3, len(self.maze) - 5)]
        self.monster_move_timer = 0  # Timer to control monster movement
        self.traps = self.place_traps(10)

    def place_traps(self, num_traps):
        traps = []
        empty_cells = [(x, y) for y in range(1, len(self.maze) - 1) for x in range(1, len(self.maze[0]) - 1) if self.maze[y][x] == 0]
        num_traps = min(num_traps, len(empty_cells))
        for _ in range(num_traps):
            if empty_cells:
                trap_pos = random.choice(empty_cells)
                traps.append(trap_pos)
                empty_cells.remove(trap_pos)
        return traps

    def update_monsters(self):
        if self.monster_move_timer >= 90:  # Move monsters every 90 frames (1.5 seconds at 60 FPS)
            new_monsters = []
            for mx, my in self.monsters:
                possible_moves = []
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                    nx, ny = mx + dx, my + dy
                    if self.maze[ny][nx] == 0:  # Check if the space is open
                        possible_moves.append((nx, ny))
                if possible_moves:
                    new_monsters.append(random.choice(possible_moves))  # Choose a random valid move
                else:
                    new_monsters.append((mx, my))  # Stay in place if no move is possible
            self.monsters = new_monsters
            self.monster_move_timer = 0  # Reset the timer
        self.monster_move_timer += 1

    def check_collision(self):
        for mx, my in self.monsters:
            if int(self.player_x) == mx and int(self.player_y) == my:
                self.state = GameOverState(self)

    def check_trap_collision(self):
        for tx, ty in self.traps:
            if int(self.player_x) == tx and int(self.player_y) == ty:
                return True
        return False

    def move_player(self, speed):
        old_x = self.player_x
        old_y = self.player_y
        new_x = self.player_x + math.cos(self.player_angle) * speed
        new_y = self.player_y + math.sin(self.player_angle) * speed

        if self.maze[int(new_y)][int(self.player_x)] == 0:
            self.player_y = new_y
        elif self.maze[int(new_y)][int(self.player_x)] == 1:
            self.player_x += math.cos(self.player_angle) * speed * 0.1  # Slide along the wall

        if self.maze[int(self.player_y)][int(new_x)] == 0:
            self.player_x = new_x
        elif self.maze[int(self.player_y)][int(new_x)] == 1:
            self.player_y += math.sin(self.player_angle) * speed * 0.1  # Slide along the wall

        # After sliding, if the player is still inside a wall, reset the player's position
        if self.maze[int(self.player_y)][int(self.player_x)] == 1:
            self.player_x = old_x
            self.player_y = old_y

    def update_player(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player_move = pyxel.KEY_UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player_move = pyxel.KEY_DOWN
        else:
            self.player_move = pyxel.KEY_UNKNOWN

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_angle -= 0.1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_angle += 0.1
        if self.player_move == pyxel.KEY_UP:
            self.move_player(0.1)
        if self.player_move == pyxel.KEY_DOWN:
            self.move_player(-0.1)

    def check_collisions(self):
        self.check_collision()
        if self.check_trap_collision():
            self.maze = self.generate_maze(31, 31)
            self.traps = self.place_traps(10)
        if int(self.player_x) == self.goal_x and int(self.player_y) == self.goal_y:
            self.state = ClearState(self)

    def draw_maze(self):
        pyxel.cls(0)
        for ray in range(0, pyxel.width, 2):
            floor = pyxel.height/2
            pyxel.line(ray, floor, ray, pyxel.height, 3)

        for ray in range(0, pyxel.width, 2):
            ray_angle = self.player_angle - 0.5 + (ray / pyxel.width)
            distance_to_wall = 0
            is_goal = False

            eye_x = math.cos(ray_angle)
            eye_y = math.sin(ray_angle)

            while not is_goal and distance_to_wall < 30:
                distance_to_wall += 0.1
                test_x = int(self.player_x + eye_x * distance_to_wall)
                test_y = int(self.player_y + eye_y * distance_to_wall)

                if test_x == self.goal_x and test_y == self.goal_y:
                    is_goal = True

            ceiling = int(pyxel.height / 2 - pyxel.height / distance_to_wall)
            floor = pyxel.height - ceiling

            color = 8

            if is_goal:
                pyxel.line(ray, 0, ray, floor, color)

        for ray in range(0, pyxel.width, 2):
            ray_angle = self.player_angle - 0.5 + (ray / pyxel.width)
            distance_to_wall = 0
            hit_wall = False
            is_goal = False

            eye_x = math.cos(ray_angle)
            eye_y = math.sin(ray_angle)

            while not hit_wall and distance_to_wall < 30:
                distance_to_wall += 0.1
                test_x = int(self.player_x + eye_x * distance_to_wall)
                test_y = int(self.player_y + eye_y * distance_to_wall)

                if test_x < 0 or test_x >= len(self.maze[0]) or test_y < 0 or test_y >= len(self.maze):
                    hit_wall = True
                    distance_to_wall = 10
                elif self.maze[test_y][test_x] == 1:
                    hit_wall = True
                elif test_x == self.goal_x and test_y == self.goal_y:
                    is_goal = True
                    hit_wall = True

            ceiling = int(pyxel.height / 2 - pyxel.height / distance_to_wall)
            floor = pyxel.height - ceiling

            if is_goal:
                color = 8
            else:
                far = 5
                if distance_to_wall > far:
                    distance_to_wall = far
                color = 16+int((distance_to_wall/far)*16)

            if is_goal:
                pass
            elif hit_wall:
                pyxel.line(ray, ceiling, ray, floor, color)

    def draw_entities(self):
        map_scale = 2
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = 7 if cell == 1 else 0
                pyxel.rect(x * map_scale, y * map_scale, map_scale, map_scale, color)

        pyxel.circ(int(self.player_x * map_scale), int(self.player_y * map_scale), map_scale, 11)
        pyxel.rect(self.goal_x * map_scale, self.goal_y * map_scale, map_scale, map_scale, 8)

        for mx, my in self.monsters:
            pyxel.circ(mx * map_scale + map_scale // 2, my * map_scale + map_scale // 2, map_scale // 2, 9)

        for tx, ty in self.traps:
            pyxel.circ(tx * map_scale + map_scale // 2, ty * map_scale + map_scale // 2, map_scale // 2, 12)

AdventureGame()
