class Veiculo:
  def __init__(self, placa, marca, modelo, km_total, id=None):
    self.id = id
    self.placa = placa
    self.marca = marca
    self.modelo = modelo
    self.km_total = km_total
  
  def __str__(self):
    return f'Placa: {self.placa}, Marca: {self.marca}, Modelo: {self.modelo}, km_total: {self.km_total}'