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
        self.total_levels = 3

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
        self.current_level += 1
        if self.current_level > self.total_levels:
            self.trocar_estado("VICTORY")
        else:
            self.trocar_estado("GAMEPLAY", nivel=self.current_level)

    def reiniciar_jogo(self):
        self.current_level = 1
        self.trocar_estado("GAMEPLAY", nivel=self.current_level)

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
