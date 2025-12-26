# states/victory.py
import pygame
from core.states import State


class VictoryState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 80)
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
        # Fundo verde escuro (vitória)
        screen.fill((10, 30, 15))
        
        # Título "VITÓRIA!"
        title = self.title_font.render("VITÓRIA!", True, (100, 255, 100))
        title_rect = title.get_rect(center=(screen.get_width()//2, 130))
        screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.text_font.render("Missão Cumprida", True, (150, 255, 150))
        subtitle_rect = subtitle.get_rect(center=(screen.get_width()//2, 190))
        screen.blit(subtitle, subtitle_rect)
        
        # Mensagem de vitória
        messages = [
            "O Cavaleiro Templário derrotou os ninjas",
            "e encontrou o caminho de volta para casa.",
            "",
            "A fortaleza foi conquistada!",
            "",
            "Honra e glória ao guerreiro sagrado!"
        ]
        
        y_offset = 260
        for msg in messages:
            if msg:
                text = self.small_font.render(msg, True, (200, 255, 200))
                text_rect = text.get_rect(center=(screen.get_width()//2, y_offset))
                screen.blit(text, text_rect)
            y_offset += 35
        
        # Instruções
        restart = self.small_font.render("ESPAÇO - Jogar novamente", True, (255, 255, 150))
        restart_rect = restart.get_rect(center=(screen.get_width()//2, 500))
        screen.blit(restart, restart_rect)
        
        menu_text = self.small_font.render("ESC - Voltar ao menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(screen.get_width()//2, 540))
        screen.blit(menu_text, menu_rect)
