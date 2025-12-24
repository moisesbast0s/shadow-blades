# entities/player.py
import pygame
from settings import GRAVIDADE, FORCA_PULO, VEL_PLAYER, LARGURA, ALTURA
from core.animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        PLAYER_SCALE = 0.1
        
        try:
            self.animations = {
                "idle": Animation("assets/images/player/idle", 0.15, PLAYER_SCALE, loop=True),
                "run": Animation("assets/images/player/run", 0.1, PLAYER_SCALE, loop=True),
                "jump": Animation("assets/images/player/jump", 0.2, PLAYER_SCALE, loop=True),
                "attack": Animation("assets/images/player/attack", 0.08, PLAYER_SCALE, loop=True),
                "death": Animation("assets/images/player/death", 0.15, PLAYER_SCALE, loop=False),
            }
            self.current_animation = "idle"
        except Exception as e:
            print(f"ERRO ao carregar animações do player: {e}")
            self.animations = None
            self.image = pygame.Surface((30, 40))
            self.image.fill((100, 200, 100))
        
        if self.animations:
            self.image = self.animations[self.current_animation].get_current_frame()
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_point = (x, y)
        
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.vivo = True
        self.direcao = 1
        
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.5
        
        self.hp_max = 5
        self.hp = self.hp_max
        self.invulnerable = False
        self.invuln_timer = 0
        self.invuln_duration = 2.0
        
        # Sistema de cooldown por inimigo
        self.damage_cooldown_per_enemy = {}

    def set_animation(self, animation_name):
        if self.animations and animation_name in self.animations:
            if self.current_animation != animation_name:
                self.current_animation = animation_name
                self.animations[animation_name].reset()

    def handle_input(self, keys):
        if not self.vivo or self.attacking:
            return
            
        self.vel_x = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -VEL_PLAYER
            self.direcao = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = VEL_PLAYER
            self.direcao = 1
        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.no_chao:
            self.vel_y = FORCA_PULO
            self.no_chao = False
        
        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attack_timer = 0
            self.set_animation("attack")

    def apply_gravity(self):
        self.vel_y += GRAVIDADE
        if self.vel_y > 15:
            self.vel_y = 15

    def take_damage(self, damage=1, enemy_id=None):
        """Recebe dano com cooldown por inimigo"""
        if not self.vivo:
            return
            
        # Verifica cooldown desse inimigo específico
        if enemy_id and enemy_id in self.damage_cooldown_per_enemy:
            if self.damage_cooldown_per_enemy[enemy_id] > 0:
                return  # ainda em cooldown
        
        if not self.invulnerable:
            self.hp -= damage
            self.invulnerable = True
            self.invuln_timer = 0
            
            # Marca cooldown para esse inimigo
            if enemy_id:
                self.damage_cooldown_per_enemy[enemy_id] = 2.0
            
            if self.hp <= 0:
                self.hp = 0
                self.die()

    def get_attack_hitbox(self):
        if not self.attacking:
            return None
        
        hitbox_width = 80
        hitbox_height = 60
        
        if self.direcao == 1:
            return pygame.Rect(
                self.rect.right - 10,
                self.rect.centery - hitbox_height // 2,
                hitbox_width, 
                hitbox_height
            )
        else:
            return pygame.Rect(
                self.rect.left - hitbox_width + 10,
                self.rect.centery - hitbox_height // 2,
                hitbox_width,
                hitbox_height
            )

    def update_animation(self, dt):
        if not self.vivo:
            self.set_animation("death")
        elif self.attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                self.attacking = False
        elif not self.no_chao:
            self.set_animation("jump")
        elif self.vel_x != 0:
            self.set_animation("run")
        else:
            self.set_animation("idle")
        
        if self.animations:
            self.animations[self.current_animation].update(dt)
            frame = self.animations[self.current_animation].get_current_frame()
            
            if self.direcao == -1:
                frame = pygame.transform.flip(frame, True, False)
            
            if self.invulnerable:
                blink_speed = 15
                if int(self.invuln_timer * blink_speed) % 2 == 0:
                    frame = frame.copy()
                    frame.set_alpha(100)
                else:
                    frame = frame.copy()
                    frame.fill((255, 100, 100, 50), special_flags=pygame.BLEND_ADD)
            
            old_center = self.rect.center
            self.image = frame
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, tiles, dt, map_width=1200):
        if not self.vivo:
            self.update_animation(dt)
            return
        
        # Atualiza cooldowns por inimigo
        for enemy_id in list(self.damage_cooldown_per_enemy.keys()):
            self.damage_cooldown_per_enemy[enemy_id] -= dt
            if self.damage_cooldown_per_enemy[enemy_id] <= 0:
                del self.damage_cooldown_per_enemy[enemy_id]
        
        # Atualiza invulnerabilidade
        if self.invulnerable:
            self.invuln_timer += dt
            if self.invuln_timer >= self.invuln_duration:
                self.invulnerable = False
            
        self.apply_gravity()
        
        self.rect.x += self.vel_x
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > map_width:
            self.rect.right = map_width
        
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel_x > 0:
                    self.rect.right = tile.rect.left
                elif self.vel_x < 0:
                    self.rect.left = tile.rect.right
        
        self.rect.y += self.vel_y
        self.no_chao = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel_y = 0
        
        self.update_animation(dt)

    def die(self):
        self.vivo = False
        self.vel_x = 0
        self.set_animation("death")
