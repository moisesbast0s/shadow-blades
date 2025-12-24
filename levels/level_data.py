# level/level_data.py
from level.tiles import Tile

TILE_SIZE = 48
LARGURA_MAPA = 20  # tiles

LEVEL_MAP = [
    "...............#####..................",
    "...............#...#..................",
    "...............#####..................",
    "......................................",
    "..........########....................",
    "#################################.....",  # chão na linha 5
]


CHECKPOINTS = [
    (3 * TILE_SIZE, 15 * TILE_SIZE),   # fim da masmorra
    (12 * TILE_SIZE, 8 * TILE_SIZE),   # fim do corredor  
    (18 * TILE_SIZE, 6 * TILE_SIZE),   # pátio final
]

def criar_fase():
    tiles = []
    inimigos_pos = []
    
    # Posição inicial do player - ajuste o Y para estar visível
    # Por exemplo, linha 8 ou 10 em vez de 12
    player_start = (50, 4 * TILE_SIZE)  # em vez de 12 * TILE_SIZE
    
    boss_pos = (18 * TILE_SIZE, 6 * TILE_SIZE)

    # ... resto do código ...


    for linha_idx, linha in enumerate(LEVEL_MAP):
        for col_idx, char in enumerate(linha):
            x = col_idx * TILE_SIZE
            y = linha_idx * TILE_SIZE
            
            if char == "#":
                tiles.append(Tile(x, y, TILE_SIZE, TILE_SIZE))

    # Guardas específicos por área
    inimigos_pos.extend([
        (10*TILE_SIZE, 7*TILE_SIZE),
        (13*TILE_SIZE, 7*TILE_SIZE), 
        (16*TILE_SIZE, 7*TILE_SIZE),
        (18*TILE_SIZE, 6*TILE_SIZE),
    ])
    
    return tiles, inimigos_pos, player_start, boss_pos, CHECKPOINTS
    #                                                    ^^^^^^^^^^^^

