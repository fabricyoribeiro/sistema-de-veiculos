from database.connect import ConnectDataBase
from modulos.abastecimento.abastecimento import Abastecimento

class AbastecimentoDao:
    _TABLE_NAME = 'ABASTECIMENTO'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(data_abastecimento, viagem_id, veiculo_id, posto_id, valor_gasto, km_atual)' \
                   ' values(%s, %s, %s, %s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_KM = 'SELECT * FROM {} WHERE KM_TOTAL={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, abastecimento):
        if abastecimento.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (abastecimento.data_abastecimento, abastecimento.viagem_id, abastecimento.veiculo_id, abastecimento.posto_id, abastecimento.valor_gasto, abastecimento.km_atual))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            abastecimento.id = id
            return abastecimento
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        abastecimentos = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_abastecimentos = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for abastecimento_query in all_abastecimentos:
            data = dict(zip(coluns_name, abastecimento_query))
            abastecimento = Abastecimento(**data)
            abastecimentos.append(abastecimento)
        cursor.close()
        return abastecimentos

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        abastecimento = cursor.fetchone()
        if not abastecimento:
            return None
        data = dict(zip(coluns_name, abastecimento))
        abastecimento = Abastecimento(**data)
        print(abastecimento)
        cursor.close()
        return abastecimento

    def update_abastecimento(self, abastecimentoNew, abastecimentoOld):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
            "data_abastecimento",  abastecimentoNew.data_abastecimento,
            "viagem_id", abastecimentoNew.viagem_id,
            "veiculo_id", abastecimentoNew.veiculo_id,
            "posto_id", abastecimentoNew.posto_id,
            "valor_gasto", abastecimentoNew.valor_gasto,
            "km_atual", abastecimentoNew.km_atual,
            abastecimentoOld.id
        ))
        self.database.commit()
        cursor.close()

    def delete_abastecimento(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()
    
    