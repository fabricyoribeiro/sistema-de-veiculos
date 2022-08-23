class Motorista:
  def __init__(self, nome, cpf, salario, id=None):
    self.id = id
    self.nome = nome
    self.cpf = cpf
    self.salario = salario   

  def __str__(self):
    return f'Nome: {self.nome}, id: {self.id}, cpf: {self.cpf}, salario: {self.salario}'
    