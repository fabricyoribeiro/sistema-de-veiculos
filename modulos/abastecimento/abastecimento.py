from modulos.posto.dao import PostoDao
from modulos.veiculo.dao import VeiculoDao
from modulos.viagem.dao import ViagemDao

class Abastecimento:
  VALUES = ['data_abastecimento', 'viagem_id', 'veiculo_id', 'posto_id', 'valor_gasto', 'km_atual']
  def __init__(self,data_abastecimento, viagem_id, veiculo_id, posto_id, valor_gasto, km_atual, id=None):
    self.id = id
    self.data_abastecimento = data_abastecimento
    self.viagem_id = viagem_id
    self.veiculo_id = veiculo_id
    self.posto_id = posto_id
    self.valor_gasto = valor_gasto
    self.km_atual = km_atual
  
  def __str__(self):
    return f'Id: {self.id}, viagem_id: {self.viagem_id}, veiculo id: {self.veiculo_id}, valor gasto: {self.valor_gasto}, km atual: {self.km_atual}'
  
  def get_data_dict(self):
    dao_viagem =  ViagemDao()
    dao_veiculo = VeiculoDao()
    dao_posto = PostoDao()
    viagem = dao_viagem.get_por_id(self.viagem_id)
    veiculo = dao_veiculo.get_por_id(self.veiculo_id)
    posto = dao_posto.get_por_id(self.posto_id)

    return {
      'id': self.id,
      'data_abastecimento': self.data_abastecimento,
      'viagem': viagem.get_data_dict(), 
      'veiculo': veiculo.get_data_dict() , 
      'posto': posto.get_data_dict(),
      'valor_gasto': self.valor_gasto,
      'km_atual': self.km_atual
    }