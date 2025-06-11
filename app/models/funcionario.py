class Funcionario:
    def __init__(self, id, nome, usuario, senha):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.senha = senha 

    def __str__(self):
        return f"Funcionário ID: {self.id}, Nome: {self.nome}, Usuário: {self.usuario}"

    def to_tuple(self):
        return (self.id, self.nome, self.usuario, self.senha)