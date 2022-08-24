class Marca:
  def __init__(self, marca, id=None):
    self.id = id
    self.marca = marca

  def __str__(self):
    return f'Id: {self.id}, Marca: {self.marca}'