# levels/level_6.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE


class Level6(BaseLevel):
    """
    FASE 6 - TELHADOS (noite)
    Inimigos: 6
    Objetivo: Escalar plataformas e pegar a chave no topo.
    """
    def __init__(self):
        super().__init__()

        # Background
        self.load_background("assets/images/backgrounds/bg_level6.png")

        # Layout (30 colunas x 16 linhas)
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "                      ###     ",  # 2 (plataforma da chave)
            "                              ",  # 3
            "                   #####      ",  # 4
            "                              ",  # 5
            "                 #######      ",  # 6
            "                              ",  # 7
            "           #####              ",  # 8
            "                              ",  # 9
            "        ######        ####    ",  # 10
            "                              ",  # 11
            "     #####        #####       ",  # 12
            "                              ",  # 13
            "  ######    ######    ######  ",  # 14 (telhados baixos)
            "##############################",  # 15 (chão)
        ]

        tile_types = {"#": "stone"}

        self.criar_mapa(layout, tile_types)

        # Posição inicial do jogador
        self.player_start = (2 * TILE_SIZE, 14 * TILE_SIZE)

        # Chave (em cima da plataforma da linha 2)
        self.key.add(Key(23 * TILE_SIZE, 2 * TILE_SIZE - 20))

        # Inimigos (6 ninjas)
        # Formato: Enemy(x, y, limite_esq, limite_dir, tipo="chase")
        # y recomendado: (linha_da_plataforma - 1) * TILE_SIZE

        # 1) Patrulha no chão — cobre todo o chão
        self.enemies.add(Enemy(
            4 * TILE_SIZE, 14 * TILE_SIZE,
            1 * TILE_SIZE, 29 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # 2) Guarda no telhado baixo central (linha 14, cols 12-17)
        self.enemies.add(Enemy(
            14 * TILE_SIZE, 13 * TILE_SIZE,
            2 * TILE_SIZE, 28 * TILE_SIZE,
            tipo="guard", hp=2
        ))

        # 3) Patrulha na plataforma da linha 12 (esquerda, cols 5-9)
        self.enemies.add(Enemy(
            6 * TILE_SIZE, 11 * TILE_SIZE,
            5 * TILE_SIZE, 10 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # 4) Perseguidor na plataforma da linha 10 (cols 8-13)
        self.enemies.add(Enemy(
            9 * TILE_SIZE, 9 * TILE_SIZE,
            8 * TILE_SIZE, 14 * TILE_SIZE,
            tipo="chase", hp=3
        ))

        # 5) Saltador na plataforma da linha 8 (cols 11-15)
        self.enemies.add(Enemy(
            12 * TILE_SIZE, 7 * TILE_SIZE,
            11 * TILE_SIZE, 16 * TILE_SIZE,
            tipo="jumper", hp=3
        ))

        # 6) Perseguidor na plataforma alta da linha 6 (cols 17-23)
        self.enemies.add(Enemy(
            19 * TILE_SIZE, 5 * TILE_SIZE,
            17 * TILE_SIZE, 24 * TILE_SIZE,
            tipo="chase", hp=3
        ))
