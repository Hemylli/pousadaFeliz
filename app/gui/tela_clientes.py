import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.hospede import Hospede 
import re

class TelaClientes:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db
        self.hospede_selecionado_id = None 

        self.general_bg = "#f0f1f1"
        self.purple_color = "#A679E3"
        self.cyan_color = "#80FFFF"
        self.text_dark = "black"
        
        frame = tk.Frame(master, bg=self.general_bg)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Clientes", font=("Arial", 16, "bold"),
                         bg=self.general_bg, fg=self.text_dark)
        label.pack(pady=10)

        form_frame = tk.Frame(frame, bg=self.general_bg, padx=20, pady=10)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nome:", bg=self.general_bg, fg=self.text_dark).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = tk.Entry(form_frame, width=40, bg="white", fg="black") 
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="CPF:", bg=self.general_bg, fg=self.text_dark).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_cpf = tk.Entry(form_frame, width=40, bg="white", fg="black") 
        self.entry_cpf.grid(row=1, column=1, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="Telefone:", bg=self.general_bg, fg=self.text_dark).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefone = tk.Entry(form_frame, width=40, bg="white", fg="black") 
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="Email:", bg=self.general_bg, fg=self.text_dark).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_email = tk.Entry(form_frame, width=40, bg="white", fg="black") 
        self.entry_email.grid(row=3, column=1, padx=5, pady=5, sticky="ew") 

        form_frame.grid_columnconfigure(1, weight=1) 

        botoes_acao_frame = tk.Frame(frame, bg=self.general_bg)
        botoes_acao_frame.pack(pady=10)

        button_options = {
            "font": ("Arial", 10, "bold"), "bg": self.purple_color, "fg": "white", 
            "activebackground": self.cyan_color, "activeforeground": "white",
            "bd": 1, "relief": "raised", "padx": 8, "pady": 4, "cursor": "hand2"
        }
        tk.Button(botoes_acao_frame, text="Adicionar Cliente", command=self.adicionar_hospede, **button_options).grid(row=0, column=0, padx=5)
        tk.Button(botoes_acao_frame, text="Atualizar Cliente", command=self.atualizar_hospede, **button_options).grid(row=0, column=1, padx=5)
        tk.Button(botoes_acao_frame, text="Excluir Cliente", command=self.excluir_hospede, **button_options).grid(row=0, column=2, padx=5)
        tk.Button(botoes_acao_frame, text="Limpar Campos", command=self.limpar_campos, **button_options).grid(row=0, column=3, padx=5)

        colunas = ("ID", "Nome", "CPF", "Telefone", "Email") 
        self.tabela = ttk.Treeview(frame, columns=colunas, show="headings")

        style = ttk.Style()
        try: 
            style.theme_use('clam')
        except tk.TclError:
            style.theme_use('default')
        style.configure("Treeview", background="white", foreground=self.text_dark, fieldbackground="white")
        style.configure("Treeview.Heading", background=self.purple_color, foreground="white", font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.purple_color)]) 
        style.map("Treeview.Heading", background=[('active', self.cyan_color)], foreground=[('active', self.text_dark)])

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

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_hospede)

        self.carregar_hospedes()


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
            self.entry_nome.delete(0, tk.END)
            self.entry_cpf.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            
            valores = self.tabela.item(selected_item, 'values')
            self.hospede_selecionado_id = valores[0] 

            self.entry_nome.insert(0, valores[1])
            self.entry_cpf.insert(0, valores[2])
            self.entry_telefone.insert(0, valores[3])
            self.entry_email.insert(0, valores[4])
        else:
            self.limpar_campos()

    def _validar_e_formatar_dados(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()

        if not (nome and cpf and telefone and email):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return None

        # Validação do Email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Dados Inválidos", "O formato do email é inválido.")
            return None

        # Validação e formatação do CPF (remove caracteres não numéricos)
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) != 11:
            messagebox.showwarning("Dados Inválidos", "O CPF deve conter 11 dígitos numéricos.")
            return None
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

        # Validação e formatação do Telefone (remove caracteres não numéricos)
        tel_limpo = re.sub(r'\D', '', telefone)
        if not (10 <= len(tel_limpo) <= 11):
            messagebox.showwarning("Dados Inválidos", "O telefone deve conter 10 ou 11 dígitos numéricos (com DDD).")
            return None
        if len(tel_limpo) == 11:
            tel_formatado = f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
        else:
            tel_formatado = f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"

        return nome, cpf_formatado, tel_formatado, email

    def adicionar_hospede(self):
        dados_validados = self._validar_e_formatar_dados()
        if not dados_validados:
            return

        nome, cpf, telefone, email = dados_validados

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

        dados_validados = self._validar_e_formatar_dados()
        if not dados_validados:
            return
            
        nome, cpf, telefone, email = dados_validados
        
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
