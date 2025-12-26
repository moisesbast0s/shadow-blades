# states/gameplay.py
import pygame
from core.states import State
from settings import COR_TEXTO, COR_FUNDO, LARGURA, ALTURA
from entities.player import Player
from levels.level_1 import Level1
from levels.level_2 import Level2
from levels.level_3 import Level3
from levels.level_4 import Level4  
from levels.level_5 import Level5  
from levels.level_6 import Level6
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
        """Reseta gameplay mantendo HP se veio de outra fase"""
        nivel = kwargs.get("nivel", 1)
        hp_inicial = kwargs.get("hp_atual", 5)  # ← RECEBE HP ATUAL
        
        print(f"DEBUG: Iniciando fase {nivel} com HP={hp_inicial}")
        
        try:
            if nivel == 1:
                self.level = Level1()
                self.map_width = 1200
            elif nivel == 2:
                self.level = Level2()
                self.map_width = 1200
            elif nivel == 3:
                self.level = Level3()
                self.map_width = 1200
            elif nivel == 4:
                self.level = Level4()    
                self.map_width = 1200
            elif nivel == 5:
                self.level = Level5()    
                self.map_width = 1200
            else:  # nivel == 6
                self.level = Level6()    
                self.map_width = 1200
            
            # ← Cria player com HP PRESERVADO
            self.player = Player(*self.level.player_start, hp_inicial=hp_inicial)
            print(f"DEBUG: Player criado com HP={self.player.hp}/{self.player.hp_max}")
            
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
            return
        
        # Esconde controles após 5 segundos
        if self.show_controls:
            self.controls_timer += dt
            if self.controls_timer > 5:
                self.show_controls = False
        
        # Transição entre fases (SALVA HP ANTES)
        if self.transitioning:
            self.transition_timer += dt
            if self.transition_timer >= self.transition_delay:
                # ← SALVA HP NO GAME ANTES DE TROCAR
                self.game.atualizar_hp(self.player.hp)
                self.game.proxima_fase()
            return
        
        # Atualiza player
        self.player.update(self.level.tiles, dt, self.map_width)
        
        # Atualiza inimigos
        for enemy in self.level.enemies:
            enemy.update(dt, self.level.tiles, self.player.rect.center)
        
        # Atualiza câmera
        self.update_camera()
        
        # Pegar chave
        if self.level.key and pygame.sprite.spritecollide(self.player, self.level.key, True):
            self.tem_chave = True
            self.transitioning = True
            self.transition_timer = 0
        
        # Ataque do player nos inimigos
        attack_hitbox = self.player.get_attack_hitbox()
        if attack_hitbox:
            for enemy in self.level.enemies:
                if enemy.vivo and attack_hitbox.colliderect(enemy.rect):
                    enemy.take_damage(1)
        
        # Colisão com inimigos
        if self.player.vivo and not self.player.invulnerable:
            for enemy in self.level.enemies:
                if not enemy.vivo:
                    continue
                
                if self.player.rect.colliderect(enemy.rect):
                    player_esta_acima = (self.player.rect.bottom <= enemy.rect.top + 20)
                    altura_diferenca = abs(self.player.rect.centery - enemy.rect.centery)
                    
                    if not player_esta_acima and altura_diferenca < 25:
                        self.player.take_damage(1, enemy_id=id(enemy))
                        
                        # ← ATUALIZA HP NO GAME
                        self.game.atualizar_hp(self.player.hp)
                        
                        knockback_distance = 70
                        if enemy.rect.centerx > self.player.rect.centerx:
                            self.player.rect.x -= knockback_distance
                        else:
                            self.player.rect.x += knockback_distance
                        
                        break
                    elif player_esta_acima:
                        self.player.vel_y = -10
        
        # Sistema de morte -> Game Over
        if not self.player.vivo:
            self.death_timer += dt
            if self.death_timer >= self.death_delay:
                self.game.atualizar_hp(0)  # ← força game over
        
        # Cair do mapa
        if self.player.rect.top > ALTURA + 50:
            if self.player.vivo:
                self.player.die()


    def draw(self, screen):
        if not self.level:
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
