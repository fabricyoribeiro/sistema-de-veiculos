from flask import  make_response, jsonify, request, Blueprint

from modulos.posto.posto import Posto
from modulos.posto.dao import PostoDao

app_posto = Blueprint('posto_blueprint', __name__)
app_name = 'posto'
dao_posto = PostoDao()


@app_posto.route(f'/{app_name}/', methods=['GET'])
def get_postos():
    postos = dao_posto.get_all()
    data = [posto.get_data_dict() for posto in postos]
    return make_response(jsonify(data))

@app_posto.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_posto_by_id(id):
    posto = dao_posto.get_por_id(id)
    data = posto.get_data_dict()
    return make_response(jsonify(data))


@app_posto.route(f'/{app_name}/add/', methods=['POST'])
def add_posto():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Posto.VALUES:
        if key not in data.keys():
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})
    if erros:
        return make_response({'errors': erros}, 400)

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

@app_posto.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_posto(id):
    data = request.form.to_dict(flat=True)

    postoOld = dao_posto.get_por_id(id)

    if not postoOld:
        return make_response('O id informado não existe ')
    
    postoNew = Posto(**data)
    dao_posto.update_posto(postoNew, postoOld)
    return make_response({
        'id': postoOld.id
    })

@app_posto.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_posto(id):

    posto = dao_posto.get_por_id(id)

    if not posto:
        return make_response('O id informado não existe ')
    dao_posto.delete_posto(id)
    return make_response({
        'Detetado com sucesso': True
    })   