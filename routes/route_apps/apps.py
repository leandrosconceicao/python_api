from flask import jsonify
from controllers.operations.db_operations import AppsOperations
from models.api_return import Api
from pymongo.errors import PyMongoError
from models.apps.apps import Apps

from models.queries.queries_model import QueriesModel

class AppsView:

    @staticmethod
    def get(id: int, appsName: str):
        try:
            filters = {}
            if id:
                filters['_id'] = int(id)
            if appsName:
                filters['appsName'] = QueriesModel.searchByName(appsName)
            return jsonify(Api.success(list(AppsOperations.get(filters)))), 200
        except PyMongoError as err:
            return jsonify(Api.problem(err)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500

    def post(document: dict):
        try:
            AppsOperations.post(document)
            return jsonify(Api.success()), 200
        except KeyError as err:
            return jsonify(Api.problem(f'Campo obrigatório não informado {err}')), 500
        except PyMongoError as err:
            return jsonify(Api.problem(err)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500

    def put(document: Apps):
        try:
            pr = AppsOperations.put({"_id": int(document.id)}, {'appsName': document.appsName, 'version': document.version, 'releaseDate': document.releaseDate})
            return jsonify(
                Api.success() if pr.modified_count > 0 else Api.problem('Nenhum dado foi atualizado, verifique os filtros')
            ), 200 if pr.modified_count > 0 else 400
        except PyMongoError as err:
            return jsonify(Api.problem(err)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500

    def delete(document: Apps):
        try:
            pr = AppsOperations.delete({'_id': int(document.id)})
            return jsonify(
                Api.success() if pr.deleted_count > 0
                else Api.problem('Nenhum dado excluido, verifique os filtros')
            ), 200 if pr.deleted_count > 0 else 400
        except PyMongoError as err:
            return jsonify(Api.problem(err)), 500
        except Exception as err:
            return jsonify(Api.problem(err)), 500