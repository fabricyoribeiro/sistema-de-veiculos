from ntpath import join
from flask import Flask, make_response, jsonify, request, Blueprint

from modulos.marca.dao import MarcaDao
from modulos.marca.marca import Marca



app_marca = Blueprint('marca_blueprint', __name__)
app_name = 'marca'
dao_marca = MarcaDao()


@app_marca.route(f'/{app_name}/', methods=['GET'])
def get_marcas():
    marcas = dao_marca.get_all()
    data = [marca.get_data_dict() for marca in marcas]
    return make_response(jsonify(data))


@app_marca.route(f'/{app_name}/add/', methods=['POST'])
def add_marca():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Marca.VALUES:
        if key not in data.keys():
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})
    if erros:
        return make_response({'errors': erros}, 400)
    
    print(data.get('marca'))
    marca = dao_marca.get_by_marca(data.get('marca')) 
    if marca:
        return make_response('Marca já existe', 400)
    marca = Marca(**data)
    marca = dao_marca.salvar(marca)
    return make_response({
        'id': marca.id
    })

@app_marca.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_marca_by_id(id):
    marca = dao_marca.get_por_id(id)
    if not marca:
        return 'O id informado não existe'
    data = marca.get_data_dict()
    return make_response(jsonify(data))



@app_marca.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_marca(id):
    data = request.form.to_dict(flat=True)

    marcaOld = dao_marca.get_por_id(id)

    if not marcaOld:
        return make_response('O id informado não existe ')
    
    marcaNew = Marca(**data)
    dao_marca.update_marca(marcaNew, marcaOld)
    return make_response({
        'id': marcaOld.id
    })

@app_marca.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_marca(id):

    marca = dao_marca.get_por_id(id)

    if not marca:
        return make_response('O id informado não existe ')
    dao_marca.delete_marca(id)
    return make_response({
        'Detetado com sucesso': True
    })