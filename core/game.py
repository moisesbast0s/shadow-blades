# core/game.py
import pygame
from settings import COR_FUNDO
from states.menu import MenuState
from states.gameplay import GameplayState
from states.gameover import GameOverState
from states.victory import VictoryState


class Game:
    def __init__(self, screen, clock, fps):
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
        self.current_level = 1
        self.total_levels = 6
        
        # ← NOVO: Vidas persistentes
        self.player_hp = 5
        self.player_hp_max = 5

        self.states = {
            "MENU": MenuState(self),
            "GAMEPLAY": GameplayState(self),
            "GAMEOVER": GameOverState(self),
            "VICTORY": VictoryState(self),
        }
        self.current_state = self.states["MENU"]


    def trocar_estado(self, nome_estado, **kwargs):
        self.current_state = self.states[nome_estado]
        if hasattr(self.current_state, "reset"):
            self.current_state.reset(**kwargs)


    def proxima_fase(self):
        """Avança para próxima fase SEM resetar HP"""
        self.current_level += 1
        if self.current_level > self.total_levels:
            self.trocar_estado("VICTORY")
        else:
            # ← IMPORTANTE: passa HP atual
            self.trocar_estado("GAMEPLAY", nivel=self.current_level, hp_atual=self.player_hp)


    def reiniciar_jogo(self):
        """Reinicia o jogo DO ZERO (reseta vidas)"""
        self.current_level = 1
        self.player_hp = 5  # ← RESETA VIDAS
        self.trocar_estado("GAMEPLAY", nivel=self.current_level, hp_atual=5)


    def atualizar_hp(self, novo_hp):
        """Atualiza HP global do player"""
        self.player_hp = novo_hp
        if self.player_hp <= 0:
            self.player_hp = 0
            self.trocar_estado("GAMEOVER")


    def loop_principal(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.current_state.handle_events(events)
            self.current_state.update(dt)
            
            self.screen.fill(COR_FUNDO)
            self.current_state.draw(self.screen)
            pygame.display.flip()
