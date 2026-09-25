# 🎬 Mídias e Ativos Visuais — ctOS Framework

Esta pasta destina-se ao armazenamento de ficheiros de vídeo (`.mp4`) utilizados pelos módulos de simulação visual e infraestrutura ctOS (iluminação urbana, alarmes, simulação de eventos e feeds secundários de câmeras).

---

## 📁 Estrutura de Ficheiros Recomendada

Para que o script principal reconheça e reproduza os vídeos automaticamente durante a execução, organiza os ficheiros dentro da pasta `midias/` utilizando a seguinte convenção de nomes:

```text
midias/
├── luz_ligando.mp4       # Ativado ao ligar a iluminação do poste
├── luz_desligando.mp4    # Ativado ao desligar a iluminação do poste
├── alarme_carro.mp4      # Ativado ao acionar o alarme do veículo
└── camera_feed_alt.mp4   # Feed alternativo para câmeras de circuito fechado
```

---

## ⚙️ Especificações Técnicas Recomendadas

Para garantir o melhor desempenho e evitar atrasos (*lag*) na reprodução via `ffpyplayer` e `OpenCV`, recomenda-se codificar os vídeos com as seguintes especificações:

- **Formato / Contentor:** `.mp4`
- **Codec de Vídeo:** H.264 / AVC
- **Codec de Áudio:** AAC (44.1 kHz ou 48 kHz)
- **Resolução Ideal:** 1280x720 (720p) ou 1920x1080 (1080p)
- **Taxa de Quadros (FPS):** 30 fps ou 60 fps

---

## 🛠️ Como Funciona o Carregamento no Script

O módulo de mídia utiliza a biblioteca **`ffpyplayer`** para sincronizar o áudio com a imagem em tempo real:

1. Quando uma ação de infraestrutura é executada no menu (ex: *Ligar Poste*), o script verifica se o ficheiro correspondente existe na pasta `midias/`.
2. Se o ficheiro for encontrado, uma janela de visualização dedicada é aberta e o vídeo é reproduzido com som em segundo plano (*thread* separada).
3. Caso o ficheiro não esteja presente, o sistema exibirá apenas um aviso visual e textual no terminal, mantendo a execução do código sem interromper a simulação.
