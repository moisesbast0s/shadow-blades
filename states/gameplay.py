# states/gameplay.py
import pygame
from core.states import State
from settings import COR_TEXTO, COR_FUNDO, LARGURA, ALTURA, PIXEL_FONT
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
        self._death_sfx_played = False
        self.paused = False

        # Fontes do pause
        self._pause_title_font = pygame.font.Font(PIXEL_FONT, 28)
        self._pause_font = pygame.font.Font(PIXEL_FONT, 10)


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
        self._death_sfx_played = False
        self.paused = False

        # Música de gameplay
        if hasattr(self.game, 'audio'):
            self.game.audio.play_music("gameplay")


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

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if e.key == pygame.K_q:
                    self.game.running = False

        # Não processa inputs do player se pausado
        if self.paused:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # SFX de pulo e ataque
        if hasattr(self.game, 'audio'):
            if self.player._sfx_jump:
                self.game.audio.play_sfx("jump")
            if self.player._sfx_attack:
                self.game.audio.play_sfx("attack")


    def update(self, dt):
        if not self.player or not self.level:
            return

        if self.paused:
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
                if hasattr(self.game, 'audio'):
                    self.game.audio.play_sfx("level_complete")
                # ← SALVA HP NO GAME ANTES DE TROCAR
                self.game.atualizar_hp(self.player.hp)
                self.game.proxima_fase()
            return
        
        # Atualiza player
        self.player.update(self.level.tiles, dt, self.map_width)
        
        # Atualiza inimigos
        for enemy in self.level.enemies:
            enemy.update(dt, self.level.tiles, self.player.rect.center)
            # SFX de ataque do ninja
            if enemy._sfx_attack and hasattr(self.game, 'audio'):
                self.game.audio.play_sfx("attack")
        
        # Atualiza câmera
        self.update_camera()
        
        # Atualiza animação da chave (flutuação)
        if self.level.key:
            self.level.key.update(dt)
        
        # Pegar chave
        if self.level.key and pygame.sprite.spritecollide(self.player, self.level.key, True):
            self.tem_chave = True
            if hasattr(self.game, 'audio'):
                self.game.audio.play_sfx("key_pickup")
            self.transitioning = True
            self.transition_timer = 0
        
        # Ataque do player nos inimigos
        attack_hitbox = self.player.get_attack_hitbox()
        if attack_hitbox:
            for enemy in self.level.enemies:
                if enemy.vivo and attack_hitbox.colliderect(enemy.rect):
                    enemy.take_damage(1)
                    if not enemy.vivo and hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("enemy_death")
        
        # Colisão com inimigos (contato + ataque com hitbox)
        if self.player.vivo and not self.player.invulnerable:
            for enemy in self.level.enemies:
                if not enemy.vivo:
                    continue

                # 1) Dano do ATAQUE do ninja (hitbox real)
                enemy_atk = enemy.get_attack_hitbox()
                if enemy_atk and enemy_atk.colliderect(self.player.rect):
                    enemy._dealt_damage_this_swing = True
                    hp_antes = self.player.hp
                    self.player.take_damage(1, enemy_id=id(enemy))
                    if self.player.hp < hp_antes and hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("damage")
                    self.game.atualizar_hp(self.player.hp)
                    # Knockback
                    kb = 80
                    if enemy.rect.centerx > self.player.rect.centerx:
                        self.player.rect.x -= kb
                    else:
                        self.player.rect.x += kb
                    break

                # 2) Dano de CONTATO (player encosta no ninja)
                if self.player.rect.colliderect(enemy.rect):
                    player_esta_acima = (self.player.rect.bottom <= enemy.rect.top + 20)
                    altura_diferenca = abs(self.player.rect.centery - enemy.rect.centery)
                    
                    if not player_esta_acima and altura_diferenca < 25:
                        hp_antes = self.player.hp
                        self.player.take_damage(1, enemy_id=id(enemy))

                        # SFX de dano (só se realmente tomou dano)
                        if self.player.hp < hp_antes and hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("damage")

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
                        enemy.take_damage(1)
                        if not enemy.vivo and hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("enemy_death")
        
        # Sistema de morte -> Game Over
        if not self.player.vivo:
            if not self._death_sfx_played:
                if hasattr(self.game, 'audio'):
                    self.game.audio.play_sfx("player_death")
                self._death_sfx_played = True
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

        # Overlay de pause
        if self.paused:
            self._draw_pause_overlay(screen)

    def _draw_pause_overlay(self, screen):
        """Desenha overlay semi-transparente de pause."""
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        cx = screen.get_width() // 2

        # Título "PAUSADO"
        shadow = self._pause_title_font.render("PAUSADO", True, (0, 0, 0))
        screen.blit(shadow, shadow.get_rect(center=(cx + 2, 252)))
        title = self._pause_title_font.render("PAUSADO", True, (255, 210, 80))
        screen.blit(title, title.get_rect(center=(cx, 250)))

        # Linha decorativa
        pygame.draw.line(screen, (200, 150, 40), (cx - 180, 285), (cx + 180, 285), 2)

        # Opções
        options = [
            ("ESC - Continuar", (220, 220, 240)),
            ("Q - Sair do Jogo", (200, 100, 100)),
        ]
        y = 320
        for text, color in options:
            shadow = self._pause_font.render(text, True, (0, 0, 0))
            screen.blit(shadow, shadow.get_rect(center=(cx + 1, y + 1)))
            rendered = self._pause_font.render(text, True, color)
            screen.blit(rendered, rendered.get_rect(center=(cx, y)))
            y += 40