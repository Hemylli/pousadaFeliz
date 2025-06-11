import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva

class TelaReservas:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db
        self.reserva_selecionada_id = None

        # Definir as cores (consistente com MainWindow)
        self.primary_bg = "#a5f0f3"  # Azul claro
        self.secondary_bg = "#a6b8f3" # Lilás claro
        self.text_color = "#333333"  # Cor de texto padrão

        self._configure_styles() # Aplica estilos ttk
        
        frame = tk.Frame(master, bg=self.primary_bg)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Reservas", font=("Arial", 18, "bold"),
                         bg=self.primary_bg, fg=self.text_color)
        label.pack(pady=10)

        # Tabela
        colunas = ("ID", "Hóspede", "Quarto", "Check-in", "Check-out", "Status")
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=100)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_reserva)

        # Botões
        botoes_frame = tk.Frame(frame, bg=self.primary_bg)
        botoes_frame.pack(pady=10)

        # Usando ttk.Button para se beneficiar dos estilos globais
        ttk.Button(botoes_frame, text="Nova Reserva", command=self.abrir_tela_nova_reserva).grid(row=0, column=0, padx=5)
        ttk.Button(botoes_frame, text="Editar Reserva", command=self.editar_reserva).grid(row=0, column=1, padx=5)
        ttk.Button(botoes_frame, text="Cancelar Reserva", command=self.cancelar_reserva).grid(row=0, column=2, padx=5)
        ttk.Button(botoes_frame, text="Check-out", command=self.realizar_checkout).grid(row=0, column=3, padx=5)

        self.carregar_reservas()

    def _configure_styles(self):
        # Apenas um placeholder, o estilo já é configurado na MainWindow
        # Mas é bom ter o método para consistência, caso queira estilos específicos aqui
        pass 

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
            self.reserva_selecionada_id = self.tabela.item(selected_item, 'iid')
        else:
            self.reserva_selecionada_id = None

    def abrir_tela_nova_reserva(self):
        TelaNovaReserva(self.master, self.db, self.carregar_reservas)

    def editar_reserva(self):
        if not hasattr(self, 'reserva_selecionada_id') or not self.reserva_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma reserva para editar.")
            return
        
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
                self.db.alterar_status_reserva(self.reserva_selecionada_id, "Cancelada")
                reserva = None
                for r in self.db.listar_reservas():
                    if r.id == int(self.reserva_selecionada_id):
                        reserva = r
                        break
                if reserva and reserva.status == "Ativa":
                     self.db.alterar_status_quarto(reserva.quarto.id, "Disponível")

                messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")
                self.carregar_reservas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cancelar reserva: {e}")

    def realizar_checkout(self):
        if not hasattr(self, 'reserva_selecionada_id') or not self.reserva_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma reserva para realizar o check-out.")
            return

        confirmacao = messagebox.askyesno("Confirmar Check-out", "Tem certeza que deseja realizar o check-out desta reserva?")
        if confirmacao:
            try:
                self.db.alterar_status_reserva(self.reserva_selecionada_id, "Finalizada")
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


# --- Nova Tela para Adicionar/Editar Reserva ---
class TelaNovaReserva:
    def __init__(self, master, db: Database, callback_carregar_reservas, reserva_para_editar=None):
        self.master = master
        self.db = db
        self.callback_carregar_reservas = callback_carregar_reservas
        self.reserva_para_editar = reserva_para_editar

        # Definir as cores (consistente com MainWindow)
        self.primary_bg = "#a5f0f3"
        self.secondary_bg = "#a6b8f3"
        self.text_color = "#333333"

        self._configure_styles() # Aplica estilos ttk

        self.root = tk.Toplevel(master)
        self.root.title("Nova Reserva" if not reserva_para_editar else "Editar Reserva")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        self.root.config(bg=self.primary_bg) # Fundo da janela top-level

        self.criar_widgets()
        self.carregar_dados_iniciais()
        if self.reserva_para_editar:
            self.preencher_dados_edicao()

    def _configure_styles(self):
        # Apenas um placeholder, o estilo já é configurado na MainWindow
        pass

    def criar_widgets(self):
        form_frame = tk.Frame(self.root, padx=20, pady=20, bg=self.primary_bg)
        form_frame.pack(fill="both", expand=True)

        tk.Label(form_frame, text="Hóspede:", bg=self.primary_bg, fg=self.text_color).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_hospede = ttk.Combobox(form_frame, width=40, state="readonly")
        self.combo_hospede.grid(row=0, column=1, pady=5)
        self.hospedes_dict = {}

        tk.Label(form_frame, text="Quarto (Número - Tipo - Preço):", bg=self.primary_bg, fg=self.text_color).grid(row=1, column=0, sticky="w", pady=5)
        self.combo_quarto = ttk.Combobox(form_frame, width=40, state="readonly")
        self.combo_quarto.grid(row=1, column=1, pady=5)
        self.quartos_dict = {}

        tk.Label(form_frame, text="Data de Entrada (AAAA-MM-DD):", bg=self.primary_bg, fg=self.text_color).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_data_entrada = tk.Entry(form_frame, width=30)
        self.entry_data_entrada.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Data de Saída (AAAA-MM-DD):", bg=self.primary_bg, fg=self.text_color).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_data_saida = tk.Entry(form_frame, width=30)
        self.entry_data_saida.grid(row=3, column=1, pady=5)

        if self.reserva_para_editar:
            tk.Label(form_frame, text="Status:", bg=self.primary_bg, fg=self.text_color).grid(row=4, column=0, sticky="w", pady=5)
            self.combo_status = ttk.Combobox(form_frame, width=40, state="readonly", 
                                             values=["Ativa", "Finalizada", "Cancelada"])
            self.combo_status.grid(row=4, column=1, pady=5)

        ttk.Button(form_frame, text="Salvar Reserva", command=self.salvar_reserva).grid(row=5 if not self.reserva_para_editar else 6, column=0, columnspan=2, pady=20)

    def carregar_dados_iniciais(self):
        hospedes = self.db.listar_hospedes()
        hospede_nomes = []
        for h in hospedes:
            display_name = f"{h.nome} ({h.cpf})"
            hospede_nomes.append(display_name)
            self.hospedes_dict[display_name] = h
        self.combo_hospede['values'] = hospede_nomes

        quartos = self.db.listar_quartos()
        quarto_info = []
        for q in quartos:
            display_info = f"{q.numero} - {q.tipo} - R${q.preco:.2f} ({q.status})"
            quarto_info.append(display_info)
            self.quartos_dict[display_info] = q
        self.combo_quarto['values'] = quarto_info

    def preencher_dados_edicao(self):
        hospede_display = f"{self.reserva_para_editar.hospede.nome} ({self.reserva_para_editar.hospede.cpf})"
        quarto_display = f"{self.reserva_para_editar.quarto.numero} - {self.reserva_para_editar.quarto.tipo} - R${self.reserva_para_editar.quarto.preco:.2f} ({self.reserva_para_editar.quarto.status})"

        self.combo_hospede.set(hospede_display)
        self.combo_quarto.set(quarto_display)
        self.entry_data_entrada.insert(0, self.reserva_para_editar.data_entrada)
        self.entry_data_saida.insert(0, self.reserva_para_editar.data_saida)
        if self.reserva_para_editar.status:
            self.combo_status.set(self.reserva_para_editar.status)

    def salvar_reserva(self):
        hospede_selecionado_str = self.combo_hospede.get()
        quarto_selecionado_str = self.combo_quarto.get()
        data_entrada = self.entry_data_entrada.get()
        data_saida = self.entry_data_saida.get()

        if not (hospede_selecionado_str and quarto_selecionado_str and data_entrada and data_saida):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        hospede_obj = self.hospedes_dict.get(hospede_selecionado_str)
        quarto_obj = self.quartos_dict.get(quarto_selecionado_str)

        if not hospede_obj or not quarto_obj:
            messagebox.showerror("Erro", "Selecione um hóspede e um quarto válidos.")
            return

        if data_entrada >= data_saida:
            messagebox.showwarning("Atenção", "A data de saída deve ser posterior à data de entrada.")
            return
        
        quarto_atual_id = self.reserva_para_editar.quarto.id if self.reserva_para_editar else None
        data_entrada_atual = self.reserva_para_editar.data_entrada if self.reserva_para_editar else None
        data_saida_atual = self.reserva_para_editar.data_saida if self.reserva_para_editar else None

        if not self.reserva_para_editar or \
           (quarto_obj.id != quarto_atual_id) or \
           (data_entrada != data_entrada_atual) or \
           (data_saida != data_saida_atual):
            
            is_available = self.db.verificar_disponibilidade_quarto(quarto_obj.id, data_entrada, data_saida, self.reserva_para_editar.id if self.reserva_para_editar else None)
            
            if not is_available:
                messagebox.showwarning("Atenção", "Quarto não disponível para o período selecionado.")
                return

        try:
            if self.reserva_para_editar:
                novo_status = self.combo_status.get()
                if not novo_status: 
                    novo_status = self.reserva_para_editar.status

                self.db.atualizar_reserva(
                    id_reserva=self.reserva_para_editar.id,
                    hospede_id=hospede_obj.id,
                    quarto_id=quarto_obj.id,
                    data_entrada=data_entrada,
                    data_saida=data_saida,
                    status=novo_status
                )
                messagebox.showinfo("Sucesso", "Reserva atualizada com sucesso!")

                if self.reserva_para_editar.status == "Ativa" and novo_status in ["Cancelada", "Finalizada"]:
                    self.db.alterar_status_quarto(self.reserva_para_editar.quarto.id, "Disponível")
                elif self.reserva_para_editar.status != "Ativa" and novo_status == "Ativa":
                     self.db.alterar_status_quarto(quarto_obj.id, "Ocupado")
                elif quarto_obj.id != quarto_atual_id: 
                    if self.reserva_para_editar.status == "Ativa": 
                        self.db.alterar_status_quarto(self.reserva_para_editar.quarto.id, "Disponível")
                    if novo_status == "Ativa": 
                        self.db.alterar_status_quarto(quarto_obj.id, "Ocupado")


            else:
                nova_reserva = Reserva(
                    id=None,
                    hospede=hospede_obj,
                    quarto=quarto_obj,
                    data_entrada=data_entrada,
                    data_saida=data_saida,
                    status="Ativa"
                )
                self.db.adicionar_reserva(nova_reserva)
                self.db.alterar_status_quarto(quarto_obj.id, "Ocupado")
                messagebox.showinfo("Sucesso", "Reserva adicionada com sucesso!")
            
            self.callback_carregar_reservas()
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar reserva: {e}")