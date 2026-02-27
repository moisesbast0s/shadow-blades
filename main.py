# main.py
import pygame
from settings import LARGURA, ALTURA, TITULO, FPS, ESCALA
from core.game import Game

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    # Janela real (escalada)
    janela_w = int(LARGURA * ESCALA)
    janela_h = int(ALTURA * ESCALA)
    tela_real = pygame.display.set_mode((janela_w, janela_h))
    pygame.display.set_caption(TITULO)

    # Surface interna na resolução original (toda lógica roda aqui)
    tela_interna = pygame.Surface((LARGURA, ALTURA))

    clock = pygame.time.Clock()

    jogo = Game(tela_interna, clock, FPS, tela_real)
    jogo.loop_principal()
    
    pygame.quit()

if __name__ == "__main__":
    main()
