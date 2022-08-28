from database.connect import ConnectDataBase
from modulos.motorista.motorista import Motorista


class MotoristaDao:
    _TABLE_NAME = 'MOTORISTA'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(nome, cpf, salario)' \
                   ' values(%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _SELECT_BY_CPF = "SELECT * FROM {} WHERE CPF='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def salvar(self, motorista):
        if motorista.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (motorista.nome, motorista.cpf, motorista.salario))
            id = cursor.fetchone()[0]
            self.database.commit()
            cursor.close()
            motorista.id = id
            return motorista
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        motoristas = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_motoristas = cursor.fetchall()
        coluns_name = [desc[0] for desc in cursor.description]
        for motorista_query in all_motoristas:
            data = dict(zip(coluns_name, motorista_query))
            motorista = Motorista(**data)
            motoristas.append(motorista)
        cursor.close()
        return motoristas

    def get_por_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        motorista = cursor.fetchone()
        if not motorista:
            return None
        data = dict(zip(coluns_name, motorista))
        motorista = Motorista(**data)
        cursor.close()
        return motorista

    def get_by_cpf(self, cpf):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_CPF.format(self._TABLE_NAME, cpf))
        coluns_name = [desc[0] for desc in cursor.description]
        motorista = cursor.fetchone()
        if not motorista:
            return None
        data = dict(zip(coluns_name, motorista))
        motorista = Motorista(**data)
        cursor.close()
        return motorista

    def update_motorista(self, motoristaNew, motoristaOld):
        #posto = self.get_posto_by_id(id)
        cursor = self.database.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
            "nome",  motoristaNew.nome, 
            "cpf", motoristaNew.cpf, 
            "salario", motoristaNew.salario, 
            motoristaOld.id
        ))
        self.database.commit()
        cursor.close()

    def delete_motorista(self, id):
        #posto = self.get_posto_by_id(id)
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()
