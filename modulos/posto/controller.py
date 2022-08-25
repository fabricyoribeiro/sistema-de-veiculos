from flask import  make_response, jsonify, request, Blueprint

from modulos.posto.posto import Posto
from modulos.posto.dao import PostoDao

app_empresa = Blueprint('example_blueprint', __name__)
app_name = 'posto'
dao_posto = PostoDao()


@app_empresa.route(f'/{app_name}/', methods=['GET'])
def get_postos():
    postos = dao_posto.get_all()
    data = [posto.get_data_dict() for posto in postos]
    return make_response(jsonify(data))

@app_empresa.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_posto_by_id(id):
    posto = dao_posto.get_por_id(id)
    data = posto.get_data_dict()
    return make_response(jsonify(data))


@app_empresa.route(f'/{app_name}/add/', methods=['POST'])
def add_posto():
    data = request.form.to_dict(flat=True)
    print(data)
    print(data.get('nome'))
    posto = dao_posto.get_by_cnpj(data.get('cnpj')) 
    if posto:
        return make_response('Cnpj do posto já existe', 400)
    posto = Posto(**data)
    posto = dao_posto.salvar(posto)
    return make_response({
        'id': posto.id
    })

@app_empresa.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_posto():
    pass