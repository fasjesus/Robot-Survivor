import random
import math
from pgzero.actor import Actor

# --- CONFIGURATION ---
WIDTH = 1000
HEIGHT = 700
TITLE = "Space Survivor"

# --- GLOBAL VARIABLES ---
game_state = "menu"
is_sound_on = True
score = 0
frame_counter = 0

# --- CLASSES ---
class Player(Actor):

    def __init__(self):
        super().__init__('player_idle', pos=(WIDTH // 2, HEIGHT // 2))
        self.speed = 4
        self.is_moving = False
        self.anim_frame = 1

    def move_player(self):
        self.is_moving = False
        
        # Movement controls
        if keyboard.left or keyboard.a:
            self.x -= self.speed
            self.is_moving = True
        if keyboard.right or keyboard.d:
            self.x += self.speed
            self.is_moving = True
        if keyboard.up or keyboard.w:
            self.y -= self.speed
            self.is_moving = True
        if keyboard.down or keyboard.s:
            self.y += self.speed
            self.is_moving = True

        # Screen boundaries
        self.x = max(20, min(WIDTH - 20, self.x))
        self.y = max(20, min(HEIGHT - 20, self.y))

    def animate(self):
        # Sprite animation logic
        if self.is_moving:
            self.anim_frame += 0.2
            if self.anim_frame >= 3:
                self.anim_frame = 1
            self.image = f"player_run{int(self.anim_frame)}"
        else:
            self.image = "player_idle"

    def update(self):
        self.move_player()
        self.animate()

class Threat(Actor): 

    def __init__(self):
        x = random.choice([-50, WIDTH + 50])
        y = random.randint(0, HEIGHT)
        
        super().__init__('threat', pos=(x, y)) 
        self.speed = 2 + (score * 0.1)

    def chase(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

# --- SETUP ---
player = Player()
threats = []  

# Menu Buttons
btn_start = Actor('btn_start', pos=(WIDTH//2, 250))
btn_sound = Actor('btn_sound', pos=(WIDTH//2, 350))
btn_exit = Actor('btn_exit', pos=(WIDTH//2, 450))

# --- PGZERO FUNCTIONS ---
def draw():

    screen.clear()
    
    if game_state == "menu":
        screen.draw.text("SPACE SURVIVOR", center=(WIDTH//2, 150), fontsize=60, color="white")
        btn_start.draw()
        btn_sound.draw()
        btn_exit.draw()
        
        status = "ON" if is_sound_on else "OFF"
        screen.draw.text(f"Sound: {status}", center=(WIDTH//2, 390), fontsize=20, color="yellow")

    elif game_state == "playing":
        player.draw()
    
        for threat in threats:
            threat.draw()
        screen.draw.text(f"Score: {int(score)}", (10, 10), fontsize=30, color="white")

    elif game_state == "game_over":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
        screen.draw.text(f"Final Score: {int(score)}", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=40, color="white")
        screen.draw.text("Click to Return to Menu", center=(WIDTH//2, HEIGHT//2 + 120), fontsize=25, color="gray")

def update():

    global game_state, score, frame_counter

    # Music 
    if is_sound_on:
        try:
            if not music.is_playing('music'):
                music.play('music')
        except:
            pass
    else:
        music.stop()

    if game_state == "playing":
        player.update()
        score += 0.05
        
        frame_counter += 1
        if frame_counter > 60:
            threats.append(Threat())  
            frame_counter = 0

        for threat in threats:
            threat.chase(player)
            if threat.colliderect(player):
                if is_sound_on:
                    try:
                        sounds.hit.play()
                    except:
                        pass
                game_state = "game_over"

def on_mouse_down(pos):

    global game_state, is_sound_on, threats, score, player

    if game_state == "menu":
        if btn_start.collidepoint(pos):
            player.pos = (WIDTH//2, HEIGHT//2)
            threats = []  
            score = 0
            game_state = "playing"
        
        elif btn_sound.collidepoint(pos):
            is_sound_on = not is_sound_on
            
        elif btn_exit.collidepoint(pos):
            quit()

    elif game_state == "game_over":
        game_state = "menu"