# states/gameplay.py
import pygame
from core.states import State
from settings import COR_TEXTO, COR_FUNDO, LARGURA, ALTURA
from entities.player import Player
from levels.level_1 import Level1
from levels.level_2 import Level2
from levels.level_3 import Level3

try:
    from ui.hud import HUD
    HUD_AVAILABLE = True
except Exception as e:
    print(f"AVISO: HUD não carregou: {e}")
    HUD_AVAILABLE = False

class GameplayState(State):
    def __init__(self, game):
        super().__init__(game)
        self.level = None
        self.player = None
        
        if HUD_AVAILABLE:
            self.hud = HUD(game)
        else:
            self.hud = None
        
        self.tem_chave = False
        self.death_timer = 0
        self.death_delay = 1.5
        self.transitioning = False
        self.transition_timer = 0
        self.transition_delay = 0.5
        self.camera_x = 0
        self.map_width = 1200
        self.show_controls = True
        self.controls_timer = 0

    def reset(self, **kwargs):
        print(f"DEBUG: Resetando gameplay, nivel = {kwargs.get('nivel', 1)}")
        nivel = kwargs.get("nivel", 1)
        
        try:
            if nivel == 1:
                self.level = Level1()
            elif nivel == 2:
                self.level = Level2()
            else:
                self.level = Level3()
            
            print(f"DEBUG: Level {nivel} criado com sucesso")
            print(f"DEBUG: Player start = {self.level.player_start}")
            
            self.player = Player(*self.level.player_start)
            print("DEBUG: Player criado com sucesso")
            
        except Exception as e:
            print(f"ERRO ao criar level/player: {e}")
            import traceback
            traceback.print_exc()
        
        self.tem_chave = False
        self.death_timer = 0
        self.transitioning = False
        self.transition_timer = 0
        self.camera_x = 0
        self.show_controls = True
        self.controls_timer = 0

    def update_camera(self):
        if not self.player:
            return
            
        self.camera_x = self.player.rect.centerx - LARGURA // 2
        
        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x > self.map_width - LARGURA:
            self.camera_x = self.map_width - LARGURA

    def handle_events(self, events):
        if not self.player:
            return
            
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.game.trocar_estado("MENU")

    def update(self, dt):
        if not self.player or not self.level:
            print("DEBUG: player ou level não existe!")
            return
        
        # Esconde controles após 5 segundos
        if self.show_controls:
            self.controls_timer += dt
            if self.controls_timer > 5:
                self.show_controls = False
        
        # Transição entre fases
        if self.transitioning:
            self.transition_timer += dt
            if self.transition_timer >= self.transition_delay:
                self.game.proxima_fase()
            return
        
        # Atualiza player
        try:
            self.player.update(self.level.tiles, dt, self.map_width)
        except Exception as e:
            print(f"ERRO ao atualizar player: {e}")
        
        # Atualiza inimigos
        try:
            for enemy in self.level.enemies:
                enemy.update(dt, self.level.tiles, self.player.rect.center)
        except Exception as e:
            print(f"ERRO ao atualizar enemy: {e}")
        
        # Atualiza câmera
        self.update_camera()
        
        # Pegar chave
        if self.level.key and pygame.sprite.spritecollide(self.player, self.level.key, True):
            self.tem_chave = True
            self.transitioning = True
            self.transition_timer = 0
        
        # Ataque do player nos inimigos
        try:
            attack_hitbox = self.player.get_attack_hitbox()
            if attack_hitbox:
                for enemy in self.level.enemies:
                    if enemy.vivo and attack_hitbox.colliderect(enemy.rect):
                        enemy.take_damage(1)
        except Exception as e:
            print(f"ERRO no ataque: {e}")
        
            # Colisão com inimigos (VERIFICAÇÃO MELHORADA)
        if self.player.vivo and not self.player.invulnerable:
            for enemy in self.level.enemies:
                if not enemy.vivo:
                    continue  # pula inimigos mortos
                
                if self.player.rect.colliderect(enemy.rect):
                    # Verifica se player está pisando no ninja (acima)
                    player_esta_acima = (self.player.rect.bottom <= enemy.rect.top + 20)
                    
                    # Verifica diferença de altura no centro
                    altura_diferenca = abs(self.player.rect.centery - enemy.rect.centery)
                    
                    # SÓ CAUSA DANO se:
                    # 1. NÃO estiver pisando no ninja E
                    # 2. Estiverem na mesma altura (diferença < 25px)
                    # states/gameplay.py - na colisão:

                    if not player_esta_acima and altura_diferenca < 25:
                        self.player.take_damage(1, enemy_id=id(enemy))  # ← passa ID do inimigo

                        self.player.take_damage(1)
                        
                        # Knockback forte
                        knockback_distance = 70  # ← aumentado de 50
                        if enemy.rect.centerx > self.player.rect.centerx:
                            self.player.rect.x -= knockback_distance
                        else:
                            self.player.rect.x += knockback_distance
                        
                        break  # só 1 inimigo causa dano
                    
                    # Se estiver pisando no ninja, dá um impulso para cima
                    elif player_esta_acima:
                        self.player.vel_y = -10  # pulo forçado 
        
        # Sistema de morte -> Game Over
        if not self.player.vivo:
            self.death_timer += dt
            if self.death_timer >= self.death_delay:
                self.game.trocar_estado("GAMEOVER")
        
        # Cair do mapa
        if self.player.rect.top > ALTURA + 50:
            if self.player.vivo:
                self.player.die()

    def draw(self, screen):
        if not self.level:
            print("DEBUG: level não existe em draw()")
            screen.fill(COR_FUNDO)
            f = self.game.font
            erro = f.render("ERRO: Level nao carregado", True, (255, 0, 0))
            screen.blit(erro, (200, 300))
            return
        
        # 1. Background
        if self.level.background:
            screen.blit(self.level.background, (0, 0))
        else:
            screen.fill(COR_FUNDO)
        
        # 2. Tiles
        for tile in self.level.tiles:
            screen.blit(tile.image, (tile.rect.x - self.camera_x, tile.rect.y))
        
        # 3. Chave
        for key in self.level.key:
            screen.blit(key.image, (key.rect.x - self.camera_x, key.rect.y))
        
        # 4. Inimigos
        for enemy in self.level.enemies:
            screen.blit(enemy.image, (enemy.rect.x - self.camera_x, enemy.rect.y))
        
        # 5. Player
        if self.player:
            screen.blit(self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))
        
        # 6. HUD
        if self.hud and self.player:
            try:
                self.hud.desenhar(screen, self.player, self.game.current_level, 
                                 self.game.total_levels, self.transitioning, self.show_controls)
            except Exception as e:
                print(f"ERRO ao desenhar HUD: {e}")
                f = self.game.font
                nivel_txt = f.render(f"Fase {self.game.current_level}/{self.game.total_levels}", True, COR_TEXTO)
                hp_txt = f.render(f"HP: {self.player.hp}/{self.player.hp_max}", True, COR_TEXTO)
                screen.blit(nivel_txt, (10, 10))
                screen.blit(hp_txt, (10, 45))
        elif self.player:
            f = self.game.font
            nivel_txt = f.render(f"Fase {self.game.current_level}/{self.game.total_levels}", True, COR_TEXTO)
            hp_txt = f.render(f"HP: {self.player.hp}/{self.player.hp_max}", True, COR_TEXTO)
            screen.blit(nivel_txt, (10, 10))
            screen.blit(hp_txt, (10, 45))
