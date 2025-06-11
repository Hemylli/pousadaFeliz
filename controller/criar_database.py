import sqlite3
import os
import datetime 
from controller.database import Database 

def criar_e_popular_database(db_name="pousada.db"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    os.makedirs(data_dir, exist_ok=True)
    
    db_path = os.path.join(data_dir, db_name)

    # Se o arquivo do banco de dados já existe, remove-o para garantir uma recriação limpa.
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Arquivo de banco de dados existente '{db_name}' removido para recriação.")
        except OSError as e:
            print(f"Erro ao remover o arquivo de banco de dados '{db_name}': {e}")
            raise 

    print(f"Banco de dados '{db_name}' não encontrado ou foi removido. Criando e populando...")

    # Instancia o Database
    db = Database(db_name) 

    # --- INÍCIO DA POPULAÇÃO DE DADOS ---
    # HÓSPEDES
    hospedes_data = [
        ("Ana Silva", "111.111.111-11", "(11) 98765-4321", "ana.silva@email.com"),
        ("Bruno Costa", "222.222.222-22", "(21) 99876-5432", "bruno.costa@email.com"),
        ("Carla Mendes", "333.333.333-33", "(31) 97654-3210", "carla.mendes@email.com"),
        ("Daniel Rocha", "444.444.444-44", "(41) 96543-2109", "daniel.rocha@email.com"),
        ("Eliane Souza", "555.555.555-55", "(51) 95432-1098", "eliane.souza@email.com"),
        ("Fernando Lima", "666.666.666-66", "(61) 94321-0987", "fernando.lima@email.com"),
        ("Giovana Pereira", "777.777.777-77", "(71) 93210-9876", "giovana.pereira@email.com"),
        ("Hugo Martins", "888.888.888-88", "(81) 92109-8765", "hugo.martins@email.com"),
    ]
    db.cursor.executemany("INSERT INTO hospedes (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)", hospedes_data)
    db.conexao.commit()

    # QUARTOS
    quartos_data = [
        (101, "Simples", 150.00, "Disponível"),
        (102, "Simples", 150.00, "Disponível"),
        (201, "Duplo", 250.00, "Ocupado"),
        (202, "Duplo", 250.00, "Disponível"),
        (301, "Luxo", 400.00, "Manutenção"),
        (302, "Luxo", 400.00, "Disponível"),
        (401, "Suíte Master", 700.00, "Disponível"),
    ]
    db.cursor.executemany("INSERT INTO quartos (numero, tipo, preco, status) VALUES (?, ?, ?, ?)", quartos_data)
    db.conexao.commit()

    # FUNCIONÁRIOS
    funcionarios_data = [
        ("Admin", "admin", "admin123"), 
        ("Gerente", "gerente", "senha123"),
        ("Recepcionista A", "recepcaoa", "recep123"),
    ]
    db.cursor.executemany("INSERT INTO funcionarios (nome, usuario, senha) VALUES (?, ?, ?)", funcionarios_data)
    db.conexao.commit()

    # RESERVAS
    def _get_hospede_id_by_cpf(cursor, cpf):
        cursor.execute("SELECT id FROM hospedes WHERE cpf=?", (cpf,))
        result = cursor.fetchone()
        return result[0] if result else None

    def _get_quarto_id_by_numero(cursor, numero):
        cursor.execute("SELECT id FROM quartos WHERE numero=?", (numero,))
        result = cursor.fetchone()
        return result[0] if result else None

    ana_silva_id = _get_hospede_id_by_cpf(db.cursor, "111.111.111-11")
    bruno_costa_id = _get_hospede_id_by_cpf(db.cursor, "222.222.222-22")
    carla_mendes_id = _get_hospede_id_by_cpf(db.cursor, "333.333.333-33")
    daniel_rocha_id = _get_hospede_id_by_cpf(db.cursor, "444.444.444-44")

    quarto_101_id = _get_quarto_id_by_numero(db.cursor, 101)
    quarto_102_id = _get_quarto_id_by_numero(db.cursor, 102)
    quarto_201_id = _get_quarto_id_by_numero(db.cursor, 201)
    quarto_302_id = _get_quarto_id_by_numero(db.cursor, 302)

    hoje = datetime.date.today()
    proxima_semana = hoje + datetime.timedelta(weeks=1)
    duas_semanas = hoje + datetime.timedelta(weeks=2)
    data_futura_curta = hoje + datetime.timedelta(days=5)
    data_passada_entrada = hoje - datetime.timedelta(days=10)
    data_passada_saida = hoje - datetime.timedelta(days=5)

    reservas_data = []
    
    if bruno_costa_id and quarto_201_id: 
         reservas_data.append((bruno_costa_id, quarto_201_id, hoje.strftime("%Y-%m-%d"), proxima_semana.strftime("%Y-%m-%d"), "Ativa"))
    
    if ana_silva_id and quarto_101_id: 
        reservas_data.append((ana_silva_id, quarto_101_id, data_passada_entrada.strftime("%Y-%m-%d"), data_passada_saida.strftime("%Y-%m-%d"), "Finalizada"))

    if carla_mendes_id and quarto_302_id: 
        reservas_data.append((carla_mendes_id, quarto_302_id, data_futura_curta.strftime("%Y-%m-%d"), proxima_semana.strftime("%Y-%m-%d"), "Cancelada"))
    
    if daniel_rocha_id and quarto_102_id: 
        reservas_data.append((daniel_rocha_id, quarto_102_id, hoje.strftime("%Y-%m-%d"), duas_semanas.strftime("%Y-%m-%d"), "Ativa")) # Ajustado para hoje para testar conflito

    if reservas_data:
        db.cursor.executemany("INSERT INTO reservas (hospede_id, quarto_id, data_entrada, data_saida, status) VALUES (?, ?, ?, ?, ?)", reservas_data)
        db.conexao.commit()
    
    db.fechar_conexao()
    print("População de dados concluída. Banco de dados está pronto.")