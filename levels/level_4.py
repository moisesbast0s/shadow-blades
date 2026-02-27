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
  
        # INIMIGOS (4) — posições corrigidas, respeitando paredes internas
        # Paredes verticais: col 4 (linhas 2-14), col 12 (linhas 8-14)
        # Seção chão 1: cols 0-3  |  Seção 2: cols 5-11  |  Seção 3: cols 13-29

        # 1. Patrulha na seção 2 (entre paredes col 4 e col 12)
        self.enemies.add(Enemy(
            8 * TILE_SIZE, 14 * TILE_SIZE,
            5 * TILE_SIZE, 12 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # 2. Perseguidor na seção 3 (depois da parede col 12)
        self.enemies.add(Enemy(
            20 * TILE_SIZE, 14 * TILE_SIZE,
            13 * TILE_SIZE, 29 * TILE_SIZE,
            tipo="chase", hp=2
        ))

        # 3. Patrulha na plataforma superior (linha 2, cols 4-27)
        self.enemies.add(Enemy(
            10 * TILE_SIZE, 1 * TILE_SIZE,
            5 * TILE_SIZE, 27 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # 4. Saltador na seção 3 (pode pular sobre a parede col 12)
        self.enemies.add(Enemy(
            25 * TILE_SIZE, 14 * TILE_SIZE,
            13 * TILE_SIZE, 29 * TILE_SIZE,
            tipo="jumper", hp=2
        ))