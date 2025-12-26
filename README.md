# GAME DESIGN DOCUMENT (GDD)
## Lâminas das Sombras (Shadow Blades)

**Versão**: 1.0  
**Data**: 26 de dezembro de 2025  
**Status**: Beta - Funcional, aguardando ajustes finais

**Desenvolvedores**: 

---

## 1. VISÃO GERAL (High Concept)

**Lâminas das Sombras** é um jogo de plataforma 2D de ação onde você controla um Cavaleiro Templário preso em território hostil, enfrentando ninjas traiçoeiros para encontrar o caminho de volta para casa.

### Pitch (150 caracteres)
*"Cavaleiro Templário vs Ninjas. Sobreviva, lute e escape da fortaleza das sombras neste jogo de plataforma 2D cheio de ação."*

---

## 2. PILARES DO JOGO

### 2.1 Meta (Objetivo)
Sobreviver aos ataques dos ninjas, atravessar 3 fases perigosas e escapar da fortaleza inimiga com vida.

### 2.2 Dinâmica Central
- **Exploração**: Navegar por plataformas, evitar armadilhas e encontrar a chave de saída
- **Combate**: Enfrentar ninjas ágeis usando espada corpo a corpo
- **Sobrevivência**: Gerenciar 5 pontos de vida através de 3 fases consecutivas

### 2.3 Mecânicas (Regras)
- **Sistema de Vidas**: 5 HP que persistem entre fases (não resetam)
- **Combate por proximidade**: Ataque corpo a corpo com hitbox direcional
- **Invulnerabilidade temporária**: 2 segundos após receber dano
- **Morte dos inimigos**: Ninjas morrem com 1 golpe, mas atacam em grupo
- **Progressão linear**: Fase 1 → Fase 2 → Fase 3 → Vitória

---

## 3. GAMEPLAY E MECÂNICAS

### 3.1 Controles

| Ação | Tecla | Descrição |
|------|-------|-----------|
| Mover Esquerda | A / ← | Move o cavaleiro para esquerda |
| Mover Direita | D / → | Move o cavaleiro para direita |
| Pular | ESPAÇO / W / ↑ | Pula (só no chão) |
| Atacar | J | Golpe de espada com alcance médio |
| Pausar | ESC | Volta ao menu principal |

### 3.2 Ações do Personagem

#### Movimentação
- **Velocidade**: Média (mais pesado que os ninjas)
- **Pulo**: Alcance vertical médio, realista
- **Gravidade**: Peso consistente, sem "pulo flutuante"

#### Combate
- **Ataque básico**: Golpe de espada horizontal
- **Alcance**: 80px à frente do personagem
- **Duração**: 0.5 segundos de animação
- **Cooldown**: Pode atacar novamente após animação terminar
- **Hitbox**: 80x60 pixels, muda de lado conforme direção

#### Sistema de Dano
- **HP Total**: 5 pontos
- **Dano por hit**: 1 HP
- **Invulnerabilidade**: 2 segundos após sofrer dano (pisca vermelho)
- **Knockback**: Empurrado 70px para trás ao ser atingido
- **Morte**: HP chega a 0 → Game Over

### 3.3 Visão do Jogador
- **Câmera lateral**: Segue o player horizontalmente
- **Centralização**: Player sempre no centro da tela (quando possível)
- **Limites**: Câmera não ultrapassa bordas do mapa (1200px de largura)

### 3.4 Sistema de Progressão

#### Estrutura das Fases
1. **Fase 1 - Ruínas do Templo**: Tutorial implícito, 2-3 ninjas, plataformas simples
2. **Fase 2 - Jardim de Bambu**: 5-6 ninjas, plataformas mais altas, buracos
3. **Fase 3 - Telhados da Fortaleza**: 8+ ninjas, plataformas complexas, ninja boss (3 HP)

#### Condições de Vitória (por fase)
- Coletar a **chave** ao final do mapa
- Transição automática após 0.5 segundos
- **HP é mantido** para a próxima fase

#### Condições de Derrota
- HP chega a 0
- Cair de plataformas (morte instantânea)

---

## 4. NARRATIVA E PERSONAGENS

### 4.1 História

#### Contexto Histórico
Durante as Cruzadas, um Cavaleiro Templário em missão no Oriente é emboscado e capturado por uma ordem secreta de ninjas. Aprisionado em uma fortaleza remota, ele descobre que a única saída é atravessar três níveis mortais vigiados pelos assassinos das sombras.

#### Narrativa do Jogo
Sem aliados, ferido mas determinado, o cavaleiro deve usar sua espada sagrada e armadura resistente para enfrentar inimigos rápidos e letais. Cada fase representa uma área da fortaleza: as ruínas externas, o jardim interno e os telhados onde o líder ninja aguarda.

#### Tom
Sério mas estilizado. Combate visceral com estética cartunesca (pixel art).

### 4.2 Personagens

#### Player: Cavaleiro Templário
- **Nome**: Cuca Cabeludo
- **Idade**: ~19 anos (Twink)
- **Aparência**: Armadura branca/prata, elmo com pluma vermelha, escudo circular, espada longa
- **Personalidade**: Honrado, corajoso, resiliente
- **Habilidades**:
  - Alta resistência (5 HP)
  - Ataque corpo a corpo forte
  - Mais lento que os ninjas, mas aguenta mais dano
- **Animações**: idle, run, jump, attack, death

#### Inimigos: Ninjas
- **Tipo**: Assassinos orientais
- **Aparência**: Roupa preta/vermelha, máscara, katana
- **Comportamento**:
  - **Patrulha**: Andam entre limites definidos (idle/run)
  - **Detecção**: Alcance de 400px horizontalmente
  - **Perseguição**: Correm em direção ao player quando detectam
  - **Ataque**: Golpe corpo a corpo quando < 60px de distância
- **Fraqueza**: Morrem com 1 golpe
- **Perigo**: Aparecem em grupos, cercam o jogador

#### Boss (Fase 3): Ninja Mestre
- **Diferencial**: 3 HP em vez de 1
- **Velocidade**: 1.5x mais rápido que ninjas normais
- **Alcance de detecção**: 600px
- **Animações**: idle, run, attack, death

---

## 5. ESTILO ARTÍSTICO E SOM

### 5.1 Direção de Arte

#### Estilo Visual
- **Pixel Art Low-Res**: Estilo retrô 16-bit (inspirado em SNES/Genesis)
- **Paleta de Cores**:
  - **Cavaleiro**: Prata/branco, vermelho (pluma), dourado (detalhes)
  - **Ninjas**: Preto, vermelho escuro, cinza
  - **Cenário**: Tons terrosos (marrom, bege), lanternas (amarelo/laranja), vegetação (verde escuro)

#### Ambientação por Fase
1. **Fase 1 - Ruínas**: Pedras antigas, lanternas, céu noturno estrelado
2. **Fase 2 - Jardim**: Bambus, lanternas de papel, ponte de madeira
3. **Fase 3 - Telhados**: Telhas japonesas, lua cheia, silhuetas de montanhas

### 5.2 Interface (UI/UX)

#### HUD (Heads-Up Display)
- **Posição**: Canto superior esquerdo
- **Elementos**:
  - HP: 5 corações (vazios quando perde vida)
  - Fase: "Fase X/3"
  - Controles: Aparecem nos primeiros 5 segundos de cada fase

#### Telas

**1. Menu Inicial**
- Título: "LÂMINAS DAS SOMBRAS"
- Subtítulo: "Shadow Blades"
- História curta (3 linhas)
- Controles
- "Pressione ESPAÇO para começar"

**2. Gameplay**
- HUD minimalista
- Foco no cenário e personagens

**3. Game Over**
- Fundo vermelho escuro
- "DERROTA"
- Mensagem: "Os ninjas das sombras prevaleceram"
- Opções: Tentar de novo / Menu

**4. Vitória**
- Fundo verde escuro
- "VITÓRIA! Missão Cumprida"
- Mensagem: "O cavaleiro encontrou o caminho de volta"
- Opções: Jogar de novo / Menu

### 5.3 Trilha Sonora e Efeitos

#### Música
- **Menu**: Tema épico medieval com toques orientais
- **Fase 1**: Tensão crescente, bateria suave
- **Fase 2**: Intensifica, adiciona shamisen (instrumento japonês)
- **Fase 3/Boss**: Combate intenso, taiko drums, cordas dramáticas
- **Vitória**: Fanfarra heroica
- **Game Over**: Melodia melancólica com sino

#### Efeitos Sonoros

**Player:**
- Passos pesados (metal batendo)
- Golpe de espada (whoosh + impacto)
- Pulo (esforço vocal + vento)
- Receber dano (grito + metal)
- Morte (queda dramática)

**Ninjas:**
- Passos leves/rápidos
- Whoosh ao correr
- Golpe rápido
- Morte (grito curto)

**Ambiente:**
- Vento suave
- Lanternas crepitando
- Bambu balançando (Fase 2)

---

## 6. ASPECTOS TÉCNICOS

### 6.1 Plataforma de Publicação
- **Primária**: PC (Windows, Linux, Mac)
- **Futura**: Possível port para Web (HTML5 via Pygbag)
- **Não planejado**: Mobile, Consoles

### 6.2 Público-Alvo
- **Idade**: 10+ anos (violência cartunesca, sem sangue)
- **Perfil**: Jogadores casuais a medianos que curtem:
  - Jogos de plataforma 2D
  - Pixel art retrô
  - Combate simples mas desafiador
  - Temática medieval/oriental

### 6.3 Tecnologia Utilizada

#### Engine e Linguagem
- **Engine**: Pygame (Python)
- **Linguagem**: Python 3.x
- **Resolução**: 800x600 pixels
- **FPS**: 60 quadros por segundo


#### Sistemas Implementados
- ✅ Sistema de animação multi-frame
- ✅ Sistema de colisão tile-based
- ✅ Sistema de câmera seguindo player
- ✅ Sistema de HP persistente entre fases
- ✅ IA de inimigos (patrulha + perseguição + ataque)
- ✅ Sistema de invulnerabilidade com feedback visual
- ✅ Sistema de knockback ao receber dano
- ✅ Sistema de estados (Menu/Gameplay/GameOver/Victory)

### 6.4 Requisitos Técnicos

**Mínimos:**
- OS: Windows 7+ / Linux / macOS 10.12+
- Processador: 1.5 GHz
- RAM: 512 MB
- Gráficos: Qualquer placa com OpenGL 2.0+
- Armazenamento: 50 MB

**Dependências:**
- Python 3.8+
- Pygame 2.0+

---

## 7. ESCOPO DO PROJETO

### 7.1 Versão Atual (MVP - Minimum Viable Product)
- ✅ 3 fases jogáveis
- ✅ 1 tipo de inimigo (ninja padrão)
- ✅ Sistema de combate básico
- ✅ Sistema de HP persistente
- ✅ Telas de menu, game over e vitória
- ✅ HUD funcional



## 8. DIFERENCIAL COMPETITIVO

### O que torna "Lâminas das Sombras" único?

1. **Contraste de estilos**: Cavaleiro pesado/resistente VS ninjas ágeis/frágeis
2. **HP persistente**: Decisões táticas importam (não resetar entre fases aumenta tensão)
3. **Estética única**: Mistura de medieval europeu com oriental (cruzadas + ninjas)
4. **Pixel art polido**: Animações fluidas, paleta coesa
5. **Curva de dificuldade equilibrada**: Fases curtas mas desafiadoras

---

## 9. CRONOGRAMA DE DESENVOLVIMENTO

| Fase | Duração | Tarefas | Status |
|------|---------|---------|--------|
| **Protótipo** | 2 semanas | Movimento básico, 1 fase, colisões | ✅ Concluído |
| **Alpha** | 3 semanas | 3 fases, inimigos, combate, animações | ✅ Concluído |
| **Beta** | 2 semanas | Telas, HUD, polish, balanceamento | ✅ Concluído |
| **Polish** | 1 semana | Som, efeitos visuais, correções | 🔄 Em andamento |
| **Release** | - | Publicação no itch.io / GitHub | ⏳ Planejado |

---

## 10. EQUIPE E CRÉDITOS

**Game Designer & Programador**: Moises
**Artista de Sprites**: [Fonte dos assets ou "Stock Assets"]  
**Engine**: Pygame (Python)  
**Inspirações**: Hollow Knight, Dead Cells, Shovel Knight, Mark of the Ninja

---

## 11. CONTATO E LINKS

- **GitHub**: [teste]
- **Itch.io**: [testes]
- **Email**: [teste]

---

**Documento criado em**: 26 de dezembro de 2025  
**Versão**: 1.0  
**Status do Projeto**: Beta - Funcional, aguardando polish final

---

## Notas de Desenvolvimento

### Changelog
- **26/12/2025**: Criação do documento inicial
- Sistema de vidas persistentes implementado
- Telas atualizadas com novo tema
- 6 fases jogáveis completas

### Próximos Passos
1. Adicionar sistema de som
2. Adicionar partículas e polish visual
3. Testes de balanceamento
4. Preparar para publicação
