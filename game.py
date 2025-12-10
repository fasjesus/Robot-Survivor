from pygame import Rect
from pgzero.actor import Actor

# --- CONSTANTS ---
WIDTH = 770
HEIGHT = 640
TILE_SIZE = 64
TITLE = "Robot Survivor"

# --- GLOBAL VARIABLES ---
game_state = "menu" 
sound_enabled = True

# --- ASSETS CONFIGURATION ---
PLAYER_WALK = ['character_robot_walk0', 'character_robot_walk1']
PLAYER_IDLE = ['character_robot_idle', 'character_robot_walk0'] 

ENEMY_WALK = ['character_zombie_walk0', 'character_zombie_walk1']
ENEMY_IDLE = ['character_zombie_idle', 'character_zombie_walk0']

# Map Dictionary
ASSETS_MAP = {
    "W": "block_06",    # Wall
    "P": "player",      # Player Spawn
    ".": "ground_01",   # Floor
    "X": "ground_02"    # Exit/Goal
}

# Level Design (13x10 grid)
MAP_LAYOUT = [
    "WWWWWWWWWWWW",
    "W..........W",
    "W..P.......W",
    "W...WW.....W",
    "W..........W",
    "W......E...W",
    "W..E.......W",
    "W..........W",
    "W.......X..W",
    "WWWWWWWWWWWW"
]

# --- CLASSES ---
class GameSprite(Actor):

    def __init__(self, img_idle, img_walk, grid_x, grid_y):
        super().__init__(img_idle[0])
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos = (grid_x * TILE_SIZE + 32, grid_y * TILE_SIZE + 32)
        
        self.target_x = self.x
        self.target_y = self.y
        self.is_moving = False
        self.speed = 4
        
        self.anim_idle = img_idle
        self.anim_walk = img_walk
        self.anim_timer = 0
        self.frame_index = 0

    def animate(self):
        self.anim_timer += 1
        
        if self.is_moving:
            frames = self.anim_walk
            delay = 5 
        else:
            frames = self.anim_idle
            delay = 20
            
        if self.anim_timer > delay:
            self.anim_timer = 0
            self.frame_index += 1
            
        if self.frame_index >= len(frames):
            self.frame_index = 0
            
        self.image = frames[self.frame_index]

    def update_smooth_movement(self):
        if not self.is_moving:
            return

        if self.x < self.target_x:
            self.x += self.speed
        elif self.x > self.target_x:
            self.x -= self.speed

        if self.y < self.target_y:
            self.y += self.speed
        elif self.y > self.target_y:
            self.y -= self.speed

        dist_x = abs(self.x - self.target_x)
        dist_y = abs(self.y - self.target_y)
        
        if dist_x < self.speed and dist_y < self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False

class Player(GameSprite):

    def attempt_move(self, dx, dy, walls):
        if self.is_moving:
            return False
            
        target_gx = self.grid_x + dx
        target_gy = self.grid_y + dy
        
        if (target_gx, target_gy) not in walls:
            self.grid_x = target_gx
            self.grid_y = target_gy
            self.target_x = self.grid_x * TILE_SIZE + 32
            self.target_y = self.grid_y * TILE_SIZE + 32
            self.is_moving = True
            
            if sound_enabled:
                try: sounds.hit.play()
                except: pass
            return True
        return False

class Enemy(GameSprite):

    def __init__(self, img_idle, img_walk, grid_x, grid_y):
        super().__init__(img_idle, img_walk, grid_x, grid_y)
        self.move_counter = 0

    def ai_turn(self, player_target, walls):
        if self.is_moving:
            return

        self.move_counter += 1
        
        if self.move_counter % 2 != 0:
            return
        dx = 0
        dy = 0
        
        if self.grid_x < player_target.grid_x: dx = 1
        elif self.grid_x > player_target.grid_x: dx = -1
        
        if self.grid_y < player_target.grid_y: dy = 1
        elif self.grid_y > player_target.grid_y: dy = -1

        moved = False

        if dx != 0:
            if (self.grid_x + dx, self.grid_y) not in walls:
                self.grid_x += dx
                moved = True

        if not moved and dy != 0:
            if (self.grid_x, self.grid_y + dy) not in walls:
                self.grid_y += dy
                moved = True
                
        if moved:
            self.target_x = self.grid_x * TILE_SIZE + 32
            self.target_y = self.grid_y * TILE_SIZE + 32
            self.is_moving = True

# --- GAME SETUP ---

walls = []
wall_actors = []
enemies = []
floor_tiles = []
player = None
exit_pos = None

btn_start_rect = Rect((WIDTH//2 - 100, 200), (200, 50))
btn_sound_rect = Rect((WIDTH//2 - 100, 300), (200, 50))
btn_exit_rect  = Rect((WIDTH//2 - 100, 400), (200, 50))

def setup_level():
    global player, exit_pos, walls, enemies, floor_tiles, wall_actors
    
    walls.clear()
    wall_actors.clear()
    enemies.clear()
    floor_tiles.clear()

    for row_idx, row_data in enumerate(MAP_LAYOUT):
        for col_idx, char in enumerate(row_data):
            x = col_idx * TILE_SIZE + 32
            y = row_idx * TILE_SIZE + 32
            
            floor_tiles.append(Actor(ASSETS_MAP["."], pos=(x, y)))
            
            if char == "W":
                walls.append((col_idx, row_idx))
                wall_actors.append(Actor(ASSETS_MAP["W"], pos=(x, y)))
            elif char == "P":
                player = Player(PLAYER_IDLE, PLAYER_WALK, col_idx, row_idx)
            elif char == "E":
                enemies.append(Enemy(ENEMY_IDLE, ENEMY_WALK, col_idx, row_idx))
            elif char == "X":
                exit_pos = (col_idx, row_idx)
                floor_tiles.append(Actor(ASSETS_MAP["X"], pos=(x, y)))

setup_level()

# --- PGZERO EVENTS ---

def update():
    global game_state
    
    # Music Control
    if sound_enabled and game_state in ["menu", "playing"]:
        music.set_volume(0.3)
        if not music.is_playing('music'): 
            music.play('music')
             
    else:
        music.stop()

    if game_state == "playing":
        player.animate()
        player.update_smooth_movement()

        # VICTORY CHECK
        if (player.grid_x, player.grid_y) == exit_pos:
            if sound_enabled:
                try: sounds.victory.play()
                except: pass
            game_state = "victory"

        for enemy in enemies:
            enemy.animate()
            enemy.update_smooth_movement()
            
            # GAME OVER CHECK
            if enemy.grid_x == player.grid_x and enemy.grid_y == player.grid_y:
                if sound_enabled:
                    try: sounds.gameover.play()
                    except: pass
                game_state = "game_over"

def draw():
    screen.clear()
    
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "game_over":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
        screen.draw.text("Press SPACE to Menu", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")
    elif game_state == "victory":
        screen.draw.text("YOU SURVIVED!", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="green")
        screen.draw.text("Press SPACE to Menu", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")

def draw_game():
    for tile in floor_tiles:
        tile.draw()
    for wall in wall_actors:
        wall.draw() 
    player.draw()
    for enemy in enemies:
        enemy.draw()

def draw_menu():
    screen.draw.text("ROBOT SURVIVOR", center=(WIDTH//2, 100), fontsize=60, color="cyan")
    
    screen.draw.filled_rect(btn_start_rect, "blue")
    screen.draw.text("START GAME", center=btn_start_rect.center, fontsize=30)
    
    color = "green" if sound_enabled else "red"
    text = "SOUND: ON" if sound_enabled else "SOUND: OFF"
    screen.draw.filled_rect(btn_sound_rect, color)
    screen.draw.text(text, center=btn_sound_rect.center, fontsize=30)
    
    screen.draw.filled_rect(btn_exit_rect, "gray")
    screen.draw.text("EXIT", center=btn_exit_rect.center, fontsize=30)

def on_mouse_down(pos):
    global game_state, sound_enabled
 
    if game_state == "menu":
        if btn_start_rect.collidepoint(pos):
            if sound_enabled:
                try: sounds.click.play()
                except: pass
            setup_level()
            game_state = "playing"
            
        elif btn_sound_rect.collidepoint(pos):
            if sound_enabled:
                try: sounds.click.play()
                except: pass
            sound_enabled = not sound_enabled
            
        elif btn_exit_rect.collidepoint(pos):
            if sound_enabled:
                try: sounds.click.play()
                except: pass
            try: quit()
            except: exit()

def on_key_down(key):
    global game_state
    
    if game_state in ["game_over", "victory"]:
        if key == keys.SPACE:
            game_state = "menu"
            
    elif game_state == "playing" and not player.is_moving:
        moved = False
        if key == keys.LEFT:  moved = player.attempt_move(-1, 0, walls)
        elif key == keys.RIGHT: moved = player.attempt_move(1, 0, walls)
        elif key == keys.UP:    moved = player.attempt_move(0, -1, walls)
        elif key == keys.DOWN:  moved = player.attempt_move(0, 1, walls)
        
        if moved:
            for enemy in enemies:
                enemy.ai_turn(player, walls)