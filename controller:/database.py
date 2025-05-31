import sqlite3
from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva

class Database:
    def __init__(self, db_path="data/pousada.db"):
        self.db_path = db_path
        self.conexao = sqlite3.connect(self.db_path)
        self.cursor = self.conexao.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospedes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
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

    # ----------------------------
    # BUSCAS AUXILIARES
    # ----------------------------
    def buscar_hospede_por_id(self, id):
        self.cursor.execute('SELECT * FROM hospedes WHERE id = ?', (id,))
        r = self.cursor.fetchone()
        return Hospede(*r) if r else None

    def buscar_quarto_por_id(self, id):
        self.cursor.execute('SELECT * FROM quartos WHERE id = ?', (id,))
        r = self.cursor.fetchone()
        return Quarto(*r) if r else None

    # ----------------------------
    # FECHAR CONEXÃO
    # ----------------------------
    def fechar_conexao(self):
        self.conexao.close()
