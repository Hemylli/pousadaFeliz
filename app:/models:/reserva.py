from app.models.hospede import Hospede
from app.models.quarto import Quarto

class Reserva:
    def __init__(self, id, hospede: Hospede, quarto: Quarto, data_entrada, data_saida, status="Ativa"):
        self.id = id
        self.hospede = hospede
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.status = status  # Ativa, Finalizada, Cancelada...

    def __str__(self):
        return (f"Reserva {self.id} - Hóspede: {self.hospede.nome} - "
                f"Quarto: {self.quarto.numero} - "
                f"De {self.data_entrada} a {self.data_saida} - {self.status}")
