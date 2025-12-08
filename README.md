# 💥 Space Survivor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame Zero](https://img.shields.io/badge/Engine-Pygame%20Zero-red)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

**Space Survivor** é um jogo 2D de sobrevivência desenvolvido em Python utilizando a biblioteca **Pygame Zero**. O objetivo é simples: controlar o **Player** e sobreviver o maior tempo possível evitando as **Threats** (ameaças) que perseguem o jogador implacavelmente.

## 🎮 Funcionalidades

- **Movimentação:** Controle o personagem usando as setas do teclado ou W/A/S/D.
- **Sistema de Ameaças:** Inimigos ("Threats") com IA de perseguição básica que aumentam em número conforme o tempo passa.
- **Pontuação Progressiva:** O score aumenta baseado no tempo de sobrevivência.
- **Interface de Menu:** Menu inicial com opções de Iniciar, Controle de Som e Sair.
- **Animação de Sprites:** O jogador possui animação de corrida e estado "idle".

## 🛠️ Pré-requisitos

Para rodar este projeto, você precisa ter o **Python** instalado e a biblioteca **Pygame Zero**.

```bash
pip install -r requirements.txt
```

## 📂 Estrutura de Arquivos

Para que o jogo funcione corretamente, é essencial que as imagens estejam na pasta `images` e os sons na pasta `sounds`.

```text
/
├── game.py    # Código principal do jogo
├── README.md            
├── images/              # Pasta para sprites
│   ├── player_idle.png
│   ├── player_run1.png
│   ├── player_run2.png
│   ├── threat.png       
│   ├── btn_start.png
│   ├── btn_sound.png
│   └── btn_exit.png
└── sounds/              # Pasta opcional para áudio
    ├── music.mp3
    └── hit.wav
```

## 🚀 Como Executar

1.  Clone este repositório ou baixe os arquivos preservando a estrutura de pastas.
2.  Abra o terminal na pasta do projeto e execute:

```bash
pgzrun game.py
```

## 🕹️ Controles

| Tecla | Ação |
| :--- | :--- |
| **W / Seta Cima** | Mover para Cima |
| **S / Seta Baixo** | Mover para Baixo |
| **A / Seta Esquerda** | Mover para Esquerda |
| **D / Seta Direita** | Mover para Direita |
| **Mouse (Clique)** | Interagir com Botões do Menu |

## 🧠 Lógica do Código

O projeto segue os princípios de Orientação a Objetos:

  - **Classe `Player`:** Gerencia a posição, colisão e animação do personagem.
  - **Classe `Threat`:** Gerencia o comportamento de perseguição (`chase logic`) utilizando vetores para calcular a direção do jogador.

## 📝 Autor

Desenvolvido por **Flávia Jesus**.

