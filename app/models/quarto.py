class Quarto:
    def __init__(self, id, numero, tipo, preco, status="Disponível"):
        self.id = id
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.status = status  # Disponível, Ocupado, Manutenção...

    def __str__(self):
        return f"Quarto {self.numero} - {self.tipo} - {self.status}"
