from database.connect import ConnectDataBase
from modulos.motorista.dao import MotoristaDao

print(ConnectDataBase().get_instance())

dao_motorista = MotoristaDao()
motoristas = dao_motorista.get_all()
print(motoristas)