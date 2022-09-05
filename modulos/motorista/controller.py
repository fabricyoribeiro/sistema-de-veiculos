from flask import Flask, make_response, jsonify, request, Blueprint

from modulos.motorista.dao import MotoristaDao
from modulos.motorista.motorista import Motorista



app_motorista = Blueprint('motorista_blueprint', __name__)
app_name = 'motorista'
dao_motorista = MotoristaDao()


@app_motorista.route(f'/{app_name}/', methods=['GET'])
def get_motoristas():
    motoristas = dao_motorista.get_all()
    data = [motorista.get_data_dict() for motorista in motoristas]
    return make_response(jsonify(data))


@app_motorista.route(f'/{app_name}/add/', methods=['POST'])
def add_motorista():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Motorista.VALUES:
        if key not in data.keys():
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})

    for i in data['salario']:
        if i.isdigit() == False:
            if i not in '.':
                erros.append({'field': 'salario', 'mensage': 'Este campo só aceita números'})
                break

    if erros:
        return make_response({'errors': erros}, 400)

    print(data)
    print(data.get('nome'))
    motorista = dao_motorista.get_by_cpf(data.get('cpf')) 
    if motorista:
        return make_response('Cpf do motorista já existe', 400)
    motorista = Motorista(**data)
    motorista = dao_motorista.salvar(motorista)
    return make_response({
        'id': motorista.id
    })

@app_motorista.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_motorista_by_id(id):
    motorista = dao_motorista.get_por_id(id)
    data = motorista.get_data_dict()
    return make_response(jsonify(data))



@app_motorista.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_motorista(id):
    data = request.form.to_dict(flat=True)

    motoristaOld = dao_motorista.get_por_id(id)

    if not motoristaOld:
        return make_response('O id informado não existe ')
    
    motoristaNew = Motorista(**data)
    dao_motorista.update_motorista(motoristaNew, motoristaOld)
    return make_response({
        'id': motoristaOld.id
    })

@app_motorista.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_motorista(id):

    motorista = dao_motorista.get_por_id(id)

    if not motorista:
        return make_response('O id informado não existe ')
    dao_motorista.delete_motorista(id)
    return make_response({
        'Detetado com sucesso': True
    })