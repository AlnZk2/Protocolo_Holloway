# 💻 ctOS v2.0 - Protocolo Holloway

Um protótipo iterativo e interativo inspirado no universo de *Watch Dogs*, projetado para simulações de invasão urbana, controle de câmeras, interceptação de chamadas/mensagens e manipulação de infraestrutura ctOS em tempo real.

---

## 🚀 Funcionalidades Principais

- **Vigilância por Câmera em Tempo Real (OpenCV & MediaPipe):**
  - Detecção facial precisa com visualizador no estilo "visão noturna/hack".
  - Status dinâmico: exibe **`IDENTIFICANDO...`** até que o perfil seja hackeado no menu do celular, atualizando para **`TARGET: AlnZk2 | Desenvolvedor`**.
- **Interface Hacker Mobile (Tkinter & Threads):**
  - **Identificação Profiler:** Coleta de dados do alvo (Nome, Ocupação, Telefone).
  - **Vetores de Distração:** Pop-ups simulados de chamada telefônica, chat de SMS e injeção de e-mails SPAM.
- **Controle de Infraestrutura Urbana:**
  - Manipulação de semáforos, alarmes de veículos e rede de iluminação pública.
- **Terminal de Laptop Avançado:**
  - Minigame de alinhamento de frequência e bypass de firewall.
  - Invasão de feeds de câmeras (Padrão e Circuito Fechado).
  - Interceptação de nós de rede e antena urbana.

---

## 🛠️ Bibliotecas de Funcionalidade (Python)

- **`opencv-python`**: Processamento de vídeo em tempo real e renderização do feed da câmera.
- **`mediapipe`**: Detecção facial avançada via inteligência artificial.
- **`numpy`**: Operações matriciais e geração de ruído térmico na imagem da webcam.
- **`ffpyplayer`**: Reprodução de vídeos (`.mp4`) com sincronização de áudio para os módulos de mídia.
- **`tkinter`**: Interface gráfica nativa (GUI) para os aplicativos simulados do smartphone e janelas pop-up.

---

## 🐧 Guia de Instalação e Execução — LINUX (Ubuntu / Debian)

### Opção A: Instalação Direta no Sistema
Copie e cole o bloco abaixo no terminal para atualizar o sistema, instalar as dependências e executar o projeto:

```sudo apt update && sudo apt install -y python3-pip python3-tk python3-opencv ffmpeg libsm6 libxext6 && pip3 install opencv-python mediapipe numpy ffpyplayer && python3 main.py```

### Opção B: Instalação via Ambiente Virtual (VENV)
Caso prefira rodar em um ambiente isolado:

```sudo apt update && sudo apt install -y python3-pip python3-tk python3-venv python3-opencv ffmpeg libsm6 libxext6 && python3 -m venv venv && source venv/bin/activate && pip install opencv-python mediapipe numpy ffpyplayer && python3 main.py```

---

## 🪟 Guia de Instalação e Execução — WINDOWS

### Pré-requisitos
- Ter o **Python 3.8 ou superior** instalado.
- Certifique-se de ter marcado a opção **"Add Python to PATH"** na instalação do Python.

### Instalação e Execução
Abra o **Prompt de Comando (CMD)** ou **PowerShell** e execute:

```pip install opencv-python mediapipe numpy ffpyplayer && python main.py```

---

## 👤 Créditos
Desenvolvido por **AlnZk2 | Desenvolvedor**.
