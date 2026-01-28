import pygame
import random
import math


class PlayerManager:
    def __init__(self):
        self.current_player = None

        self.font_large = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 18)

            # Nowe zmienne dla animacji w locie
        self.confetti_particles = []
        self.record_broken = False
        self.animation_start_time = 0

    def setup_confetti(self, screen_width):
        """Inicjalizuje animację i zapisuje czas startu"""
        self.record_broken = True
        self.animation_start_time = pygame.time.get_ticks()  # Zapisujemy czas startu w ms

        self.confetti_particles = []
        for _ in range(50):
            self.confetti_particles.append({
                "x": random.randint(0, screen_width),
                "y": random.randint(-800, 0),
                "color": random.choice([(255, 215, 0), (255, 50, 50), (50, 255, 50), (50, 50, 255)]),
                "speed": random.randint(3, 7),
                "size": random.randint(3, 6)
            })

    def draw_ingame_animation(self, screen, screen_width):
        """Rysuje animację tylko przez 5 sekund"""
        if not self.record_broken:
            return

        # Sprawdzamy, ile czasu minęło od startu
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_start_time > 5000: # 5000 ms = 5 sekund
            self.record_broken = False
            return

        # Rysowanie konfetti
        for p in self.confetti_particles:
            p["y"] += p["speed"]
            if p["y"] > 800:
                p["y"] = -10
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

        # Pulsujący napis
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01))
        text_color = (255, 215, 0) if pulse > 0.5 else (255, 255, 255)
        record_surf = self.font_medium.render("NEW WORLD RECORD!", True, text_color)
        screen.blit(record_surf, (screen_width // 2 - record_surf.get_width() // 2, 150))
    def get_nickname_input(self, screen, screen_width, screen_height):
        """Wyświetla ekran do wprowadzenia nicku gracza"""
        nickname = ""
        input_active = True
        clock = pygame.time.Clock()

        while input_active:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(nickname) > 0:
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        if event.unicode.isprintable() and len(nickname) < 20:
                            nickname += event.unicode

            # Rysowanie ekranu
            screen.fill((135, 206, 235))  # SKY_BLUE

            title_surf = self.font_large.render("INFINITE JUMPER", True, (255, 255, 255))
            screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 100))

            prompt_surf = self.font_medium.render("Wprowadź swój nick:", True, (255, 255, 255))
            screen.blit(prompt_surf, (screen_width // 2 - prompt_surf.get_width() // 2, 250))

            # Pole wprowadzania
            input_rect = pygame.Rect(screen_width // 2 - 150, 320, 300, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_rect)
            pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)

            nickname_surf = self.font_medium.render(nickname, True, (0, 0, 0))
            screen.blit(nickname_surf, (input_rect.x + 10, input_rect.y + 10))

            hint_surf = self.font_small.render("Naciśnij ENTER aby potwierdzić", True, (255, 255, 255))
            screen.blit(hint_surf, (screen_width // 2 - hint_surf.get_width() // 2, 400))

            pygame.display.flip()

        return nickname

    def display_game_over_menu(self, screen, screen_width, screen_height, current_player, score, leaderboard):
        """Wyświetla menu po zakonczeniu gry"""
        menu_active = True
        clock = pygame.time.Clock()

        while menu_active:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "restart"
                    elif event.key == pygame.K_c:
                        return "change_player"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"

            # Rysowanie menu
            screen.fill((135, 206, 235))

            go_surf = self.font_large.render("KONIEC GRY", True, (220, 50, 50))
            screen.blit(go_surf, (screen_width // 2 - go_surf.get_width() // 2, 30))

            # 2. AKTUALNY WYNIK
            info_text = f"Gracz: {current_player}  |  Wynik: {score}"
            info_surf = self.font_medium.render(info_text, True, (255, 255, 255))
            screen.blit(info_surf, (screen_width // 2 - info_surf.get_width() // 2, 90))

            # 3. TABELA TOP 10 (Strefa: y=140 do y=520)
            table_x = screen_width // 2 - 180
            table_y = 140
            table_width = 360
            table_height = 380

            # Rysowanie ramki tabeli
            pygame.draw.rect(screen, (20, 20, 40), (table_x, table_y, table_width, table_height))
            pygame.draw.rect(screen, (255, 215, 0), (table_x, table_y, table_width, table_height), 2)

            # Nagłówek tabeli
            header_surf = self.font_small.render("RANKING NAJLEPSZYCH", True, (255, 215, 0))
            screen.blit(header_surf, (screen_width // 2 - header_surf.get_width() // 2, table_y + 10))

            # Wyświetlanie rekordów
            top_10 = leaderboard.get_top_10()
            for i, entry in enumerate(top_10):
                # Złoty kolor dla pierwszego miejsca, biały dla reszty
                text_color = (255, 215, 0) if i == 0 else (255, 255, 255)

                rank_text = f"{i + 1}. {entry['nickname']:<15} {entry['score']:>6}"
                rank_surf = self.font_small.render(rank_text, True, text_color)
                screen.blit(rank_surf, (table_x + 20, table_y + 45 + i * 30))

            # 4. PRZYCISKI STEROWANIA (Strefa: pod tabelą, od y=550)
            button_start_y = 550

            # Każdy przycisk w nowej linii dla lepszej czytelności
            controls = [
                ("[SPACE] - Zagraj ponownie", (50, 200, 50)),
                ("[C] - Zmień gracza", (255, 255, 255)),
                ("[ESC] - Wyjdź do pulpitu", (220, 50, 50))
            ]

            for i, (text, color) in enumerate(controls):
                btn_surf = self.font_small.render(text, True, color)
                screen.blit(btn_surf, (screen_width // 2 - btn_surf.get_width() // 2, button_start_y + i * 35))

            pygame.display.flip()

    def display_first_place_message(self, screen, screen_width, screen_height, score):
        """Wyświetla animowany komunikat gratulacyjny za 1 miejsce"""
        display_time = 0
        clock = pygame.time.Clock()

        # Inicjalizacja konfetti
        confetti = []
        for _ in range(100):
            confetti.append({
                "x": random.randint(0, screen_width),
                "y": random.randint(-screen_height, 0),
                "color": random.choice([(255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 20, 147), (0, 191, 255)]),
                "speed": random.randint(2, 6),
                "size": random.randint(4, 8)
            })

        while display_time < 4000:  # Wydłużone do 4 sekund dla efektu
            dt = clock.tick(60)
            display_time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            # Tło
            screen.fill((20, 20, 40))  # Ciemniejsze tło, by konfetti było widać

            # Aktualizacja i rysowanie konfetti
            for p in confetti:
                p["y"] += p["speed"]
                if p["y"] > screen_height:
                    p["y"] = -10
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

            # Efekt pulsowania tekstu (używamy math.sin do zmiany skali)
            import math
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
            text_color = (255, 215, 0) if pulse > 0.5 else (255, 255, 255)

            congrats_surf = self.font_large.render("NEW WORLD RECORD!", True, text_color)
            screen.blit(congrats_surf, (screen_width // 2 - congrats_surf.get_width() // 2, 250))

            score_surf = self.font_medium.render(f"TWÓJ WYNIK: {score}", True, (255, 255, 255))
            screen.blit(score_surf, (screen_width // 2 - score_surf.get_width() // 2, 280))

            sub_surf = self.font_small.render("JESTEŚ NAJLEPSZY NA ŚWIECIE!", True, (200, 200, 200))
            screen.blit(sub_surf, (screen_width // 2 - sub_surf.get_width() // 2, 350))

            pygame.display.flip()

        return True

    def display_leaderboard(self, screen, screen_width, screen_height, leaderboard):
        """Wyświetla tabelę rekordów"""
        menu_active = True
        clock = pygame.time.Clock()

        while menu_active:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        return

            # Rysowanie tabeli
            screen.fill((135, 206, 235))

            title_surf = self.font_large.render("TOP 10 RANKING", True, (255, 215, 0))
            screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 20))

            top_10 = leaderboard.get_top_10()

            y_offset = 80
            for i, entry in enumerate(top_10, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                ranking_text = f"{medal} {entry['nickname']} - {entry['score']}"
                ranking_surf = self.font_medium.render(ranking_text, True, (255, 255, 255))
                screen.blit(ranking_surf, (50, y_offset))
                y_offset += 40

            hint_surf = self.font_small.render("Naciśnij ESC lub SPACE aby wrócić", True, (255, 255, 255))
            screen.blit(hint_surf, (screen_width // 2 - hint_surf.get_width() // 2, screen_height - 50))

            pygame.display.flip()