from flask import jsonify
from pymongo.errors import PyMongoError
from controllers.operations.db_operations import MenuOperations
from models.api_return import Api
from models.queries.queries_model import QueriesModel

class MenuViews:

    @staticmethod
    def get(id: int, name: str, estId: int):
        try:
            filters = {}
            if id:
                filters['_id'] = int(id)
            if name:
                filters['name'] = QueriesModel.searchByName(name)
            if estId:
                filters['establishmentsId'] = int(estId)
            return jsonify(Api.success(list(MenuOperations.get(filters)))), 200
        except PyMongoError as pyErr:
            return jsonify(Api.problem(pyErr)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500
    
    @staticmethod
    def post(document: dict):
        try:
            MenuOperations.post(document)
            return jsonify(Api.success()), 200
        except PyMongoError as pyErr:
            return jsonify(Api.problem(pyErr)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500

    @staticmethod
    def put(document: dict):
        try:
            if document['id'] is None:
                return jsonify(Api.problem('Campo obrigatório não foi informado')), 400
            else:
                fields = {}
                if document['name']:
                    fields['name'] = document['name']
                if document['establishmentsId']:
                    fields['establishmentsId'] = int(document['establishmentsId'])
                pr = MenuOperations.put({"_id": int(document['id'])}, fields)
                return jsonify(
                    Api.success() if pr.modified_count > 0 else Api.problem('Nenhum dado foi atualizado, verifique os filtros')
                ), 200 if pr.modified_count > 0 else 400
        except KeyError as err:
            return jsonify(Api.problem(f'Campo obrigatório não foi informado {err}')), 400
        except PyMongoError as pyErr:
            return jsonify(Api.problem(pyErr)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500

    @staticmethod
    def delete(filter):
        try:
            if filter['id'] is None:
                return jsonify(Api.problem('Campo obrigatório não foi informado')), 400
            else:
                pr = MenuOperations.delete({"_id": int(filter['id'])})
                return jsonify(
                    Api.success() if pr.deleted_count > 0 else Api.problem('Nenhum dado excluido, verifique os filtros')
                ), 200 if pr.deleted_count > 0 else 400
        except PyMongoError as pyErr:
            return jsonify(Api.problem(pyErr)), 500
        except KeyError as err:
            return jsonify(Api.problem(f'Campo obrigatório não informado {err}')), 400
        except Exception as err:
            return jsonify(Api.problem(f'Ocorreu um erro desconhecido {err}')), 500
            