from database.connect import ConnectDataBase
from modulos.modelo.modelo import Modelo


class ModeloDao:
    _TABLE_NAME = 'MODELO'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(descricao, marca_id)' \
                   ' values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_DESCRICAO = "SELECT * FROM {} WHERE DESCRICAO='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}'  WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, modelo):
        if modelo.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (modelo.descricao, modelo.marca_id))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            modelo.id = id
            return modelo
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        modelos = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_modelos = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for modelo_query in all_modelos:
            data = dict(zip(coluns_name, modelo_query))
            modelo = Modelo(**data)
            modelos.append(modelo)
        cursor.close()
        return modelos

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        modelo = cursor.fetchone()
        if not modelo:
            return None
        data = dict(zip(coluns_name, modelo))
        modelo = Modelo(**data)
        cursor.close()
        return modelo

    def get_by_descricao(self, modelo):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_DESCRICAO.format(self._TABLE_NAME, modelo))
        coluns_name = [desc[0] for desc in cursor.description]
        modelo = cursor.fetchone()
        if not modelo:
            return None
        data = dict(zip(coluns_name, modelo))
        modelo = Modelo(**data)
        cursor.close()
        return modelo

    def update_modelo(self, modeloNew, modeloOld):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
            "descricao",  modeloNew.descricao,
            "marca_id", modeloNew.marca_id,
            modeloOld.id
        ))
        self.database.commit()
        cursor.close()

    def delete_modelo(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()