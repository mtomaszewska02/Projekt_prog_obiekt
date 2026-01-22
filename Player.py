import pygame
from Settings import *  # Pamiętaj o wielkości liter w nazwie pliku (Settings vs settings)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

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
        self.jump_buffer_time = 0
        self.last_ground_time = pygame.time.get_ticks()  # Start on ground!
        self.jump_released = True  # Śledzi czy przycisk skoku został puszczony

    def _generate_colors(self, w, h):
        return {
            "idle": create_texture(w, h, PLAYER_SKIN["color_idle"]),
            "run": create_texture(w, h, PLAYER_SKIN["color_run"]),
            "jump": create_texture(w, h, PLAYER_SKIN["color_jump"])
        }

    # --- TUTAJ BYŁ BŁĄD - TO JEST POPRAWIONA FUNKCJA ---
    def jump(self):
        now = pygame.time.get_ticks()
        
        # Sprawdź czy możemy skoczyć (na ziemi lub coyote time)
        time_since_ground = now - self.last_ground_time
        can_jump = time_since_ground <= COYOTE_TIME
        

        if can_jump:
            # Jeśli trzymamy przycisk, tylko ustaw bufor
            if not self.jump_released:
                self.jump_buffer_time = now
                return
            
            # Wykonaj skok!
            self.jump_released = False
            
            # Combo skoków - UPROSZCZONY
            time_since_last_jump = now - self.last_jump_time
            # Jeśli to pierwszy skok (last_jump_time == 0) LUB minęło > 2 sekundy
            if self.last_jump_time == 0 or time_since_last_jump >= 2000:
                self.jump_count = 1  # Start nowego combo
            # Jeśli skok w ciągu 2 sekund i nie przekroczyliśmy limitu
            elif time_since_last_jump < 2000 and self.jump_count < 8:
                self.jump_count += 1

            self.last_jump_time = now
            
            # Zbalansowany combo multiplier
            combo_multiplier = 1 + (self.jump_count * 0.10)
            
            # Skok zależy od prędkości poziomej
            speed_factor = 1 + (abs(self.vel.x) / MAX_HORIZONTAL_SPEED) * JUMP_SPEED_BONUS
            
            # Zastosuj oba multipliery
            self.vel.y = JUMP_POWER * combo_multiplier * speed_factor
            
            # Zmniejszony boost prędkości z combo (było 2, teraz 0.5)
            self.max_speed_boost = self.jump_count * 0.5
            self.jump_buffer_time = 0  # Resetuj bufor
            return

        # Jeśli nie możemy skoczyć, zapisz jako bufor
        else:
            self.jump_buffer_time = now

        
        hits_platform = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits_platform and not can_jump:
            self.vel.y = JUMP_POWER - 1.5 * abs(self.vel.x)
    
    def jump_cut(self):
        """Zmniejsza prędkość skoku gdy gracz puści przycisk"""
        if self.vel.y < 0:
            self.vel.y *= JUMP_CUT_MULTIPLIER

    def update(self):
        now = pygame.time.get_ticks()
        self.acc = pygame.math.Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()

        speed = ACCELERATION + self.max_speed_boost
        # Reduced air control - can't fight momentum as easily
        is_grounded = self.game.check_ground()
        control = 1.0 if is_grounded else 0.4  # Much less air control (było 1.0 zawsze)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -speed * control
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = speed * control
            self.facing_right = True

        # Sprawdź czy przycisk skoku jest puszczony (do wykrycia kolejnego wciśnięcia)
        if not (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]):
            self.jump_released = True
        
        # Reset combo po 2 sekundach bez skoku
        if self.last_jump_time > 0 and now - self.last_jump_time >= 2000:
            self.jump_count = 0
            self.max_speed_boost = 0
            
        # Jump buffering - automatycznie próbuj wykonać buforowany skok
        if self.jump_buffer_time > 0 and now - self.jump_buffer_time <= JUMP_BUFFER:
            # Sprawdź czy jesteśmy na ziemi
            if now - self.last_ground_time <= COYOTE_TIME and self.jump_released:
                # Wykonaj skok wywołując jump() - będzie działać bo jump_released = True
                self.jump()

        # Fizyka ruchu + Tarcie (Zbalansowane)
        self.vel += self.acc
        if is_grounded and self.acc.x == 0:
            self.vel.x *= 1 - FRICTION  # Użyj FRICTION z settings
        else:
            # Umiarkowane tarcie w powietrzu = dobry balans momentum i kontroli
            self.vel.x *= 0.98  # Było 0.995 - za mało tarcia
        self.pos += self.vel + 0.5 * self.acc

        # Zawijanie ekranu - ściany odbijają gracza
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH
            self.vel.x = -self.vel.x * 0.9  # Wysoka energia odbicia - 90% prędkości zachowane
        elif self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = -self.vel.x * 0.9  # Wysoka energia odbicia - 90% prędkości zachowane
        
        # Ograniczenie prędkości poziomej
        self.vel.x = max(-MAX_HORIZONTAL_SPEED, min(self.vel.x, MAX_HORIZONTAL_SPEED))
        
        self.rect.midbottom = self.pos
        self.animate()
        
        # Aktualizuj pozycję po animacji (rotacja może zmienić rect)
        self.rect.midbottom = self.pos

    def animate(self):
        # Wybierz odpowiedni obraz
        if self.vel.y < 0:
            base_image = self.images["jump"]
        elif abs(self.vel.x) > 1:
            base_image = self.images["run"]
        else:
            base_image = self.images["idle"]

        # Odbij jeśli patrzy w lewo
        if not self.facing_right:
            base_image = pygame.transform.flip(base_image, True, False)
        
        # COMBO ROTATION - tylko w powietrzu podczas combo!
        if self.jump_count > 5 and self.vel.y != GRAVITY:  # Combo + w powietrzu (nie na ziemi)
            # Prędkość rotacji zależy od:
            # 1. Combo level (więcej combo = bardziej wild)
            # 2. Prędkość pozioma (więcej momentum = szybszy spin)
            
            combo_factor = self.jump_count * 5  # Zwiększone dla lepszej widoczności
            # speed_factor = abs(self.vel.x) * 0.2
            total_rotation_speed = combo_factor # + speed_factor
            
            # Kierunek rotacji zależy od kierunku ruchu!
            # Prawo = zgodnie z ruchem wskazówek, Lewo = przeciwnie
            direction = 1 if self.vel.x > 0 else -1
            
            # Kąt bazowany na czasie i prędkości
            angle = (pygame.time.get_ticks() * total_rotation_speed / 100 * direction) % 360
            
            # Obróć obraz
            self.image = pygame.transform.rotate(base_image, angle)
            
            # Zachowaj środek po rotacji (rotacja zmienia rozmiar obrazka)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        else:
            self.image = base_image
