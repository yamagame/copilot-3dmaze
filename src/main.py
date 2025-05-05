# title: Copilot Adventure
# author: yamagame
# desc: Sample pyxel shooting game with GitHub Copilot
# site: https://github.com/yamagame/copilot-adventure
# license: MIT
# version: 0.1
import pyxel
import math
import random

class AdventureGame:
    def __init__(self):
        pyxel.init(256, 240, title="Maze Adventure")  # Adjust resolution
        pyxel.mouse(True)  # Enable mouse input
        self.maze_size_width = 31
        self.maze_size_height = 31
        self.trap_num = 10
        self.reset_game()
        self.state = "title"  # Add a state to manage title and game
        self.mouse_dragging = False  # Track mouse dragging state
        self.last_mouse_x = pyxel.mouse_x
        self.last_mouse_y = pyxel.mouse_y
        pyxel.run(self.update, self.draw)

    def generate_maze(self, width, height):
        # Initialize the maze with all walls
        maze = [[1 for x in range(width)] for y in range(height)]
        
        # Create a grid which is twice the size of the maze to handle passages between cells
        grid_width = (width - 1) // 2
        grid_height = (height - 1) // 2
        
        # Use depth-first search to generate a perfect maze (no loops or isolated areas)
        stack = [(1, 1)]
        visited = set()
        
        while stack:
            x, y = stack[-1]
            visited.add((x, y))
            maze[y][x] = 0  # Mark current cell as a passage
            
            # Get all neighbors that haven't been visited yet
            neighbors = []
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:  # Up, Right, Down, Left
                nx, ny = x + dx, y + dy
                if 0 < nx < width-1 and 0 < ny < height-1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny, x + dx//2, y + dy//2))
            
            if neighbors:
                # Choose a random neighbor
                nx, ny, wx, wy = random.choice(neighbors)
                # Remove the wall between the current cell and the chosen neighbor
                maze[wy][wx] = 0
                stack.append((nx, ny))
            else:
                # Backtrack
                stack.pop()
        
        # Ensure the start and goal positions are clear
        maze[1][1] = 0  # Start point
        maze[height - 2][height - 2] = 0  # End point
        
        # Remove some dead ends to create multiple paths
        for y in range(1, height-1):
            for x in range(1, width-1):
                if maze[y][x] == 0:
                    # Count walls around this cell
                    wall_count = 0
                    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        if maze[y+dy][x+dx] == 1:
                            wall_count += 1
                    
                    # If this is a dead end (2 walls around it), randomly open it
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
        self.maze = self.generate_maze(self.maze_size_width, self.maze_size_height)
        self.goal_x = len(self.maze[0]) - 2
        self.goal_y = len(self.maze) - 2
        self.player_x = 1.5
        self.player_y = 1.5
        self.player_angle = math.pi / 2  # Initialize player angle to face downward
        self.player_move = pyxel.KEY_UNKNOWN
        self.monsters = [(len(self.maze[0]) - 3, len(self.maze) - 3),(len(self.maze[0]) - 5, len(self.maze) - 3),(len(self.maze[0]) - 3, len(self.maze) - 5)]  # Initialize monster positions
        self.monster_move_timer = 0  # Timer to control monster movement
        self.traps = self.place_traps(self.trap_num)

    def place_traps(self, num_traps):
        # Place traps randomly in non-wall locations
        traps = []
        empty_cells = [(x, y) for y in range(1, len(self.maze) - 1) for x in range(1, len(self.maze[0]) - 1) if self.maze[y][x] == 0]
        num_traps = min(num_traps, len(empty_cells))  # Limit the number of traps
        for _ in range(num_traps):
            if empty_cells:
                trap_pos = random.choice(empty_cells)
                traps.append(trap_pos)
                empty_cells.remove(trap_pos)
        return traps

    def update_monsters(self):
        if self.monster_move_timer % 10 == 0:  # Move monsters every 10 frames
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
        self.monster_move_timer += 1

    def check_collision(self):
        for mx, my in self.monsters:
            if int(self.player_x) == mx and int(self.player_y) == my:
                self.state = "gameover"

    def check_trap_collision(self):
        for tx, ty in self.traps:
            if int(self.player_x) == tx and int(self.player_y) == ty:
                return True
        return False

    def update(self):
        if self.state == "title":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
                self.state = "game"
        elif self.state == "game":
            if pyxel.btnp(pyxel.KEY_R):
                self.maze = self.generate_maze(self.maze_size_width, self.maze_size_height)
                self.goal_x = len(self.maze[0]) - 2
                self.goal_y = len(self.maze) - 2

            # Handle mouse dragging for rotation
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if not self.mouse_dragging:
                    self.mouse_dragging = True
                    self.last_mouse_x = pyxel.mouse_x
                    self.last_mouse_y = pyxel.mouse_y
                else:
                    dx = pyxel.mouse_x - self.last_mouse_x
                    self.player_angle += dx * 0.02
                    self.last_mouse_x = pyxel.mouse_x

            else:
                self.mouse_dragging = False

            if pyxel.btn(pyxel.KEY_UP):
                self.player_move = pyxel.KEY_UP
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.player_move = pyxel.KEY_DOWN
            # Handle forward/backward movement based on vertical mouse drag
            elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                dy = pyxel.mouse_y - self.last_mouse_y
                if abs(dy) > 4:  # Check if vertical drag exceeds 4 pixels
                    self.player_move = pyxel.KEY_UP if dy < 0 else pyxel.KEY_DOWN
            else:
                self.last_mouse_y = pyxel.mouse_y  # Reset vertical drag tracking when button is released
                self.player_move = pyxel.KEY_UNKNOWN

            # Keyboard controls remain unchanged
            if pyxel.btn(pyxel.KEY_LEFT):
                self.player_angle -= 0.1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.player_angle += 0.1
            if self.player_move == pyxel.KEY_UP:
                new_x = self.player_x + math.cos(self.player_angle) * 0.1
                new_y = self.player_y + math.sin(self.player_angle) * 0.1
                if self.maze[int(new_y)][int(new_x)] == 0:
                    self.player_x = new_x
                    self.player_y = new_y
            if self.player_move == pyxel.KEY_DOWN:
                new_x = self.player_x - math.cos(self.player_angle) * 0.1
                new_y = self.player_y - math.sin(self.player_angle) * 0.1
                if self.maze[int(new_y)][int(new_x)] == 0:
                    self.player_x = new_x
                    self.player_y = new_y

            self.update_monsters()
            self.check_collision()
            if self.check_trap_collision():
                self.maze = self.generate_maze(self.maze_size_width, self.maze_size_height)  # Regenerate the maze
                self.traps = self.place_traps(self.trap_num)

            # Check if the player has reached the goal
            if int(self.player_x) == self.goal_x and int(self.player_y) == self.goal_y:
                self.state = "clear"
        elif self.state == "gameover":
            if pyxel.btnp(pyxel.KEY_R):
                self.state = "title"  # Return to title screen

    def draw(self):
        if self.state == "title":
            pyxel.cls(0)
            pyxel.text(80, 100, "MAZE ADVENTURE", pyxel.frame_count % 16)
            pyxel.text(60, 140, "PRESS SPACE TO START", 7)
        elif self.state == "game":
            pyxel.cls(0)
            for ray in range(pyxel.width):  # Cast rays based on new screen width
                ray_angle = self.player_angle - 0.5 + (ray / pyxel.width)
                distance_to_wall = 0
                hit_wall = False
                is_goal = False  # Track if the ray hits the goal

                eye_x = math.cos(ray_angle)
                eye_y = math.sin(ray_angle)

                while not hit_wall and distance_to_wall < 10:
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
                    color = 8  # Red for the goal
                else:
                    color = 7 if distance_to_wall < 2 else 6 if distance_to_wall < 4 else 5

                if hit_wall or is_goal:
                    # Draw wall or goal
                    pyxel.line(ray, ceiling, ray, floor, color)

                    # Draw wall outlines for better visibility
                    if ray > 0 and (distance_to_wall - 0.1) != 0:
                        prev_ceiling = int(pyxel.height / 2 - pyxel.height / (distance_to_wall - 0.1))
                        prev_floor = pyxel.height - prev_ceiling
                        pyxel.line(ray - 1, prev_ceiling, ray, ceiling, 0)  # Top outline
                        pyxel.line(ray - 1, prev_floor, ray, floor, 0)  # Bottom outline

                pyxel.line(ray, 0, ray, ceiling, 0)
                pyxel.line(ray, floor, ray, pyxel.height, 3)

            # Draw 2D map in the top-left corner, scaled to fit new resolution
            map_scale = 2  # Adjust scale for new resolution
            for y, row in enumerate(self.maze):
                for x, cell in enumerate(row):
                    color = 7 if cell == 1 else 0
                    pyxel.rect(x * map_scale, y * map_scale, map_scale, map_scale, color)

            # Draw player position on the scaled-up 2D map
            pyxel.circ(int(self.player_x * map_scale), int(self.player_y * map_scale), map_scale, 11)

            # Draw the goal as a red tower on the 2D map
            pyxel.rect(self.goal_x * map_scale, self.goal_y * map_scale, map_scale, map_scale, 8)

            # Draw monsters on the 2D map
            for mx, my in self.monsters:
                pyxel.circ(mx * map_scale + map_scale // 2, my * map_scale + map_scale // 2, map_scale // 2, 9)

            # Draw traps on the 2D map
            for tx, ty in self.traps:
                pyxel.circ(tx * map_scale + map_scale // 2, ty * map_scale + map_scale // 2, map_scale // 2, 12)  # Red color for traps
        elif self.state == "clear":
            pyxel.cls(0)
            pyxel.text(100, 120, "CONGRATULATIONS!", 10)
            pyxel.text(80, 140, "YOU REACHED THE GOAL!", 7)
            if pyxel.btnp(pyxel.KEY_R):
                self.state = "title"  # Return to title screen
        elif self.state == "gameover":
            pyxel.cls(0)
            pyxel.text(100, 120, "GAME OVER", 8)
            pyxel.text(80, 140, "PRESS R TO RESTART", 7)
            if pyxel.btnp(pyxel.KEY_R):
                self.state = "title"  # Return to title screen

AdventureGame()
