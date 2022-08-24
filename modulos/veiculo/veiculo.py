class Veiculo:
  def __init__(self, placa, modelo_id, km_total, id=None):
    self.id = id
    self.placa = placa
    self.modelo_id = modelo_id
    self.km_total = km_total
  
  def __str__(self):
    return f'Placa: {self.placa}, Modelo: {self.modelo}, km_total: {self.km_total}'