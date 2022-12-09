import json
from pydoc import isdata
from re import search
from this import d
from webbrowser import get
from controllers.orders.orders_controller import OrderController
from pymongo.errors import PyMongoError
from models.api_return import Api
from flask import jsonify

from models.collections.collections_data import Collections


class OrdersView:

    @staticmethod
    def get(req: dict):
        bd: dict = {}
        id = req.get('id')
        idTable = req.get('idTable')
        status = req.get('status')
        excludeStatus = req.get('excludeStatus')
        accountStatus = req.get('accountStatus')
        saller = req.get('saller')
        storeCode = req.get('storeCode')
        printed = req.get('printed')
        operationDay = req.get('operationDay')
        isTableOrders = req.get('isTableOrders')
        if id:
            bd['_id'] = int(id)
        if isTableOrders:
            if json.loads(isTableOrders):
                bd['idMesa'] = {'$ne': ""}
        if idTable:
            bd['idMesa'] = idTable
        if excludeStatus:
            if json.loads(excludeStatus) and status:
                bd['accountStatus'] = {'$nin': [status, 'Fechada']}
        if accountStatus:
            bd['accountStatus'] = accountStatus
        if saller:
            bd['operador'] = saller
        if storeCode:
            bd['storeCode'] = storeCode
        if printed:
            bd['printed'] = json.loads(printed)
        if operationDay:
            bd['diaOperacao'] = operationDay
        try:
            print(bd)
            d = list(Collections.ORDERS.find(bd).sort('data', 1))
            searchHasData: bool = len(d) > 0
            return jsonify(Api(searchHasData, 'Success' if searchHasData else 'Busca não retornou dados', d).getDataReturn()), 200 if searchHasData else 406
        except PyMongoError as err:
            return jsonify(Api(False, f'Ocorreu um problema {err}').getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=f'Ocorreu um problema {err}').getReturn()), 500

    @staticmethod
    def postOrder(request: dict):
        try:
            if request.get('_id') and request.get("pedidos") and request.get("storeCode"):
                Collections.ORDERS.insert_one(request)
                return jsonify(Api(True, 'Success').getReturn()), 200
            else:
                return jsonify(Api.problem(message=f"Parametros necessários não foram enviados"))
        except KeyError as err:
            return jsonify(Api.problem(message=f"Parametros necessários não foram enviados {err}"))
        except PyMongoError as err:
            return jsonify(Api(message=f'{err}').getReturn()), 500

    @staticmethod
    def delOrder(request: dict):
        id = request.get('id')
        if (id):
            try:
                o = Collections.ORDERS.find_one_and_delete(
                    {'_id': int(id)})
                return jsonify(
                    Api(True if o is not None else False,
                        'Success' if o is not None else 'Valor não encontrado', o).getReturn()), 200
            except PyMongoError as err:
                return jsonify(Api(False, f'Ocorreu um erro {err}').getReturn()), 400
        return jsonify(Api.problem(message='Parametros inválidos não foram enviados ("ID")'))

    @staticmethod
    def putOrder(request: dict):
        try:
            if request and request.get('id'):
                p = OrderController.updateOrder(request)
                isDataModified: bool = p.modified_count > 0
                return jsonify(Api(isDataModified, 'Success' if isDataModified else 'Nenhum dado atualizado, verifique os filtros.').getReturn()), 200 if isDataModified else 400
            else:
                return jsonify(Api.problem(message='Parametro necessário não foi informado'))
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(f'Ocorreu um erro desconhecido {err}')), 500

    @staticmethod
    def putOrderItem(request: dict):
        try:
            id: str = request.get("id")
            data: list = request.get("orders")
            if id and (data and len(data) > 0):
                o : dict = Collections.ORDERS.find_one({"_id": id})
                if o.get('accountStatus') == 'Aguardando pagamento':
                    return jsonify(Api.problem(message='Mesa aguardando pagamento, não é possível adicionar pedido')), 403
                else:
                    p = OrderController.pushItems(id, data)
                    return jsonify(Api(True if p.modified_count > 0 else False, 'Success' if p.modified_count > 0 else 'Nenhum dado atualizado, verifique os filtros').getReturn()), 200 if p.modified_count > 0 else 400
            return jsonify(Api.problem(message='Parametros necessários não foram enviados, verifique')), 405
        except PyMongoError as err:
            return jsonify(Api(message=f'{err}').getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=f'{err}').getReturn()), 500

    def popOrderItem(request: dict):
        try:
            id: str = request.get('id')
            data: list = request.get("orders")
            if id and (data and len(data) > 0):
                p = OrderController.popItems(id, data)
                return jsonify(Api(True if p.modified_count > 0 else False, 'Success' if p.modified_count > 0 else 'Nenhum dado atualizado, verifique os filtros').getReturn()), 200 if p.modified_count > 0 else 400
            return jsonify(Api.problem(message='Parametros necessários não foram enviados, verifique')), 405
        except PyMongoError as err:
            return jsonify(Api(message=f'{err}').getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=f'{err}').getReturn()), 500

    @staticmethod
    def addPaymentToOrder(request: dict):
        try:
            if request.get('id') and request.get('data'):
                r = OrderController.addPayment(request)
                return jsonify(
                    Api(status=True if r.modified_count > 0 else False,
                        message='Success' if r.modified_count > 0 else 'Nenhum dado atualizado, verifique os filtros').getReturn()
                ), 200
            return jsonify(
                Api.problem()
            ), 400
        except KeyError as err:
            return jsonify(Api.problem(message=f'Parametro obrigatório não foi informado {err}'))
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(message=f"Ocorreu um erro desconhecido: {err}")), 503

    @staticmethod
    def transferItems(request: dict):
        try:
            to: str = request.get('to')
            frm: str = request.get('from')
            items: list = request.get('items')
            if to and frm and (items is not None and len(items) > 0):
                Collections.ORDERS.update_one(
                    {"idMesa": frm},
                    {'$push': {"pedidos": {"$each": items}}}
                )
                Collections.ORDERS.update_one(
                    {"idMesa": to},
                    {'$pull': {"pedidos": {"$each": items}}}
                )
                return jsonify(Api.success()), 200
            else:
                return jsonify(Api.problem(message='Parametros necessários não foram enviados')), 400
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'Ocorreu um problema ao salvar os dados {err}')), 500
        except Exception as err:
            return jsonify(Api.problem(message=f'Ocorreu um erro desconhecido {err}')), 503

    @staticmethod
    def getPreparation(storeCode: str):
        try:
            if storeCode:
                d = OrderController.getPreparationOrders(storeCode=storeCode)
                hasData: bool = len(d) > 0
                return jsonify(Api(hasData, 'Success' if hasData else 'Nenhum dado encontrado', data=d if hasData else []).getDataReturn()), 200 if hasData else 400
            return jsonify(Api.problem(message='Parametro obrigatório não foi informado')), 400
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'Ocorreu um problema ao salvar os dados {err}')), 500
        except Exception as err:
            return jsonify(Api.problem(message=f'Ocorreu um erro desconhecido {err}')), 503
