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
            "  K                           ",  # 4
            "MMM                           ",  # 5
            "                              ",  # 6
            "                              ",  # 7
            "    MM                        ",  # 8 - espaço de 1 tile
            "                              ",  # 9
            "                              ",  # 10
            "      MM                      ",  # 11 - espaço de 2 tiles
            "                              ",  # 12
            "                              ",  # 13
            "        MM                    ",  # 14 - espaço de 2 tiles
            "##############################",  # 15
        ]
        
        tile_types = {
            "#": "stone",
            "M": "marble",
        }
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        self.key.add(Key(2 * TILE_SIZE, 4 * TILE_SIZE - 10))
        
        # 2 ninjas perseguidores
        self.enemies.add(Enemy(18 * TILE_SIZE, 14 * TILE_SIZE, 
                              5 * TILE_SIZE, 28 * TILE_SIZE, tipo="chase"))
        self.enemies.add(Enemy(10 * TILE_SIZE, 13 * TILE_SIZE, 
                              3 * TILE_SIZE, 18 * TILE_SIZE, tipo="chase"))
