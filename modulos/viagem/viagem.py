from modulos.motorista.dao import MotoristaDao
from modulos.veiculo.dao import VeiculoDao


class Viagem:
  VALUES=["veiculo_id", "motorista_id", "destino"]
  def __init__(self, veiculo_id, motorista_id, destino, id=None):
    self.id = id
    self.veiculo_id = veiculo_id
    self.motorista_id = motorista_id
    self.destino = destino
  
  def __str__(self) :
    return f'Veiculo id: {self.veiculo_id}, Motorista id: {self.motorista_id}, Destino: {self.destino}'
  
  def get_data_dict(self):
    dao_veiculo = VeiculoDao()
    dao_motorista = MotoristaDao()
    veiculo = dao_veiculo.get_por_id(self.veiculo_id)
    motorista = dao_motorista.get_por_id(self.motorista_id)
    return {
      'id': self.id,
      'veiculo': veiculo.get_data_dict(),
      'motorista': motorista.get_data_dict(),
      'destino': self.destino
    }