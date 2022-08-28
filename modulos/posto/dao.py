from database.connect import ConnectDataBase
from modulos.posto.posto import Posto


class PostoDao:
    _TABLE_NAME = 'POSTO'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, cidade, cnpj)' \
                   ' values(%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_CNPJ = "SELECT * FROM {} WHERE CNPJ='{}'"
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"
    _DELETE = 'DELETE FROM {} WHERE ID={}'

    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, posto):
        if posto.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (posto.nome, posto.cidade, posto.cnpj))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            posto.id = id
            return posto
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        postos = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_postos = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for posto_query in all_postos:
            data = dict(zip(coluns_name, posto_query))
            posto = Posto(**data)
            postos.append(posto)
        cursor.close()
        return postos

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        posto = cursor.fetchone()
        if not posto:
            return None
        data = dict(zip(coluns_name, posto))
        posto = Posto(**data)
        cursor.close()
        return posto
    
    def get_by_cnpj(self, cnpj):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CNPJ.format(self._TABLE_NAME, cnpj))
        coluns_name = [desc[0] for desc in cursor.description]
        posto = cursor.fetchone()
        if not posto:
            return None
        data = dict(zip(coluns_name, posto))
        posto = Posto(**data)
        cursor.close()
        return posto

    def update_posto(self, postoNew, postoOld):
            #posto = self.get_posto_by_id(id)
            cursor = self.database.cursor()
            cursor.execute(self._UPDATE.format(self._TABLE_NAME,
             "nome",  postoNew.nome, 
             "cidade", postoNew.cidade, 
             "cnpj", postoNew.cnpj, 
             postoOld.id
            ))
            self.database.commit()
            cursor.close()

    def delete_posto(self, id):
            #posto = self.get_posto_by_id(id)
            cursor = self.database.cursor()
            cursor.execute(self._DELETE.format(self._TABLE_NAME, id
            ))
            self.database.commit()
            cursor.close()

        
    
    #TODO: atualizar posto