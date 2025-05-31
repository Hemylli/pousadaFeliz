import tkinter as tk
from tkinter import ttk
from .tela_reservas import TelaReservas
from .tela_quartos import TelaQuartos
from .tela_clientes import TelaClientes


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Pousada Feliz - Sistema de Gestão")
        self.master.geometry("800x600")

        self.create_menu()

        # Frame onde as telas serão exibidas
        self.container = tk.Frame(self.master)
        self.container.pack(fill="both", expand=True)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        menu_gerenciar = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gerenciar", menu=menu_gerenciar)
        menu_gerenciar.add_command(label="Reservas", command=self.abrir_tela_reservas)
        menu_gerenciar.add_command(label="Quartos", command=self.abrir_tela_quartos)
        menu_gerenciar.add_command(label="Clientes", command=self.abrir_tela_clientes)
        menu_gerenciar.add_separator()
        menu_gerenciar.add_command(label="Sair", command=self.master.quit)
        btn_funcionarios = tk.Button(self.root, text="Funcionários", width=20, height=2, command=self.abrir_tela_funcionarios)
        btn_funcionarios.place(x=350, y=100)  # Ajuste conforme seu layout


    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def abrir_tela_reservas(self):
        self.limpar_tela()
        TelaReservas(self.container)

    def abrir_tela_quartos(self):
        self.limpar_tela()
        TelaQuartos(self.container)

    def abrir_tela_clientes(self):
        self.limpar_tela()
        TelaClientes(self.container)

    def abrir_tela_funcionarios(self):
    from app.gui.tela_funcionarios import TelaFuncionarios
    TelaFuncionarios()
