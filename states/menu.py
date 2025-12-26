# states/menu.py
import pygame
from core.states import State


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 40)
        self.text_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Cores temáticas (Cavaleiro = prata/branco, Ninjas = vermelho/preto)
        self.bg_color = (15, 15, 25)
        self.title_color = (220, 220, 255)
        self.subtitle_color = (200, 180, 180)
        self.accent_color = (255, 200, 100)


    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.game.reiniciar_jogo()


    def draw(self, screen):
        screen.fill(self.bg_color)
        
        # Título principal
        title = self.title_font.render("LÂMINAS DAS SOMBRAS", True, self.title_color)
        title_rect = title.get_rect(center=(screen.get_width()//2, 100))
        screen.blit(title, title_rect)
        
        # Subtítulo em inglês
        subtitle = self.subtitle_font.render("Shadow Blades", True, self.subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(screen.get_width()//2, 160))
        screen.blit(subtitle, subtitle_rect)
        
        # História (3 linhas)
        story_lines = [
            "Você é um Cavaleiro Templário preso em território hostil.",
            "Ninjas traiçoeiros cercam sua rota de fuga.",
            "Lute pela sobrevivência e encontre o caminho de volta!"
        ]
        
        y_offset = 240
        for line in story_lines:
            text = self.text_font.render(line, True, (200, 200, 210))
            text_rect = text.get_rect(center=(screen.get_width()//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 35
        
        # Botão de início (destaque)
        start_text = self.subtitle_font.render("Pressione ESPAÇO para começar", True, self.accent_color)
        start_rect = start_text.get_rect(center=(screen.get_width()//2, 400))
        screen.blit(start_text, start_rect)
        
        # Controles
        controls_title = self.text_font.render("CONTROLES:", True, (180, 180, 190))
        controls_title_rect = controls_title.get_rect(center=(screen.get_width()//2, 470))
        screen.blit(controls_title, controls_title_rect)
        
        controls = [
            "A/D ou SETAS - Mover",
            "ESPAÇO - Pular",
            "J - Atacar",
            "ESC - Pausar"
        ]
        
        y_offset = 505
        for control in controls:
            text = self.small_font.render(control, True, (150, 150, 160))
            text_rect = text.get_rect(center=(screen.get_width()//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 25
