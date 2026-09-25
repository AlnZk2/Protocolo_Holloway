import time
import random
import os
import sys
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk
from ffpyplayer.player import MediaPlayer

# --- ESTILIZAÇÃO TERMINAL HACKER ---
GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

# --- LISTA DE NOMES E SOBRENOMES ---
NOMES_ALEATORIOS = [
    "Marcus Holloway", "Aiden Pearce", "Clara Lille", "Sitara Dhawan",
    "Wrench Smith", "Raymond Kenney", "T-Bone Grady", "Jordi Chin",
    "Sabrina Brooks", "Lucas Vance", "Elena Rostova", "Gabriel Thorne",
    "Beatriz Lima", "Julian Mercer", "Kaitlyn Ward"
]

# --- EMPRESAS FAKE PARA EMAIL ---
EMPRESAS_EMAILS = [
    "@ctos-corp.net",
    "@bloom-technologies.com",
    "@haum-data.io",
    "@invitro-labs.com",
    "@tidiss-security.org"
]

# --- CONVERSAS PARA O APLICATIVO DE MENSAGENS ---
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
    ]
]

EMAILS_SPAM = [
    {"assunto": "ALERTA DE SEGURANÇA: Acesso não autorizado", "remetente": "security", "corpo": "Detectamos um login suspeito na sua conta ctOS a partir de um IP desconhecido."},
    {"assunto": "Você ganhou um prêmio exclusivo!", "remetente": "promo", "corpo": "Parabéns! Seu número foi sorteado. Clique no link para resgatar 10.000 créditos."},
    {"assunto": "URGENTE: Atualização de senha necessária", "remetente": "admin", "corpo": "Sua conta bancária será bloqueada em 24h caso não confirme seus dados cadastrais."}
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

# --- DADOS FIXOS PARA O TESTE ---
NPC_DADOS = {
    "nome": "AlnZk2",
    "idade": 24,
    "trabalho": "Desenvolvedor",
    "telefone": f"+55 ({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
}

def tocar_som_notificacao():
    def _tocar():
        # Emite um bip de terminal compatível com ambientes POSIX/Linux
        sys.stdout.write('\a')
        sys.stdout.flush()
    threading.Thread(target=_tocar, daemon=True).start()

def limpar_tela():
    os.system('clear' if os.name != 'nt' else 'cls')

def cabeçalho(titulo):
    print(f"{GREEN}{'='*55}")
    print(f"{BRIGHT_GREEN} [ctOS v2.0 Linux - {titulo}]")
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

        tocando = [True]

        def som_chamada_loop():
            while tocando[0]:
                tocar_som_notificacao()
                time.sleep(1.2)

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

            for i in range(5, 0, -1):
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

# --- CASCATA DE PSEUDOCÓDIGO ---
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
        f"ctos_bus.override_telemetry(node_id='{hex(random.randint(0x10, 0xFF))}')"
    ]
    
    snippets = [
        f"import ctOS.core.system as ctos_sys",
        f"import ctOS.net.sockets as sys_net",
        f"target_identifier = '{acao.lower().replace(' ', '_')}'"
    ] + random.sample(rotinas, 3) + [f"signal_override_status: 200 OK | EXPLOIT_SUCCESSFUL"]
    
    for line in snippets:
        hex_prefix = f"0x{random.randint(0x1000, 0xFFFF):04X}"
        sub_thread = f"TID-{random.randint(100, 999)}"
        print(f"{GREEN}[{hex_prefix}][{sub_thread}] {MAGENTA}>{RESET} ", end="", flush=True)
        for char in line:
            print(char, end="", flush=True)
            time.sleep(random.uniform(0.002, 0.010))
        print()
        time.sleep(random.uniform(0.02, 0.05))
        
    print(f"\n{BRIGHT_GREEN}[!] COMANDO '{acao.upper()}' CONCLUÍDO COM SUCESSO.{RESET}\n")
    time.sleep(0.4)

def minigame_hacker():
    banco_palavras = ["BYPASS", "OVERRIDE", "GATEWAY", "FIREWALL", "EXPLOIT", "PAYLOAD", "PACKET", "DECRYPT"]
    vidas = 3
    print(f"{CYAN}[INICIANDO INTERFACE DE HACKING...]{RESET}")
    time.sleep(0.3)

    while vidas > 0:
        palavra_correta = random.choice(banco_palavras)
        distratores = random.sample([p for p in banco_palavras if p != palavra_correta], 2)
        opcoes = [palavra_correta] + distratores
        random.shuffle(opcoes)

        print(f"\n{GREEN}--- TERMINAL ALVO ---{RESET}")
        print(f"ALVO: {BRIGHT_GREEN}>>> {palavra_correta} <<<{RESET}")
        print(f"SINAL DE REDE: {YELLOW}{'♥' * vidas}{RESET}\n")
        
        for i, opt in enumerate(opcoes, 1):
            print(f" [{i}] {opt}")
        
        try:
            escolha = int(input(f"\n{GREEN}Selecione o pacote correto (1-3): {RESET}"))
            if opcoes[escolha - 1] == palavra_correta:
                print(f"{BRIGHT_GREEN}[+] PACOTE ACEITO! INJETANDO COMANDO...{RESET}")
                time.sleep(0.4)
                return True
            else:
                vidas -= 1
                print(f"{RED}[!] FALHA NO SINCRONISMO! (-1 Vida){RESET}")
        except (ValueError, IndexError):
            vidas -= 1
            print(f"{RED}[!] ENTROPIA DE DADOS! (-1 Vida){RESET}")

    print(f"\n{RED}[CRÍTICO] SINAL PERDIDO! Cooldown ativado...{RESET}")
    sistema_estado["cooldown_geral"] = time.time() + 20
    input("\nPressione ENTER para continuar...")
    return False

# --- FEED DE WEBCAM COM DETECÇÃO E DADOS ---
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
        noise = np.random.randint(0, 20, (h_img, w_img), dtype='uint8')
        green_frame[:, :, 1] = cv2.add(green_frame[:, :, 1], noise)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

        for (x, y, w, h) in faces:
            cv2.rectangle(green_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Atualização visual da detecção
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

# --- MENUS ---
def menu_celular():
    while True:
        limpar_tela()
        cabeçalho("CELULAR - INTERFACE DE PROXIMIDADE")
        
        print(" [1] Identificar Pessoa")
        print(" [2] Enviar Distração (Canal Direto)")
        print(" [0] Guardar Celular")
        
        opcao = input(f"\n{GREEN}ctOS_Mobile> {RESET}")
        
        if opcao == "0": break

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
            print(" [1] Ligação Falsa")
            print(" [2] Mensagem SMS")
            print(" [3] E-mail SPAM")
            print(" [0] Voltar")
            
            sub_op = input(f"\n{GREEN}Vetor> {RESET}")
            if sub_op == "1" and minigame_hacker():
                cascata_pseudocodigo("Voice Call Spoofing Module")
                GUI_chamada_celular(NPC_DADOS["nome"])
                input("\nPressione ENTER...")
            elif sub_op == "2" and minigame_hacker():
                cascata_pseudocodigo("SMS Injector Service")
                GUI_mensagem_celular(NPC_DADOS["nome"])
                input("\nPressione ENTER...")
            elif sub_op == "3" and minigame_hacker():
                cascata_pseudocodigo("SMTP Payload Delivery")
                GUI_email_celular(NPC_DADOS["nome"])
                input("\nPressione ENTER...")

def menu_laptop():
    while True:
        limpar_tela()
        cabeçalho("LAPTOP - TERMINAL AVANÇADO DE ACESSO")
        
        print(" [1] Invasão de Câmeras de Segurança (Ativar Feed)")
        print(" [2] Desativar Câmera de Segurança")
        print(" [0] Guardar Laptop")
        
        opcao = input(f"\n{GREEN}ctOS_Laptop> {RESET}")
        if opcao == "0": break

        if opcao == "1":
            if minigame_hacker():
                cascata_pseudocodigo("Wireless Cam Signal Hijack")
                ativar_camera("STANDARD_CAM_01")
                input("\nSinal transmitido! Pressione ENTER...")
        elif opcao == "2":
            cascata_pseudocodigo("Terminating Video Stream Connection")
            desativar_camera()
            input("\nPressione ENTER...")

def main():
    while True:
        limpar_tela()
        cabeçalho("MENU PRINCIPAL DE DISPOSITIVOS")
        
        npc = f"{BRIGHT_GREEN}IDENTIFICADO{RESET}" if sistema_estado['npc_identificado'] else f"{YELLOW}DESCONHECIDO{RESET}"
        print(f"STATUS PERFIL NPC: [{npc}]\n")
        print(" [1] Pegar Celular na Mão")
        print(" [2] Abrir Laptop")
        print(" [0] Sair")
        
        escolha = input(f"\n{GREEN}ctOS_Root> {RESET}")
        
        if escolha == "1": menu_celular()
        elif escolha == "2": menu_laptop()
        elif escolha == "0":
            sistema_estado["camera_rodando"] = False
            print(f"\n{BRIGHT_GREEN} Projeto mantido por AlnZk2 | Desenvolvedor 👻 {RESET}")
            break

if __name__ == "__main__":
    main()
