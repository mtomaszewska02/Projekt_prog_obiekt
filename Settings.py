import pygame

# --- EKRAN ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Infinite Jumper - Python"

# --- FIZYKA ---
GRAVITY = 0.8
FRICTION = -0.12
ACCELERATION = 0.5
JUMP_POWER = -16
LAVA_SPEED = 1.5  # Prędkość podnoszenia się podłoża

# --- GENEROWANIE POZIOMU ---
PLATFORM_GAP_Y = (20, 70)  # Min i max odległość pionowa między platformami
PLATFORM_WIDTH_RANGE = (80, 200)
MAX_PLATFORMS = 17          # Ile platform naraz na ekranie

# --- KOLORY ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
SKY_BLUE = (135, 206, 235)
LAVA_COLOR = (255, 69, 0)

# --- KONFIGURACJA WYGLĄDU GRACZA (Point 7 & Customization) ---
# Ścieżki do grafik
BG_IMAGE_PATH = "grafika/background.png"
PLATFORM_IMAGE_PATH = "grafika/platform.png"

# Zmień konfigurację gracza na:
PLAYER_SKIN = {
    "width": 32,
    "height": 48,
    "color_idle": (0,0,0), # Te kolory są teraz ignorowane, bo jest obrazek
    "color_run": (0,0,0),
    "color_jump": (0,0,0),
    "image_path": "grafika/hero.png"} # Ścieżka do pliku wygenerowanego skryptem

# Funkcja pomocnicza do generowania tekstur (nie musisz jej zmieniać)
def create_texture(width, height, color, char_sign=""):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    pygame.draw.rect(surf, (255,255,255), (width-10, 5, 5, 5)) # Oczy
    return surf
#doaivsdv