# levels/level_2.py
from levels.base_level import BaseLevel, Key
from entities.enemy import Enemy
from settings import TILE_SIZE


class Level2(BaseLevel):
    """
    FASE 2 - FLORESTA SOMBRIA
    Dificuldade: ★★☆☆☆☆
    Inimigos: 2 (1 Patrol + 1 Chase)
    Objetivo: Introduzir inimigo patrulha
    """
    def __init__(self):
        super().__init__()
        
        self.load_background("assets/images/backgrounds/bg_level2.png")
        
        layout = [
            "                                    ",  # 0
            "                                    ",  # 1
            "                                    ",  # 2
            "                                ### ",  # 3 - chave aqui
            "                                    ",  # 4
            "                        ####        ",  # 5
            "                                    ",  # 6
            "              ####                  ",  # 7
            "                                    ",  # 8
            "        ###                     ##  ",  # 9
            "                                    ",  # 10
            "                    ###             ",  # 11
            "    ##                              ",  # 12
            "                          ##        ",  # 13
            "                                    ",  # 14
            "####################################",  # 15
        ]
        
        tile_types = {"#": "stone"}
        
        self.criar_mapa(layout, tile_types)
        self.player_start = (2 * TILE_SIZE, 14 * TILE_SIZE)
        
        # ✅ CHAVE CORRIGIDA - na plataforma da linha 3, coluna 32
        # O layout tem 36 colunas (contando os espaços), então coluna 32 está OK
        # Mas vamos colocar um pouco mais acima das plataformas da linha 3
        self.key.add(Key(32 * TILE_SIZE, 2 * TILE_SIZE + 10))
        
        # Debug para verificar
        print(f"DEBUG Fase 2:")
        print(f"  Chave posicionada em: x={32 * TILE_SIZE}, y={2 * TILE_SIZE + 10}")
        print(f"  Largura do layout: {len(layout[0])} colunas")
        
        # INIMIGOS (2)
        # 1. Patrulha lenta no início
        self.enemies.add(Enemy(
            8 * TILE_SIZE, 14 * TILE_SIZE,
            4 * TILE_SIZE, 12 * TILE_SIZE,
            tipo="patrol"
        ))
        
        # 2. Perseguidor mais rápido no meio-fim
        self.enemies.add(Enemy(
            25 * TILE_SIZE, 14 * TILE_SIZE,
            15 * TILE_SIZE, 34 * TILE_SIZE,
            tipo="chase"
        ))
