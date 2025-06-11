import sqlite3
import os
from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.funcionario import Funcionario 

class Database:
    def __init__(self, db_name="pousada.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        
        os.makedirs(data_dir, exist_ok=True)
        
        self.db_path = os.path.join(data_dir, db_name) 
        self.conexao = sqlite3.connect(self.db_path)
        self.cursor = self.conexao.cursor()
        self.criar_tabelas() 

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospedes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quartos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL UNIQUE,
                tipo TEXT NOT NULL,
                preco REAL NOT NULL,
                status TEXT DEFAULT 'Disponível'
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hospede_id INTEGER NOT NULL,
                quarto_id INTEGER NOT NULL,
                data_entrada TEXT NOT NULL,
                data_saida TEXT NOT NULL,
                status TEXT DEFAULT 'Ativa',
                FOREIGN KEY (hospede_id) REFERENCES hospedes(id),
                FOREIGN KEY (quarto_id) REFERENCES quartos(id)
            )
        ''')

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            );
        """)

        self.conexao.commit()

    # ----------------------------
    # CRUD HÓSPEDES
    # ----------------------------
    def adicionar_hospede(self, hospede: Hospede):
        self.cursor.execute('''
            INSERT INTO hospedes (nome, cpf, telefone, email)
            VALUES (?, ?, ?, ?)
        ''', (hospede.nome, hospede.cpf, hospede.telefone, hospede.email))
        self.conexao.commit()

    def listar_hospedes(self):
        self.cursor.execute('SELECT * FROM hospedes')
        registros = self.cursor.fetchall()
        return [Hospede(*r) for r in registros]

    def buscar_hospede_por_id(self, id):
        self.cursor.execute('SELECT * FROM hospedes WHERE id = ?', (id,))
        r = self.cursor.fetchone()
        return Hospede(*r) if r else None

    def alterar_hospede(self, hospede_id, nome=None, cpf=None, telefone=None, email=None):
        self.cursor.execute('SELECT * FROM hospedes WHERE id = ?', (hospede_id,))
        hospede = self.cursor.fetchone()
        if not hospede:
            print("Hóspede não encontrado.")
            return

        novo_nome = nome if nome else hospede[1]
        novo_cpf = cpf if cpf else hospede[2]
        novo_telefone = telefone if telefone else hospede[3]
        novo_email = email if email else hospede[4]

        self.cursor.execute('''
            UPDATE hospedes
            SET nome = ?, cpf = ?, telefone = ?, email = ?
            WHERE id = ?
        ''', (novo_nome, novo_cpf, novo_telefone, novo_email, hospede_id))
        self.conexao.commit()

    def excluir_hospede(self, id_hospede):
        """Exclui um hóspede do banco de dados pelo ID."""
        self.cursor.execute("DELETE FROM hospedes WHERE id = ?", (id_hospede,))
        self.conexao.commit()


    # ----------------------------
    # CRUD QUARTOS
    # ----------------------------
    def adicionar_quarto(self, quarto: Quarto):
        self.cursor.execute('''
            INSERT INTO quartos (numero, tipo, preco, status)
            VALUES (?, ?, ?, ?)
        ''', (quarto.numero, quarto.tipo, quarto.preco, quarto.status))
        self.conexao.commit()

    def listar_quartos(self):
        self.cursor.execute('SELECT * FROM quartos')
        registros = self.cursor.fetchall()
        return [Quarto(*r) for r in registros]
    
    def buscar_quarto_por_id(self, id): 
        self.cursor.execute('SELECT * FROM quartos WHERE id = ?', (id,))
        r = self.cursor.fetchone()
        return Quarto(*r) if r else None

    def alterar_quarto(self, id_quarto, numero=None, tipo=None, preco=None, status=None):
        """Atualiza um quarto existente no banco de dados."""
        self.cursor.execute('SELECT * FROM quartos WHERE id = ?', (id_quarto,))
        quarto = self.cursor.fetchone()
        if not quarto:
            print(f"Quarto com ID {id_quarto} não encontrado.")
            return

        # Pega os valores atuais se os novos não forem fornecidos
        novo_numero = numero if numero is not None else quarto[1]
        novo_tipo = tipo if tipo is not None else quarto[2]
        novo_preco = preco if preco is not None else quarto[3]
        novo_status = status if status is not None else quarto[4]

        self.cursor.execute('''
            UPDATE quartos
            SET numero = ?, tipo = ?, preco = ?, status = ?
            WHERE id = ?
        ''', (novo_numero, novo_tipo, novo_preco, novo_status, id_quarto))
        self.conexao.commit()

    def alterar_status_quarto(self, quarto_id, novo_status): 
        self.cursor.execute('''
            UPDATE quartos SET status = ? WHERE id = ?
        ''', (novo_status, quarto_id))
        self.conexao.commit()
    
    def excluir_quarto(self, id_quarto):
        """Exclui um quarto do banco de dados pelo ID."""
        self.cursor.execute("DELETE FROM quartos WHERE id = ?", (id_quarto,))
        self.conexao.commit()


    # ----------------------------
    # CRUD RESERVAS
    # ----------------------------
    def adicionar_reserva(self, reserva: Reserva):
        self.cursor.execute('''
            INSERT INTO reservas (hospede_id, quarto_id, data_entrada, data_saida, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            reserva.hospede.id,
            reserva.quarto.id,
            reserva.data_entrada,
            reserva.data_saida,
            reserva.status
        ))
        self.conexao.commit()

    def listar_reservas(self):
        self.cursor.execute('SELECT * FROM reservas')
        registros = self.cursor.fetchall()
        reservas = []

        for r in registros:
            id_reserva, hospede_id, quarto_id, data_entrada, data_saida, status = r

            hospede = self.buscar_hospede_por_id(hospede_id)
            quarto = self.buscar_quarto_por_id(quarto_id)

            if hospede and quarto:
                reserva = Reserva(
                    id=id_reserva,
                    hospede=hospede,
                    quarto=quarto,
                    data_entrada=data_entrada,
                    data_saida=data_saida,
                    status=status
                )
                reservas.append(reserva)

        return reservas
    
    def atualizar_reserva(self, id_reserva, hospede_id, quarto_id, data_entrada, data_saida, status):
        """Atualiza uma reserva existente no banco de dados."""
        self.cursor.execute("""
            UPDATE reservas
            SET hospede_id = ?, quarto_id = ?, data_entrada = ?, data_saida = ?, status = ?
            WHERE id = ?
        """, (hospede_id, quarto_id, data_entrada, data_saida, status, id_reserva))
        self.conexao.commit()
        

    def alterar_status_reserva(self, reserva_id, novo_status): 
        self.cursor.execute('''
            UPDATE reservas SET status = ? WHERE id = ?
        ''', (novo_status, reserva_id))
        self.conexao.commit()

    # ----------------------------
    # VERIFICAR DISPONIBILIDADE
    # ----------------------------

    def verificar_disponibilidade_quarto(self, quarto_id, data_entrada, data_saida, id_reserva_ignorar=None):
        query = '''
            SELECT * FROM reservas
            WHERE quarto_id = ?
            AND status = 'Ativa'
            AND (
                (data_entrada <= ? AND data_saida > ?) OR  -- Nova reserva começa antes da atual e termina depois
                (data_entrada < ? AND data_saida >= ?) OR  -- Nova reserva começa antes da atual e termina na atual
                (data_entrada >= ? AND data_saida <= ?)    -- Nova reserva está contida na atual
            )
        '''
        params = [quarto_id, data_saida, data_entrada, data_saida, data_entrada, data_entrada, data_saida]
        
        if id_reserva_ignorar:
            query += " AND id != ?"
            params.append(id_reserva_ignorar)

        self.cursor.execute(query, tuple(params))
        conflitos = self.cursor.fetchall()
        return len(conflitos) == 0


    def listar_periodos_ocupados_quarto(self, quarto_id):
        """
        Retorna uma lista de tuplas (data_entrada, data_saida)
        com os períodos já reservados desse quarto.
        """
        self.cursor.execute('''
            SELECT data_entrada, data_saida
            FROM reservas
            WHERE quarto_id = ? AND status = 'Ativa'
        ''', (quarto_id,))

        return self.cursor.fetchall()
    
    # ----------------------------
    # CRUD FUNCIONÁRIOS
    # ----------------------------
    def cadastrar_funcionario(self, nome, usuario, senha):
        try:
            self.cursor.execute("INSERT INTO funcionarios (nome, usuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar_funcionarios(self):
        self.cursor.execute("SELECT * FROM funcionarios")
        registros = self.cursor.fetchall()
        return [Funcionario(*r) for r in registros] 

    def atualizar_funcionario(self, id_funcionario, nome, usuario, senha):
        self.cursor.execute("""
            UPDATE funcionarios
            SET nome = ?, usuario = ?, senha = ?
            WHERE id = ?
        """, (nome, usuario, senha, id_funcionario))
        self.conexao.commit()

    def excluir_funcionario(self, id_funcionario):
        self.cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_funcionario,))
        self.conexao.commit()

    def autenticar_funcionario(self, usuario, senha):
        self.cursor.execute("SELECT * FROM funcionarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        funcionario_data = self.cursor.fetchone()
        if funcionario_data:
            return Funcionario(*funcionario_data)
        return None 

    # ----------------------------
    # FECHAR CONEXÃO
    # ----------------------------
    def fechar_conexao(self):
        self.conexao.close()