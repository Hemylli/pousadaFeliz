import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.funcionario import Funcionario # Importa o modelo Funcionario

class TelaFuncionarios:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db 
        
        self.primary_bg = "#a5f0f3"  
        self.secondary_bg = "#a6b8f3" 
        self.text_color = "#333333"  
        
        self.root = tk.Toplevel(master) # Tela de funcionários é uma Toplevel
        self.root.title("Gerenciamento de Funcionários")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.config(bg=self.primary_bg) # Fundo da janela top-level

        self.id_selecionado = None

        frame = tk.Frame(self.root, bg=self.primary_bg) # Frame principal da tela
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Funcionários", font=("Arial", 18, "bold"),
                         bg=self.primary_bg, fg=self.text_color)
        label.pack(pady=10)

        # Labels e Entrys
        form_frame = tk.Frame(frame, bg=self.primary_bg)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nome:", bg=self.primary_bg, fg=self.text_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Usuário:", bg=self.primary_bg, fg=self.text_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_usuario = ttk.Entry(form_frame, width=30)
        self.entry_usuario.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Senha:", bg=self.primary_bg, fg=self.text_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_senha = ttk.Entry(form_frame, width=30, show="*")
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)

        # Botões
        botoes_frame = tk.Frame(frame, bg=self.primary_bg)
        botoes_frame.pack(pady=10)

        ttk.Button(botoes_frame, text="Adicionar", command=self.adicionar_funcionario).grid(row=0, column=0, padx=5)
        ttk.Button(botoes_frame, text="Atualizar", command=self.atualizar_funcionario).grid(row=0, column=1, padx=5)
        ttk.Button(botoes_frame, text="Excluir", command=self.excluir_funcionario).grid(row=0, column=2, padx=5)
        ttk.Button(botoes_frame, text="Limpar Campos", command=self.limpar_campos).grid(row=0, column=3, padx=5)


        # Tabela
        self.tabela = ttk.Treeview(frame, columns=("ID", "Nome", "Usuário", "Senha"), show="headings")
        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Usuário", text="Usuário")
        self.tabela.heading("Senha", text="Senha")

        self.tabela.column("ID", width=50)
        self.tabela.column("Nome", width=150)
        self.tabela.column("Usuário", width=150)
        self.tabela.column("Senha", width=150)

        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)
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
            valores = self.tabela.item(selected_item, "values")
            self.id_selecionado = valores[0]

            self.limpar_campos()
            self.entry_nome.insert(0, valores[1])
            self.entry_usuario.insert(0, valores[2])
            self.entry_senha.insert(0, valores[3])
        else:
            self.id_selecionado = None

    def atualizar_funcionario(self):
        if not hasattr(self, 'id_selecionado') or not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um funcionário para atualizar.")
            return

        nome = self.entry_nome.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if nome and usuario and senha:
            try:
                self.db.atualizar_funcionario(self.id_selecionado, nome, usuario, senha)
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
                self.limpar_campos()
                self.carregar_funcionarios()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar funcionário: {e}")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def excluir_funcionario(self):
        if not hasattr(self, 'id_selecionado') or not self.id_selecionado:
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