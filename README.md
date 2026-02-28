# GAME DESIGN DOCUMENT (GDD)
## Lâminas das Sombras (Shadow Blades)


**Desenvolvedores**: 

[Moises Bastos](https://github.com/moisesbast0s)\
[Hebert Vinicius](https://github.com/Hebert-Sanches)\
[Vinicius Nobre](https://github.com/Viniciusnobre23)\
[Luiz Vinicius Maia](https://github.com/LuizViniciusMaia)\
[Joao Gabriel](https://github.com/gabriielcst)\
[Adeilson Dorneles](https://github.com/Ade1lson)

---

## 1. VISÃO GERAL 

**Lâminas das Sombras** é um jogo de plataforma 2D de ação onde você controla um Cavaleiro Templário preso em território hostil, enfrentando ninjas traiçoeiros para encontrar o caminho de volta para casa.

---

## 2. PILARES DO JOGO

### 2.1 Meta (Objetivo)
Sobreviver aos ataques dos ninjas, atravessar 6 fases perigosas e escapar da fortaleza inimiga com vida.

### 2.2 Dinâmica Central
- **Exploração**: Navegar por plataformas, evitar armadilhas e encontrar a chave de saída
- **Combate**: Enfrentar ninjas ágeis usando espada corpo a corpo
- **Sobrevivência**: Gerenciar 5 pontos de vida através de 6 fases consecutivas

### 2.3 Mecânicas (Regras)
- **Sistema de Vidas**: 5 HP que persistem entre fases (não resetam)
- **Combate por proximidade**: Ataque corpo a corpo com hitbox direcional
- **Invulnerabilidade temporária**: 2 segundos após receber dano
- **Morte dos inimigos**: Ninjas morrem com 1-3 golpes dependendo do tipo e fase
- **Progressão linear**: Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 5 → Fase 6 → Vitória

---

## 3. GAMEPLAY E MECÂNICAS

### 3.1 Controles

| Ação | Tecla | Descrição |
|------|-------|-----------|
| Mover Esquerda | A / ← | Move o cavaleiro para esquerda |
| Mover Direita | D / → | Move o cavaleiro para direita |
| Pular | ESPAÇO / W / ↑ | Pula |
| Atacar | J | Golpe de espada com alcance curto |
| Pausar | ESC | Pausa o jogo  |
| Sair | Q | Fecha o jogo (funciona em qualquer tela) |

### 3.2 Ações do Personagem

#### Movimentação
- **Velocidade**: 4 px/frame (mais pesado que os ninjas)
- **Pulo**: Força de -15, alcance vertical médio
- **Gravidade**: 0.5 por frame, velocidade terminal de 10 px/frame

#### Combate
- **Ataque básico**: Golpe de espada horizontal
- **Hitbox de ataque**: 30×35 pixels à frente do personagem
- **Duração**: 0.5 segundos de animação
- **Cooldown**: Pode atacar novamente após animação terminar
- **Direção**: Hitbox muda de lado conforme direção do jogador

#### Sistema de Dano
- **HP Total**: 5 pontos
- **Dano por hit**: 1 HP
- **Invulnerabilidade**: 2 segundos após sofrer dano (pisca vermelho/transparente)
- **Cooldown por inimigo**: 2 segundos — o mesmo inimigo não pode causar dano consecutivo
- **Morte**: HP chega a 0 → Game Over

### 3.3 Visão do Jogador
- **Câmera lateral**: Segue o player horizontalmente
- **Limites**: Câmera não ultrapassa bordas do mapa (varia por fase: 1200px ou 1440px)

### 3.4 Sistema de Progressão

#### Estrutura das Fases

| Fase | Nome | Dificuldade | Inimigos | Tipos |
|------|------|-------------|----------|-------|
| 1 | Tutorial | ★☆☆☆☆☆ | 1 | Chase |
| 2 | Floresta Sombria | ★★☆☆☆☆ | 2 | Patrol + Chase |
| 3 | Ponte Suspensa | ★★★☆☆☆ | 3 | Patrol + Chase + Guard |
| 4 | Cavernas Subterrâneas | ★★★★☆☆ | 4 | Patrol ×2 + Chase + Jumper |
| 5 | Castelo Final | ★★★★★☆ | 5 | Patrol + Chase + Guard + Jumper ×2 |
| 6 | Telhados | ★★★★★★ | 6 | Patrol ×2 + Chase ×2 + Guard + Jumper |

#### Condições de Vitória (por fase)
- Coletar a **chave dourada** posicionada no mapa
- Transição automática para próxima fase
- **HP é mantido** para a próxima fase (não reseta)

#### Condições de Derrota
- HP chega a 0
- Cair de plataformas (morte instantânea)

---

## 4. NARRATIVA E PERSONAGENS

### 4.1 História

#### Contexto Histórico
Durante as Cruzadas, um Cavaleiro Templário em missão no Oriente é emboscado e capturado por uma ordem secreta de ninjas. Aprisionado em uma fortaleza remota, ele descobre que a única saída é atravessar seis níveis mortais vigiados pelos assassinos das sombras.

#### Narrativa do Jogo
Sem aliados, ferido mas determinado, o cavaleiro deve usar sua espada sagrada e armadura resistente para enfrentar inimigos rápidos e letais. Cada fase representa uma área diferente da fortaleza: ruínas externas, floresta sombria, pontes suspensas, cavernas subterrâneas, o castelo principal e os telhados onde a fuga final acontece.

#### Tom
Sério mas estilizado. Combate visceral com estética cartunesca (pixel art).

### 4.2 Personagens

#### Player: Cavaleiro Templário
- **Aparência**: Armadura branca/prata, elmo com pluma vermelha, escudo circular, espada longa
- **Personalidade**: Honrado, corajoso, resiliente
- **Habilidades**:
  - Alta resistência (5 HP)
  - Ataque corpo a corpo forte (hitbox 30×35)
  - Mais lento que os ninjas, mas aguenta mais dano
- **Animações**: idle, run, jump, attack, death

#### Inimigos: Ninjas (4 Tipos de Comportamento)

**Atributos Gerais:**
- Aparência: Roupa preta/vermelha, máscara, katana
- Detecção: 350px horizontal, 120px vertical
- Alcance de ataque: 60px
- Todos atacam corpo a corpo quando o player está próximo

| Tipo | Comportamento | Cooldown de Ataque | Descrição |
|------|---------------|-------------------|-----------|
| **Patrol** | Patrulha entre limites, pausa ao virar | 1.8s | Não persegue o player. Previsível mas perigoso em grupo |
| **Chase** | Patrulha + persegue ao detectar | 1.0s | Tipo mais comum. Corre em direção ao player quando detectado |
| **Jumper** | Como chase, mas pula obstáculos | 1.0s | Pode saltar sobre paredes e desníveis para alcançar o player |
| **Guard** | Fica parado, só ataca quando player chega | 0.8s | Guarda posições-chave. Ataque rápido mas imóvel |

**Variação de HP por fase:**
- Fases 1-2: 1 HP (morrem com 1 golpe)
- Fases 3-6: 2-3 HP (exigem mais golpes)

---

## 5. ESTILO ARTÍSTICO E SOM

### 5.1 Direção de Arte

#### Estilo Visual
- **Pixel Art Low-Res**: Estilo retrô 16-bit (inspirado em SNES/Genesis)
- **Fonte**: Press Start 2P (pixel font) em toda a interface
- **Paleta de Cores**:
  - **Cavaleiro**: Prata/branco, vermelho (pluma), dourado (detalhes)
  - **Ninjas**: Preto, vermelho escuro, cinza
  - **Cenário**: Tons terrosos (marrom, bege), lanternas (amarelo/laranja), vegetação (verde escuro)
  - **HUD**: Corações vermelhos, texto dourado

#### Ambientação por Fase
1. **Fase 1 - Tutorial**: Ruínas simples, plataformas básicas, céu noturno
2. **Fase 2 - Floresta Sombria**: Vegetação densa, mapa mais largo (36 colunas)
3. **Fase 3 - Ponte Suspensa**: Pontes em múltiplas alturas, plataformas laterais
4. **Fase 4 - Cavernas Subterrâneas**: Paredes verticais internas, escada gradual
5. **Fase 5 - Castelo Final**: Plataformas dispersas, mapa largo (36 colunas)
6. **Fase 6 - Telhados**: Plataformas em escada ascendente, chave no topo

### 5.2 Interface (UI/UX)

#### HUD (Heads-Up Display)
- **Posição**: Canto superior esquerdo
- **Elementos**:
  - HP: 5 corações pixel art (vazios quando perde vida)
  - Fase: "Fase X/6" (canto superior direito)
  - Controles: Aparecem nos primeiros 5 segundos de cada fase

#### Telas

**1. Menu Inicial**
- Imagem de fundo: pixel art com fortaleza, cavaleiro, ninjas, lua
- Título: "SHADOW BLADES" (pixel font dourada)
- Texto de história + controles
- ESPAÇO para começar / Q para sair

**2. Gameplay**
- HUD minimalista (corações + fase)
- Sistema de pausa com overlay semi-transparente ("PAUSADO")
  - ESC para continuar
  - Q para sair

**3. Game Over**
- Fundo vermelho escuro
- "DERROTA" (pixel font vermelha)
- Mensagem: "Os ninjas das sombras prevaleceram"
- ESPAÇO: tentar de novo / ESC: menu / Q: sair

**4. Vitória**
- Fundo verde escuro
- "VITÓRIA! Missão Cumprida"
- Mensagem: "O cavaleiro encontrou o caminho de volta para casa"
- ESPAÇO: jogar de novo / ESC: menu / Q: sair

### 5.3 Trilha Sonora e Efeitos

#### Sistema de Áudio
- **AudioManager**: Gerenciador centralizado de música e efeitos
- **Músicas**: Geradas proceduralmente (WAV placeholders) por estado (menu, gameplay, gameover, victory)
- **Volume**: Música 40% / SFX 60%

#### Efeitos Sonoros

**Player:**
- Pulo (esforço)
- Golpe de espada (whoosh + impacto)
- Receber dano (impacto)
- Morte (queda)

**Ninjas:**
- Golpe de ataque
- Morte (grito curto)

---

## 6. ASPECTOS TÉCNICOS


### 6.1 Tecnologia Utilizada

#### Engine e Linguagem
- **Engine**: Pygame 2.5.2 (SDL 2.30.0)
- **Linguagem**: Python 3.12
- **Resolução interna**: 1200×800 pixels
- **Resolução da janela**: Escalável (padrão 1.5× = 1800×1200)
- **FPS**: 60 quadros por segundo
- **Tile Size**: 40×40 pixels

#### Arquitetura do Projeto
```
main.py              → Ponto de entrada, inicialização
settings.py          → Constantes globais (resolução, física, áudio)
core/
  game.py            → Loop principal, máquina de estados, escala
  animation.py       → Sistema de animação multi-frame
  asset_loader.py    → Carregamento de assets
  states.py          → Classe base State
entities/
  player.py          → Cavaleiro (movimento, combate, HP)
  enemy.py           → Ninja (4 tipos de IA, patrulha, ataque)
levels/
  base_level.py      → Classe base + Tile + Key (chave coletável)
  level_1.py → 6.py  → Layout e configuração de cada fase
  level_data.py      → Dados auxiliares de level design
  tiles.py           → Tipos de tiles
states/
  menu.py            → Tela de menu inicial
  gameplay.py        → Estado principal (jogo, pausa, colisões)
  gameover.py        → Tela de derrota
  victory.py         → Tela de vitória
ui/
  hud.py             → Interface in-game (corações, fase)
assets/
  fonts/             → Press Start 2P (pixel font)
  images/            → Sprites, backgrounds, UI
  audio/             → Músicas e efeitos (gerados proceduralmente)
```

#### Sistemas Implementados
- ✅ Sistema de animação multi-frame com flip direcional
- ✅ Sistema de colisão tile-based (horizontal + vertical)
- ✅ Sistema de câmera seguindo player com limites de mapa
- ✅ Sistema de HP persistente entre fases
- ✅ IA de inimigos com 4 comportamentos (patrol, chase, jumper, guard)
- ✅ Sistema de invulnerabilidade com feedback visual (pisca)
- ✅ Sistema de knockback ao receber dano
- ✅ Sistema de estados (Menu / Gameplay / GameOver / Victory)
- ✅ Sistema de áudio (AudioManager com música + SFX)
- ✅ Sistema de pausa (ESC toggle) com overlay
- ✅ Sistema de escala proporcional da janela
- ✅ Pixel font (Press Start 2P) em toda interface
- ✅ Chave coletável com animação flutuante
- ✅ Cooldown de ataque por tipo de inimigo
- ✅ Colisão horizontal com tiles (inimigos não atravessam paredes)
- ✅ 6 fases completas com level design único

### 6.2 Requisitos Técnicos

**Mínimos:**
- OS: Windows 7+ / Linux / macOS 10.12+
- Processador: Celeron 1.5 GHz
- RAM: 512 MB
- Gráficos: NVIDIA GeForce RTX 5090
- Armazenamento: 50 MB

**Dependências:**
- Python 3.8+
- Pygame 2.0+

---


## 7. DIFERENCIAL COMPETITIVO

### O que torna "Lâminas das Sombras" único?

1. **Contraste de estilos**: Cavaleiro pesado/resistente VS ninjas ágeis/frágeis
2. **HP persistente**: Decisões táticas importam (não resetar entre fases aumenta tensão)
3. **Estética única**: Mistura de medieval europeu com oriental (cruzadas + ninjas)
4. **4 tipos de IA inimiga**: Cada tipo exige uma estratégia diferente de abordagem
5. **Curva de dificuldade progressiva**: De 1 inimigo simples a 6 ninjas com múltiplos comportamentos


---

## 8. EQUIPE E CRÉDITOS

**Game Designer & Programador**: Todo o grupo  
**Engine**: Pygame (Python)  
**Fonte**: Press Start 2P (Google Fonts - OFL License)  
**Inspirações**: Hollow Knight, Dead Cells, Shovel Knight, Mark of the Ninja



## Notas de Desenvolvimento

### Changelog
- **26/11/2025**: Criação do documento inicial (v1.0)
- **27/02/2026**: Atualização completa do GDD (v2.0)
  - 6 fases jogáveis completas
  - 4 tipos de inimigos implementados (patrol, chase, jumper, guard)
  - Sistema de áudio (AudioManager com música e SFX)
  - Sistema de pausa (ESC toggle) com overlay
  - Pixel font (Press Start 2P) em toda interface
  - Sistema de escala proporcional da janela (ESCALA configurável)
  - Hitbox de ataque refinado (30×35px)
  - Colisão horizontal com tiles para inimigos
  - Chave coletável com animação flutuante
  - Menu com pixel art de fundo
  - Controle Q para sair em qualquer tela
