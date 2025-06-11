from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from controller.database import Database 
from app.gui.main_window import MainWindow 
import tkinter as tk

def create_objects():
    hospede = Hospede(1, "Ana Souza", "12345678900", "21999999999", "ana@gmail.com")
    quarto = Quarto(1, 101, "Simples", 150.0)
    reserva = Reserva(1, hospede, quarto, "2025-06-01", "2025-06-05")

    # Testando
    print(hospede)
    print(quarto)
    print(reserva)


def bd_conection():
    # instância do banco de dados
    db = Database()

    # Testes de listagem
    print("=== HÓSPEDES ===")
    for h in db.listar_hospedes():
        print(h)

    print("\n=== QUARTOS ===")
    for q in db.listar_quartos():
        print(q)

    print("\n=== RESERVAS ===")
    for r in db.listar_reservas():
        print(r)

# Instância global 
db_instance = None

if __name__ == "__main__":
    # Cria a instância do banco de dados UMA VEZ
    db_instance = Database()

    root = tk.Tk()
    app = MainWindow(root, db_instance)
    root.mainloop()

    # Fechar a conexão quando a aplicação Tkinter for encerrada
    if db_instance:
        db_instance.fechar_conexao()