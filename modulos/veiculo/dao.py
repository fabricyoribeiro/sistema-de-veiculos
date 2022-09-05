from database.connect import ConnectDataBase
from modulos.veiculo.veiculo import Veiculo


class VeiculoDao:
    _TABLE_NAME = 'VEICULO'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(placa, modelo_id, km_total)' \
                   ' values(%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_PLACA = "SELECT * FROM {} WHERE PLACA='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, veiculo):
        if veiculo.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (veiculo.placa, veiculo.modelo_id, veiculo.km_total))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            veiculo.id = id
            return veiculo
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        veiculos = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_veiculos = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for veiculo_query in all_veiculos:
            data = dict(zip(coluns_name, veiculo_query))
            veiculo = Veiculo(**data)
            veiculos.append(veiculo)
        cursor.close()
        return veiculos

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        veiculo = cursor.fetchone()
        if not veiculo:
            return None
        data = dict(zip(coluns_name, veiculo))
        veiculo = Veiculo(**data)
        cursor.close()
        return veiculo

    def get_by_placa(self, placa):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_PLACA.format(self._TABLE_NAME, placa))
        coluns_name = [desc[0] for desc in cursor.description]
        veiculo = cursor.fetchone()
        if not veiculo:
            return None
        data = dict(zip(coluns_name, veiculo))
        veiculo = Veiculo(**data)
        cursor.close()
        return veiculo

    def update_veiculo(self, veiculoNew, veiculoOld):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
            "placa",  veiculoNew.placa,
            "modelo_id", veiculoNew.modelo_id,
            "km_total", veiculoNew.km_total,
            veiculoOld.id
        ))
        self.database.commit()
        cursor.close()

    def delete_veiculo(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()