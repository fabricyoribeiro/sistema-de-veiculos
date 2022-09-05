from database.connect import ConnectDataBase
from modulos.marca.marca import Marca


class MarcaDao:
    _TABLE_NAME = 'MARCA'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(marca, classificacao)' \
                   ' values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_MARCA = "SELECT * FROM {} WHERE MARCA='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}'  WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, marca):
        if marca.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (marca.marca, marca.classificacao))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            marca.id = id
            return marca
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        marcas = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_marcas = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for marca_query in all_marcas:
            data = dict(zip(coluns_name, marca_query))
            marca = Marca(**data)
            marcas.append(marca)
        cursor.close()
        return marcas

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        marca = cursor.fetchone()
        if not marca:
            return None
        data = dict(zip(coluns_name, marca))
        marca = Marca(**data)
        cursor.close()
        return marca

    def get_by_marca(self, marca):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_MARCA.format(self._TABLE_NAME, marca))
        coluns_name = [desc[0] for desc in cursor.description]
        marca = cursor.fetchone()
        if not marca:
            return None
        data = dict(zip(coluns_name, marca))
        marca = Marca(**data)
        cursor.close()
        return marca

    def update_marca(self, marcaNew, marcaOld):
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
            "marca",  marcaNew.marca,
            "classificacao", marcaNew.classificacao,
            marcaOld.id
        ))
        self.database.commit()
        cursor.close()

    def delete_marca(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()