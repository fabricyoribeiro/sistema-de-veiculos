from modulos.modelo.dao import ModeloDao


class Veiculo:
  VALUES=['placa','modelo_id', 'km_total']
  def __init__(self, placa, modelo_id, km_total, id=None):
    self.id = id
    self.placa = placa
    self.modelo_id = modelo_id
    self.km_total = km_total
  
  def __str__(self):
    return f'Placa: {self.placa}, Modelo: {self.modelo}, km_total: {self.km_total}'
  
  def get_data_dict(self):
    dao_modelo = ModeloDao()
    modelo = dao_modelo.get_por_id(self.modelo_id)
    return {
      'id': self.id, 
      'placa': self.placa, 
      'modelo': modelo.get_data_dict(), 
      'km_total': self.km_total
      }