# ui/hud.py
import pygame
from settings import COR_TEXTO

class HUD:
    def __init__(self, game):
        self.game = game
        self.font_small = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Cores temáticas da Fortaleza
        self.cor_barra = (40, 30, 50)
        self.cor_borda = (120, 100, 80)
        self.cor_vermelho = (220, 50, 50)
        self.cor_dourado = (255, 215, 0)
        
        # Cria sprites de coração (fallback se não tiver imagem)
        self.heart_full = self.criar_coracao(True)
        self.heart_empty = self.criar_coracao(False)
        
        # Tenta carregar imagem de coração se existir
        try:
            self.heart_full = pygame.image.load("assets/images/ui/heart_full.png").convert_alpha()
            self.heart_full = pygame.transform.scale(self.heart_full, (24, 24))
        except:
            pass
        
        try:
            self.heart_empty = pygame.image.load("assets/images/ui/heart_empty.png").convert_alpha()
            self.heart_empty = pygame.transform.scale(self.heart_empty, (24, 24))
        except:
            pass

    def criar_coracao(self, cheio=True):
        """Cria um coração pixel art simples"""
        heart = pygame.Surface((24, 24), pygame.SRCALPHA)
        cor = (220, 50, 50) if cheio else (80, 80, 80)
        
        # Desenha coração com pixels
        pixels = [
            "      ****    ****      ",
            "    ********  ******    ",
            "   ******************   ",
            "   ******************   ",
            "    ****************    ",
            "     **************     ",
            "      ************      ",
            "       **********       ",
            "        ********        ",
            "         ******         ",
            "          ****          ",
            "           **           ",
        ]
        
        for y, row in enumerate(pixels):
            for x, char in enumerate(row):
                if char == '*':
                    pygame.draw.rect(heart, cor, (x, y*2, 2, 2))
        
        return heart

    def desenhar_vidas(self, screen, player):
        """Desenha os corações de HP E as vidas restantes"""
        x_inicial = 20
        y_inicial = 20
        espaco = 28
        
        # HP (corações)
        for i in range(player.hp_max):
            x = x_inicial + (i * espaco)
            if i < player.hp:
                screen.blit(self.heart_full, (x, y_inicial))
            else:
                screen.blit(self.heart_empty, (x, y_inicial))
        

    def desenhar_painel_fase(self, screen, nivel_atual, total_niveis):
        """Desenha painel estilizado da fase"""
        # Painel no canto superior direito
        painel_width = 200
        painel_height = 60
        painel_x = screen.get_width() - painel_width - 20
        painel_y = 15
        
        # Fundo do painel
        pygame.draw.rect(screen, self.cor_barra, 
                        (painel_x, painel_y, painel_width, painel_height))
        pygame.draw.rect(screen, self.cor_borda, 
                        (painel_x, painel_y, painel_width, painel_height), 3)
        
        # Texto da fase
        fase_txt = self.font_medium.render(f"FASE {nivel_atual}", True, self.cor_dourado)
        total_txt = self.font_small.render(f"de {total_niveis}", True, COR_TEXTO)
        
        # Centraliza textos no painel
        fase_x = painel_x + (painel_width - fase_txt.get_width()) // 2
        total_x = painel_x + (painel_width - total_txt.get_width()) // 2
        
        screen.blit(fase_txt, (fase_x, painel_y + 10))
        screen.blit(total_txt, (total_x, painel_y + 38))

    def desenhar_instrucoes(self, screen):
        """Desenha controles na parte inferior"""
        instrucoes = [
            "WASD/Setas: Mover",
            "ESPACO: Pular",
            "J: Atacar",
            "ESC: Menu"
        ]
        
        y_inicial = screen.get_height() - 120
        
        # Fundo semi-transparente
        fundo = pygame.Surface((screen.get_width(), 120))
        fundo.set_alpha(100)
        fundo.fill((20, 20, 30))
        screen.blit(fundo, (0, y_inicial))
        
        # Desenha instruções
        y_offset = y_inicial + 10
        for texto in instrucoes:
            txt_surface = self.font_small.render(texto, True, COR_TEXTO)
            screen.blit(txt_surface, (20, y_offset))
            y_offset += 25

    def desenhar_mensagem(self, screen, mensagem, cor=(100, 255, 100)):
        """Desenha mensagem centralizada (ex: passando de fase)"""
        txt = self.font_large.render(mensagem, True, cor)
        x = (screen.get_width() - txt.get_width()) // 2
        y = screen.get_height() // 2 - 50
        
        # Fundo da mensagem
        padding = 20
        pygame.draw.rect(screen, (20, 20, 30), 
                        (x - padding, y - padding, 
                         txt.get_width() + padding*2, txt.get_height() + padding*2))
        pygame.draw.rect(screen, self.cor_dourado, 
                        (x - padding, y - padding, 
                         txt.get_width() + padding*2, txt.get_height() + padding*2), 3)
        
        screen.blit(txt, (x, y))

    def desenhar(self, screen, player, nivel_atual, total_niveis, transitioning=False, show_controls=False):
        """Desenha todo o HUD"""
        # Vidas (corações)
        self.desenhar_vidas(screen, player)
        
        # Painel de fase
        self.desenhar_painel_fase(screen, nivel_atual, total_niveis)
        
        # Mensagem de transição
        if transitioning:
            self.desenhar_mensagem(screen, "Proxima Fase!")
        
        # Controles (opcional, pode mostrar só no começo)
        if show_controls:
            self.desenhar_instrucoes(screen)
