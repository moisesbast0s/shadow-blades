# levels/level_2.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE

class Level2(BaseLevel):
    def __init__(self):
        super().__init__()
        
        self.load_background("assets/images/backgrounds/bg_level2.png")
        
        # Rampa ESPAÇADA - player passa entre os blocos
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "                              ",  # 2
            "                              ",  # 3
            "                              ",  # 4
            "                              ",  # 5
            "                              ",  # 6
            "                              ",  # 7
            "                              ",  # 8 - espaço de 1 tile
            "                              ",  # 9
            "            M                 ",  # 10
            "                              ",  # 11 - espaço de 2 tiles
            "                              ",  # 12
            "                              ",  # 13
            "                              ",  # 14 - espaço de 2 tiles
            "##############################",  # 15
        ]
        
        tile_types = {
            "#": "stone",
            "M": "marble",
        }
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        self.key.add(Key(10 * TILE_SIZE, 14 * TILE_SIZE - 10)) # Posição da chave Coluna 10, Linha 13
        
      