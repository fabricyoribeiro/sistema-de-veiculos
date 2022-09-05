from ntpath import join
from flask import Flask, make_response, jsonify, request, Blueprint
from modulos.marca.marca import Marca

from modulos.veiculo.dao import VeiculoDao
from modulos.modelo.modelo import Modelo
from modulos.modelo.dao import ModeloDao
from modulos.veiculo.veiculo import Veiculo



app_veiculo = Blueprint('veiculo_blueprint', __name__)
app_name = 'veiculo'
dao_veiculo = VeiculoDao()
dao_modelo = ModeloDao()


@app_veiculo.route(f'/{app_name}/', methods=['GET'])
def get_veiculos():
    veiculos = dao_veiculo.get_all()
    data = [veiculo.get_data_dict() for veiculo in veiculos]
    return make_response(jsonify(data))


@app_veiculo.route(f'/{app_name}/add/', methods=['POST'])
def add_veiculo():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Veiculo.VALUES:
        if key not in data.keys() or data[key] =='':
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})

    if data.get('modelo_id') != None:
        for i in data['modelo_id']:
            if i.isdigit()==False:
                erros.append({'field': 'modelo_id', 'mensage': 'Este campo só aceita números inteiros'})
                break

    if data.get('km_total') != None:
        for i in data['km_total']:
            if i.isdigit() == False:
                if i not in '.':
                    erros.append({'field': 'km_total', 'mensage': 'Este campo só aceita números'})
                break

    if erros:
        return make_response({'errors': erros}, 400)
    print(data)
    
    modelo = dao_modelo.get_por_id(data.get('modelo_id'))

    if not  modelo:
        return make_response({'erro': "id do modelo não existe."}, 400)
    
    veiculo = dao_veiculo.get_by_placa(data.get('placa')) 
    if veiculo:
        return make_response('Placa já existe', 400)
    veiculo = Veiculo(**data)
    veiculo = dao_veiculo.salvar(veiculo)
    return make_response({
        'id': veiculo.id
    })

@app_veiculo.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_veiculo_by_id(id):
    veiculo = dao_veiculo.get_por_id(id)
    if not veiculo:
        return 'O id informado não existe'
    data = veiculo.get_data_dict()
    return make_response(jsonify(data))



@app_veiculo.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_veiculo(id):
    data = request.form.to_dict(flat=True)

    veiculoOld = dao_veiculo.get_por_id(id)

    modelo = dao_modelo.get_por_id(data.get('modelo_id'))
    if not modelo:
        return make_response({'erro': "id do modelo não existe."}, 400)

    if not veiculoOld:
        return make_response('O id informado não existe ')
    
    veiculoNew = Veiculo(**data)
    dao_veiculo.update_veiculo(veiculoNew, veiculoOld)
    return make_response({
        'id': veiculoOld.id
    })

@app_veiculo.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_veiculo(id):

    veiculo = dao_veiculo.get_por_id(id)

    if not veiculo:
        return make_response('O id informado não existe ')
    dao_veiculo.delete_veiculo(id)
    return make_response({
        'Detetado com sucesso': True
    })