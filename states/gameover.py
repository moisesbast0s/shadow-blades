# states/gameover.py
import pygame
from core.states import State
from settings import COR_TEXTO

class GameOverState(State):
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.game.reiniciar_jogo()
                if e.key == pygame.K_ESCAPE:
                    self.game.trocar_estado("MENU")

    def draw(self, screen):
        f = self.game.font
        t1 = f.render("GAME OVER", True, COR_TEXTO)
        t2 = f.render("ENTER: tentar de novo | ESC: menu", True, COR_TEXTO)
        screen.blit(t1, (screen.get_width()//2 - t1.get_width()//2, 230))
        screen.blit(t2, (screen.get_width()//2 - t2.get_width()//2, 300))
