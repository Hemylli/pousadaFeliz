import tkinter as tk
from controller.database import Database
from controller.criar_database import criar_e_popular_database
from app.gui.tela_login import TelaLogin

if __name__ == "__main__":
    criar_e_popular_database()
    db_instance = Database()

    root = tk.Tk()
    app = TelaLogin(root, db_instance)
    root.mainloop()

    if db_instance:
        db_instance.fechar_conexao()
        print("Conexão com o banco de dados fechada.")
