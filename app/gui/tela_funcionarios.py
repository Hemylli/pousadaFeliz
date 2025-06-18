import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.funcionario import Funcionario 

class TelaFuncionarios:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db 
        
        self.general_bg = "#f0f1f1"  
        self.purple_color = "#A679E3" 
        self.cyan_color = "#80FFFF" 
        self.text_dark = "black"  
        
        self.frame = tk.Frame(master, bg=self.general_bg)
        self.frame.pack(fill="both", expand=True)

        self.id_selecionado = None

        label = tk.Label(self.frame, text="Gerenciamento de Funcionários", font=("Arial", 16, "bold"),
                         bg=self.general_bg, fg=self.text_dark)
        label.pack(pady=10)

        # Labels e Entrys 
        form_frame = tk.Frame(self.frame, bg=self.general_bg, padx=20, pady=10) 
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nome:", bg=self.general_bg, fg=self.text_dark).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = tk.Entry(form_frame, width=30, bg="white", fg="black") 
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="Usuário:", bg=self.general_bg, fg=self.text_dark).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_usuario = tk.Entry(form_frame, width=30, bg="white", fg="black") 
        self.entry_usuario.grid(row=1, column=1, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="Senha:", bg=self.general_bg, fg=self.text_dark).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_senha = tk.Entry(form_frame, width=30, show="*", bg="white", fg="black") 
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5, sticky="ew") 

        # Configurar expansão de colunas
        form_frame.grid_columnconfigure(1, weight=1) 

        # Botões 
        botoes_frame = tk.Frame(self.frame, bg=self.general_bg)
        botoes_frame.pack(pady=10)

        button_options = {
            "font": ("Arial", 10), "bg": self.purple_color, "fg": "white", 
            "activebackground": self.cyan_color, "activeforeground": "white",
            "bd": 1, "relief": "raised", "padx": 8, "pady": 4, "cursor": "hand2"
        }
        tk.Button(botoes_frame, text="Adicionar", command=self.adicionar_funcionario, **button_options).grid(row=0, column=0, padx=5)
        tk.Button(botoes_frame, text="Atualizar", command=self.atualizar_funcionario, **button_options).grid(row=0, column=1, padx=5)
        tk.Button(botoes_frame, text="Excluir", command=self.excluir_funcionario, **button_options).grid(row=0, column=2, padx=5)
        tk.Button(botoes_frame, text="Limpar Campos", command=self.limpar_campos, **button_options).grid(row=0, column=3, padx=5)


        # Tabela 
        self.tabela = ttk.Treeview(self.frame, columns=("ID", "Nome", "Usuário", "Senha"), show="headings")

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


        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Usuário", text="Usuário")
        self.tabela.heading("Senha", text="Senha")

        self.tabela.column("ID", width=50)
        self.tabela.column("Nome", width=150)
        self.tabela.column("Usuário", width=150)
        self.tabela.column("Senha", width=150)

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_linha)

        self.carregar_funcionarios()

    def adicionar_funcionario(self):
        nome = self.entry_nome.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if nome and usuario and senha:
            sucesso = self.db.cadastrar_funcionario(nome, usuario, senha)
            if sucesso:
                messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
                self.limpar_campos()
                self.carregar_funcionarios()
            else:
                messagebox.showerror("Erro", "Usuário já existe ou outro erro de banco de dados!")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def carregar_funcionarios(self):
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        funcionarios = self.db.listar_funcionarios()
        for f in funcionarios:
            self.tabela.insert("", "end", values=(f.id, f.nome, f.usuario, f.senha), iid=f.id)

    def selecionar_linha(self, event):
        selected_item = self.tabela.focus()
        if selected_item:
            # Limpa os campos de entrada primeiro
            self.entry_nome.delete(0, tk.END)
            self.entry_usuario.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)

            # Pega os valores e define o ID selecionado
            valores = self.tabela.item(selected_item, "values")
            self.id_selecionado = valores[0]

            # Preenche os campos com os novos valores
            self.entry_nome.insert(0, valores[1])
            self.entry_usuario.insert(0, valores[2])
            self.entry_senha.insert(0, valores[3])
        else:
            # Se nada for selecionado, limpa tudo
            self.limpar_campos()

    def atualizar_funcionario(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um funcionário para atualizar.")
            return

        nome = self.entry_nome.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not (nome and usuario and senha):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        
        try:
            self.db.atualizar_funcionario(self.id_selecionado, nome, usuario, senha)
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar funcionário: {e}")

    def excluir_funcionario(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um funcionário para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Deseja excluir este funcionário?")
        if confirmacao:
            try:
                self.db.excluir_funcionario(self.id_selecionado)
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                self.limpar_campos()
                self.carregar_funcionarios()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir funcionário: {e}")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.id_selecionado = None
