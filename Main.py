import pygame
import sys
import random
from Settings import *
from Player import Player
from World_objects import Platform, Lava


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.highscore = 0

        try:
            bg_img = pygame.image.load(BG_IMAGE_PATH).convert()
            # Skaluj tło do rozmiaru ekranu
            self.background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Brak tła, używam koloru.")
            self.background = None  # Fallback
        self.load_data()
        self.new_game()

    def load_data(self):
        try:
            with open(HS_FILE, 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
    def new_game(self):
        # Grupy spritów
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.danger_zone = pygame.sprite.Group()

        # Tworzenie obiektów
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Lawa
        self.lava = Lava()
        self.danger_zone.add(self.lava)
        self.all_sprites.add(self.lava)

        # Platforma startowa
        p1 = Platform(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - 60)
        self.all_sprites.add(p1)
        self.platforms.add(p1)

        self.score = 0

    def check_ground(self):
        # Sprawdza czy gracz stoi na ziemi
        if self.player.vel.y >= 0:  # ZMIENIONE: >= zamiast > (obejmuje też vel.y = 0)
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0
                    self.player.last_ground_time = pygame.time.get_ticks()
                    return True
        return False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                # Zmniejsz wysokość skoku gdy gracz puści przycisk (lepsze czucie)
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.jump_cut()

    def update(self):
        self.all_sprites.update()

        # 1. KOLIZJE Z PLATFORMAMI
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.pos.y < hits[0].rect.bottom:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0

        # 2. KOLIZJE ZE ŚCIANAMI (Boki platform) - uproszczone
        # W tym trybie gry (jumping up) kolizje boczne są mniej ważne niż w puzzle platformerach,
        # ale są obsługiwane przez logikę Wall Jump w player.py

        # 3. KAMERA (PRZESUWANIE EKRANU W GÓRĘ)
        # Dla wyższego ekranu: scroll startuje gdy gracz jest w połowie ekranu (zamiast 1/4)
        scroll_threshold = SCREEN_HEIGHT / 2
        if self.player.rect.top <= scroll_threshold:
            self.player.pos.y += abs(self.player.vel.y)
            # Przesuń platformy w dół
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()  # Usuń te co spadły

            # Przesuń lawę w dół (wizualnie), choć ona logicznie ciągle goni gracza
            self.lava.rect.y += abs(self.player.vel.y)
            self.score += int(abs(self.player.vel.y))

        # 4. GENEROWANIE NOWYCH PLATFORM
        while len(self.platforms) < MAX_PLATFORMS:
            width = random.randint(*PLATFORM_WIDTH_RANGE)
            x = random.randrange(0, SCREEN_WIDTH - width)
            # Nowa platforma jest wyżej niż najwyższa obecna
            highest_plat = min(self.platforms, key=lambda p: p.rect.top)
            y = highest_plat.rect.top - random.randint(*PLATFORM_GAP_Y)

            p = Platform(x, y)
            self.platforms.add(p)
            self.all_sprites.add(p)

        # 5. ŚMIERĆ (DOTKNIĘCIE LAWY LUB SPADNIĘCIE)
        death_by_lava = pygame.sprite.spritecollide(self.player, self.danger_zone, False)
        fell_off = self.player.rect.top > SCREEN_HEIGHT + 200

        if death_by_lava or fell_off:
            if self.score > self.highscore:
                self.highscore = self.score
                with open(HS_FILE, 'w') as f:
                    f.write(str(self.highscore))
            print(f"Koniec gry! Twój wynik: {self.score}, Rekord: {self.highscore}")
            self.new_game()

    def draw(self):
        # --- ZMIANA TUTAJ: Rysowanie tła ---
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(SKY_BLUE)  # Stare tło jednokolorowe

        self.all_sprites.draw(self.screen)

        # Rysowanie wyniku bieżącego
        score_surf = self.font.render(f"Wysokość: {self.score}", True, BLACK)
        self.screen.blit(score_surf, (10, 10))

        # Rysowanie REKORDU
        hs_surf = self.font.render(f"Rekord: {self.highscore}", True, RED)
        self.screen.blit(hs_surf, (10, 35))

        # COMBO COUNTER - Icy Tower style
        if self.player.jump_count > 1:
            combo_font = pygame.font.SysFont("Arial", 36, bold=True)
            combo_text = f"COMBO x{self.player.jump_count}!"
            combo_surf = combo_font.render(combo_text, True, RED)
            combo_x = SCREEN_WIDTH // 2 - combo_surf.get_width() // 2
            self.screen.blit(combo_surf, (combo_x, 100))

        pygame.display.flip()


if __name__ == "__main__":
    g = Game()
    g.run()
    pygame.quit()
    sys.exit()

