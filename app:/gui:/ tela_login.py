import tkinter as tk
from tkinter import messagebox
from .main_window import MainWindow


class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - Pousada Feliz")
        self.master.geometry("400x300")

        self.label_usuario = tk.Label(master, text="Usuário")
        self.label_usuario.pack(pady=10)
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        self.label_senha = tk.Label(master, text="Senha")
        self.label_senha.pack(pady=10)
        self.entry_senha = tk.Entry(master, show="*")
        self.entry_senha.pack()

        self.botao_login = tk.Button(master, text="Entrar", command=self.verificar_login)
        self.botao_login.pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario == "admin" and senha == "admin":
            self.master.destroy()  # Fecha a janela de login
            root = tk.Tk()
            MainWindow(root)
            root.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
