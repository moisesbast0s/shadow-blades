    # levels/level_4.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE

class Level4(BaseLevel):
    """
    FASE 4 - CAVERNAS SUBTERRÂNEAS
    Dificuldade: ★★★★☆☆
    Inimigos: 4 (2 Patrol + 2 Chase)
    Objetivo: Testar a movimentação
    """
    def __init__(self):
        super().__init__()
        
        self.load_background("assets/images/backgrounds/bg_level4.png")
        
        # Escada GRADUAL e ALCANÇÁVEL - cada degrau tem apenas 2 tiles de altura
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "#   ########################  ",  # 2
            "    #                         ",  # 3
            "    #                         ",  # 4 - chave no topo
            "   ##                         ",  # 5
            "    #                         ",  # 6
            "    #                         ",  # 7 - apenas 2 tiles acima
            "    #       #                 ",  # 8
            "    #       #                 ",  # 9 - apenas 2 tiles acima
            "#   #       #                 ",  # 10
            "    #       #      ###        ",  # 11 - apenas 2 tiles acima
            "    #       #                 ",  # 12
            "    #       #                 ",  # 13 - plataformas próximas
            "    #       #                 ",  # 14
            "##############################",  # 15 - chão
        ]
        
        tile_types = {"#": "rock"}
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (80, 14 * TILE_SIZE)
        self.key.add(Key(10 * TILE_SIZE, 14 * TILE_SIZE - 10)) # Posição da chave Coluna 10, Linha 13
  
        # INIMIGOS (2)
        # 1. Patrulha lenta no início
        self.enemies.add(Enemy(
            8 * TILE_SIZE, 14 * TILE_SIZE,
            4 * TILE_SIZE, 30 * TILE_SIZE,
            tipo="patrol"
        ))
        
        # 2. Perseguidor mais rápido no meio-fim
        self.enemies.add(Enemy(
            8 * TILE_SIZE, 14 * TILE_SIZE,
            4 * TILE_SIZE, 28 * TILE_SIZE,
            tipo="chase"
        ))
        #Patrulha lenta
        self.enemies.add(Enemy(
            20 * TILE_SIZE, 2 * TILE_SIZE,
            4 * TILE_SIZE, 30 * TILE_SIZE,
            tipo="patrol"
        ))
        #Perseguidor mais rápido
        self.enemies.add(Enemy(
            17 * TILE_SIZE, 14 * TILE_SIZE,
            4 * TILE_SIZE, 28 * TILE_SIZE,
            tipo="chase"
        ))