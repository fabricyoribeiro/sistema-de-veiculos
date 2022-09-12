from modulos.motorista.controller import app_motorista
from flask import Flask
from modulos.posto.controller import app_posto
from modulos.marca.controller import app_marca
from modulos.modelo.controller import app_modelo
from modulos.veiculo.controller import app_veiculo
from modulos.viagem.controller import app_viagem
from modulos.abastecimento.controller import app_abastecimento

app = Flask(__name__)
app.register_blueprint(app_posto)
app.register_blueprint(app_motorista)
app.register_blueprint(app_marca)
app.register_blueprint(app_modelo)
app.register_blueprint(app_veiculo)
app.register_blueprint(app_viagem)
app.register_blueprint(app_abastecimento)

app.run()