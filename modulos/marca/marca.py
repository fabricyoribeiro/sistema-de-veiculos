class Marca:
  VALUES = ['marca', 'classificacao']
  def __init__(self, marca, classificacao,id=None):
    self.id = id
    self.marca = marca
    self.classificacao = classificacao

  def __str__(self):
    return f'Id: {self.id}, Marca: {self.marca}, classificacao: {self.classificacao}'
  
  def get_data_dict(self):
    return {'id':self.id, 'marca': self.marca, 'classificacao': self.classificacao}