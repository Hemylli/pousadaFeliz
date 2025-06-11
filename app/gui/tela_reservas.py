# app/gui/tela_reservas.py
import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.reserva import Reserva

class TelaReservas:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db
        
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
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_reserva) # Adiciona evento de seleção

        # Botões
        botoes_frame = tk.Frame(frame)
        botoes_frame.pack(pady=10)

        tk.Button(botoes_frame, text="Nova Reserva", width=15, command=self.abrir_tela_nova_reserva).grid(row=0, column=0, padx=5)
        tk.Button(botoes_frame, text="Editar Reserva", width=15, command=self.editar_reserva).grid(row=0, column=1, padx=5)
        tk.Button(botoes_frame, text="Cancelar Reserva", width=15, command=self.cancelar_reserva).grid(row=0, column=2, padx=5)
        tk.Button(botoes_frame, text="Check-out", width=15, command=self.realizar_checkout).grid(row=0, column=3, padx=5) # Botão de Check-out

        self.carregar_reservas() # Carrega os dados na tabela ao iniciar

    def carregar_reservas(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        try:
            reservas = self.db.listar_reservas()
            for r in reservas:
                self.tabela.insert("", "end", values=(
                    r.id,
                    r.hospede.nome,
                    r.quarto.numero,
                    r.data_entrada,
                    r.data_saida,
                    r.status
                ), iid=r.id)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar reservas: {e}")

    def selecionar_reserva(self, event):
        selected_item = self.tabela.focus()
        if selected_item:
            self.reserva_selecionada_id = self.tabela.item(selected_item, 'iid') # Pega o ID da reserva
            print(f"Reserva selecionada: ID {self.reserva_selecionada_id}")
        else:
            self.reserva_selecionada_id = None

    def abrir_tela_nova_reserva(self):
        TelaNovaReserva(self.master, self.db, self.carregar_reservas)

    def editar_reserva(self):
        if not hasattr(self, 'reserva_selecionada_id') or not self.reserva_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma reserva para editar.")
            return
        
        # Buscar a reserva completa pelo ID para passar para a tela de edição
        reserva_para_editar = None
        for r in self.db.listar_reservas():
            if r.id == int(self.reserva_selecionada_id):
                reserva_para_editar = r
                break
        
        if reserva_para_editar:
            TelaNovaReserva(self.master, self.db, self.carregar_reservas, reserva_para_editar)
        else:
            messagebox.showerror("Erro", "Reserva não encontrada para edição.")


    def cancelar_reserva(self):
        if not hasattr(self, 'reserva_selecionada_id') or not self.reserva_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma reserva para cancelar.")
            return

        confirmacao = messagebox.askyesno("Confirmar Cancelamento", "Tem certeza que deseja cancelar esta reserva?")
        if confirmacao:
            try:
                # Altera o status da reserva no banco de dados
                self.db.alterar_status_reserva(self.reserva_selecionada_id, "Cancelada")
                # Altera o status do quarto para Disponível se a reserva estava "Ativa"
                reserva = None
                for r in self.db.listar_reservas():
                    if r.id == int(self.reserva_selecionada_id):
                        reserva = r
                        break
                if reserva and reserva.status == "Ativa": # Verifica o status anterior antes de alterar o quarto
                     self.db.alterar_status_quarto(reserva.quarto.id, "Disponível")

                messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")
                self.carregar_reservas() # Recarrega a tabela
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cancelar reserva: {e}")

    def realizar_checkout(self):
        if not hasattr(self, 'reserva_selecionada_id') or not self.reserva_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma reserva para realizar o check-out.")
            return

        confirmacao = messagebox.askyesno("Confirmar Check-out", "Tem certeza que deseja realizar o check-out desta reserva?")
        if confirmacao:
            try:
                # Altera o status da reserva para 'Finalizada'
                self.db.alterar_status_reserva(self.reserva_selecionada_id, "Finalizada")
                
                # Altera o status do quarto para 'Disponível'
                reserva = None
                for r in self.db.listar_reservas():
                    if r.id == int(self.reserva_selecionada_id):
                        reserva = r
                        break
                if reserva:
                    self.db.alterar_status_quarto(reserva.quarto.id, "Disponível")

                messagebox.showinfo("Sucesso", "Check-out realizado com sucesso!")
                self.carregar_reservas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao realizar check-out: {e}")