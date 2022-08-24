class Posto:
  def __init__(self, nome, cidade, cnpj, id=None):
    self.id = id
    self.nome = nome
    self.cidade = cidade
    self.cnpj = cnpj
  
  def __str__(self):
    return f'Nome: {self.nome}, cidade: {self.cidade}, cnpj: {self.cnpj}, id: {self.id}'