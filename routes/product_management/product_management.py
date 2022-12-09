import json
from flask import jsonify
from pymongo.errors import PyMongoError
from models.api_return import Api
from controllers.operations.db_operations import ImageOperations, SessionsOperations
from models.collections.collections_data import Collections
from models.queries.queries_model import QueriesModel
from pymongo.results import InsertOneResult


class ProductManagement:

    @staticmethod
    def get(request: dict):
        query: dict = {}
        id: int = request.get('id')
        cat: str = request.get('categoria')
        prep = request.get('preparacao')
        prod: str = request.get('produto')
        status = request.get('status')
        isActive = request.get('isActive')
        storeCode: str = request.get('storeCode')
        if id:
            query['_id'] = int(id)
        if cat:
            query['categoria'] = cat
        if prep:
            query['preparacao'] = json.loads(prep)
        if prod:
            query['produto'] = QueriesModel.searchByName(prod)
        if status:
            query['status'] = json.loads(status)
        if storeCode:
            query['storeCode'] = storeCode
        if isActive:
            query['isActive'] = json.loads(isActive)
        return jsonify(Api(
            True, 'Success', list(Collections.PRODUCTS.find(
                query
            ))
        ).getDataReturn()), 200

    @staticmethod
    def post(document: dict):
        try:
            print(document)
            if document and document.get('_id') and document.get('name') and document.get('storeCode'):
                SessionsOperations.post(
                    {"_id": int(document.get('_id')), "name": document.get('name'), "storeCode": document.get(
                        "storeCode"), "products": document.get('products'), "visible": document.get('visible')}
                )
                return jsonify(Api.success()), 200
            else:
                return jsonify(Api.problem(
                    message='Parametros necessários não foram enviados.'
                )), 405
        except PyMongoError as err:
            return jsonify(Api.problem(f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(f'{err}')), 500

    @staticmethod
    def put(document: dict):
        try:
            if document.get('id') is None and document.get('storeCode') is None:
                return jsonify(Api.problem('Campo obrigatório não foi informado.'))
            else:
                pr = SessionsOperations.put(
                    filters={"_id": int(document.get('_id'))}, document={"name": document.get("name"), "visible": document.get('visible')})
                return jsonify(
                    Api.success() if pr.modified_count > 0 else Api.problem(
                        'Nenhum dado foi atualizado, verifique os filtros')
                ), 200 if pr.modified_count > 0 else 400
        except KeyError as err:
            return jsonify(Api.problem(f'Campo obrigatório não foi informado {err}')), 400
        except PyMongoError as err:
            return jsonify(Api.problem(f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(f'{err}')), 500

    @staticmethod
    def delete(filter: dict):
        try:
            if filter.get('id') is None:
                return jsonify(Api.problem('Campo obrigatório não foi informado')), 400
            else:
                pr = SessionsOperations.delete({"_id": int(filter.get('id'))})
                return jsonify(
                    Api.success() if pr.deleted_count > 0 else Api.problem(
                        'Nenhum dado excluido, verifique os filtros')
                ), 200 if pr.deleted_count > 0 else 400
        except PyMongoError as pyErr:
            return jsonify(Api.problem(pyErr)), 500
        except KeyError as err:
            return jsonify(Api.problem(f'Campo obrigatório não informado {err}')), 400
        except Exception as err:
            return jsonify(Api.problem(f'Ocorreu um erro desconhecido {err}')), 500

    @staticmethod
    def patch(doc: dict):
        try:
            if doc.get('type') is None and doc.get('sessionId') is None and doc.get('productIds') is None:
                return jsonify(Api.problem('Campo obrigatório não foi informado')), 403
            if doc.get('type') == "input":
                q = SessionsOperations.patchIn(
                    doc.get('sessionId'), doc.get("productIds"))
                return jsonify(
                    Api.success() if q.modified_count > 0 else Api.problem(
                        "Nenhum dado atualizado, verifique os filtros")
                ), 200 if q.modified_count > 0 else 400
            elif doc.get('type') == 'remove':
                q = SessionsOperations.patchOut(
                    doc.get('sessionId'), doc.get("productIds"))
                return jsonify(
                    Api.success() if q.modified_count > 0 else Api.problem(
                        "Nenhum dado atualizado, verifique os filtros")
                ), 200 if q.modified_count > 0 else 400
            else:
                return jsonify(Api.problem('Parametro inválido')), 403
        except PyMongoError as pyErr:
            return jsonify(Api.problem(pyErr)), 500
        except KeyError as err:
            return jsonify(Api.problem(f'Campo obrigatório não informado {err}')), 403
        except Exception as err:
            return jsonify(Api.problem(f'Ocorreu um erro desconhecido {err}')), 500


class ManageProductImage:

    @staticmethod
    def delete(name: str):
        try:
            if name:
                ImageOperations.delete(name)
                return jsonify(Api.success())
            return jsonify(Api.problem()), 200
        except PyMongoError as err:
            return jsonify(Api.problem(f'Ocorreu um erro desconhecido {err}')), 500


class AddOnesView:

    @staticmethod
    def get(data: dict):
        try:
            storeCode: str = data.get('storeCode')
            if storeCode:
                d = list(Collections.ADDONES.find({
                    "storeCode": data.get("storeCode")
                }))
                return jsonify(Api.success(d)), 200
            return Api.noParams(), 403
        except PyMongoError as err:
            return Api.problem(message=f'Ocorreu um problema ao realizar o procedimento {err}'), 500
        except Exception as err:
            return Api.problem(message=f'Ocorreu um erro desconhecido {err}'), 500

    @staticmethod
    def post(data: dict):
        try:
            print(data)
            storeCode: str = data.get('storeCode')
            if storeCode:
                r = Collections.ADDONES.insert_one(data)
                isSucceful: bool = r.acknowledged
                return jsonify(Api(status=isSucceful, message='Success' if isSucceful else 'Nenhum dado inserido').getReturn()), 200 if isSucceful else 400
            return Api.noParams()
        except PyMongoError as err:
            return jsonify(Api.problem(f'Ocorreu um problema no procedimento {err}')), 500
        except Exception as err:
            return jsonify(Api.problem(f'Ocorreu um erro desconhecido {err}')), 500