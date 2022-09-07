from ntpath import join
from flask import Flask, make_response, jsonify, request, Blueprint
from modulos.marca.marca import Marca

from modulos.modelo.dao import ModeloDao
from modulos.modelo.modelo import Modelo
from modulos.marca.dao import MarcaDao



app_modelo = Blueprint('modelo_blueprint', __name__)
app_name = 'modelo'
dao_modelo = ModeloDao()
dao_marca = MarcaDao()


@app_modelo.route(f'/{app_name}/', methods=['GET'])
def get_modelos():
    modelos = dao_modelo.get_all()
    data = [modelo.get_data_dict() for modelo in modelos]
    return make_response(jsonify(data))


@app_modelo.route(f'/{app_name}/add/', methods=['POST'])
def add_modelo():
    data = request.form.to_dict(flat=True)

    erros = []

    print(data.keys())
    print(Modelo.VALUES)
    for key in Modelo.VALUES:
        if key not in data.keys()  or data[key] =='':
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})
    
    if data.get('marca_id') != None:
        for i in data['marca_id']:
            if i.isdigit()==False:
                erros.append({'field': 'marca_id', 'mensage': 'Este campo só aceita números inteiros'})
                break

    if erros:
        return make_response({'errors': erros}, 400)
    
    marca = dao_marca.get_por_id(data.get('marca_id'))

    if not  marca:
        return make_response({'erro': "id da marca não existe."}, 400)
    

    print(data.get('descricao'))
    modelo = dao_modelo.get_by_descricao(data.get('descricao')) 
    if modelo:
        return make_response('Descricao já existe', 400)
    modelo = Modelo(**data)
    modelo = dao_modelo.salvar(modelo)
    return make_response({
        'id': modelo.id
    })

@app_modelo.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_modelo_by_id(id):
    modelo = dao_modelo.get_por_id(id)
    if not modelo:
        return 'O id informado não existe'
    data = modelo.get_data_dict()
    return make_response(jsonify(data))



@app_modelo.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_modelo(id):
    data = request.form.to_dict(flat=True)

    erros = []

    print(data.keys())
    print(Modelo.VALUES)
    for key in Modelo.VALUES:
        if key not in data.keys()  or data[key] =='':
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})
    
    if data.get('marca_id') != None:
        for i in data['marca_id']:
            if i.isdigit()==False:
                erros.append({'field': 'marca_id', 'mensage': 'Este campo só aceita números inteiros'})
                break

    if erros:
        return make_response({'errors': erros}, 400)
    print(data)
   

    modeloOld = dao_modelo.get_por_id(id)

    marca = dao_marca.get_por_id(data.get('marca_id'))
    if not marca:
        return make_response({'erro': "id da marca não existe."}, 400)

    if not modeloOld:
        return make_response('O id informado não existe ')
    
    modeloNew = Modelo(**data)
    dao_modelo.update_modelo(modeloNew, modeloOld)
    return make_response({
        'id': modeloOld.id
    })

@app_modelo.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_modelo(id):

    modelo = dao_modelo.get_por_id(id)

    if not modelo:
        return make_response('O id informado não existe ')
    dao_modelo.delete_modelo(id)
    return make_response({
        'Detetado com sucesso': True
    })