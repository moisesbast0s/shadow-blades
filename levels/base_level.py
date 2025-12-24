# levels/base_level.py
import pygame
from settings import TILE_SIZE, LARGURA, ALTURA

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type="stone"):
        super().__init__()
        
        try:
            if tile_type == "stone":
                self.image = pygame.image.load("assets/images/tiles/stone.png").convert()
            elif tile_type == "marble":
                self.image = pygame.image.load("assets/images/tiles/marble.png").convert()
            elif tile_type == "rock":
                self.image = pygame.image.load("assets/images/tiles/rock.png").convert()
            elif tile_type == "sand":
                self.image = pygame.image.load("assets/images/tiles/sand.png").convert()
            else:
                self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.image.fill((80, 80, 100))
            
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"AVISO: tile {tile_type} não carregado: {e}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((80, 80, 100))
        
        self.rect = self.image.get_rect(topleft=(x, y))

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/objects/key.png").convert_alpha()
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class BaseLevel:
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.key = pygame.sprite.GroupSingle()
        self.player_start = (50, 300)
        self.background = None
        
    def load_background(self, bg_path):
        try:
            bg_original = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(bg_original, (LARGURA, ALTURA))
        except Exception as e:
            print(f"AVISO: background {bg_path} não carregado: {e}")
            self.background = None
        
    def criar_mapa(self, layout, tile_types=None):
        if tile_types is None:
            tile_types = {"#": "stone"}
        
        for row_idx, row in enumerate(layout):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                
                if char in tile_types:
                    self.tiles.add(Tile(x, y, tile_types[char]))
