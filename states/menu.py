# states/menu.py
import pygame
from core.states import State
from settings import PIXEL_FONT


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(PIXEL_FONT, 32)
        self.subtitle_font = pygame.font.Font(PIXEL_FONT, 18)
        self.text_font = pygame.font.Font(PIXEL_FONT, 11)
        self.small_font = pygame.font.Font(PIXEL_FONT, 9)
        
        # Cores temáticas (Cavaleiro = prata/branco, Ninjas = vermelho/preto)
        self.bg_color = (15, 15, 25)
        self.title_color = (220, 220, 255)
        self.subtitle_color = (200, 180, 180)
        self.accent_color = (255, 200, 100)

        # Imagem de fundo pixel art
        try:
            self.bg_image = pygame.image.load("assets/images/backgrounds/menu_bg.png").convert()
        except:
            self.bg_image = None


    def reset(self, **kwargs):
        """Toca música do menu ao entrar neste estado."""
        if hasattr(self.game, 'audio'):
            self.game.audio.play_music("menu")

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.game.reiniciar_jogo()
                if e.key == pygame.K_q:
                    self.game.running = False


    def draw(self, screen):
        # Fundo pixel art
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(self.bg_color)
            
            # Título principal
            title = self.title_font.render("LÂMINAS DAS SOMBRAS", True, self.title_color)
            title_rect = title.get_rect(center=(screen.get_width()//2, 100))
            screen.blit(title, title_rect)
            
            # Subtítulo
            subtitle = self.subtitle_font.render("Shadow Blades", True, self.subtitle_color)
            subtitle_rect = subtitle.get_rect(center=(screen.get_width()//2, 160))
            screen.blit(subtitle, subtitle_rect)
        
        # História (3 linhas) — semi-transparente sobre a imagem
        story_lines = [
            "Você é um Cavaleiro Templário preso em território hostil.",
            "Ninjas traiçoeiros cercam sua rota de fuga.",
            "Lute pela sobrevivência e encontre o caminho de volta!"
        ]
        
        y_offset = 240
        for line in story_lines:
            # Sombra para legibilidade
            shadow = self.text_font.render(line, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2 + 1, y_offset + 1))
            screen.blit(shadow, shadow_rect)
            
            text = self.text_font.render(line, True, (220, 220, 230))
            text_rect = text.get_rect(center=(screen.get_width()//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 35
        
        # Controles
        controls_title = self.text_font.render("CONTROLES:", True, (200, 200, 210))
        ct_shadow = self.text_font.render("CONTROLES:", True, (0, 0, 0))
        screen.blit(ct_shadow, ct_shadow.get_rect(center=(screen.get_width()//2 + 1, 471)))
        screen.blit(controls_title, controls_title.get_rect(center=(screen.get_width()//2, 470)))
        
        controls = [
            "A/D ou SETAS - Mover",
            "ESPACO - Pular",
            "J - Atacar",
            "ESC - Pausar",
            "Q - Sair do Jogo"
        ]
        
        y_offset = 505
        for control in controls:
            shadow = self.small_font.render(control, True, (0, 0, 0))
            screen.blit(shadow, shadow.get_rect(center=(screen.get_width()//2 + 1, y_offset + 1)))
            text = self.small_font.render(control, True, (180, 180, 190))
            screen.blit(text, text.get_rect(center=(screen.get_width()//2, y_offset)))
            y_offset += 25
