# level/tiles.py
import pygame
from settings import COR_TILE

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(COR_TILE)
        self.rect = self.image.get_rect(topleft=(x, y))
