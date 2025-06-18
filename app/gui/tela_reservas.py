import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.gui.tela_nova_reserva import TelaNovaReserva 

class TelaReservas:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db
        self.reserva_selecionada_id = None

        self.general_bg = "#f0f1f1"  
        self.purple_color = "#A679E3" 
        self.cyan_color = "#80FFFF" 
        self.text_dark = "black"  
        
        frame = tk.Frame(master, bg=self.general_bg)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Reservas", font=("Arial", 16, "bold"),
                         bg=self.general_bg, fg=self.text_dark)
        label.pack(pady=10)

        # Tabela 
        colunas = ("ID", "Hóspede", "Quarto", "Check-in", "Check-out", "Status")
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        # Estilo básico para Treeview e Heading
        style = ttk.Style()
        try: 
            style.theme_use('clam')
        except tk.TclError:
            style.theme_use('default')
        style.configure("Treeview", background="white", foreground=self.text_dark, fieldbackground="white")
        style.configure("Treeview.Heading", background=self.purple_color, foreground="white", font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.purple_color)]) 
        style.map("Treeview.Heading", background=[('active', self.cyan_color)], foreground=[('active', self.text_dark)]) 

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=100)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_reserva)

        # Botões
        botoes_frame = tk.Frame(frame, bg=self.general_bg)
        botoes_frame.pack(pady=10)

        button_options = {
            "font": ("Arial", 10, "bold"), "bg": self.purple_color, "fg": "white", 
            "activebackground": self.cyan_color, "activeforeground": self.text_dark,
            "bd": 0, "relief": "flat", "padx": 10, "pady": 5, "cursor": "hand2"
        }

        tk.Button(botoes_frame, text="Nova Reserva", command=self.abrir_tela_nova_reserva, **button_options).grid(row=0, column=0, padx=5)
        tk.Button(botoes_frame, text="Editar Reserva", command=self.editar_reserva, **button_options).grid(row=0, column=1, padx=5)
        tk.Button(botoes_frame, text="Cancelar Reserva", command=self.cancelar_reserva, **button_options).grid(row=0, column=2, padx=5)
        tk.Button(botoes_frame, text="Check-out", command=self.realizar_checkout, **button_options).grid(row=0, column=3, padx=5)

        self.carregar_reservas()

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
                ), iid=str(r.id)) 
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar reservas: {e}")

    def selecionar_reserva(self, event):
        selected_item_iid = self.tabela.focus() 
        if selected_item_iid:
            self.reserva_selecionada_id = selected_item_iid 
            print(f"DEBUG: RESERVA SELECIONADA ID: {self.reserva_selecionada_id}") 
        else:
            self.reserva_selecionada_id = None
            print("DEBUG: Nenhuma reserva selecionada.")

    def abrir_tela_nova_reserva(self):
        TelaNovaReserva(self.master, self.db, self.carregar_reservas)

    def editar_reserva(self):
        if self.reserva_selecionada_id is None:
            messagebox.showwarning("Atenção", "Selecione uma reserva para editar.")
            return
        
        reserva_para_editar = self.db.buscar_reserva_por_id(int(self.reserva_selecionada_id)) 
        
        if reserva_para_editar:
            TelaNovaReserva(self.master, self.db, self.carregar_reservas, reserva_para_editar)
        else:
            messagebox.showerror("Erro", "Reserva não encontrada para edição (ID pode ser inválida ou não existir mais).")

    def cancelar_reserva(self):
        if self.reserva_selecionada_id is None:
            messagebox.showwarning("Atenção", "Selecione uma reserva para cancelar.")
            return

        confirmacao = messagebox.askyesno("Confirmar Cancelamento", "Tem certeza que deseja cancelar esta reserva?")
        if confirmacao:
            try:
                self.db.alterar_status_reserva(int(self.reserva_selecionada_id), "Cancelada") 
                reserva = self.db.buscar_reserva_por_id(int(self.reserva_selecionada_id))
                if reserva and reserva.status != "Cancelada": 
                     self.db.alterar_status_quarto(reserva.quarto.id, "Disponível")

                messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")
                self.carregar_reservas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cancelar reserva: {e}")

    def realizar_checkout(self):
        if self.reserva_selecionada_id is None:
            messagebox.showwarning("Atenção", "Selecione uma reserva para realizar o check-out.")
            return

        confirmacao = messagebox.askyesno("Confirmar Check-out", "Tem certeza que deseja realizar o check-out desta reserva?")
        if confirmacao:
            try:
                self.db.alterar_status_reserva(int(self.reserva_selecionada_id), "Finalizada") 
                reserva = self.db.buscar_reserva_por_id(int(self.reserva_selecionada_id))
                if reserva and reserva.status != "Finalizada": 
                    self.db.alterar_status_quarto(reserva.quarto.id, "Disponível")

                messagebox.showinfo("Sucesso", "Check-out realizado com sucesso!")
                self.carregar_reservas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao realizar check-out: {e}")