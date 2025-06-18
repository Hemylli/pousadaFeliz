import tkinter as tk
from tkinter import ttk 
import os 
from PIL import Image, ImageTk 
from app.gui.tela_reservas import TelaReservas      
from app.gui.tela_quartos import TelaQuartos        
from app.gui.tela_clientes import TelaClientes      
from app.gui.tela_funcionarios import TelaFuncionarios 
from app.gui.tela_nova_reserva import TelaNovaReserva 
from app.gui.tela_login import TelaLogin 

class MainWindow:
    def __init__(self, master, db): 
        print("DEBUG: MainWindow: Inicializando (Layout Dinâmico e Final - Correção Atributos)...")
        self.master = master
        self.master.title("Pousada Feliz - Sistema de Gestão")
        self.master.geometry("1200x800") 
        self.master.minsize(1000, 700) 
        self.db = db 

        self.welcome_left_bg = "#f0f1f1"  
        self.general_bg = "#FFFFFF" 
        self.purple_color = "#A679E3" 
        self.cyan_color = "#80FFFF" 
        self.text_dark = "black" 

        style = ttk.Style()
        try:
            style.theme_use('clam') 
        except tk.TclError:
            style.theme_use('default')
        style.configure("Treeview", background="white", foreground=self.text_dark, fieldbackground="white")
        style.configure("TCombobox", fieldbackground='white', foreground=self.text_dark)

        self.initial_layout_frame = tk.Frame(self.master, bg=self.general_bg)
        self.app_layout_frame = tk.Frame(self.master, bg=self.general_bg)

        self._show_initial_layout() 
        print("DEBUG: MainWindow: Inicialização completa. Entrando no mainloop.")


    def _show_initial_layout(self):
        """Exibe o layout de boas-vindas com divisão 50/50 e logo grande."""
        print("DEBUG: Exibindo layout inicial (Boas-vindas)...")
        self.app_layout_frame.pack_forget() 
        self.initial_layout_frame.pack(fill="both", expand=True)

        for widget in self.initial_layout_frame.winfo_children():
            widget.destroy()

        self.left_panel = tk.Frame(self.initial_layout_frame, bg=self.welcome_left_bg)
        self.left_panel.pack(side="left", fill="both", expand=True)

        self._load_logo_for_panel(self.left_panel, "pousada_feliz.png", size=(400, 400), 
                                  bg_color=self.welcome_left_bg, bind_command=self._show_initial_layout)

        self.right_panel = tk.Frame(self.initial_layout_frame, bg=self.general_bg)
        self.right_panel.pack(side="left", fill="both", expand=True)

        right_header_frame = tk.Frame(self.right_panel, bg=self.general_bg)
        right_header_frame.pack(side="top", fill="x", pady=20)
        
        tk.Label(right_header_frame, text="Pousada Feliz", font=("Arial", 30, "bold"), 
                 fg=self.purple_color, bg=self.general_bg).pack()
        tk.Frame(right_header_frame, bg="#CCCCCC", height=2).pack(fill="x", padx=50, pady=10)

        nav_buttons_frame = tk.Frame(self.right_panel, bg=self.general_bg)
        nav_buttons_frame.pack(pady=20)

        self._create_navigation_buttons(nav_buttons_frame, is_vertical=True)

        self.container = tk.Frame(self.right_panel, bg=self.general_bg)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(self.container, text="Seja Bem-Vindo!", font=("Arial", 24, "bold"), 
                 bg=self.general_bg, fg="gray").pack(pady=100) 

        print("DEBUG: Layout inicial configurado.")


    def _show_app_layout_with_screen(self, screen_class):
        print(f"DEBUG: Exibindo layout do aplicativo para tela: {screen_class.__name__}")
        self.initial_layout_frame.pack_forget() 
        self.app_layout_frame.pack(fill="both", expand=True)

        for widget in self.app_layout_frame.winfo_children():
            widget.destroy()

        app_header_frame = tk.Frame(self.app_layout_frame, bg=self.purple_color) 
        app_header_frame.pack(side="top", fill="x", pady=0, padx=0) 

        self._load_logo_for_panel(app_header_frame, "pousada_feliz.png", size=(50, 50), 
                                  bg_color=self.purple_color, bind_command=self._show_initial_layout)

        tk.Label(app_header_frame, text="Pousada Feliz", font=("Arial", 20, "bold"), 
                 fg="white", bg=self.purple_color).pack(side="left", padx=10) 

        header_nav_buttons_container = tk.Frame(app_header_frame, bg=self.purple_color)
        header_nav_buttons_container.pack(side="right", padx=10)

        self._create_navigation_buttons(header_nav_buttons_container, is_vertical=False)

        self.container = tk.Frame(self.app_layout_frame, bg=self.general_bg) # container para o app_layout
        self.container.pack(fill="both", expand=True)

        self.limpar_tela_container() 
        screen_class(self.container, self.db) 

        print(f"DEBUG: Layout do aplicativo para {screen_class.__name__} configurado.")


    def _load_logo_for_panel(self, parent_panel, image_name, size, bg_color, bind_command=None, pack_options=None):
        if pack_options is None:
            pack_options = {"side": "left", "padx": 250, "pady": 50} # Default para compatibilidade

        try:
            current_script_path = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_script_path)) 
            assets_path = os.path.join(project_root, 'assets')
            image_full_path = os.path.join(assets_path, image_name)

            print(f"DEBUG: Logo: Tentando carregar imagem de: {image_full_path}")
            original_image = Image.open(image_full_path)
            resized_image = original_image.resize(size, Image.LANCZOS)
            if not hasattr(parent_panel, '_logo_refs'):
                parent_panel._logo_refs = {}
            parent_panel._logo_refs[image_name] = ImageTk.PhotoImage(resized_image) 

            logo_label = tk.Label(parent_panel, image=parent_panel._logo_refs[image_name], bg=bg_color)
            if bind_command:
                logo_label.bind("<Button-1>", lambda e: bind_command()) 
                logo_label.config(cursor="hand2") 
            
            logo_label.pack(**pack_options)

            print("DEBUG: Logo: Imagem carregada e exibida com sucesso.")

        except FileNotFoundError:
            print(f"ERRO: Imagem de logo '{image_name}' NÃO ENCONTRADA em '{image_full_path}'.")
        except Exception as e:
            print(f"ERRO CRÍTICO: ao carregar imagem de logo: {e}")

    def _create_navigation_buttons(self, parent_frame, is_vertical=True):
        common_button_options = {
            "font": ("Arial", 12, "bold"),
            "fg": "white", 
            "bd": 0, 
            "relief": "flat", 
            "width": 15 if is_vertical else 12, 
            "pady": 8 if is_vertical else 5, 
            "cursor": "hand2" 
        }
        
        bg_purple = self.purple_color
        bg_cyan = self.cyan_color
        
        tk.Button(parent_frame, text="RESERVAS", command=lambda: self._show_app_layout_with_screen(TelaReservas), 
                  bg=bg_purple, **common_button_options).pack(pady=5, side="top" if is_vertical else "left", padx=5 if not is_vertical else 0)
        tk.Button(parent_frame, text="QUARTOS", command=lambda: self._show_app_layout_with_screen(TelaQuartos), 
                  bg=bg_purple, **common_button_options).pack(pady=5, side="top" if is_vertical else "left", padx=5 if not is_vertical else 0)
        tk.Button(parent_frame, text="CLIENTES", command=lambda: self._show_app_layout_with_screen(TelaClientes), 
                  bg=bg_purple, **common_button_options).pack(pady=5, side="top" if is_vertical else "left", padx=5 if not is_vertical else 0)
        tk.Button(parent_frame, text="FUNCIONÁRIOS", command=lambda: self._show_app_layout_with_screen(TelaFuncionarios), 
                  bg=bg_purple, **common_button_options).pack(pady=5, side="top" if is_vertical else "left", padx=5 if not is_vertical else 0)
        
        if is_vertical:
            tk.Frame(parent_frame, height=20, bg=parent_frame['bg']).pack() 
        else:
             tk.Frame(parent_frame, width=20, bg=parent_frame['bg']).pack(side="left")
        
        tk.Button(parent_frame, text="SAIR", command=self.master.quit, 
                  bg=bg_cyan, **common_button_options).pack(pady=5, side="top" if is_vertical else "left", padx=5 if not is_vertical else 0)


    def limpar_tela_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def abrir_tela_reservas(self):
        self._show_app_layout_with_screen(TelaReservas) 

    def abrir_tela_quartos(self):
        self._show_app_layout_with_screen(TelaQuartos) 

    def abrir_tela_clientes(self):
        self._show_app_layout_with_screen(TelaClientes) 

    def abrir_tela_funcionarios(self):
        self._show_app_layout_with_screen(TelaFuncionarios)