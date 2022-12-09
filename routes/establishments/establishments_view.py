from flask import jsonify
from controllers.establishments.establishments_api import EstablishmentsApi
from models.api_return import Api
from pymongo.errors import PyMongoError

from models.collections.collections_data import Collections


class EstablishmentsView:

    @staticmethod
    def get(args):
        try:
            filters = {}
            if args.get('id'):
                filters['_id'] = int(args.get('id'))
            if args.get('cgc'):
                filters['ownerId'] = args.get('cgc')
            print(filters)
            data = Collections.ESTABLISHMENTS.find(filters)
            return jsonify(
                Api.success(dados=list(data)) if data is not None else Api.problem(
                    message='Nenhum dado')
            ), 200 if data is not None else 400
        except PyMongoError as err:
            return jsonify(Api.problem(f'{err}'))
        except Exception as err:
            return jsonify(Api.problem(f'{err}'))

    @staticmethod
    def post(request):
        req = EstablishmentsApi.post(request)
        return jsonify(
            Api.success() if req.statusProcess else Api.problem(
                message=req.message)
        ), 200 if req.statusProcess else 400

    @staticmethod
    def put(id, request):
        req = EstablishmentsApi.put(int(id), request)
        return jsonify(
            Api.success() if req.statusProcess else Api.problem(message=req.message)
        ), 200 if req.statusProcess else 400

    @staticmethod
    def insertStore(id: dict, data):
        try:
            if id and data:
                dt = EstablishmentsApi.insertStore(
                    int(id), data
                )
                return jsonify(
                    Api.success() if dt.modified_count > 0 else Api.problem(message='Nenhum dado modificado, verifique os filtros e tente novamente.')
                ), 200 if dt.modified_count > 0 else 400
            return jsonify(Api.problem(message='Campos obrigatórios não foram informados')), 400
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(message=f'{err}')), 500

    @staticmethod
    def removeStore(id: dict, data):
        try:
            if id and data:
                dt = EstablishmentsApi.removeStore(
                    int(id), data
                )
                return jsonify(
                    Api.success() if dt.modified_count > 0 else Api.problem(
                        message='Nenhum dado modificado, verifique os filtros e tente novamente.')
                    ), 200 if dt.modified_count > 0 else 400
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(message=f'{err}')), 500


    @staticmethod
    def delete(id):
        req = EstablishmentsApi.delete(int(id))
        return jsonify(
            Api.success() if req.statusProcess else Api.problem(message=req.message)
        ), 200 if req.statusProcess else 400