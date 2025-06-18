import tkinter as tk
from tkinter import ttk, messagebox
from controller.database import Database
from app.models.quarto import Quarto

class TelaQuartos:
    def __init__(self, master, db: Database):
        self.master = master
        self.db = db
        self.quarto_selecionado_id = None 

        self.general_bg = "#f0f1f1"  
        self.purple_color = "#A679E3" 
        self.cyan_color = "#80FFFF" 
        self.text_dark = "black" 
        
        frame = tk.Frame(master, bg=self.general_bg)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text="Gerenciamento de Quartos", font=("Arial", 16, "bold"),
                         bg=self.general_bg, fg=self.text_dark)
        label.pack(pady=10)

        # Campos de Entrada para Adicionar/Editar 
        form_frame = tk.Frame(frame, bg=self.general_bg, padx=20, pady=10) 
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Número:", bg=self.general_bg, fg=self.text_dark).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_numero = tk.Entry(form_frame, width=20, bg="white", fg="black") 
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5, sticky="ew") 
        
        tk.Label(form_frame, text="Tipo:", bg=self.general_bg, fg=self.text_dark).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_tipo = ttk.Combobox(form_frame, width=15, values=["Simples", "Duplo", "Suíte", "Luxo"], state="readonly")
        self.combo_tipo.grid(row=0, column=3, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="Preço:", bg=self.general_bg, fg=self.text_dark).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_preco = tk.Entry(form_frame, width=20, bg="white", fg="black") 
        self.entry_preco.grid(row=1, column=1, padx=5, pady=5, sticky="ew") 

        tk.Label(form_frame, text="Status:", bg=self.general_bg, fg=self.text_dark).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.combo_status = ttk.Combobox(form_frame, width=15, values=["Disponível", "Ocupado", "Manutenção", "Limpeza"], state="readonly")
        self.combo_status.grid(row=1, column=3, padx=5, pady=5, sticky="ew") 

        # Configurar expansão de colunas
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1) 


        # Botões de Ação 
        botoes_acao_frame = tk.Frame(frame, bg=self.general_bg)
        botoes_acao_frame.pack(pady=10)

        button_options = {
            "font": ("Arial", 10, "bold"), "bg": self.purple_color, "fg": "white", 
            "activebackground": self.cyan_color, "activeforeground": "white",
            "bd": 0, "relief": "flat", "padx": 8, "pady": 4, "cursor": "hand2"
        }
        tk.Button(botoes_acao_frame, text="Adicionar Quarto", command=self.adicionar_quarto, **button_options).grid(row=0, column=0, padx=5)
        tk.Button(botoes_acao_frame, text="Atualizar Quarto", command=self.atualizar_quarto, **button_options).grid(row=0, column=1, padx=5)
        tk.Button(botoes_acao_frame, text="Excluir Quarto", command=self.excluir_quarto, **button_options).grid(row=0, column=2, padx=5)
        tk.Button(botoes_acao_frame, text="Limpar Campos", command=self.limpar_campos, **button_options).grid(row=0, column=3, padx=5)

        # Tabela 
        colunas = ("ID", "Número", "Tipo", "Preço", "Status")
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


        self.tabela.heading("ID", text="ID")
        self.tabela.column("ID", width=50) 
        self.tabela.heading("Número", text="Número")
        self.tabela.column("Número", width=80)
        self.tabela.heading("Tipo", text="Tipo")
        self.tabela.column("Tipo", width=100)
        self.tabela.heading("Preço", text="Preço")
        self.tabela.column("Preço", width=100)
        self.tabela.heading("Status", text="Status")
        self.tabela.column("Status", width=100)

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_quarto)

        self.carregar_quartos()

    def carregar_quartos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        try:
            quartos = self.db.listar_quartos()
            for q in quartos:
                self.tabela.insert("", "end", values=(q.id, q.numero, q.tipo, q.preco, q.status), iid=q.id)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar quartos: {e}")

    def limpar_campos(self):
        self.entry_numero.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_preco.delete(0, tk.END)
        self.combo_status.set("")
        self.quarto_selecionado_id = None

    def selecionar_quarto(self, event):
        selected_item = self.tabela.focus()
        if selected_item:
            # Limpa os campos antes de preenchê-los com os novos dados
            self.entry_numero.delete(0, tk.END)
            self.combo_tipo.set("")
            self.entry_preco.delete(0, tk.END)
            self.combo_status.set("")
            
            # Pega os valores e define o ID selecionado
            valores = self.tabela.item(selected_item, 'values')
            self.quarto_selecionado_id = valores[0] 

            # Preenche os campos com os dados da linha selecionada
            self.entry_numero.insert(0, valores[1])
            self.combo_tipo.set(valores[2])
            self.entry_preco.insert(0, valores[3])
            self.combo_status.set(valores[4])
        else:
            # Se nada for selecionado, limpa todos os campos e o ID
            self.limpar_campos()

    def adicionar_quarto(self):
        numero = self.entry_numero.get()
        tipo = self.combo_tipo.get()
        preco_str = self.entry_preco.get()
        status = self.combo_status.get()

        if not (numero and tipo and preco_str and status):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        try:
            numero = int(numero)
            preco = float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "Número e Preço devem ser valores numéricos válidos.")
            return

        try:
            novo_quarto = Quarto(id=None, numero=numero, tipo=tipo, preco=preco, status=status)
            self.db.adicionar_quarto(novo_quarto)
            messagebox.showinfo("Sucesso", "Quarto adicionado com sucesso!")
            self.limpar_campos()
            self.carregar_quartos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar quarto: {e}")

    def atualizar_quarto(self):
        if not self.quarto_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um quarto para atualizar.")
            return

        numero = self.entry_numero.get()
        tipo = self.combo_tipo.get()
        preco_str = self.entry_preco.get()
        status = self.combo_status.get()

        if not (numero and tipo and preco_str and status):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        
        try:
            numero = int(numero)
            preco = float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "Número e Preço devem ser valores numéricos válidos.")
            return

        try:
            self.db.alterar_quarto(self.quarto_selecionado_id, numero, tipo, preco, status)
            
            messagebox.showinfo("Sucesso", "Quarto atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_quartos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar quarto: {e}")

    def excluir_quarto(self):
        if not self.quarto_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um quarto para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este quarto? Todas as reservas relacionadas a ele ficarão inconsistentes se você não as gerenciar.")
        if confirmacao:
            try:
                self.db.excluir_quarto(self.quarto_selecionado_id)

                messagebox.showinfo("Sucesso", "Quarto excluído com sucesso!")
                self.limpar_campos()
                self.carregar_quartos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir quarto: {e}")
