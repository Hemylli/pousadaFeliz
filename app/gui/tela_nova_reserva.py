import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva


class TelaNovaReserva:
    def __init__(self, master, db: Database, callback_carregar_reservas, reserva_para_editar=None):
        self.master = master
        self.db = db
        self.callback_carregar_reservas = callback_carregar_reservas # Função para recarregar a tabela principal
        self.reserva_para_editar = reserva_para_editar # Objeto Reserva se estiver em modo de edição

        self.root = tk.Toplevel(master)
        self.root.title("Nova Reserva" if not reserva_para_editar else "Editar Reserva")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        self.criar_widgets()
        self.carregar_dados_iniciais()
        if self.reserva_para_editar:
            self.preencher_dados_edicao()

    def criar_widgets(self):
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)

        # Hóspede
        tk.Label(form_frame, text="Hóspede:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_hospede = ttk.Combobox(form_frame, width=40, state="readonly")
        self.combo_hospede.grid(row=0, column=1, pady=5)
        self.hospedes_dict = {} # Para mapear nome para objeto/id

        # Quarto
        tk.Label(form_frame, text="Quarto (Número - Tipo - Preço):").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_quarto = ttk.Combobox(form_frame, width=40, state="readonly")
        self.combo_quarto.grid(row=1, column=1, pady=5)
        self.quartos_dict = {} # Para mapear string para objeto/id

        # Data de Entrada
        tk.Label(form_frame, text="Data de Entrada (AAAA-MM-DD):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_data_entrada = tk.Entry(form_frame, width=30)
        self.entry_data_entrada.grid(row=2, column=1, pady=5)

        # Data de Saída
        tk.Label(form_frame, text="Data de Saída (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_data_saida = tk.Entry(form_frame, width=30)
        self.entry_data_saida.grid(row=3, column=1, pady=5)

        # Status (apenas para edição, nova reserva começa 'Ativa')
        if self.reserva_para_editar:
            tk.Label(form_frame, text="Status:").grid(row=4, column=0, sticky="w", pady=5)
            self.combo_status = ttk.Combobox(form_frame, width=40, state="readonly", 
                                             values=["Ativa", "Finalizada", "Cancelada"])
            self.combo_status.grid(row=4, column=1, pady=5)


        # Botão Salvar
        btn_salvar = tk.Button(form_frame, text="Salvar Reserva", 
                               command=self.salvar_reserva)
        btn_salvar.grid(row=5 if not self.reserva_para_editar else 6, column=0, columnspan=2, pady=20)

    def carregar_dados_iniciais(self):
        # Carregar Hóspedes
        hospedes = self.db.listar_hospedes()
        hospede_nomes = []
        for h in hospedes:
            display_name = f"{h.nome} ({h.cpf})"
            hospede_nomes.append(display_name)
            self.hospedes_dict[display_name] = h # Mapeia string exibida para o objeto Hospede
        self.combo_hospede['values'] = hospede_nomes

        # Carregar Quartos
        quartos = self.db.listar_quartos()
        quarto_info = []
        for q in quartos:
            display_info = f"{q.numero} - {q.tipo} - R${q.preco:.2f} ({q.status})"
            quarto_info.append(display_info)
            self.quartos_dict[display_info] = q # Mapeia string exibida para o objeto Quarto
        self.combo_quarto['values'] = quarto_info

    def preencher_dados_edicao(self):
        # Preenche os campos com os dados da reserva existente
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

        # Validação de datas (simples)
        if data_entrada >= data_saida:
            messagebox.showwarning("Atenção", "A data de saída deve ser posterior à data de entrada.")
            return
        
        # Verificar disponibilidade do quarto APENAS para novas reservas ou se a data mudou na edição
        is_available = self.db.verificar_disponibilidade_quarto(quarto_obj.id, data_entrada, data_saida)
        
        if not is_available and (not self.reserva_para_editar or \
                                 (self.reserva_para_editar and (self.reserva_para_editar.data_entrada != data_entrada or \
                                                               self.reserva_para_editar.data_saida != data_saida or \
                                                               self.reserva_para_editar.quarto.id != quarto_obj.id))):
            messagebox.showwarning("Atenção", "Quarto não disponível para o período selecionado.")
            return

        try:
            if self.reserva_para_editar:
                novo_status = self.combo_status.get()
                if not novo_status: novo_status = self.reserva_para_editar.status # Mantem o status se não for alterado
                
                # Exemplo: Se só alterar o status (como seu DB já faz)
                if novo_status != self.reserva_para_editar.status:
                     self.db.alterar_status_reserva(self.reserva_para_editar.id, novo_status)
                     messagebox.showinfo("Sucesso", "Status da reserva atualizado!")
                else:
                    messagebox.showinfo("Informação", "Nenhuma alteração de status realizada.")
                
                # Se você quiser permitir alterar Hóspede, Quarto, Datas:
                # 1. Adicione um método ao database.py:
                #    def atualizar_reserva(self, id_reserva, hospede_id, quarto_id, data_entrada, data_saida, status):
                #        self.cursor.execute("UPDATE reservas SET hospede_id=?, quarto_id=?, data_entrada=?, data_saida=?, status=? WHERE id=?", 
                #                            (hospede_id, quarto_id, data_entrada, data_saida, status, id_reserva))
                #        self.conexao.commit()
                # 2. Chame aqui:
                #    self.db.atualizar_reserva(self.reserva_para_editar.id, hospede_obj.id, quarto_obj.id, data_entrada, data_saida, novo_status)


            else:
                # Adicionar nova reserva
                nova_reserva = Reserva(
                    id=None,
                    hospede=hospede_obj,
                    quarto=quarto_obj,
                    data_entrada=data_entrada,
                    data_saida=data_saida,
                    status="Ativa" # Nova reserva sempre começa ativa
                )
                self.db.adicionar_reserva(nova_reserva)
                # Opcional: mudar status do quarto para 'Ocupado' se necessário
                self.db.alterar_status_quarto(quarto_obj.id, "Ocupado")
                messagebox.showinfo("Sucesso", "Reserva adicionada com sucesso!")
            
            self.callback_carregar_reservas() # Recarrega a tabela na tela principal
            self.root.destroy() # Fecha a janela de nova reserva

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar reserva: {e}")