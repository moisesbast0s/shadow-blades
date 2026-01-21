# entities/enemy.py
import pygame
from settings import VEL_INIMIGO, GRAVIDADE
from core.animation import Animation


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, limite_esq, limite_dir, tipo="chase"):
        super().__init__()
        
        ENEMY_SCALE = 0.12
        
        try:
            self.animations = {
                "idle": Animation("assets/images/enemy/idle", 0.15, ENEMY_SCALE, loop=True),
                "run": Animation("assets/images/enemy/run", 0.1, ENEMY_SCALE, loop=True),
                "attack": Animation("assets/images/enemy/attack", 0.1, ENEMY_SCALE, loop=True),
                "death": Animation("assets/images/enemy/death", 0.15, ENEMY_SCALE, loop=False),
            }
            self.current_animation = "idle"
        except Exception as e:
            print(f"AVISO: Erro ao carregar animações: {e}")
            self.animations = None
            self.image = pygame.Surface((30, 30))
            self.image.fill((200, 80, 80))
        
        if self.animations:
            self.image = self.animations[self.current_animation].get_current_frame()
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_x = VEL_INIMIGO
        self.vel_y = 0
        
        # ✅ CORREÇÃO: Garantir ordem correta dos limites
        self.limite_esq = min(limite_esq, limite_dir)
        self.limite_dir = max(limite_esq, limite_dir)
        
        self.direcao = 1
        self.vivo = True
        self.no_chao = False
        
        self.tipo = tipo
        self.detection_range = 400
        self.chase_speed = VEL_INIMIGO * 1.8
        
        self.hp = 1
        self.death_timer = 0
        self.death_duration = 0.8
        
        # ✅ DEBUG
        print(f"Enemy criado em x={x}, limites: {self.limite_esq} -> {self.limite_dir}")


    def set_animation(self, animation_name):
        if self.animations and animation_name in self.animations:
            if self.current_animation == "death":
                return
            
            if self.current_animation != animation_name:
                self.current_animation = animation_name
                self.animations[animation_name].reset()


    def take_damage(self, damage=1):
        if self.vivo:
            self.hp -= damage
            if self.hp <= 0:
                self.die()


    def die(self):
        self.vivo = False
        self.vel_x = 0
        self.vel_y = 0
        self.current_animation = "death"
        if self.animations:
            self.animations["death"].reset()


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


    def detect_player(self, player_pos):
        if not player_pos:
            return False
        
        distance_x = abs(player_pos[0] - self.rect.centerx)
        distance_y = abs(player_pos[1] - self.rect.centery)
        
        return distance_x <= self.detection_range and distance_y <= 50


    def update(self, dt, tiles=None, player_pos=None):
        if not self.vivo:
            self.death_timer += dt
            if self.animations:
                self.animations[self.current_animation].update(dt)
                self.image = self.animations[self.current_animation].get_current_frame()
            
            if self.death_timer >= self.death_duration:
                self.kill()
            return
        
        # ✅ COMPORTAMENTO CORRIGIDO
        if self.tipo == "chase" and player_pos and self.detect_player(player_pos):
            # Persegue o player
            if player_pos[0] < self.rect.centerx:
                self.vel_x = -self.chase_speed
                self.direcao = -1
            else:
                self.vel_x = self.chase_speed
                self.direcao = 1
            
            # Usa RUN quando persegue
            distance_to_player = abs(player_pos[0] - self.rect.centerx)
            if distance_to_player < 60:
                self.set_animation("attack")
            else:
                self.set_animation("run")
        else:
            # ✅ PATRULHA CORRIGIDA - Lógica simplificada e funcional
            # Move continuamente na direção atual
            self.vel_x = VEL_INIMIGO * self.direcao
            
            # Verifica colisão com limites e inverte direção
            if self.direcao == 1:  # Indo para direita
                if self.rect.right >= self.limite_dir:
                    self.direcao = -1
                    self.rect.right = self.limite_dir  # Força posição no limite
            else:  # Indo para esquerda (direcao == -1)
                if self.rect.left <= self.limite_esq:
                    self.direcao = 1
                    self.rect.left = self.limite_esq  # Força posição no limite
            
            # Usa RUN quando patrulha
            if abs(self.vel_x) > 0.1:
                self.set_animation("run")
            else:
                self.set_animation("idle")
        
        # ✅ MOVIMENTO HORIZONTAL
        self.rect.x += self.vel_x
        
        # ✅ SEGURANÇA ADICIONAL - força dentro dos limites
        if self.rect.left < self.limite_esq:
            self.rect.left = self.limite_esq
            self.direcao = 1
        elif self.rect.right > self.limite_dir:
            self.rect.right = self.limite_dir
            self.direcao = -1
        
        # Gravidade
        self.apply_gravity(tiles)
        
        # Atualiza animação
        if self.animations:
            self.animations[self.current_animation].update(dt)
            frame = self.animations[self.current_animation].get_current_frame()
            
            if self.direcao == -1:
                frame = pygame.transform.flip(frame, True, False)
            
            old_center = self.rect.center
            self.image = frame
            self.rect = self.image.get_rect()
            self.rect.center = old_center
