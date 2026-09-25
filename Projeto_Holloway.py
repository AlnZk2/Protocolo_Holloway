import time
import random
import os
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk
from ffpyplayer.player import MediaPlayer

# Tenta importar winsound para efeitos sonoros nativos no Windows
try:
    import winsound
except ImportError:
    winsound = None

# --- ESTILIZAÇÃO TERMINAL HACKER ---
GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

# --- LISTA DE NOMES E SOBRENOMES (15 OPÇÕES PARA SORTEIO DE SECUNDÁRIOS) ---
NOMES_ALEATORIOS = [
    "Marcus Holloway", "Aiden Pearce", "Clara Lille", "Sitara Dhawan",
    "Wrench Smith", "Raymond Kenney", "T-Bone Grady", "Jordi Chin",
    "Sabrina Brooks", "Lucas Vance", "Elena Rostova", "Gabriel Thorne",
    "Beatriz Lima", "Julian Mercer", "Kaitlyn Ward"
]

# --- EMPRESAS FAKE PARA EMAIL (5 OPÇÕES) ---
EMPRESAS_EMAILS = [
    "@ctos-corp.net",
    "@bloom-technologies.com",
    "@haum-data.io",
    "@invitro-labs.com",
    "@tidiss-security.org"
]

# --- 10 TIPOS DE CONVERSAS EXTENSAS (MÍNIMO 6 MENSAGENS) ---
CONVERSAS_MENSAGENS = [
    [
        ("NPC", "Cara, você viu a última atualização do ctOS?"),
        ("VOCÊ", "Ainda não, deram bypass no firewall de novo?"),
        ("NPC", "Sim! A rede inteira da região tá instável."),
        ("VOCÊ", "Acho melhor a gente se encontrar no hackerspace."),
        ("NPC", "Beleza, leva o laptop com as chaves RSA."),
        ("VOCÊ", "Tô saindo agora, me espera na entrada dos fundos."),
        ("NPC", "Fechado, não demorar que a patrulha tá passando.")
    ],
    [
        ("NPC", "Onde você tá? A reunião de emergência já começou!"),
        ("VOCÊ", "Tô preso no trânsito, os semáforos enlouqueceram."),
        ("NPC", "Corre, o chefe tá procurando seu relatório agora mesmo."),
        ("VOCÊ", "Diz pra ele que tive um problema no servidor local."),
        ("NPC", "Ele tá bravo, falou que quer ver o log de acessos."),
        ("VOCÊ", "Chego em 5 minutos, segura a barra aí pra mim!"),
        ("NPC", "Vou tentar enrolar ele com o café, voa!")
    ],
    [
        ("NPC", "Você pagou o servidor da DedSec esse mês?"),
        ("VOCÊ", "Achei que você tinha feito a transferência ontem..."),
        ("NPC", "Droga! Vão derrubar nosso nó de comunicação!"),
        ("VOCÊ", "Calma, vou acessar o painel e pagar via cripto."),
        ("NPC", "Faz isso rápido antes que o script de corte rode."),
        ("VOCÊ", "Pronto, transação confirmada na blockchain."),
        ("NPC", "Uf, salvo pelo gongo. Sinal restabelecido!")
    ],
    [
        ("NPC", "Ei, me passa aquele exploit de CAN-Bus de veículos?"),
        ("VOCÊ", "Enviando pelo canal criptografado agora..."),
        ("NPC", "Recebido! Valeu, vou testar no carro do alvo."),
        ("VOCÊ", "Toma cuidado com o alarme, ele dispara telemetria."),
        ("NPC", "Relaxa, já isolei a antena de GPS dele."),
        ("VOCÊ", "Boa! Me avisa se conseguir o controle da direção."),
        ("NPC", "Deu certo! O painel tá respondendo aos meus comandos.")
    ],
    [
        ("NPC", "Cuidado com as câmeras do quarteirão 4."),
        ("VOCÊ", "Valeu o aviso! Tô usando o laptop pra fechar o circuito."),
        ("NPC", "Boa. Limpa os logs de acesso assim que terminar."),
        ("VOCÊ", "Sempre faço isso. Onde é o ponto de extração?"),
        ("NPC", "No beco atrás do posto de conveniência."),
        ("VOCÊ", "Tô a caminho, desativa a iluminação da rua pra mim."),
        ("NPC", "Apagando os postes agora. Boa sorte!")
    ],
    [
        ("NPC", "Conseguiu interceptar os arquivos do diretor?"),
        ("VOCÊ", "Tô baixando o dump de dados via Wi-Fi público."),
        ("NPC", "Demora muito? Eles tão suspeitando do tráfego."),
        ("VOCÊ", "Faltam só 20MB. O gargalo é a velocidade da rede."),
        ("NPC", "Apressa isso, o sistema antiafraude tá varrendo a rede."),
        ("VOCÊ", "Download concluído! Apagando rastros do terminal."),
        ("NPC", "Perfeito! Salva no pendrive criptografado e vaza.")
    ],
    [
        ("NPC", "Meu drone de reconhecimento perdeu o sinal!"),
        ("VOCÊ", "Estranho... tem algum jammer operando por perto?"),
        ("NPC", "Acho que sim, o sinal do rádio caiu pra zero."),
        ("VOCÊ", "Vou tentar dar um override na frequência de controle."),
        ("NPC", "Conseguiu? Ele tá caindo perto do perímetro da polícia!"),
        ("VOCÊ", "Pronto! Forcei a rota de retorno automático."),
        ("NPC", "Caramba, essa foi por pouco. Já recuperei ele aqui.")
    ],
    [
        ("NPC", "Disparei o alarme silencioso do galpão sem querer!"),
        ("VOCÊ", "Como você fez isso?! A segurança vai chegar em 3 minutos."),
        ("NPC", "Encostei no sensor térmico da porta principal."),
        ("VOCÊ", "Tô enviando um sinal falso de reset para o painel principal."),
        ("NPC", "Funcionou? As sirenes no teto pararam de piscar."),
        ("VOCÊ", "Sim, reescrevi o log. Mas você tem 60 segundos pra sair."),
        ("NPC", "Entendido, pegando a chave física e saindo!")
    ],
    [
        ("NPC", "Conseguiu as placas de rede novas que eu pedi?"),
        ("VOCÊ", "Consegui, são de alta potência com suporte a monitor mode."),
        ("NPC", "Excelente! Precisava delas pra quebrar a senha WPA3."),
        ("VOCÊ", "Deixei no armário secreto do laboratório."),
        ("NPC", "Show! Precisa de algo em troca pro projeto?"),
        ("VOCÊ", "Só me consegue o firmware modificado do rádio."),
        ("NPC", "Pode deixar, subo no servidor até o fim do dia.")
    ],
    [
        ("NPC", "Tudo pronto pro teste do apagão na subestação?"),
        ("VOCÊ", "O script tá carregado e pronto pra disparar."),
        ("NPC", "Tem certeza que não vai afetar os hospitais?"),
        ("VOCÊ", "Isolei a linha hospitalar no bypass do código."),
        ("NPC", "Ótimo. Dispara o corte em 3... 2... 1..."),
        ("VOCÊ", "Subestação fora do ar! A cidade inteira ficou no escuro."),
        ("NPC", "Operação limpa. Vamos nos mover nas sombras agora.")
    ]
]

EMAILS_SPAM = [
    {"assunto": "ALERTA DE SEGURANÇA: Acesso não autorizado", "remetente": "security", "corpo": "Detectamos um login suspeito na sua conta ctOS a partir de um IP desconhecido."},
    {"assunto": "Você ganhou um prêmio exclusivo!", "remetente": "promo", "corpo": "Parabéns! Seu número foi sorteado. Clique no link para resgatar 10.000 créditos."},
    {"assunto": "URGENTE: Atualização de senha necessária", "remetente": "admin", "corpo": "Sua conta bancária será bloqueada em 24h caso não confirme seus dados cadastrais."},
    {"assunto": "Oportunidade Única: Invista em Cripto", "remetente": "trader", "corpo": "Multiplique seu capital em poucas horas com nosso novo robô de operações automatizadas."},
    {"assunto": "Fatura em atraso - Notificação Final", "remetente": "cobranca", "corpo": "Identificamos um débito em aberto. Evite o corte de sinal efetuando o pagamento."}
]

# --- ESTADO GERAL DO SISTEMA ---
sistema_estado = {
    "acesso_urbano": False,
    "chave_circuito_fechado": False,
    "cooldown_geral": 0,
    "semaforo_vinculado": False,
    "carro_registrado": False,
    "alarme_carro_ativo": False,
    "poste_ligado": True,
    "cooldown_poste": 0,
    "npc_identificado": False,
    "camera_rodando": False,
    "titulo_camera_atual": ""
}

# --- DADOS FIXOS PARA TESTE DE IDENTIFICAÇÃO ---
NPC_DADOS = {
    "nome": "AlnZk2",
    "idade": 24,
    "trabalho": "Desenvolvedor",
    "telefone": f"+55 ({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
}

def tocar_som_notificacao():
    def _tocar():
        if winsound:
            modo = random.randint(1, 5)
            if modo == 1:
                for freq in [523, 659, 783, 1046]: winsound.Beep(freq, 100)
            elif modo == 2:
                for freq in [880, 440, 880, 440]: winsound.Beep(freq, 120)
            elif modo == 3:
                for freq in [1200, 1500, 1800]: winsound.Beep(freq, 80)
            elif modo == 4:
                for freq in range(400, 1000, 150): winsound.Beep(freq, 60)
            else:
                winsound.Beep(800, 250)
                time.sleep(0.05)
                winsound.Beep(1200, 300)
    threading.Thread(target=_tocar, daemon=True).start()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def cabeçalho(titulo):
    print(f"{GREEN}{'='*55}")
    print(f"{BRIGHT_GREEN} [ctOS v2.0 - {titulo}]")
    print(f"{GREEN}{'='*55}{RESET}\n")

# --- GUIS DE CELULAR (TKINTER) ---
def GUI_chamada_celular(nome_target=None):
    def _run():
        nome = nome_target if nome_target else NPC_DADOS["nome"]
        num_aleatorio = NPC_DADOS["telefone"]
        
        root = tk.Tk()
        root.title("ctOS Mobile - Incoming Call")
        root.geometry("320x520")
        root.configure(bg="#111111")
        root.resizable(False, False)
        root.eval('tk::PlaceWindow . center')

        tocando = [True]

        def som_chamada_loop():
            while tocando[0]:
                if winsound:
                    winsound.Beep(440, 400)
                    time.sleep(0.1)
                    winsound.Beep(440, 600)
                    time.sleep(1.5)
                else:
                    time.sleep(2)

        threading.Thread(target=som_chamada_loop, daemon=True).start()

        lbl_status = tk.Label(root, text="CHAMADA RECEBIDA", font=("Helvetica", 10, "bold"), fg="#00FF00", bg="#111111")
        lbl_status.pack(pady=(40, 10))

        tk.Label(root, text=nome, font=("Helvetica", 16, "bold"), fg="#FFFFFF", bg="#111111").pack(pady=5)
        tk.Label(root, text=num_aleatorio, font=("Helvetica", 11), fg="#888888", bg="#111111").pack(pady=5)

        canvas = tk.Canvas(root, width=100, height=100, bg="#111111", highlightthickness=0)
        canvas.create_oval(10, 10, 90, 90, outline="#00FF00", width=2)
        canvas.create_text(50, 50, text="👤", font=("Helvetica", 35), fill="#FFFFFF")
        canvas.pack(pady=30)

        def recusar():
            tocando[0] = False
            root.destroy()

        def atender():
            tocando[0] = False
            lbl_status.config(text="EM CHAMADA...", fg="#00FFFF")
            btn_atender.config(state="disabled")
            btn_recusar.config(state="disabled")
            
            def encerrar_apos_2s():
                time.sleep(2)
                root.destroy()
                
            threading.Thread(target=encerrar_apos_2s, daemon=True).start()

        btn_frame = tk.Frame(root, bg="#111111")
        btn_frame.pack(side="bottom", pady=40)

        btn_atender = tk.Button(btn_frame, text="📞 Atender", font=("Helvetica", 11, "bold"), bg="#28a745", fg="white", width=10, height=2, command=atender, relief="flat")
        btn_atender.grid(row=0, column=0, padx=10)

        btn_recusar = tk.Button(btn_frame, text="📵 Recusar", font=("Helvetica", 11, "bold"), bg="#dc3545", fg="white", width=10, height=2, command=recusar, relief="flat")
        btn_recusar.grid(row=0, column=1, padx=10)

        root.mainloop()

    threading.Thread(target=_run).start()

def GUI_mensagem_celular(nome_target=None):
    def _run():
        tocar_som_notificacao()
        nome = nome_target if nome_target else NPC_DADOS["nome"]
        conversa = random.choice(CONVERSAS_MENSAGENS)

        root = tk.Tk()
        root.title("ctOS Messages")
        root.geometry("380x640")
        root.configure(bg="#1e1e1e")
        root.resizable(False, False)
        root.eval('tk::PlaceWindow . center')

        header = tk.Frame(root, bg="#2d2d2d", height=50)
        header.pack(fill="x")
        tk.Label(header, text=f"💬 {nome}", font=("Helvetica", 12, "bold"), fg="#00FF00", bg="#2d2d2d").pack(pady=12)

        chat_frame = tk.Frame(root, bg="#1e1e1e")
        chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_timer = tk.Label(root, text="", font=("Helvetica", 9, "bold"), fg="#FFCC00", bg="#1e1e1e")
        lbl_timer.pack(pady=5)

        def render_conversa():
            for autor, txt in conversa:
                time.sleep(1.8)
                tocar_som_notificacao()
                
                align = "e" if autor == "VOCÊ" else "w"
                bg_color = "#0b93f6" if autor == "VOCÊ" else "#3b3b3d"
                
                msg_box = tk.Label(chat_frame, text=f"{txt}", font=("Helvetica", 10), fg="white", bg=bg_color, wraplength=240, justify="left", padx=10, pady=6)
                msg_box.pack(anchor=align, pady=4)

            for i in range(6, 0, -1):
                lbl_timer.config(text=f"Encerrando app em {i}s...")
                time.sleep(1)
            root.destroy()

        threading.Thread(target=render_conversa, daemon=True).start()
        root.mainloop()

    threading.Thread(target=_run).start()

def GUI_email_celular(nome_target=None):
    def _run():
        tocar_som_notificacao()
        nome = nome_target if nome_target else NPC_DADOS["nome"]
        email_data = random.choice(EMAILS_SPAM)
        empresa_dominio = random.choice(EMPRESAS_EMAILS)
        remetente_final = email_data['remetente'] + empresa_dominio

        root = tk.Tk()
        root.title("ctOS Mail - Inbox")
        root.geometry("380x520")
        root.configure(bg="#121212")
        root.resizable(False, False)
        root.eval('tk::PlaceWindow . center')

        header = tk.Frame(root, bg="#005f73", height=60)
        header.pack(fill="x")
        tk.Label(header, text="📧 Mail Client (SPAM INJECTION)", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#005f73").pack(pady=15)

        card = tk.Frame(root, bg="#1e1e1e", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(card, text=f"Para: {nome}", font=("Helvetica", 9), fg="#888888", bg="#1e1e1e").pack(anchor="w", padx=10, pady=(10, 2))
        tk.Label(card, text=f"De: {remetente_final}", font=("Helvetica", 9, "bold"), fg="#00FF00", bg="#1e1e1e").pack(anchor="w", padx=10, pady=2)
        tk.Label(card, text=f"Assunto: {email_data['assunto']}", font=("Helvetica", 11, "bold"), fg="#FFFFFF", bg="#1e1e1e", wraplength=320, justify="left").pack(anchor="w", padx=10, pady=10)
        
        ttk.Separator(card, orient="horizontal").pack(fill="x", padx=10, pady=5)
        tk.Label(card, text=email_data['corpo'], font=("Helvetica", 10), fg="#DDDDDD", bg="#1e1e1e", wraplength=320, justify="left").pack(anchor="w", padx=10, pady=10)

        tk.Label(root, text="[SPAM INJECTED - CLOSING IN 4s]", font=("Helvetica", 9, "bold"), fg="#FF3333", bg="#121212").pack(pady=10)

        def auto_close():
            time.sleep(4)
            root.destroy()

        threading.Thread(target=auto_close, daemon=True).start()
        root.mainloop()

    threading.Thread(target=_run).start()

# --- GERADOR DE CASCATA DE PSEUDOCÓDIGO ---
def cascata_pseudocodigo(acao):
    limpar_tela()
    print(f"{CYAN}[+] EXECUÇÃO DE EXPLOIT EM TEMPO REAL: {acao.upper()}{RESET}\n")
    
    ip_alvo = f"192.168.1.{random.randint(10, 254)}"
    mac_alvo = f"{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}"
    
    rotinas = [
        f"sys_net.bind_raw_socket(target_ip='{ip_alvo}', port={random.randint(1024, 65535)})",
        f"arp_spoofer.poison_cache(gateway='192.168.1.1', target_mac='{mac_alvo}')",
        f"crypto_engine.rsa_decrypt(key_size=2048, mode=OAEP_PADDING)",
        f"kernel.alloc_stack_frame(size=0x4000, prot=PAGE_EXECUTE_READWRITE)",
        f"memory_injector.write_bytes(address=0x7FFF001A, payload_len=512)",
        f"syscall(SYS_ptrace, PTRACE_ATTACH, pid={random.randint(1000, 9999)})",
        f"ctos_bus.override_telemetry(node_id='{hex(random.randint(0x10, 0xFF))}')",
        f"shellcode.exec(payload_type='REVERSE_TCP_SHELL')",
    ]
    
    snippets = [
        f"import ctOS.core.system as ctos_sys",
        f"import ctOS.net.sockets as sys_net",
        f"target_identifier = '{acao.lower().replace(' ', '_')}'",
        f"resolving_dns(target='{ip_alvo}') -> HOST_REACHABLE",
    ] + random.sample(rotinas, 4) + [f"signal_override_status: 200 OK | EXPLOIT_SUCCESSFUL"]
    
    for line in snippets:
        hex_prefix = f"0x{random.randint(0x1000, 0xFFFF):04X}"
        sub_thread = f"TID-{random.randint(100, 999)}"
        print(f"{GREEN}[{hex_prefix}][{sub_thread}] {MAGENTA}>{RESET} ", end="", flush=True)
        for char in line:
            print(char, end="", flush=True)
            time.sleep(random.uniform(0.003, 0.015))
        print()
        time.sleep(random.uniform(0.03, 0.08))
        
    print(f"\n{BRIGHT_GREEN}[!] COMANDO '{acao.upper()}' CONCLUÍDO COM SUCESSO.{RESET}\n")
    time.sleep(0.4)

def verificar_cooldown():
    agora = time.time()
    if agora < sistema_estado["cooldown_geral"]:
        restante = int(sistema_estado["cooldown_geral"] - agora)
        print(f"{RED}[!] SISTEMA EM COOLDOWN - Aguarde {restante}s{RESET}")
        time.sleep(1)
        return True
    return False

def minigame_hacker():
    banco_palavras = ["BYPASS", "OVERRIDE", "GATEWAY", "FIREWALL", "EXPLOIT", "PAYLOAD", "PACKET", "DECRYPT", "BUFFER", "INJECT"]
    vidas = 3
    print(f"{CYAN}[INICIANDO INTERFACE DE HACKING...]{RESET}")
    time.sleep(0.4)

    while vidas > 0:
        palavra_correta = random.choice(banco_palavras)
        distratores = random.sample([p for p in banco_palavras if p != palavra_correta], 2)
        opcoes = [palavra_correta] + distratores
        random.shuffle(opcoes)

        print(f"\n{GREEN}--- TERMINAL ALVO ---{RESET}")
        print(f"ALVO/TEXTO BASE: {BRIGHT_GREEN}>>> {palavra_correta} <<<{RESET}")
        print(f"SINAL DE REDE: {YELLOW}{'♥' * vidas}{RESET} (Vidas restantes: {vidas})\n")
        
        for i, opt in enumerate(opcoes, 1):
            print(f" [{i}] {opt}")
        
        try:
            escolha = int(input(f"\n{GREEN}Selecione o pacote correto (1-3): {RESET}"))
            if opcoes[escolha - 1] == palavra_correta:
                print(f"{BRIGHT_GREEN}[+] PACOTE ACEITO! INJETANDO COMANDO...{RESET}")
                time.sleep(0.5)
                return True
            else:
                vidas -= 1
                print(f"{RED}[!] FALHA NO SINCRONISMO! (-1 Vida){RESET}")
                time.sleep(0.8)
        except (ValueError, IndexError):
            vidas -= 1
            print(f"{RED}[!] ENTROPIA DE DADOS! (-1 Vida){RESET}")
            time.sleep(0.8)

    print(f"\n{RED}[CRÍTICO] SINAL PERDIDO! Cooldown de 30 segundos...{RESET}")
    sistema_estado["cooldown_geral"] = time.time() + 30
    input("\nPressione ENTER para continuar...")
    return False

# --- EXIBIÇÃO DE VÍDEOS DE MÍDIA ---
def _tocar_video_alarme():
    pasta_midias = os.path.join(os.path.dirname(__file__), "midias")
    if not os.path.exists(pasta_midias):
        os.makedirs(pasta_midias)
        return

    extensoes_validas = ('.mp4', '.avi', '.mkv', '.mov')
    videos = [os.path.join(pasta_midias, f) for f in os.listdir(pasta_midias) if f.lower().endswith(extensoes_validas) and "luz_" not in f.lower()]

    if not videos:
        print(f"{YELLOW}[!] Nenhum vídeo de alarme encontrado em './midias/'.{RESET}")
        return

    video_path = random.choice(videos)
    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)

    window_title = "ctOS - CAR ALARM TRIGGER FEED"
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, 1280, 720)

    while cap.isOpened():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if not ret: break

        frame = cv2.resize(frame, (1280, 720))
        cv2.putText(frame, "WARNING: VEHICLE ALARM TRIGGERED", (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow(window_title, frame)

        if val != 'eof' and val is not None: time.sleep(val)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    player.close_player()
    cap.release()
    cv2.destroyWindow(window_title)

def _tocar_video_poste(acao):
    pasta_midias = os.path.join(os.path.dirname(__file__), "midias")
    nome_arquivo = "luz_desligando.mp4" if acao == "desligar" else "luz_ligando.mp4"
    video_path = os.path.join(pasta_midias, nome_arquivo)

    if not os.path.exists(video_path):
        print(f"{YELLOW}[!] Vídeo '{nome_arquivo}' não encontrado na pasta './midias/'.{RESET}")
        return

    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)

    window_title = "ctOS - LIGHTING GRID CONTROL FEED"
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, 1280, 720)

    while cap.isOpened():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if not ret: break

        frame = cv2.resize(frame, (1280, 720))
        cv2.putText(frame, f"POWER GRID: {acao.upper()}", (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow(window_title, frame)

        if val != 'eof' and val is not None: time.sleep(val)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    player.close_player()
    cap.release()
    cv2.destroyWindow(window_title)

# --- THREAD DE TRANSMISSÃO DA WEBCAM E IDENTIFICAÇÃO ---
def _loop_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sistema_estado["camera_rodando"] = False
        return

    xml_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(xml_path)

    if face_cascade.empty():
        local_xml = "haarcascade_frontalface_default.xml"
        if not os.path.exists(local_xml):
            import urllib.request
            try:
                urllib.request.urlretrieve("https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml", local_xml)
            except Exception:
                sistema_estado["camera_rodando"] = False
                return
        face_cascade = cv2.CascadeClassifier(local_xml)

    while sistema_estado["camera_rodando"]:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        h_img, w_img = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        green_frame = np.zeros_like(frame)
        green_frame[:, :, 1] = gray
        noise = np.random.randint(0, 25, (h_img, w_img), dtype='uint8')
        green_frame[:, :, 1] = cv2.add(green_frame[:, :, 1], noise)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

        for (x, y, w, h) in faces:
            # Caixa em torno do rosto
            cv2.rectangle(green_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Condição de identificação em tempo real
            if sistema_estado["npc_identificado"]:
                info_text = f"TARGET: {NPC_DADOS['nome']} | {NPC_DADOS['trabalho']}"
                cv2.putText(green_frame, info_text, (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                cv2.putText(green_frame, "IDENTIFICANDO...", (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        cv2.putText(green_frame, f"ctOS SURVEILLANCE - {sistema_estado['titulo_camera_atual']}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("ctOS - Video Surveillance Feed", green_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sistema_estado["camera_rodando"] = False
            break

    cap.release()
    cv2.destroyAllWindows()

def ativar_camera(titulo):
    if not sistema_estado["camera_rodando"]:
        sistema_estado["camera_rodando"] = True
        sistema_estado["titulo_camera_atual"] = titulo
        threading.Thread(target=_loop_camera, daemon=True).start()

def desativar_camera():
    sistema_estado["camera_rodando"] = False

# --- MÓDULO CELULAR ---
def menu_celular():
    while True:
        limpar_tela()
        cabeçalho("CELULAR - INTERFACE DE PROXIMIDADE")
        
        print(" [1] Identificar Pessoa")
        print(" [2] Enviar Distração (Selecione o Canal)")
        print(" [3] Aplicativo Urbano (Semáforo, Poste, Alarme)")
        print(" [0] Guardar Celular")
        
        opcao = input(f"\n{GREEN}ctOS_Mobile> {RESET}")
        
        if opcao == "0": break
        if verificar_cooldown(): continue

        if opcao == "1":
            limpar_tela()
            cabeçalho("IDENTIFICAR PESSOA")
            if sistema_estado["npc_identificado"]:
                print(f"{YELLOW}[SISTEMA] Alvo já registrado!{RESET}\n")
                print(f" Nome: {NPC_DADOS['nome']} | Ocupação: {NPC_DADOS['trabalho']}")
                input("\nPressione ENTER...")
            else:
                if minigame_hacker():
                    cascata_pseudocodigo("Profilers scan & Deep Data Extraction")
                    sistema_estado["npc_identificado"] = True
                    print(f"\n{BRIGHT_GREEN}=== DADOS EXTRAÍDOS COM SUCESSO ==={RESET}")
                    print(f" Nome: {NPC_DADOS['nome']} | Ocupação: {NPC_DADOS['trabalho']}")
                    print(f" Telefone: {NPC_DADOS['telefone']}")
                    input("\nPressione ENTER...")

        elif opcao == "2":
            limpar_tela()
            cabeçalho("ENVIO DE DISTRAÇÃO")
            if not sistema_estado["npc_identificado"]:
                print(f"{YELLOW}[AVISO] É necessário 'Identificar a pessoa' primeiro!{RESET}")
                input("\nPressione ENTER...")
                continue
            
            print(" Selecione o vetor de distração:")
            print(" [1] Ligação Falsa (Interface de Chamada)")
            print(" [2] Mensagem SMS (Simulador de Chat)")
            print(" [3] E-mail SPAM (Interface Mail)")
            print(" [0] Voltar")
            
            sub_op = input(f"\n{GREEN}Vetor> {RESET}")
            if sub_op == "1":
                if minigame_hacker():
                    cascata_pseudocodigo("Voice Call Spoofing Module")
                    GUI_chamada_celular(NPC_DADOS["nome"])
                    print(f"{BRIGHT_GREEN}[+] Interface de Chamada acionada!{RESET}")
                    input("\nPressione ENTER...")
            elif sub_op == "2":
                if minigame_hacker():
                    cascata_pseudocodigo("SMS Injector Service")
                    GUI_mensagem_celular(NPC_DADOS["nome"])
                    print(f"{BRIGHT_GREEN}[+] Aplicativo de Mensagens disparado!{RESET}")
                    input("\nPressione ENTER...")
            elif sub_op == "3":
                if minigame_hacker():
                    cascata_pseudocodigo("SMTP Payload Delivery")
                    GUI_email_celular(NPC_DADOS["nome"])
                    print(f"{BRIGHT_GREEN}[+] E-mail de SPAM injetado!{RESET}")
                    input("\nPressione ENTER...")

        elif opcao == "3":
            menu_urbano_celular()

def menu_urbano_celular():
    while True:
        limpar_tela()
        cabeçalho("APLICATIVO URBANO - CELULAR")
        
        if not sistema_estado["acesso_urbano"]:
            print(f"{RED}[BLOQUEADO] Obtenha acesso à região usando a Antena pelo Laptop.{RESET}\n")
            input("Pressione ENTER para voltar...")
            break
            
        print(" [1] Semáforo de Trânsito")
        print(" [2] Sistema de Alarme de Veículo")
        print(" [3] Poste de Iluminação")
        print(" [0] Voltar")
        
        op = input(f"\n{GREEN}ctOS_Urban> {RESET}")
        if op == "0": break
        if verificar_cooldown(): continue

        if op == "1":
            limpar_tela()
            cabeçalho("CONTROLE DE SEMÁFORO")
            if not sistema_estado["semaforo_vinculado"]:
                if minigame_hacker():
                    cascata_pseudocodigo("Traffic Light Protocol Intercept")
                    sistema_estado["semaforo_vinculado"] = True
                    input("\nPressione ENTER...")
            else:
                print(" [1] VERDE | [2] AMARELO | [3] VERMELHO")
                cor = input("\nCor: ")
                cores = {"1": "VERDE", "2": "AMARELO", "3": "VERMELHO"}
                if cor in cores:
                    cascata_pseudocodigo(f"Override Traffic Signal -> {cores[cor]}")
                    input("\nPressione ENTER...")

        elif op == "2":
            limpar_tela()
            cabeçalho("SISTEMA DE ALARME DO CARRO")
            if not sistema_estado["carro_registrado"]:
                if minigame_hacker():
                    cascata_pseudocodigo("CAN-Bus Keyless Injection")
                    sistema_estado["carro_registrado"] = True
                    input("\nPressione ENTER...")
            else:
                print(" [1] Ligar Alarme | [2] Desligar Alarme")
                a = input("Opção: ")
                if a == "1":
                    cascata_pseudocodigo("Trigger Alarm Module")
                    _tocar_video_alarme()
                    input("\nPressione ENTER...")
                elif a == "2":
                    cascata_pseudocodigo("Silence Alarm Module")
                    input("\nPressione ENTER...")

        elif op == "3":
            limpar_tela()
            cabeçalho("POSTE DE ILUMINAÇÃO")
            if time.time() < sistema_estado["cooldown_poste"]:
                print(f"{YELLOW}[COOLDOWN] Aguarde alguns segundos...{RESET}")
                input("\nPressione ENTER...")
                continue
                
            print(" [1] Alternar Luzes (Ligar/Desligar)")
            if input("\nEscolha: ") == "1":
                if minigame_hacker():
                    cascata_pseudocodigo("Grid Power Switch Override")
                    acao_luz = "desligar" if sistema_estado["poste_ligado"] else "ligar"
                    sistema_estado["poste_ligado"] = not sistema_estado["poste_ligado"]
                    sistema_estado["cooldown_poste"] = time.time() + 10
                    _tocar_video_poste(acao_luz)
                    input("\nPressione ENTER...")

# --- MÓDULO LAPTOP ---
def menu_laptop():
    while True:
        limpar_tela()
        cabeçalho("LAPTOP - TERMINAL AVANÇADO DE ACESSO")
        
        print(" [1] Invasão de Câmeras de Segurança (Ativar Feed)")
        print(" [2] Desativar Câmera de Segurança")
        print(" [3] Acessar Mesa de Circuito de Câmeras (Obter Chave)")
        print(" [4] Hackear Antena de Sinal Urbano (Liberar Celular)")
        print(" [0] Guardar Laptop")
        
        opcao = input(f"\n{GREEN}ctOS_Laptop> {RESET}")
        if opcao == "0": break
        if verificar_cooldown(): continue

        if opcao == "1":
            limpar_tela()
            cabeçalho("INVASÃO DE CÂMERAS")
            print(" [1] Câmera Padrão | [2] Circuito Fechado")
            cam_op = input("\nTipo: ")
            if cam_op == "1":
                if minigame_hacker():
                    cascata_pseudocodigo("Wireless Cam Signal Hijack")
                    ativar_camera("STANDARD_CAM_01")
                    input("\nSinal transmitido! Pressione ENTER...")
            elif cam_op == "2":
                if not sistema_estado["chave_circuito_fechado"]:
                    print(f"\n{RED}[ACESSO NEGADO] Obtenha a chave na Mesa de Circuito.{RESET}")
                    input("\nPressione ENTER...")
                else:
                    if minigame_hacker():
                        cascata_pseudocodigo("Decrypting Closed-Circuit Stream")
                        ativar_camera("CLOSED_CIRCUIT_CAM_02")
                        input("\nSinal transmitido! Pressione ENTER...")

        elif opcao == "2":
            limpar_tela()
            cabeçalho("DESATIVAR CÂMERA")
            cascata_pseudocodigo("Terminating Video Stream Connection")
            desativar_camera()
            input("\nPressione ENTER...")

        elif opcao == "3":
            limpar_tela()
            cabeçalho("MESA DE CIRCUITO DE CÂMERAS")
            if minigame_hacker():
                cascata_pseudocodigo("Master Security Key Dump")
                sistema_estado["chave_circuito_fechado"] = True
                print(f"\n{BRIGHT_GREEN}[+] CHAVE DE ACESSO OBTIDA!{RESET}")
                input("\nPressione ENTER...")

        elif opcao == "4":
            limpar_tela()
            cabeçalho("ANTENA DE SINAL URBANO")
            if minigame_hacker():
                cascata_pseudocodigo("Urban Node Antenna Override")
                sistema_estado["acesso_urbano"] = True
                print(f"\n{BRIGHT_GREEN}[+] ACESSO URBANO LIBERADO!{RESET}")
                input("\nPressione ENTER...")

# --- MENU PRINCIPAL DO PROTÓTIPO ---
def main():
    while True:
        limpar_tela()
        cabeçalho("MENU DE DISPOSITIVOS DE HACKING")
        
        urb = f"{BRIGHT_GREEN}ATIVO{RESET}" if sistema_estado['acesso_urbano'] else f"{RED}BLOQUEADO{RESET}"
        key = f"{BRIGHT_GREEN}SIM{RESET}" if sistema_estado['chave_circuito_fechado'] else f"{RED}NÃO{RESET}"
        npc = f"{BRIGHT_GREEN}IDENTIFICADO{RESET}" if sistema_estado['npc_identificado'] else f"{YELLOW}DESCONHECIDO{RESET}"
        
        print(f"STATUS REDE: [Urbano: {urb}] | [Chave Câmeras: {key}] | [Perfil NPC: {npc}]\n")
        print(" [1] Pegar Celular na Mão")
        print(" [2] Abrir Laptop")
        print(" [0] Sair da experiência")
        
        escolha = input(f"\n{GREEN}ctOS_Root> {RESET}")
        
        if escolha == "1": menu_celular()
        elif escolha == "2": menu_laptop()
        elif escolha == "0":
            sistema_estado["camera_rodando"] = False
            print(f"\n{BRIGHT_GREEN} Até mais! Projeto feito por AlnZk2 👻 {RESET}")
            break

if __name__ == "__main__":
    main()