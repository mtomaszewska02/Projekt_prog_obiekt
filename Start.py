import pygame
import math

# Inicjalizacja wszystkich modułów Pygame
pygame.init()

# Stałe gry
SCREEN_WIDTH = 400      # Szerokość okna gry
SCREEN_HEIGHT = 300     # Wysokość okna gry
GROUND_HEIGHT = 40      # Wysokość podłoża
PLAYER_SIZE = 40        # Rozmiar kwadratu (gracza)

# Kolory w formacie RGB
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Ustawienie okna gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Obiekt zegara do kontroli liczby klatek na sekundę
clock = pygame.time.Clock()

# Pozycja początkowa gracza (kwadratu) - środek ekranu, tuż nad podłożem
player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
player_base_y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_SIZE

# Parametry podskoku
AMPLITUDE = 60           # Maksymalna wysokość skoku (piksele)
FREQUENCY = 1.5          # Liczba skoków na sekundę

# Główna pętla gry
running = True
while running:
    # Obsługa zdarzeń (np. zamknięcie okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wypełnienie tła na biało
    screen.fill(WHITE)



    # Rysowanie podłoża (statyczny prostokąt na dole ekranu)
    ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(screen, GREEN, ground_rect)

    # Obliczanie pozycji Y gracza na podstawie funkcji sinusoidalnej
    # Dzięki temu kwadrat automatycznie podskakuje w górę i w dół w pętli
    czas = pygame.time.get_ticks() / 1000.0  # czas w sekundach od uruchomienia gry
    # Używamy wartości bezwzględnej, aby ruch był cykliczny (góra-dół)
    player_y = player_base_y - AMPLITUDE * abs(math.sin(FREQUENCY * math.pi * czas))

    # Zapewnienie, że kwadrat nie przejdzie przez podłoże
    if player_y > player_base_y:
        player_y = player_base_y

    # Rysowanie kwadratu gracza
    player_rect = pygame.Rect(player_x, int(player_y), PLAYER_SIZE, PLAYER_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Ograniczenie liczby klatek na sekundę do 60 (płynna animacja)
    clock.tick(120)

# Zakończenie działania Pygame
pygame.quit()