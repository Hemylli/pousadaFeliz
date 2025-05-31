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
    db = Database()

    # Listando dados
    print("=== HÓSPEDES ===")
    for h in db.listar_hospedes():
        print(h)

    print("\n=== QUARTOS ===")
    for q in db.listar_quartos():
        print(q)

    print("\n=== RESERVAS ===")
    for r in db.listar_reservas():
        print(r)

    db.fechar_conexao()


if __name__ == "__main__":
    bd_conection()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
