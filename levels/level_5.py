    # levels/level_1.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE

class Level5(BaseLevel):
    def __init__(self):
        super().__init__()
        
        self.load_background("assets/images/backgrounds/bg_level1.png")
        
        # Escada GRADUAL e ALCANÇÁVEL - cada degrau tem apenas 2 tiles de altura
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "                              ",  # 2
            "                              ",  # 3
            "                              ",  # 4 - chave no topo
            "                              ",  # 5
            "                              ",  # 6
            "                ###           ",  # 7 - apenas 2 tiles acima
            "                              ",  # 8
            "                              ",  # 9 - apenas 2 tiles acima
            "                              ",  # 10
            "                              ",  # 11 - apenas 2 tiles acima
            "                              ",  # 12
            "                              ",  # 13 - plataformas próximas
            "                              ",  # 14
            "##############################",  # 15 - chão
        ]
        
        tile_types = {"#": "stone"}
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        self.key.add(Key(10 * TILE_SIZE, 14 * TILE_SIZE - 10)) # Posição da chave Coluna 10, Linha 13
        
       