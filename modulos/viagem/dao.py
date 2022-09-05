from database.connect import ConnectDataBase
from modulos.viagem.viagem import Viagem


class ViagemDao:
    _TABLE_NAME = 'VIAGEM'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(veiculo_id, motorista_id, destino)' \
                   ' values(%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, viagem):
        if viagem.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (viagem.veiculo_id, viagem.motorista_id, viagem.destino))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            viagem.id = id
            return viagem
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        viagens = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_viagens = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for viagem_query in all_viagens:
            data = dict(zip(coluns_name, viagem_query))
            viagem = Viagem(**data)
            viagens.append(viagem)
        cursor.close()
        return viagens

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        viagem = cursor.fetchone()
        if not viagem:
            return None
        data = dict(zip(coluns_name, viagem))
        viagem = Viagem(**data)
        cursor.close()
        return viagem

    def update_viagem(self, viagemNew, viagemOld):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
            "veiculo_id",  viagemNew.veiculo_id,
            "motorista_id", viagemNew.motorista_id,
            "destino", viagemNew.destino,
            viagemOld.id
        ))
        self.database.commit()
        cursor.close()

    def delete_viagem(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()