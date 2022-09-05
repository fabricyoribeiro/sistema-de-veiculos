from ntpath import join
from flask import Flask, make_response, jsonify, request, Blueprint


from modulos.veiculo.dao import VeiculoDao

from modulos.motorista.dao import MotoristaDao
from modulos.viagem.dao import ViagemDao
from modulos.viagem.viagem import Viagem



app_viagem = Blueprint('viagem_blueprint', __name__)
app_name = 'viagem'
dao_veiculo = VeiculoDao()
dao_motorista = MotoristaDao()
dao_viagem = ViagemDao()


@app_viagem.route(f'/{app_name}/', methods=['GET'])
def get_viagenss():
    viagens = dao_viagem.get_all()
    data = [viagem.get_data_dict() for viagem in viagens]
    return make_response(jsonify(data))


@app_viagem.route(f'/{app_name}/add/', methods=['POST'])
def add_viagem():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Viagem.VALUES:
        if key not in data.keys() or data[key] =='':
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})
    
    if data.get('veiculo_id') != None:
        for i in data['veiculo_id']:
            if i.isdigit()==False:
                erros.append({'field': 'veiculo_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    
    if data.get('motorista_id') != None:
        for i in data['motorista_id']:
            if i.isdigit()==False:
                erros.append({'field': 'motorista_id', 'mensage': 'Este campo só aceita números inteiros'})
                break

    if erros:
        return make_response({'errors': erros}, 400)
    print(data)
   
    veiculo = dao_veiculo.get_por_id(data.get('veiculo_id'))
        
    motorista = dao_motorista.get_por_id(data.get('motorista_id'))

    if not  veiculo:
        return make_response({'erro': "id do veiculo não existe."}, 400)

    if not  motorista:
        return make_response({'erro': "id do motorista não existe."}, 400)
    
    viagem = Viagem(**data)
    viagem = dao_viagem.salvar(viagem)
    return make_response({
        'id': viagem.id
    })

@app_viagem.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_viagem_by_id(id):
    viagem = dao_viagem.get_por_id(id)
    if not viagem:
        return 'O id informado não existe'
    data = viagem.get_data_dict()
    return make_response(jsonify(data))



@app_viagem.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_viagem(id):
    data = request.form.to_dict(flat=True)

    viagemOld = dao_viagem.get_por_id(id)

    veiculo = dao_veiculo.get_por_id(data.get('veiculo_id'))
    if not veiculo:
        return make_response({'erro': "id do veículo não existe."}, 400)

    motorista = dao_motorista.get_por_id(data.get('motorista_id'))
    if not motorista:
        return make_response({'erro': "id do motorista não existe."}, 400)

    if not viagemOld:
        return make_response('O id informado não existe ')
    
    viagemNew = Viagem(**data)
    dao_viagem.update_viagem(viagemNew, viagemOld)
    return make_response({
        'id': viagemOld.id
    })

@app_viagem.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_viagem(id):

    viagem = dao_viagem.get_por_id(id)

    if not viagem:
        return make_response('O id informado não existe ')
    dao_viagem.delete_viagem(id)
    return make_response({
        'Detetado com sucesso': True
    })