# levels/level_1.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE


class Level1(BaseLevel):
    """
    FASE 1 - TUTORIAL
    Dificuldade: ★☆☆☆☆☆
    Inimigos: 1 (Chase)
    Objetivo: Aprender mecânicas básicas
    """
    def __init__(self):
        super().__init__()
        
        self.load_background("assets/images/backgrounds/bg_level1.png")
        
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "                              ",  # 2
            "                              ",  # 3
            "                              ",  # 4
            "                        ###   ",  # 5
            "                              ",  # 6
            "                              ",  # 7
            "             #########        ",  # 8
            "                              ",  # 9
            "                              ",  # 10
            "       ##                     ",  # 11
            "   #                          ",  # 12
            "                              ",  # 13
            "                              ",  # 14
            "##############################",  # 15
        ]
        
        tile_types = {"#": "stone"}
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        
        # Chave acessível no topo
        self.key.add(Key(26 * TILE_SIZE, 3 * TILE_SIZE - 10))
        
        # 1 ninja perseguidor — cobre todo o chão
        self.enemies.add(Enemy(
            15 * TILE_SIZE, 14 * TILE_SIZE,
            1 * TILE_SIZE, 29 * TILE_SIZE,
            tipo="chase", hp=1
        ))
