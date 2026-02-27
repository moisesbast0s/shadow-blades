from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE

class Level3(BaseLevel):
    """
    FASE 3 - PONTE SUSPENSA (Nobre)
    Inimigos: 3
    """
    def __init__(self):
        super().__init__()
        
        # Carrega o background da Fase 3
        self.load_background("assets/images/backgrounds/bg_level3.png")
        
        # Layout da fase reformulado com mais pontes suspensas
        layout = [
            "                              ",  # 0
            "                              ",  # 1
            "                              ",  # 2
            "          ########            ",  # 3 (Ponte Alta - Checkpoint/Chave aqui!)
            "                              ",  # 4
            "                              ",  # 5
            "    ####            ####      ",  # 6 (Pontes médias)
            "                              ",  # 7
            "                              ",  # 8
            "        ############          ",  # 9 (Ponte central)
            "                              ",  # 10
            "  RR                      RR  ",  # 11 (Plataformas laterais)
            "                              ",  # 12
            "                              ",  # 13
            "                              ",  # 14
            "##############################",  # 15 (Chão com um buraco grande no meio)
        ]
        
        tile_types = {
            "#": "stone",
            "R": "rock",
        }
        
        self.criar_mapa(layout, tile_types)
        
        # Posições iniciais do jogador
        self.player_start = (2 * TILE_SIZE, 14 * TILE_SIZE) # Inicia no chão à esquerda
        
        # --- CHECKPOINT / CHAVE ---
        # Colocando a chave em cima da ponte suspensa mais alta (linha 3, no meio)
        self.key.add(Key(14 * TILE_SIZE, 2 * TILE_SIZE)) 
        
        # --- ADICIONANDO OS 3 NINJAS COM LIMITES DE PATRULHA ATUALIZADOS ---
        # Formato: Enemy(pos_x, pos_y, limite_esquerda, limite_direita)
        
        # Ninja 1: Ponte central suspensa, linha 9 (patrulha cols 8-19)
        self.enemies.add(Enemy(
            12 * TILE_SIZE, 8 * TILE_SIZE,
            8 * TILE_SIZE, 19 * TILE_SIZE,
            tipo="patrol", hp=2
        ))

        # Ninja 2: Chão — perseguidor (cobre todo o chão)
        self.enemies.add(Enemy(
            26 * TILE_SIZE, 14 * TILE_SIZE,
            1 * TILE_SIZE, 29 * TILE_SIZE,
            tipo="chase", hp=2
        ))

        # Ninja 3: Ponte média esquerda, linha 6 — guarda (cols 4-7)
        self.enemies.add(Enemy(
            5 * TILE_SIZE, 5 * TILE_SIZE,
            4 * TILE_SIZE, 7 * TILE_SIZE,
            tipo="guard", hp=1
        ))

