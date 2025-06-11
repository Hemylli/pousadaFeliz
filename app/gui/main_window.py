import tkinter as tk
from tkinter import ttk
import os 
from PIL import Image, ImageTk
from app.gui.tela_reservas import TelaReservas      
from app.gui.tela_quartos import TelaQuartos        
from app.gui.tela_clientes import TelaClientes      
from app.gui.tela_funcionarios import TelaFuncionarios 

class MainWindow:
    def __init__(self, master, db): 
        print("MainWindow: Inicializando...")
        self.master = master
        self.master.title("Pousada Feliz - Sistema de Gestão")
        self.master.geometry("1000x700") # Tamanho inicial maior
        self.master.minsize(800, 600) # Tamanho mínimo da janela
        self.db = db 

        # Definir as cores do projeto
        self.primary_bg = "#a5f0f3"  # Azul claro
        self.secondary_bg = "#a6b8f3" # Lilás claro
        self.text_color = "#333333"  # Cor de texto padrão (cinza escuro)
        self.button_hover_bg = "#80b0f0" # Azul um pouco mais escuro para hover

        print("MainWindow: Chamando _configure_styles...")
        self._configure_styles() # Configura estilos globais para ttk widgets
        print("MainWindow: _configure_styles concluído.")
        
        self.master.config(bg=self.primary_bg) # Define o fundo da janela principal
        print(f"MainWindow: Cor de fundo do master definida para {self.primary_bg}.")

        # --- Frame do Cabeçalho (Logo e Título) ---
        self.header_frame = tk.Frame(self.master, bg=self.secondary_bg, bd=2, relief="raised")
        self.header_frame.pack(side="top", fill="x", pady=10, padx=10)
        print("MainWindow: header_frame criado e empacotado.")

        print("MainWindow: Chamando _load_logo...")
        self._load_logo("pousada_feliz.png") # Carrega e posiciona o logo
        print("MainWindow: _load_logo concluído.")
        
        tk.Label(self.header_frame, text="Pousada Feliz", font=("Arial", 28, "bold"), 
                 bg=self.secondary_bg, fg=self.text_color).pack(side="left", padx=20, pady=5)
        print("MainWindow: Título da aplicação adicionado.")

        # --- Botões de Navegação (Menu Horizontal) ---
        self.nav_buttons_frame = tk.Frame(self.master, bg=self.primary_bg)
        self.nav_buttons_frame.pack(side="top", fill="x", pady=5)
        print("MainWindow: nav_buttons_frame criado.")
        self._create_navigation_buttons(self.nav_buttons_frame)
        print("MainWindow: Botões de navegação criados.")

        # --- Frame onde as telas secundárias serão exibidas (o "container") ---
        self.container = tk.Frame(self.master, bg=self.primary_bg)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        print("MainWindow: container criado e empacotado.")

        # Exibir uma tela de boas-vindas inicial
        print("MainWindow: Chamando _show_welcome_screen...")
        self._show_welcome_screen()
        print("MainWindow: _show_welcome_screen concluído.")

        print("MainWindow: Chamando create_menu...")
        self.create_menu() 
        print("MainWindow: create_menu concluído.")
        print("MainWindow: Inicialização completa. Entrando no mainloop.")


    def _configure_styles(self):
        style = ttk.Style()
        
        try:
            style.theme_use('clam') 
            print("Styles: Tema 'clam' aplicado.")
        except tk.TclError:
            print("Styles: Tema 'clam' não disponível, usando o tema padrão.")
            style.theme_use('default')
        
        style.configure('.', background=self.primary_bg, foreground=self.text_color)
        style.configure('TFrame', background=self.primary_bg)
        style.configure('TLabel', background=self.primary_bg, foreground=self.text_color)
        
        style.configure('TButton',
                        background=self.secondary_bg,
                        foreground=self.text_color,
                        font=('Arial', 10, 'bold'),
                        padding=10,
                        relief="flat")
        style.map('TButton',
                  background=[('active', self.button_hover_bg)],
                  foreground=[('active', 'white')])

        style.configure("Treeview",
                        background="white", 
                        foreground=self.text_color,
                        rowheight=25,
                        fieldbackground="white")
        style.map('Treeview',
                  background=[('selected', self.secondary_bg)]) 
        style.configure("Treeview.Heading",
                        background=self.secondary_bg,
                        foreground=self.text_color,
                        font=('Arial', 10, 'bold'))
        style.map("Treeview.Heading",
                  background=[('active', self.button_hover_bg)])
        
        style.configure('TCombobox',
                        fieldbackground='white',
                        background=self.primary_bg,
                        foreground=self.text_color)
        style.map('TCombobox',
                  selectbackground=[('readonly', self.primary_bg)],
                  selectforeground=[('readonly', self.text_color)],
                  fieldbackground=[('readonly', 'white')],
                  background=[('readonly', self.secondary_bg)])
        print("Styles: Todos os estilos configurados.")

    def _load_logo(self, image_name):
        try:
            current_script_path = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_script_path)) 
            assets_path = os.path.join(project_root, 'assets')
            image_full_path = os.path.join(assets_path, image_name)

            print(f"Logo: Tentando carregar imagem de: {image_full_path}")
            original_image = Image.open(image_full_path)
            # Redimensiona a imagem
            resized_image = original_image.resize((60, 60), Image.LANCZOS) 
            self.logo_photo = ImageTk.PhotoImage(resized_image) 

            logo_label = tk.Label(self.header_frame, image=self.logo_photo, bg=self.secondary_bg)
            logo_label.pack(side="left", padx=10, pady=5)
            print("Logo: Imagem carregada e exibida com sucesso.")

        except FileNotFoundError:
            print(f"Erro CRÍTICO: Imagem de logo '{image_name}' NÃO ENCONTRADA em '{image_full_path}'.")
            print("Por favor, verifique se 'pousada_feliz.png' está na pasta 'assets' na raiz do seu projeto.")
        
        except Exception as e:
            print(f"Erro CRÍTICO ao carregar imagem de logo: {e}")
            print(f"Detalhes do erro: {e}")
            print(f"Caminho que causou o erro: {image_full_path}")

    def _create_navigation_buttons(self, parent_frame):
        button_options = {
            "font": ("Arial", 12, "bold"),
            "bg": self.secondary_bg,
            "fg": self.text_color,
            "activebackground": self.button_hover_bg,
            "activeforeground": "white",
            "bd": 0, 
            "relief": "flat",
            "padx": 15,
            "pady": 8,
            "cursor": "hand2" 
        }
        
        buttons_center_frame = tk.Frame(parent_frame, bg=parent_frame['bg'])
        buttons_center_frame.pack(expand=True)

        tk.Button(buttons_center_frame, text="Reservas", command=self.abrir_tela_reservas, **button_options).pack(side="left", padx=10)
        tk.Button(buttons_center_frame, text="Quartos", command=self.abrir_tela_quartos, **button_options).pack(side="left", padx=10)
        tk.Button(buttons_center_frame, text="Clientes", command=self.abrir_tela_clientes, **button_options).pack(side="left", padx=10)
        tk.Button(buttons_center_frame, text="Funcionários", command=self.abrir_tela_funcionarios, **button_options).pack(side="left", padx=10)
        tk.Button(buttons_center_frame, text="Sair", command=self.master.quit, **button_options).pack(side="left", padx=10)


    def _show_welcome_screen(self):
        self.limpar_tela()
        welcome_frame = tk.Frame(self.container, bg=self.primary_bg)
        welcome_frame.pack(fill="both", expand=True)
        tk.Label(welcome_frame, text="Bem-vindo ao Sistema da Pousada Feliz!",
                 font=("Arial", 24, "italic"), bg=self.primary_bg, fg=self.text_color).pack(pady=50)
        tk.Label(welcome_frame, text="Selecione uma opção nos botões acima para começar.",
                 font=("Arial", 16), bg=self.primary_bg, fg=self.text_color).pack(pady=10)


    def create_menu(self):
        menubar = tk.Menu(self.master, bg=self.secondary_bg, fg=self.text_color, bd=1, relief="flat")
        self.master.config(menu=menubar)

        menu_gerenciar = tk.Menu(menubar, tearoff=0, bg=self.secondary_bg, fg=self.text_color)
        menubar.add_cascade(label="Gerenciar", menu=menu_gerenciar)
        menu_gerenciar.add_command(label="Reservas", command=self.abrir_tela_reservas, bg=self.secondary_bg, fg=self.text_color)
        menu_gerenciar.add_command(label="Quartos", command=self.abrir_tela_quartos, bg=self.secondary_bg, fg=self.text_color)
        menu_gerenciar.add_command(label="Clientes", command=self.abrir_tela_clientes, bg=self.secondary_bg, fg=self.text_color)
        menu_gerenciar.add_command(label="Funcionários", command=self.abrir_tela_funcionarios, bg=self.secondary_bg, fg=self.text_color)
        menu_gerenciar.add_separator(bg=self.secondary_bg)
        menu_gerenciar.add_command(label="Sair", command=self.master.quit, bg=self.secondary_bg, fg=self.text_color)


    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def abrir_tela_reservas(self):
        self.limpar_tela()
        TelaReservas(self.container, self.db) 

    def abrir_tela_quartos(self):
        self.limpar_tela()
        TelaQuartos(self.container, self.db) 

    def abrir_tela_clientes(self):
        self.limpar_tela()
        TelaClientes(self.container, self.db) 

    def abrir_tela_funcionarios(self):
        self.limpar_tela()
        TelaFuncionarios(self.container, self.db)