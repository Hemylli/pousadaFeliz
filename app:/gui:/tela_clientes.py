import tkinter as tk
from tkinter import ttk


class TelaClientes:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Clientes", font=("Arial", 18))
        label.pack(pady=10)

        # Tabela de clientes
        colunas = ("ID", "Nome", "Email", "Telefone")
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=120)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)

        # Área para envio de mensagem
        label_mensagem = tk.Label(frame, text="Enviar Mensagem para Cliente:")
        label_mensagem.pack(pady=5)

        self.texto_mensagem = tk.Text(frame, height=5, width=80)
        self.texto_mensagem.pack(pady=5)

        botao_enviar = tk.Button(frame, text="Enviar", width=10, command=self.enviar_mensagem)
        botao_enviar.pack(pady=5)

    def enviar_mensagem(self):
        mensagem = self.texto_mensagem.get("1.0", tk.END).strip()
        if mensagem:
            print(f"Mensagem enviada: {mensagem}")
            self.texto_mensagem.delete("1.0", tk.END)
