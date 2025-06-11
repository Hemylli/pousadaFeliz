import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database 

class TelaFuncionarios:
    def __init__(self, master, db: Database): 
        self.master = master 
        self.db = db 
        self.root = tk.Toplevel(master) # A Toplevel deve ser filha de outra janela Tkinter
        self.root.title("Gerenciamento de Funcionários")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.id_selecionado = None # Inicializa para evitar AttributeError

        self.criar_widgets()
        self.carregar_funcionarios()


    def criar_widgets(self):
        # Labels e Entrys
        tk.Label(self.root, text="Nome:").place(x=20, y=20)
        self.entry_nome = tk.Entry(self.root, width=30)
        self.entry_nome.place(x=80, y=20)

        tk.Label(self.root, text="Usuário:").place(x=20, y=60)
        self.entry_usuario = tk.Entry(self.root, width=30)
        self.entry_usuario.place(x=80, y=60)

        tk.Label(self.root, text="Senha:").place(x=20, y=100)
        self.entry_senha = tk.Entry(self.root, width=30, show="*")
        self.entry_senha.place(x=80, y=100)

        # Botões
        tk.Button(self.root, text="Adicionar", command=self.adicionar_funcionario).place(x=400, y=20)
        tk.Button(self.root, text="Atualizar", command=self.atualizar_funcionario).place(x=400, y=60)
        tk.Button(self.root, text="Excluir", command=self.excluir_funcionario).place(x=400, y=100)

        # Tabela
        self.tabela = ttk.Treeview(self.root, columns=("ID", "Nome", "Usuário", "Senha"), show="headings")
        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Usuário", text="Usuário")
        self.tabela.heading("Senha", text="Senha")

        self.tabela.column("ID", width=50)
        self.tabela.column("Nome", width=150)
        self.tabela.column("Usuário", width=150)
        self.tabela.column("Senha", width=150)

        self.tabela.place(x=20, y=150, width=550, height=200)

        self.tabela.bind("<ButtonRelease-1>", self.selecionar_linha)

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
                messagebox.showerror("Erro", "Usuário já existe!")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def carregar_funcionarios(self):
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        funcionarios = self.db.listar_funcionarios()
        for funcionario in funcionarios:
            self.tabela.insert("", "end", values=funcionario)

    def selecionar_linha(self, event):
        item = self.tabela.selection()[0]
        valores = self.tabela.item(item, "values")
        self.entry_nome.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

        self.entry_nome.insert(0, valores[1])
        self.entry_usuario.insert(0, valores[2])
        self.entry_senha.insert(0, valores[3])

        self.id_selecionado = valores[0]

    def atualizar_funcionario(self):
        try:
            id_funcionario = self.id_selecionado
        except AttributeError:
            messagebox.showwarning("Atenção", "Selecione um funcionário.")
            return

        nome = self.entry_nome.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if nome and usuario and senha:
            self.db.atualizar_funcionario(id_funcionario, nome, usuario, senha)
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_funcionarios()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def excluir_funcionario(self):
        try:
            id_funcionario = self.id_selecionado
        except AttributeError:
            messagebox.showwarning("Atenção", "Selecione um funcionário.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Deseja excluir este funcionário?")
        if confirmacao:
            self.db.excluir_funcionario(id_funcionario)
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
            self.limpar_campos()
            self.carregar_funcionarios()

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.id_selecionado = None