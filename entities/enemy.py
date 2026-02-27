# entities/enemy.py
import pygame
import math
from settings import VEL_INIMIGO, GRAVIDADE, TILE_SIZE
from core.animation import Animation


class Enemy(pygame.sprite.Sprite):
    """
    Ninja inimigo com comportamentos variados.
    
    Tipos:
        patrol  — patrulha entre limites, pausa ao virar, não persegue
        chase   — patrulha normalmente, persegue ao detectar o player
        jumper  — como chase, mas pula quando encontra obstáculo ou desnível
        guard   — fica parado em idle e só ataca quando player chega perto
    """

    ENEMY_SCALE = 0.12

    def __init__(self, x, y, limite_esq, limite_dir, tipo="chase", hp=2):
        super().__init__()

        try:
            self.animations = {
                "idle":   Animation("assets/images/enemy/idle",   0.15, self.ENEMY_SCALE, loop=True),
                "run":    Animation("assets/images/enemy/run",    0.10, self.ENEMY_SCALE, loop=True),
                "jump":   Animation("assets/images/enemy/jump",   0.12, self.ENEMY_SCALE, loop=False),
                "attack": Animation("assets/images/enemy/attack", 0.08, self.ENEMY_SCALE, loop=False),
                "death":  Animation("assets/images/enemy/death",  0.12, self.ENEMY_SCALE, loop=False),
            }
            self.current_animation = "idle"
        except Exception as e:
            print(f"AVISO: Erro ao carregar animações do ninja: {e}")
            self.animations = None
            self.image = pygame.Surface((30, 30))
            self.image.fill((200, 80, 80))

        if self.animations:
            self.image = self.animations[self.current_animation].get_current_frame()

        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0

        # Limites de patrulha (corrige ordem)
        self.limite_esq = min(limite_esq, limite_dir)
        self.limite_dir = max(limite_esq, limite_dir)

        self.direcao = 1
        self.vivo = True
        self.no_chao = False

        # Tipo e dificuldade
        self.tipo = tipo
        self.hp = hp
        self.hp_max = hp

        # Velocidades por tipo
        self._patrol_speed = VEL_INIMIGO
        self._chase_speed  = VEL_INIMIGO * 1.8 if tipo != "guard" else 0
        self._jump_force    = -12

        # Detecção — ajustável por tipo
        self.detection_range_x = 350
        self.detection_range_y = 120
        self.attack_range = 60

        # Sistema de ataque com cooldown — varia por tipo
        self.attacking = False
        self.attack_timer = 0
        self._dealt_damage_this_swing = False
        self._sfx_attack = False  # flag para gameplay tocar SFX

        if tipo == "guard":
            self.attack_duration = 0.4
            self.attack_cooldown = 0.8     # guarda ataca rápido
        elif tipo == "patrol":
            self.attack_duration = 0.5
            self.attack_cooldown = 1.8     # patrulheiro ataca devagar
        elif tipo == "jumper":
            self.attack_duration = 0.45
            self.attack_cooldown = 1.0
        else:  # chase
            self.attack_duration = 0.45
            self.attack_cooldown = 1.0

        self.attack_cooldown_timer = 0

        # Pausa ao inverter direção (patrulha mais natural)
        self._pause_timer = 0
        self._pause_duration = 0.4

        # Efeito de dano recebido (pisca vermelho)
        self._hit_flash_timer = 0
        self._hit_flash_duration = 0.25

        # Morte
        self.death_timer = 0
        self.death_duration = 0.9

    # ======================== ANIMAÇÃO ========================

    def set_animation(self, name):
        if not self.animations or name not in self.animations:
            return
        if self.current_animation == "death":
            return
        # Não interrompe ataque por outra animação menor
        if self.current_animation == "attack" and self.attacking and name not in ("death",):
            return
        if self.current_animation != name:
            self.current_animation = name
            self.animations[name].reset()

    # ======================== DANO / MORTE ========================

    def take_damage(self, damage=1):
        if not self.vivo:
            return
        self.hp -= damage
        self._hit_flash_timer = self._hit_flash_duration
        if self.hp <= 0:
            self.hp = 0
            self.die()

    def die(self):
        self.vivo = False
        self.vel_x = 0
        self.vel_y = 0
        self.attacking = False
        self.current_animation = "death"
        if self.animations:
            self.animations["death"].reset()

    # ======================== HITBOX DE ATAQUE ========================

    def get_attack_hitbox(self):
        """Retorna hitbox de ataque ativa — ou None se não estiver atacando."""
        if not self.attacking or self._dealt_damage_this_swing:
            return None
        w, h = 60, 50
        if self.direcao == 1:
            return pygame.Rect(self.rect.right - 5, self.rect.centery - h // 2, w, h)
        else:
            return pygame.Rect(self.rect.left - w + 5, self.rect.centery - h // 2, w, h)

    # ======================== DETECÇÃO ========================

    def detect_player(self, player_pos):
        if not player_pos:
            return False
        dx = abs(player_pos[0] - self.rect.centerx)
        dy = abs(player_pos[1] - self.rect.centery)
        return dx <= self.detection_range_x and dy <= self.detection_range_y

    def _player_in_attack_range(self, player_pos):
        if not player_pos:
            return False
        dx = abs(player_pos[0] - self.rect.centerx)
        dy = abs(player_pos[1] - self.rect.centery)
        return dx <= self.attack_range and dy <= 40

    # ======================== FÍSICA ========================

    def apply_gravity(self, tiles):
        self.vel_y += GRAVIDADE
        if self.vel_y > 15:
            self.vel_y = 15

        self.rect.y += self.vel_y
        self.no_chao = False

        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = tile.rect.top
                        self.vel_y = 0
                        self.no_chao = True
                    elif self.vel_y < 0:
                        self.rect.top = tile.rect.bottom
                        self.vel_y = 0

    def _check_edge_ahead(self, tiles):
        """Verifica se há chão à frente. Retorna False se estiver perto de uma borda."""
        probe_x = self.rect.centerx + (self.direcao * (self.rect.width // 2 + 4))
        probe_y = self.rect.bottom + 8
        probe_rect = pygame.Rect(probe_x - 2, probe_y, 4, 4)
        for tile in tiles:
            if probe_rect.colliderect(tile.rect):
                return True
        return False

    # ======================== COMPORTAMENTOS ========================

    def _behavior_patrol(self, dt, tiles, player_pos):
        """Patrulha entre limites; contra-ataca se o player estiver muito perto."""
        # Se o player está perto, vira e ataca (reação defensiva)
        if player_pos and self._player_in_attack_range(player_pos):
            self.direcao = 1 if player_pos[0] > self.rect.centerx else -1
            self.vel_x = 0
            self._try_attack()
            return

        # Pausa breve ao chegar no limite
        if self._pause_timer > 0:
            self._pause_timer -= dt
            self.vel_x = 0
            return

        self.vel_x = self._patrol_speed * self.direcao

        at_limit = False
        if self.direcao == 1 and self.rect.right >= self.limite_dir:
            self.rect.right = self.limite_dir
            at_limit = True
        elif self.direcao == -1 and self.rect.left <= self.limite_esq:
            self.rect.left = self.limite_esq
            at_limit = True

        # Verifica borda de plataforma (não cai)
        if self.no_chao and not self._check_edge_ahead(tiles):
            at_limit = True

        if at_limit:
            self.direcao *= -1
            self._pause_timer = self._pause_duration
            self.vel_x = 0

    def _behavior_chase(self, dt, tiles, player_pos):
        """Patrulha normalmente; persegue e ataca quando detecta o player."""
        if player_pos and self.detect_player(player_pos):
            # Perto o suficiente para atacar
            if self._player_in_attack_range(player_pos):
                self.vel_x = 0
                self._try_attack()
            else:
                # Persegue, mas não cai de plataformas
                target_dir = 1 if player_pos[0] > self.rect.centerx else -1
                self.direcao = target_dir

                if self.no_chao and not self._check_edge_ahead(tiles):
                    self.vel_x = 0
                else:
                    self.vel_x = self._chase_speed * self.direcao
        else:
            self._behavior_patrol(dt, tiles, player_pos)

    def _behavior_jumper(self, dt, tiles, player_pos):
        """Como chase, mas pula quando o player está acima ou há obstáculo."""
        if player_pos and self.detect_player(player_pos):
            if self._player_in_attack_range(player_pos):
                self.vel_x = 0
                self._try_attack()
            else:
                target_dir = 1 if player_pos[0] > self.rect.centerx else -1
                self.direcao = target_dir

                player_above = player_pos[1] < self.rect.centery - 30
                at_edge = self.no_chao and not self._check_edge_ahead(tiles)

                if self.no_chao and (player_above or at_edge):
                    self.vel_y = self._jump_force
                    self.no_chao = False

                if self.no_chao and not at_edge:
                    self.vel_x = self._chase_speed * self.direcao
                elif not self.no_chao:
                    self.vel_x = self._chase_speed * 0.7 * self.direcao
                else:
                    self.vel_x = 0
        else:
            self._behavior_patrol(dt, tiles, player_pos)

    def _behavior_guard(self, dt, tiles, player_pos):
        """Fica parado; avança um pouco e ataca quando o player chega perto."""
        self.vel_x = 0
        if player_pos and self._player_in_attack_range(player_pos):
            self.direcao = 1 if player_pos[0] > self.rect.centerx else -1
            self._try_attack()
        elif player_pos and self.detect_player(player_pos):
            self.direcao = 1 if player_pos[0] > self.rect.centerx else -1
            # Dash curto em direção ao player quando perto
            dx = abs(player_pos[0] - self.rect.centerx)
            if dx < 120 and self.no_chao:
                self.vel_x = VEL_INIMIGO * 1.2 * self.direcao

    def _try_attack(self):
        """Inicia ataque se o cooldown permitir."""
        if not self.attacking and self.attack_cooldown_timer <= 0:
            self.attacking = True
            self.attack_timer = 0
            self._dealt_damage_this_swing = False
            self._sfx_attack = True
            self.set_animation("attack")

    # ======================== UPDATE PRINCIPAL ========================

    def _choose_animation(self):
        """Seleciona a animação correta baseada no estado — chamada UMA vez por frame."""
        if not self.vivo:
            return
        if self.attacking:
            return
        if not self.no_chao:
            self.set_animation("jump")
            return
        if abs(self.vel_x) > 0.1:
            self.set_animation("run")
        else:
            self.set_animation("idle")

    def update(self, dt, tiles=None, player_pos=None):
        # Reset flag de SFX
        self._sfx_attack = False
        if not self.vivo:
            self.death_timer += dt
            if self.animations:
                self.animations[self.current_animation].update(dt)
                self.image = self.animations[self.current_animation].get_current_frame()
            if self.death_timer >= self.death_duration:
                self.kill()
            return

        # Timers
        if self._hit_flash_timer > 0:
            self._hit_flash_timer -= dt

        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt

        # Gerencia estado de ataque
        if self.attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                self.attacking = False
                self.attack_cooldown_timer = self.attack_cooldown

        # Comportamento por tipo
        if not self.attacking:
            if self.tipo == "patrol":
                self._behavior_patrol(dt, tiles, player_pos)
            elif self.tipo == "chase":
                self._behavior_chase(dt, tiles, player_pos)
            elif self.tipo == "jumper":
                self._behavior_jumper(dt, tiles, player_pos)
            elif self.tipo == "guard":
                self._behavior_guard(dt, tiles, player_pos)
            else:
                self._behavior_chase(dt, tiles, player_pos)
        else:
            self.vel_x = 0  # Parado ao atacar

        # Movimento horizontal
        self.rect.x += self.vel_x

        # Colisão horizontal com paredes (tiles)
        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    if self.vel_x > 0:
                        self.rect.right = tile.rect.left
                        self.direcao = -1
                        self._pause_timer = self._pause_duration
                    elif self.vel_x < 0:
                        self.rect.left = tile.rect.right
                        self.direcao = 1
                        self._pause_timer = self._pause_duration
                    self.vel_x = 0

        # Segurança — garante dentro dos limites
        if self.rect.left < self.limite_esq:
            self.rect.left = self.limite_esq
            self.direcao = 1
        if self.rect.right > self.limite_dir:
            self.rect.right = self.limite_dir
            self.direcao = -1

        # Gravidade
        self.apply_gravity(tiles)

        # Escolhe animação UMA vez (sem conflito)
        self._choose_animation()

        # Renderiza frame — preserva rect.bottom para não oscilar no chão
        if self.animations:
            self.animations[self.current_animation].update(dt)
            frame = self.animations[self.current_animation].get_current_frame()

            if self.direcao == -1:
                frame = pygame.transform.flip(frame, True, False)

            # Flash vermelho ao levar dano
            if self._hit_flash_timer > 0:
                frame = frame.copy()
                frame.fill((255, 60, 60, 80), special_flags=pygame.BLEND_ADD)

            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx
            self.image = frame
            self.rect = self.image.get_rect()
            self.rect.centerx = old_centerx
            self.rect.bottom = old_bottom
