from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE

class Level5(BaseLevel):
    """
    FASE 5 - O CASTELO FINAL (Gabriel)
    Inimigos: 5 (Mistura de Patrulha e Perseguição)
    """
    def __init__(self):
        super().__init__()
        
        # MUDANDO O CENÁRIO: Certifique-se que essa imagem existe na pasta backgrounds
        self.load_background("assets/images/backgrounds/bg_level5.png")
        
        # LAYOUT NOVO (Diferente da Fase 1 e 2)
        layout = [
            "                                    ",  # 0
            "    K                               ",  # 1 (Chave no topo esquerdo)
            "  #####                             ",  # 2
            "                                    ",  # 3
            "             #######                ",  # 4 (Plataforma central)
            "                                    ",  # 5
            "      ####             ####         ",  # 6
            "                                    ",  # 7
            "               ###                  ",  # 8
            "    ####                 ####       ",  # 9
            "                                    ",  # 10
            "           #######                  ",  # 11
            "  ###                               ",  # 12
            "                                ### ",  # 13
            "                                    ",  # 14
            "####################################",  # 15 (Chão)
        ]
        
        tile_types = {"#": "stone"}
        self.criar_mapa(layout, tile_types)
        
        # Jogador começa na direita para dificultar
        self.player_start = (30 * TILE_SIZE, 14 * TILE_SIZE)
        
        # POSICIONANDO A CHAVE
        self.key.add(Key(4 * TILE_SIZE, 1 * TILE_SIZE))
        
        # --- ADICIONANDO OS 5 INIMIGOS ---
        
        # 1. Patrulha no chão (metade esquerda)
        self.enemies.add(Enemy(
            10 * TILE_SIZE, 14 * TILE_SIZE,
            1 * TILE_SIZE, 18 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # 2. Perseguidor no chão (metade direita com overlap)
        self.enemies.add(Enemy(
            22 * TILE_SIZE, 14 * TILE_SIZE,
            14 * TILE_SIZE, 35 * TILE_SIZE,
            tipo="chase", hp=2
        ))

        # 3. Patrulha na plataforma central (linha 4, cols 13-19)
        self.enemies.add(Enemy(
            15 * TILE_SIZE, 3 * TILE_SIZE,
            13 * TILE_SIZE, 20 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # 4. Guarda na plataforma esquerda (linha 9, cols 4-7)
        self.enemies.add(Enemy(
            6 * TILE_SIZE, 8 * TILE_SIZE,
            4 * TILE_SIZE, 8 * TILE_SIZE,
            tipo="guard", hp=2
        ))

        # 5. Saltador no chão — cobre todo o mapa
        self.enemies.add(Enemy(
            8 * TILE_SIZE, 14 * TILE_SIZE,
            1 * TILE_SIZE, 35 * TILE_SIZE,
            tipo="jumper", hp=3
        ))