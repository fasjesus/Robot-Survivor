# 💥 Robot Survivor 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame Zero](https://img.shields.io/badge/Engine-Pygame%20Zero-red)
![Status](https://img.shields.io/badge/Status-Finalizado-green)

**Robot Survivor** é um jogo do gênero **Roguelike** desenvolvido em Python utilizando a engine **Pygame Zero**. O jogo apresenta uma mecânica de movimentação baseada em grade (grid-based), onde o jogador deve navegar por um mapa, evitar inimigos com inteligência artificial de perseguição e alcançar a saída.

## 🎮 Funcionalidades

- **Sistema de Turnos:** Os inimigos só se movem quando o jogador se move, permitindo planejamento estratégico.
- **Movimentação em Grade:** Movimento preciso tile-a-tile com animação suave (smooth movement).
- **Animação de Sprites:** Personagens possuem animações distintas para os estados "Idle" (Parado/Respirando) e "Walk" (Andando).
- **Áudio Imersivo:** - Trilha sonora de fundo (BGM) em loop.
  - Efeitos sonoros (SFX) para passos, vitórias, derrotas e cliques.
  - Botão Mute no menu.
- **Level Design:** Mapa construído dinamicamente a partir de uma matriz de texto.

## 🛠️ Pré-requisitos

Para rodar este projeto, você precisa ter o **Python 3.11** instalado (importante: a versão 3.14 não funciona para esse projeto).

As dependências principais são:
- `pgzero`
- `pygame` (apenas para usar o Rect)

## 📂 Estrutura de Arquivos

A estrutura de pastas é **estrita** devido aos requisitos do Pygame Zero. Certifique-se de que os arquivos estejam organizados desta forma:

```text
/
├── requirements.txt      # Dependências (pgzero)
├── game.py               # Código principal (Lógica, Classes, Loops)
├── README.md             
├── images/               # Sprites 
│   ├── character_robot_idle.png
│   ├── character_robot_walk0.png
│   ├── character_zombie_idle.png
│   ├── block_06.png
│   └── ... (outros assets visuais)
├── sounds/               # Efeitos sonoros curtos (.ogg)
│   ├── click.ogg
│   ├── hit.ogg
│   ├── victory.ogg
│   └── gameover.ogg
└── music/                # Música de fundo longa
    └── music.ogg
```
## 🚀 Como Executar

Clone o repositório ou baixe os arquivos.Abra o terminal na pasta raiz do projeto.
Passo 1: Criar e ativar o ambiente virtual (Recomendado)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
```
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```
Passo 2: Instalar dependências
```bash
pip install -r requirements.txt
```
Passo 3: Rodar o jogo
```bash
pgzrun game.py
```
## 🕹️ Controles/Tecla 
Setas: move o personagem (Cima, Baixo, Esq, Dir)
Mouse (Clique): Interagir com botões do Menu (Start, Sound, Exit)
Espaço (Space): Voltar ao Menu após Vitória ou Game Over🧠 

## 🧠 Lógica do Código
O projeto utiliza Programação Orientada a Objetos (POO):

Classe GameSprite(Actor): Classe mãe que gerencia a lógica comum a todos os personagens, como interpolação de movimento (para não "pular" de um quadrado para outro instantaneamente) e o sistema de animação de frames.

Classe Player: Herda de GameSprite. Implementa a lógica de colisão com paredes e detecção de vitória.

Classe Enemy: Herda de GameSprite. Implementa uma IA simples que calcula a distância até o jogador e tenta encurtá-la a cada turno.

Sistema de Mapa: O mapa é renderizado iterando sobre a lista MAP_LAYOUT, onde:

W = Parede (Wall)

P = Ponto de partida do Jogador

E = Inimigo (Enemy)

X = Saída/Objetivo

## Autoria
Desenvolvido por Flávia Jesus.
