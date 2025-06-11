import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.hospede import Hospede 

class TelaClientes:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db
        self.hospede_selecionado_id = None 

        self.primary_bg = "#a5f0f3"  
        self.secondary_bg = "#a6b8f3" 
        self.text_color = "#333333"  
        
        frame = tk.Frame(master, bg=self.primary_bg)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Clientes", font=("Arial", 18, "bold"),
                         bg=self.primary_bg, fg=self.text_color)
        label.pack(pady=10)

        # Campos de Entrada para Adicionar/Editar
        form_frame = tk.Frame(frame, bg=self.primary_bg)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nome:", bg=self.primary_bg, fg=self.text_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(form_frame, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="CPF:", bg=self.primary_bg, fg=self.text_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_cpf = ttk.Entry(form_frame, width=40) 
        self.entry_cpf.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Telefone:", bg=self.primary_bg, fg=self.text_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefone = ttk.Entry(form_frame, width=40) 
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email:", bg=self.primary_bg, fg=self.text_color).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_email = ttk.Entry(form_frame, width=40) 
        self.entry_email.grid(row=3, column=1, padx=5, pady=5)

        # Botões de Ação
        botoes_acao_frame = tk.Frame(frame, bg=self.primary_bg)
        botoes_acao_frame.pack(pady=10)

        ttk.Button(botoes_acao_frame, text="Adicionar Cliente", command=self.adicionar_hospede).grid(row=0, column=0, padx=5)
        ttk.Button(botoes_acao_frame, text="Atualizar Cliente", command=self.atualizar_hospede).grid(row=0, column=1, padx=5)
        ttk.Button(botoes_acao_frame, text="Excluir Cliente", command=self.excluir_hospede).grid(row=0, column=2, padx=5)
        ttk.Button(botoes_acao_frame, text="Limpar Campos", command=self.limpar_campos).grid(row=0, column=3, padx=5)


        # Tabela de clientes
        colunas = ("ID", "Nome", "CPF", "Telefone", "Email") 
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        self.tabela.heading("ID", text="ID")
        self.tabela.column("ID", width=50)
        self.tabela.heading("Nome", text="Nome")
        self.tabela.column("Nome", width=150)
        self.tabela.heading("CPF", text="CPF")
        self.tabela.column("CPF", width=100)
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.column("Telefone", width=100)
        self.tabela.heading("Email", text="Email")
        self.tabela.column("Email", width=150)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_hospede)

        self.carregar_hospedes()

        # Área para envio de mensagem 
        label_mensagem = tk.Label(frame, text="Enviar Mensagem para Cliente Selecionado:", bg=self.primary_bg, fg=self.text_color)
        label_mensagem.pack(pady=5)

        self.texto_mensagem = tk.Text(frame, height=3, width=80)
        self.texto_mensagem.pack(pady=5)

        ttk.Button(frame, text="Enviar Mensagem", command=self.enviar_mensagem).pack(pady=5)

    def carregar_hospedes(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        try:
            hospedes = self.db.listar_hospedes()
            for h in hospedes:
                self.tabela.insert("", "end", values=(h.id, h.nome, h.cpf, h.telefone, h.email), iid=h.id)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar hóspedes: {e}")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.hospede_selecionado_id = None

    def selecionar_hospede(self, event):
        selected_item = self.tabela.focus()
        if selected_item:
            valores = self.tabela.item(selected_item, 'values')
            self.hospede_selecionado_id = valores[0] 

            self.limpar_campos() 
            self.entry_nome.insert(0, valores[1])
            self.entry_cpf.insert(0, valores[2])
            self.entry_telefone.insert(0, valores[3])
            self.entry_email.insert(0, valores[4])
        else:
            self.hospede_selecionado_id = None

    def adicionar_hospede(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()

        if not (nome and cpf and telefone and email):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        try:
            novo_hospede = Hospede(id=None, nome=nome, cpf=cpf, telefone=telefone, email=email)
            self.db.adicionar_hospede(novo_hospede)
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            self.limpar_campos()
            self.carregar_hospedes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar cliente: {e}")

    def atualizar_hospede(self):
        if not self.hospede_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para atualizar.")
            return

        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()

        if not (nome and cpf and telefone and email):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        
        try:
            self.db.alterar_hospede(self.hospede_selecionado_id, nome, cpf, telefone, email)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_hospedes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")

    def excluir_hospede(self):
        if not self.hospede_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este cliente? Isso pode afetar reservas existentes.")
        if confirmacao:
            try:
                self.db.excluir_hospede(self.hospede_selecionado_id)

                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.limpar_campos()
                self.carregar_hospedes()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir cliente: {e}")

    def enviar_mensagem(self):
        mensagem = self.texto_mensagem.get("1.0", tk.END).strip()
        if not hasattr(self, 'hospede_selecionado_id') or not self.hospede_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para enviar a mensagem.")
            return

        if mensagem:
            hospede_selecionado = self.db.buscar_hospede_por_id(self.hospede_selecionado_id)
            if hospede_selecionado:
                messagebox.showinfo("Mensagem Enviada", f"Simulando envio para {hospede_selecionado.nome} ({hospede_selecionado.email}):\n{mensagem}")
                self.texto_mensagem.delete("1.0", tk.END)
            else:
                messagebox.showerror("Erro", "Cliente selecionado não encontrado no banco de dados.")
        else:
            messagebox.showwarning("Atenção", "Digite uma mensagem para enviar.")