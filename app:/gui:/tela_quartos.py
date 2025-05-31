import tkinter as tk
from tkinter import ttk


class TelaQuartos:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Quartos", font=("Arial", 18))
        label.pack(pady=10)

        # Tabela
        colunas = ("Número", "Tipo", "Status", "Preço")
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=100)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)

        # Botões
        botoes_frame = tk.Frame(frame)
        botoes_frame.pack(pady=10)

        tk.Button(botoes_frame, text="Adicionar Quarto", width=15).grid(row=0, column=0, padx=5)
        tk.Button(botoes_frame, text="Editar Quarto", width=15).grid(row=0, column=1, padx=5)
        tk.Button(botoes_frame, text="Excluir Quarto", width=15).grid(row=0, column=2, padx=5)
