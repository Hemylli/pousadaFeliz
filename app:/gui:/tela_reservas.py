import tkinter as tk
from tkinter import ttk


class TelaReservas:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Reservas", font=("Arial", 18))
        label.pack(pady=10)

        # Tabela
        colunas = ("ID", "Hóspede", "Quarto", "Check-in", "Check-out", "Status")
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=100)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)

        # Botões
        botoes_frame = tk.Frame(frame)
        botoes_frame.pack(pady=10)

        tk.Button(botoes_frame, text="Nova Reserva", width=15).grid(row=0, column=0, padx=5)
        tk.Button(botoes_frame, text="Editar Reserva", width=15).grid(row=0, column=1, padx=5)
        tk.Button(botoes_frame, text="Cancelar Reserva", width=15).grid(row=0, column=2, padx=5)
