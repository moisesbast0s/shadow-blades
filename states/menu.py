# states/menu.py
import pygame
from core.states import State
from settings import COR_TEXTO

class MenuState(State):
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.game.reiniciar_jogo()

    def draw(self, screen):
        f = self.game.font
        titulo = f.render("Ecos da Fortaleza", True, COR_TEXTO)
        subtitulo = f.render("A Fuga de Sao Jose", True, COR_TEXTO)
        instr = f.render("ENTER para comecar", True, COR_TEXTO)
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 180))
        screen.blit(subtitulo, (screen.get_width()//2 - subtitulo.get_width()//2, 230))
        screen.blit(instr, (screen.get_width()//2 - instr.get_width()//2, 300))
