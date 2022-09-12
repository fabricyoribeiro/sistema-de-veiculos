from datetime import datetime
from ntpath import join
from flask import Flask, make_response, jsonify, request, Blueprint
from modulos.abastecimento.abastecimento import Abastecimento
from modulos.abastecimento.dao import AbastecimentoDao
from modulos.posto.dao import PostoDao


from modulos.veiculo.dao import VeiculoDao

from modulos.motorista.dao import MotoristaDao
from modulos.viagem.dao import ViagemDao
from modulos.viagem.viagem import Viagem



app_abastecimento = Blueprint('abastecimento_blueprint', __name__)
app_name = 'abastecimento'
dao_veiculo = VeiculoDao()
dao_motorista = MotoristaDao()
dao_viagem = ViagemDao()
dao_posto = PostoDao()
dao_abastecimento = AbastecimentoDao()


@app_abastecimento.route(f'/{app_name}/', methods=['GET'])
def get_abastecimentos():
    abastecimentos = dao_abastecimento.get_all()
    data = [abastecimento.get_data_dict() for abastecimento in abastecimentos]
    return make_response(jsonify(data))


@app_abastecimento.route(f'/{app_name}/add/', methods=['POST'])
def add_abastecimento():
    data = request.form.to_dict(flat=True)
    print(data.get('data_abastecimento'))


    # return data
    erros = []
    for key in Abastecimento.VALUES:
        if key not in data.keys() or data[key] =='':
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})

    if data.get('data_abastecimento') != None:
        if len(data.get('data_abastecimento')) != 10:
          erros.append({'field': 'data_abastecimento', 'mensage': "Este campo só aceita 10 caracteres"})
        for i in data['data_abastecimento']:
            if i.isdigit() == False:
                if i not in '-':
                    erros.append({'field': 'data_abastecimento', 'mensage': 'Este campo só aceita números'})
                    break
    
    if data.get('viagem_id') != None:
        for i in data['viagem_id']:
            if i.isdigit()==False:
                erros.append({'field': 'viagem_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    if data.get('veiculo_id') != None:
        for i in data['veiculo_id']:
            if i.isdigit()==False:
                erros.append({'field': 'veiculo_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    
    if data.get('posto_id') != None:
        for i in data['posto_id']:
            if i.isdigit()==False:
                erros.append({'field': 'posto_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    
    if data.get('valor_gasto') != None:
        for i in data['valor_gasto']:
            if i.isdigit() == False:
                if i not in '.':
                    erros.append({'field': 'valor_gasto', 'mensage': 'Este campo só aceita números'})
                    break
    if data.get('km_atual') != None:
        for i in data['km_atual']:
            if i.isdigit() == False:
                if i not in '.':
                    erros.append({'field': 'km_atual', 'mensage': 'Este campo só aceita números'})
                    break

    if erros:
        return make_response({'errors': erros}, 400)
   
    veiculo = dao_veiculo.get_por_id(data.get('veiculo_id'))
    
    viagem = dao_viagem.get_por_id(data.get('viagem_id'))

    posto = dao_posto.get_por_id(data.get('posto_id'))

    if not  veiculo:
        return make_response({'erro': "id do veiculo não existe."}, 400)

    if not  viagem:
        return make_response({'erro': "id da viagem não existe."}, 400)

    if not  posto:
        return make_response({'erro': "id de posto não existe."}, 400)

    data_abastecimento = data.get('data_abastecimento')
    data_abastecimento = datetime.strptime(data_abastecimento,"%Y-%m-%d").date()

    data['data_abastecimento'] = data_abastecimento


    abastecimento = Abastecimento(**data)
    abastecimento = dao_abastecimento.salvar(abastecimento)
    return make_response({
        'id': abastecimento.id
    })

@app_abastecimento.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_abastecimento_by_id(id):
    abastecimento = dao_abastecimento.get_por_id(id)
    if not abastecimento:
        return 'O id informado não existe'
    data = abastecimento.get_data_dict()
    return make_response(jsonify(data))


@app_abastecimento.route(f'/{app_name}/atualizar/<int:id>/', methods=['PUT'])
def update_abastecimento(id):
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Abastecimento.VALUES:
        if key not in data.keys() or data[key] =='':
            erros.append({'field': key, 'mensage': "Este campo é obrigátorio."})

    if data.get('data_abastecimento') != None:
        if len(data.get('data_abastecimento')) != 10:
          erros.append({'field': 'data_abastecimento', 'mensage': "Este campo só aceita 10 caracteres"})
        for i in data['data_abastecimento']:
            if i.isdigit() == False:
                if i not in '-':
                    erros.append({'field': 'data_abastecimento', 'mensage': 'Este campo só aceita números'})
                    break
    
    if data.get('viagem_id') != None:
        for i in data['viagem_id']:
            if i.isdigit()==False:
                erros.append({'field': 'viagem_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    if data.get('veiculo_id') != None:
        for i in data['veiculo_id']:
            if i.isdigit()==False:
                erros.append({'field': 'veiculo_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    
    if data.get('posto_id') != None:
        for i in data['posto_id']:
            if i.isdigit()==False:
                erros.append({'field': 'posto_id', 'mensage': 'Este campo só aceita números inteiros'})
                break
    if data.get('valor_gasto') != None:
        for i in data['km_atual']:
            if i.isdigit() == False:
                if i not in '.':
                    erros.append({'field': 'valor_gasto', 'mensage': 'Este campo só aceita números'})
                    break
    
    if data.get('km_atual') != None:
        for i in data['km_atual']:
            if i.isdigit() == False:
                if i not in '.':
                    erros.append({'field': 'km_atual', 'mensage': 'Este campo só aceita números'})
                    break

    if erros:
        return make_response({'errors': erros}, 400)

    abastecimentoOld = dao_abastecimento.get_por_id(id)
    if not abastecimentoOld:
        return make_response({'erro': 'O id informado não existe.'})

    veiculo = dao_veiculo.get_por_id(data.get('veiculo_id'))
    
    viagem = dao_viagem.get_por_id(data.get('viagem_id'))

    posto = dao_posto.get_por_id(data.get('posto_id'))

    if not  veiculo:
        return make_response({'erro': "id do veiculo não existe."}, 400)

    if not  viagem:
        return make_response({'erro': "id da viagem não existe."}, 400)

    if not  posto:
        return make_response({'erro': "id de posto não existe."}, 400)
    
    data_abastecimento = data.get('data_abastecimento')
    data_abastecimento = datetime.strptime(data_abastecimento,"%Y-%m-%d").date()

    data['data_abastecimento'] = data_abastecimento
    
    abastecimentoNew = Abastecimento(**data)
    dao_abastecimento.update_abastecimento(abastecimentoNew, abastecimentoOld)
    return make_response({
        'id': abastecimentoOld.id
    })

@app_abastecimento.route(f'/{app_name}/deletar/<int:id>/', methods=['DELETE'])
def delete_abastecimento(id):

    abastecimento = dao_abastecimento.get_por_id(id)

    if not abastecimento:
        return make_response({'erro': 'O id informado não existe'})
    dao_abastecimento.delete_abastecimento(id)
    return make_response({
        'Detetado com sucesso': True
    })