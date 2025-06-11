from app.models.hospede import Hospede
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from controller.database import Database 
from app.gui.main_window import MainWindow 
import tkinter as tk
from controller.criar_database import criar_e_popular_database 

def bd_conection():
    db = Database() # Conecta ao banco de dados já populado

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


db_instance = None

if __name__ == "__main__":
    # Cria e popula o banco de dados se necessário.
    criar_e_popular_database() 
    # Cria a instância do banco de dados UMA VEZ
    db_instance = Database()

    # Inicia a interface gráfica
    root = tk.Tk()
    app = MainWindow(root, db_instance)
    root.mainloop()

    # Fechar a conexão quando a aplicação Tkinter for encerrada
    if db_instance:
        db_instance.fechar_conexao()