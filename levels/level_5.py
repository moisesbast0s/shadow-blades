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
        
        # 1. Guarda do Chão (Esquerda)
        self.enemies.add(Enemy(10 * TILE_SIZE, 14 * TILE_SIZE, 2 * TILE_SIZE, 15 * TILE_SIZE, tipo="patrol"))
        
        # 2. Perseguidor no Chão (Direita)
        self.enemies.add(Enemy(20 * TILE_SIZE, 14 * TILE_SIZE, 15 * TILE_SIZE, 34 * TILE_SIZE, tipo="chase"))
        
        # 3. Patrulha na plataforma central (Linha 4)
        self.enemies.add(Enemy(15 * TILE_SIZE, 3 * TILE_SIZE, 13 * TILE_SIZE, 20 * TILE_SIZE, tipo="patrol"))
        
        # 4. Guarda da escada (Linha 9)
        self.enemies.add(Enemy(5 * TILE_SIZE, 8 * TILE_SIZE, 4 * TILE_SIZE, 8 * TILE_SIZE, tipo="patrol"))
        
        # 5. O SEGUNDO PERSEGUIDOR (Perto da Chave)
        self.enemies.add(Enemy(10 * TILE_SIZE, 5 * TILE_SIZE, 2 * TILE_SIZE, 12 * TILE_SIZE, tipo="chase"))

        print("DEBUG: Fase 5 do Gabriel carregada com 5 inimigos!")