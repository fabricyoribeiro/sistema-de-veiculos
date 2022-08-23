class Abastecimento:
  def __init__(self, viagem_id, veiculo_id, valor_gasto, km_atual, id=None):
    self.id = id
    self.viagem_id = viagem_id
    self.veiculo_id = veiculo_id
    self.valor_gasto = valor_gasto
    self.km_atual = km_atual
  
  def __str__(self):
    return f'Id: {self.id}, viagem_id: {self.viagem_id}, veiculo id: {self.veiculo_id}, valor gasto: {self.valor_gasto}, km atual: {self.km_atual}'