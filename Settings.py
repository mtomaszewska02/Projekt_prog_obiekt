import pygame

# --- EKRAN ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "Infinite Jumper - Python"

# --- FIZYKA (Balanced) ---
GRAVITY = 0.85  # Média grawitacja (było 0.95 - za szybko, 0.8 - za wolno)
FRICTION = 0.08  # Więcej tarcia dla lepszej kontroli (było 0.06)
ACCELERATION = 0.5  # Wolniejsza akceleracja (było 1.2 - za szybko)
MAX_HORIZONTAL_SPEED = 8  # Ograniczona prędkość
JUMP_POWER = -17  # Silny skok ale nie przesadzony (było -18)
JUMP_SPEED_BONUS = 0.50  # Średni bonus z prędkości (było 0.75 - za duży)
JUMP_CUT_MULTIPLIER = 0.45  # Mocniejsze cięcie dla kontroli
LAVA_SPEED = 1.5  # Szybsza lawa = więcej presji
COYOTE_TIME = 170  # ms - więcej czasu na timing
JUMP_BUFFER = 170  # ms - większy bufor dla szybkiej gry

# --- SYSTEM WYNIKÓW ---
HS_FILE = "highscore.txt"

# --- GENEROWANIE POZIOMU ---
PLATFORM_GAP_Y = (40, 100)  # Min i max odległość pionowa między platformami (zwiększone dla wyższego ekranu)
PLATFORM_WIDTH_RANGE = (90, 150)  # Zmniejszone dla węższego ekranu (40-150)
MAX_PLATFORMS = 25          # Więcej platform dla wyższego ekranu

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

