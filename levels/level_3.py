# levels/level_3.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE

class Level3(BaseLevel):
    def __init__(self):
        super().__init__()
        
        self.load_background("assets/images/backgrounds/bg_level3.png")
        
        # Rampa espaçada
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "                              ",  # 2
            "                              ",  # 3
            "                              ",  # 4
            "                              ",  # 5
            "                              ",  # 6
            "                              ",  # 7
            "                   RR         ",  # 8
            "                              ",  # 9
            "                              ",  # 10
            "                              ",  # 11
            "                              ",  # 12
            "                              ",  # 13
            "                              ",  # 14
            "RRRRRR########################",  # 15
        ]
        
        tile_types = {
            "#": "stone",
            "R": "rock",
        }
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        self.key.add(Key(10 * TILE_SIZE, 14 * TILE_SIZE - 10)) # Posição da chave Coluna 10, Linha 13
        
