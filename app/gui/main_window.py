import tkinter as tk
from tkinter import ttk
from app.gui.tela_reservas import TelaReservas      
from app.gui.tela_quartos import TelaQuartos        
from app.gui.tela_clientes import TelaClientes      
from app.gui.tela_funcionarios import TelaFuncionarios 

class MainWindow:
    def __init__(self, master, db): 
        self.master = master
        self.master.title("Pousada Feliz - Sistema de Gestão")
        self.master.geometry("800x600")
        self.db = db 

        self.create_menu()

        # Frame onde as telas serão exibidas
        self.container = tk.Frame(self.master)
        self.container.pack(fill="both", expand=True)

        btn_funcionarios = tk.Button(self.master, text="Funcionários", width=20, height=2, command=self.abrir_tela_funcionarios)
        btn_funcionarios.pack(pady=10) 


    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        menu_gerenciar = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gerenciar", menu=menu_gerenciar)
        # Passar a instância do db para as telas que precisam dela
        menu_gerenciar.add_command(label="Reservas", command=self.abrir_tela_reservas)
        menu_gerenciar.add_command(label="Quartos", command=self.abrir_tela_quartos)
        menu_gerenciar.add_command(label="Clientes", command=self.abrir_tela_clientes)
        menu_gerenciar.add_command(label="Funcionários", command=self.abrir_tela_funcionarios)
        menu_gerenciar.add_command(label="Sair", command=self.master.quit)


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