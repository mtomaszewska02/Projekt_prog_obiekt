import pygame
from Settings import *  # Pamiętaj o wielkości liter w nazwie pliku (Settings vs settings)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.run_timer = 0
        # Ładowanie wyglądu z Settings.py
        w, h = PLAYER_SKIN["width"], PLAYER_SKIN["height"]

        if PLAYER_SKIN["image_path"]:
            try:
                img = pygame.image.load(PLAYER_SKIN["image_path"]).convert_alpha()
                img = pygame.transform.scale(img, (w, h))
                self.images = {"idle": img, "run": img, "jump": img}
            except:
                self.images = self._generate_colors(w, h)
        else:
            self.images = self._generate_colors(w, h)

        self.image = self.images["idle"]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)

        # Fizyka
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.facing_right = True
        self.jump_count = 0
        self.last_jump_time = 0
        self.max_speed_boost = 0

    def _generate_colors(self, w, h):
        return {
            "idle": create_texture(w, h, PLAYER_SKIN["color_idle"]),
            "run": create_texture(w, h, PLAYER_SKIN["color_run"]),
            "jump": create_texture(w, h, PLAYER_SKIN["color_jump"])
        }

    # --- TUTAJ BYŁ BŁĄD - TO JEST POPRAWIONA FUNKCJA ---
    def jump(self):
        now = pygame.time.get_ticks()

        # 1. PRIORYTET: Zwykły skok (jeśli stoimy na ziemi)
        if self.game.check_ground():
            # Combo skoków
            if now - self.last_jump_time < 2000 and self.jump_count < 3:
                self.jump_count += 1
            else:
                self.jump_count = 0

            self.last_jump_time = now
            multiplier = 1 + (self.jump_count * 0.1)

            self.vel.y = JUMP_POWER * multiplier
            self.max_speed_boost = self.jump_count * 0.8
            return  # WAŻNE: Kończymy funkcję, żeby nie wykonać Wall Jumpa!

        # 2. Wall Jump (tylko jeśli NIE stoimy na ziemi)
        self.rect.x += 2
        hits_right = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 4
        hits_left = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x += 2  # powrót

        if hits_right or hits_left:
            self.vel.y = JUMP_POWER
            # Jeśli ściana jest po prawej, odbij w lewo (-12), jeśli po lewej, w prawo (12)
            self.vel.x = 0 if hits_right else 12

    def update(self):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()

        moving = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if moving:
            self.run_timer += 1
        else:
            self.run_timer = 0

        current_acc = ACCELERATION + self.max_speed_boost
        if self.run_timer > 5:
            current_acc *= SPRINT_MULTIPLIER
            ###############
        sprint_progress = min(self.run_timer / SPRINT_RAMP_TIME, 1.0)
        current_multiplier = 1.0 + (sprint_progress * (SPRINT_MULTIPLIER - 1.0))
        current_acc = (ACCELERATION + self.max_speed_boost) * current_multiplier
        #######################
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -current_acc
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = current_acc
            self.facing_right = True

        # Fizyka ruchu + Tarcie (reszta kodu pozostaje bez zmian)
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Zawijanie ekranu
        if self.pos.x > SCREEN_WIDTH: self.pos.x = 0
        if self.pos.x < 0: self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos
        self.animate()

    def animate(self):
        if self.vel.y < 0:
            self.image = self.images["jump"]
        elif abs(self.vel.x) > 1:
            self.image = self.images["run"]
        else:
            self.image = self.images["idle"]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)