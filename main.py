# main.py
import pygame
from settings import LARGURA, ALTURA, TITULO, FPS
from core.game import Game

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()

    jogo = Game(tela, clock, FPS)
    jogo.loop_principal()
    
    pygame.quit()

if __name__ == "__main__":
    main()
