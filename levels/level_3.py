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
            "                         K    ",  # 4
            "                       RRR    ",  # 5
            "                              ",  # 6
            "                              ",  # 7
            "                   RR         ",  # 8
            "                              ",  # 9
            "                              ",  # 10
            "              RR              ",  # 11
            "                              ",  # 12
            "                              ",  # 13
            "         RR                   ",  # 14
            "RRRRRR########################",  # 15
        ]
        
        tile_types = {
            "#": "stone",
            "R": "rock",
        }
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        self.key.add(Key(26 * TILE_SIZE, 4 * TILE_SIZE - 10))
        
        # 3 ninjas perseguidores
        self.enemies.add(Enemy(15 * TILE_SIZE, 14 * TILE_SIZE, 
                              5 * TILE_SIZE, 28 * TILE_SIZE, tipo="chase"))
        self.enemies.add(Enemy(8 * TILE_SIZE, 13 * TILE_SIZE, 
                              3 * TILE_SIZE, 18 * TILE_SIZE, tipo="chase"))
        self.enemies.add(Enemy(22 * TILE_SIZE, 12 * TILE_SIZE, 
                              15 * TILE_SIZE, 28 * TILE_SIZE, tipo="chase"))
