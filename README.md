# Protocolo Holloway

Protótipo experimental desenvolvido em Python para testar a integração de bibliotecas de mídia, manipulação de janelas e periféricos do sistema. Inspirado na estética e nas mecânicas de invasão da franquia *Watch Dogs*, o projeto simula uma central de ferramentas "hacking" de monitoramento e intrusão capaz de capturar imagens da câmera, disparar efeitos sonoros e abrir janelas pop-up com vídeos automatizados.

---

## Objetivo

O foco deste repositório é o estudo prático do ecossistema Python fora do terminal convencional. O código foi estruturado como um laboratório para testar como diferentes módulos interagem com o hardware e o sistema operacional em tempo real:

* **Captura de Vídeo:** Acesso à webcam local e leitura de frames para simular feeds de câmeras de segurança (CFTV).
* **Automação de Janelas (Pop-ups):** Criação dinâmica de múltiplas janelas na tela para reproduzir vídeos e alertas visuais simultâneos.
* **Sincronização de Áudio:** Disparo de trilhas e efeitos sonoros em paralelo às ações da interface sem bloquear a execução do programa.
* **Execução Concorrente:** Uso de threads para gerenciar vídeo, som e interface ao mesmo tempo.

---

## Tecnologias e Bibliotecas Utilizadas

* **Python 3.13**
* **OpenCV (`opencv-python`):** Captura da webcam e processamento básico de imagem/vídeo.
* **Tkinter / Pygame:** Construção da interface, controle de eventos e abertura dos pop-ups de vídeo.
* **Pygame Mixer / Playsound:** Reprodução assíncrona dos efeitos sonoros e alarmes.
* **Bibliotecas Padrão (`threading`, `os`, `time`, `random`):** Controle de processos simultâneos, manipulação de caminhos e temporizadores.

---

## AVISO LEGAL ⚠
Este software é apenas uma simulação visual e sonora criada para fins de estudo de programação em Python. Nenhuma técnica real de invasão, exploração de vulnerabilidades ou acesso não autorizado a redes externas é realizada por este código.

Todos os nomes, identificadores, sistemas (como referências ao ctOS ou Protocolo Holloway), dados exibidos na interface e cenários apresentados são puramente fictícios, inspirados em obras de ficção e jogos eletrônicos. Qualquer semelhança com sistemas, organizações ou pessoas reais é mera coincidência. O acesso à câmera e a exibição de janelas ocorrem estritamente de forma local na máquina do próprio usuário que executa o script.
