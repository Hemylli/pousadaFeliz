class Hospede:
    def __init__(self, id, nome, cpf, telefone, email):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email

    def __str__(self):
        return f"Hóspede {self.nome} (ID: {self.id})"
