import tkinter as tk
from tkinter import messagebox
from controller.database import Database

class TelaLogin:
    def __init__(self, master, db: Database): 
        self.master = master
        self.db = db 
        self.master.title("Login - Pousada Feliz")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        self.general_bg = "#f0f1f1"  
        self.purple_color = "#A679E3" 
        self.text_dark = "black"  
        self.cyan_color = "#80FFFF" 

        self.master.config(bg=self.general_bg) 

        self.frame_login = tk.Frame(self.master, bg=self.general_bg)
        self.frame_login.pack(expand=True, fill="both")

        tk.Label(self.frame_login, text="Login - Pousada Feliz", font=("Arial", 16, "bold"), 
                 bg=self.general_bg, fg=self.text_dark).pack(pady=10)

        tk.Label(self.frame_login, text="Usuário:", bg=self.general_bg, fg=self.text_dark).pack(pady=5)
        self.entry_usuario = tk.Entry(self.frame_login, width=30, bg="white", fg="black") 
        self.entry_usuario.pack()

        tk.Label(self.frame_login, text="Senha:", bg=self.general_bg, fg=self.text_dark).pack(pady=5)
        self.entry_senha = tk.Entry(self.frame_login, show="*", width=30, bg="white", fg="black") 
        self.entry_senha.pack()

        button_options = {
            "font": ("Arial", 10, "bold"), "bg": self.purple_color, "fg": "white", 
            "activebackground": self.cyan_color, "activeforeground": "white",
            "bd": 1, "relief": "raised", "padx": 10, "pady": 5, "cursor": "hand2"
        }
        tk.Button(self.frame_login, text="Entrar", command=self.verificar_login, **button_options).pack(pady=20)

    def verificar_login(self):
        from app.gui.main_window import MainWindow

        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        funcionario = self.db.autenticar_funcionario(usuario, senha)

        if funcionario: 
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            
            # Destrói o frame de login para limpar a tela
            self.frame_login.destroy()
            
            # Reconfigura a janela para a tela principal
            self.master.title("Sistema de Gerenciamento - Pousada Feliz")
            self.master.geometry("1024x768") 
            self.master.resizable(True, True)  

            app_main = MainWindow(self.master, self.db)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
