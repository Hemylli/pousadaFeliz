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
        self.callback_carregar_reservas = callback_carregar_reservas
        self.reserva_para_editar = reserva_para_editar

        # Inicializa os dicionários 
        self.hospedes_dict = {}
        self.quartos_dict = {}

        self.general_bg = "#f0f1f1" 
        self.purple_color = "#A679E3" 
        self.cyan_color = "#80FFFF" 
        self.text_dark = "black" 
        
        self.root = tk.Toplevel(master)
        self.root.title("Nova Reserva" if not reserva_para_editar else "Editar Reserva")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.config(bg=self.general_bg)

        self.criar_widgets()
        self.root.after(100, self._inicializar_dados_e_preencher_edicao) 
        
    def _inicializar_dados_e_preencher_edicao(self):
        try:
            self.carregar_dados_iniciais()
            if self.reserva_para_editar:
                self.preencher_dados_edicao()
        except Exception as e:
            messagebox.showerror("Erro ao Inicializar Dados", f"Erro: {e}")
            self.root.destroy()

    def criar_widgets(self):
        form_frame = tk.Frame(self.root, padx=30, pady=30, bg=self.general_bg)
        form_frame.pack(expand=True, fill="both")

        label_style_options = {"bg": self.general_bg, "fg": self.text_dark, "font": ("Arial", 10)}

        tk.Label(form_frame, text="Hóspede:", **label_style_options).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_hospede = ttk.Combobox(form_frame, width=45, state="readonly", font=("Arial", 10)) 
        self.combo_hospede.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        tk.Label(form_frame, text="Quarto (Número - Tipo - Preço):", **label_style_options).grid(row=1, column=0, sticky="w", pady=5)
        self.combo_quarto = ttk.Combobox(form_frame, width=45, state="readonly", font=("Arial", 10)) 
        self.combo_quarto.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        tk.Label(form_frame, text="Data de Entrada (AAAA-MM-DD):", **label_style_options).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_data_entrada = tk.Entry(form_frame, width=30, bg="white", fg="black", font=("Arial", 10))
        self.entry_data_entrada.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        tk.Label(form_frame, text="Data de Saída (AAAA-MM-DD):", **label_style_options).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_data_saida = tk.Entry(form_frame, width=30, bg="white", fg="black", font=("Arial", 10))
        self.entry_data_saida.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        if self.reserva_para_editar:
            tk.Label(form_frame, text="Status:", **label_style_options).grid(row=4, column=0, sticky="w", pady=5)
            self.combo_status = ttk.Combobox(form_frame, width=45, state="readonly", 
                                             values=["Ativa", "Finalizada", "Cancelada"], font=("Arial", 10))
            self.combo_status.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)

        button_options = { 
            "font": ("Arial", 10, "bold"), "bg": self.purple_color, "fg": "white", 
            "activebackground": self.cyan_color, "activeforeground": "white",
            "bd": 0, "relief": "flat", "padx": 15, "pady": 8, "cursor": "hand2"
        }
        tk.Button(form_frame, text="Salvar Reserva", command=self.salvar_reserva, **button_options).grid(
            row=5 if not self.reserva_para_editar else 6, column=0, columnspan=2, pady=25, sticky="nsew"
        )
        form_frame.grid_rowconfigure(5 if not self.reserva_para_editar else 6, weight=1)

    def carregar_dados_iniciais(self):
        try:
            hospedes = self.db.listar_hospedes()
            hospede_nomes = []
            for h in hospedes:
                display_name = f"{h.nome} ({h.cpf})"
                hospede_nomes.append(display_name)
                self.hospedes_dict[display_name] = h 
            self.combo_hospede['values'] = hospede_nomes
            if hospede_nomes:
                self.combo_hospede.set(hospede_nomes[0])

            quartos = self.db.listar_quartos()
            quarto_info = []
            for q in quartos:
                display_info = f"{q.numero} - {q.tipo} - R${q.preco:.2f} ({q.status})"
                quarto_info.append(display_info)
                self.quartos_dict[display_info] = q
            self.combo_quarto['values'] = quarto_info
            if quarto_info:
                self.combo_quarto.set(quarto_info[0])

        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados", f"Não foi possível carregar hóspedes ou quartos: {e}")
            self.root.destroy()
            return

    def preencher_dados_edicao(self):
        hospede_display = f"{self.reserva_para_editar.hospede.nome} ({self.reserva_para_editar.hospede.cpf})"
        quarto_display = f"{self.reserva_para_editar.quarto.numero} - {self.reserva_para_editar.quarto.tipo} - R${self.reserva_para_editar.quarto.preco:.2f} ({self.reserva_para_editar.quarto.status})"

        if hospede_display in self.combo_hospede['values']:
            self.combo_hospede.set(hospede_display)
        else:
            print(f"DEBUG: Hóspede '{hospede_display}' não encontrado nas opções do ComboBox.")
            
        if quarto_display in self.combo_quarto['values']:
            self.combo_quarto.set(quarto_display)
        else:
            print(f"DEBUG: Quarto '{quarto_display}' não encontrado nas opções do ComboBox.")
            
        self.entry_data_entrada.delete(0, tk.END)
        self.entry_data_entrada.insert(0, self.reserva_para_editar.data_entrada)
        self.entry_data_saida.delete(0, tk.END)
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
