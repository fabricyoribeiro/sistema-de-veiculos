import psycopg2
class ConnectDataBase:
    def __init__(self):
        self._connect = psycopg2.connect(
            host="localhost",
            database="controle_gastos_veiculos",
            user="postgres",
            password="18102002"
        )
    def get_instance(self):
        return self._connect
