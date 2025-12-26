# states/gameover.py
import pygame
from core.states import State


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 90)
        self.text_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)


    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.game.reiniciar_jogo()
                if e.key == pygame.K_ESCAPE:
                    self.game.trocar_estado("MENU")


    def draw(self, screen):
        # Fundo vermelho escuro (derrota)
        screen.fill((35, 10, 10))
        
        # Título "DERROTA"
        title = self.title_font.render("DERROTA", True, (255, 80, 80))
        title_rect = title.get_rect(center=(screen.get_width()//2, 150))
        screen.blit(title, title_rect)
        
        # Mensagem de derrota
        messages = [
            "Os ninjas das sombras prevaleceram.",
            "",
            "O Cavaleiro Templário caiu em combate.",
            "",
            "A fortaleza permanece invencível..."
        ]
        
        y_offset = 260
        for msg in messages:
            if msg:  # pula linhas vazias
                text = self.text_font.render(msg, True, (255, 150, 150))
                text_rect = text.get_rect(center=(screen.get_width()//2, y_offset))
                screen.blit(text, text_rect)
            y_offset += 40
        
        # Instruções
        restart = self.small_font.render("ESPAÇO - Tentar novamente", True, (255, 220, 100))
        restart_rect = restart.get_rect(center=(screen.get_width()//2, 500))
        screen.blit(restart, restart_rect)
        
        menu_text = self.small_font.render("ESC - Voltar ao menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(screen.get_width()//2, 540))
        screen.blit(menu_text, menu_rect)
