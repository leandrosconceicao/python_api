import json
import sys
sys.dont_write_bytecode = True
from flask_cors import CORS
from models.api_return import *
from flask_talisman import Talisman
from flask import Flask, jsonify, request
from models.apps.apps import Apps
from models.collections.collections_data import Collections
from models.api_return import *
from models.endpoints.endpoints_data import Endpoints
from models.menus.menus import MenuData
from models.methods import Methods
from models.queries.queries_model import QueriesModel
from models.users import Users
from routes.authorization.authorization_view import AuthorizationView
from routes.establishments.establishments_view import EstablishmentsView
from routes.menus.menu_view import MenuViews
from routes.orders.orders_view import OrdersView
from routes.product_management.product_management import AddOnesView, ManageProductImage, ProductManagement
from routes.route_apps.apps import AppsView

from routes.menus.menu_items import MenuItems

debug = True

METHODS = ['POST', 'GET', 'PUT', 'DELETE', 'PATCH']

app = Flask(__name__)
app.config
Talisman(app, content_security_policy=None)

CORS(app)
cors = CORS(app, resources={
    r"/": {
        "origins": "*"
    }
})


@app.route(Endpoints.ORDERS_PAYMENTS, methods=METHODS)
def orders_payments():
    if request.method == 'POST':
        return OrdersView.addPaymentToOrder(request.get_json())
    return Api.unauthorized()


@app.route(Endpoints.ORDERS, methods=METHODS)
def api_orders():
    if request.method == 'GET':
        return OrdersView.get(request.args)
    if request.method == 'POST':
        return OrdersView.postOrder(request.get_json())
    if request.method == 'DELETE':
        return OrdersView.delOrder(request.args)
    if request.method == 'PUT':
        return OrdersView.putOrder(request.get_json())
    else:
        return Api.unauthorized()


@app.route(Endpoints.ORDERS_ITEMS, methods=['DELETE', 'POST', 'PUT'])
def api_orders_items():
    if request.method == 'POST':
        return OrdersView.putOrderItem(request.get_json())
    if request.method == 'DELETE':
        return OrdersView.popOrderItem(request.get_json())
    if request.method == 'PUT':
        return OrdersView.transferItems(request.get_json())
    return Api.unauthorized()

@app.route(Endpoints.ORDERS_MONITOR, methods=[Methods.get])
def api_monitor():
    if request.method == Methods.get:
        storeCode : str = request.args.get('storeCode')
        if storeCode:
            return OrdersView.getPreparation(storeCode=storeCode)
        return jsonify(Api.problem(message='Parametro obrigatório não foi informado')), 405
    return Api.unauthorized()




@app.route(Endpoints.MENUITEMS, methods=["GET"])
def menu_items():
    return MenuItems.get(request.args.get('storeCode'))


@ app.route(Endpoints.PRODUCTS, methods=METHODS)
def api_products():
    if request.method == 'GET':
        return ProductManagement.get(request.args)
    if request.method == 'POST':
        try:
            d = request.get_json()
            if d:
                Collections.PRODUCTS.insert_one(d)
                return jsonify(Api(True, message="Success").getReturn()), 200
            return jsonify(Api(message='Dados invalidos').getReturn()), 400
        except PyMongoError as err:
            return jsonify(Api(message=err).getReturn()), 400
    if request.method == 'PUT':
        try:
            d = request.get_json()
            id = request.args.get('id')
            if d and id:
                Collections.PRODUCTS.update_one(
                    {'_id': int(id)}, {'$set': d}
                )
                return jsonify(Api(True, message="Success").getReturn()), 200
            return jsonify(Api(message='Dados invalidos').getReturn()), 400
        except PyMongoError as err:
            return jsonify(Api(message=err).getReturn()), 400
    if request.method == 'DELETE':
        id = request.args.get('id')
        if id:
            try:
                return jsonify(
                    Api(True, 'Success', Collections.PRODUCTS.find_one_and_delete(
                        {'_id': int(id)}
                    )).getDataReturn()
                )
            except PyMongoError as err:
                return jsonify(
                    Api(message=err).getReturn()
                )

@app.route(Endpoints.PRODUCTS_ADD_ONES, methods=METHODS)
def api_products_addOnes():
    if request.method == Methods.get:
        return AddOnesView.get(request.args)
    if request.method == Methods.post:
        return AddOnesView.post(request.get_json())
    return Api.unauthorized()

@app.route(Endpoints.MANAGE_PRODUCT_IMAGES, methods=METHODS)
def manage_product_image():
    if request.method == Methods.delete:
        return ManageProductImage.delete(request.args.get('name'))
    return Api.unauthorized()


@ app.route(Endpoints.USERS, methods=METHODS)
def api_users():
    if request.method == 'GET':
        query: dict = {}
        est = request.args.get('storeCode')
        active = request.args.get('ativo')
        id = request.args.get('id')
        email = request.args.get('email')
        group = request.args.get('group_user')
        name = request.args.get('nome')
        username = request.args.get('username')
        if est:
            query['establishments'] = int(est)
        if id:
            query['_id'] = id
        if email:
            query['email'] = email
        if active:
            query['ativo'] = json.loads(active)
        if group:
            query['group_user'] = group
        if name:
            query['nome'] = QueriesModel.searchByName(name)
        if username:
            query['username'] = QueriesModel.searchByName(username)
        try:
            return jsonify(Api(
                True, 'Success', list(Collections.USERS.find(
                    query
                ))
            ).getDataReturn()), 200
        except PyMongoError as err:
            return jsonify(Api(
                message=f'{err}'
            ).getReturn()), 500
    elif request.method == 'POST':
        try:
            d = request.get_json()
            if d:
                Collections.USERS.insert_one(
                    Users.format(d)
                )
                return jsonify(Api(True, message="Success", data=[]).getReturn()), 200
            return jsonify(Api(message='Dados invalidos').getReturn()), 400
        except DuplicateKeyError as err:
            return jsonify(Api(message='Usuário já cadastrado').getReturn()), 500
        except PyMongoError as err:
            return jsonify(Api(message=err).getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=err).getReturn()), 500
    elif request.method == 'PUT':
        if not request.args.get('option'):
            try:
                d = request.get_json()
                id = request.args.get('id')
                if d and id:
                    Collections.USERS.update_one(
                        {'_id': id}, {'$set': d}
                    )
                    return jsonify(Api(True, message="Success").getReturn()), 200
                return jsonify(Api(message='Dados invalidos').getReturn()), 400
            except PyMongoError as err:
                return jsonify(Api.problem(f'{err}')), 500
            except Exception as err:
                return jsonify(Api.problem(f'{err}')), 500
        else:
            if request.args.get('option') == 'insert':
                try:
                    args = QueriesModel.insertInto(request.args.get(
                        'id'), 'establishments', request.get_json())
                    pr = Collections.USERS.update_one(
                        args[0], args[1]
                    )
                    return jsonify(
                        Api.success() if pr.modified_count > 0 else Api.problem(
                            'Nenhum dado foi alterado, verifique os filtros')
                    ), 200 if pr.modified_count > 0 else 400
                except PyMongoError as err:
                    return jsonify(Api.problem(f'{err}')), 500
                except Exception as err:
                    return jsonify(Api.problem(f'{err}')), 500
            else:
                try:
                    args = QueriesModel.removeFrom(request.args.get(
                        'id'), 'establishments', request.get_json())
                    pr = Collections.USERS.update_one(
                        args[0], args[1]
                    )
                    return jsonify(
                        Api.success() if pr.modified_count > 0 else Api.problem(
                            'Nenhum dado foi alterado, verifique os filtros')
                    ), 200 if pr.modified_count > 0 else 400
                except PyMongoError as err:
                    return jsonify(Api.problem(f'{err}')), 500
                except Exception as err:
                    return jsonify(Api.problem(f'{err}')), 500
    elif request.method == 'DELETE':
        id = request.args.get('id')
        if id:
            try:
                return jsonify(
                    Api(True, 'Success', Collections.USERS.find_one_and_delete(
                        {'_id': id}
                    )).getDataReturn()
                ), 200
            except PyMongoError as err:
                return jsonify(
                    Api(message=err).getReturn()
                ), 500
        return jsonify(
            Api(False, 'Dados necessários não foram enviados', [])
        ), 405
    # u = request.args.get('user')
    # if Authentication.userPermited(u):

    # return jsonify(Api(message='Necessário passar todos os parametros').getReturn()), 405


@app.route(Endpoints.CATEGORIES, methods=METHODS)
def api_categories():
    if request.method == 'GET':
        try:
            q: dict = {}
            id = request.args.get('id')
            nome = request.args.get('nome')
            storeCode = request.args.get('storeCode')
            if id:
                q['_id'] = int(id)
            if nome:
                q['nome'] = nome
            if storeCode:
                q['storeCode'] = storeCode
            return jsonify(Api(
                True, 'Success', list(
                    Collections.CATEGORIES.find(q).sort('ordenacao', 1))
            ).getDataReturn()), 200
        except PyMongoError as err:
            return jsonify(Api(
                message=f'{err}'
            ).getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=f'{err}').getReturn()), 500
    if request.method == 'POST':
        try:
            body = request.get_json()
            if body:
                Collections.CATEGORIES.insert_one(body)
                return jsonify(Api(True, message="Success").getReturn()), 200
            return jsonify(Api(message='Dados invalidos').getReturn()), 405
        except PyMongoError as err:
            return jsonify(Api(message=err).getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=err).getReturn()), 500
    if request.method == 'PUT':
        try:
            body = request.get_json()
            id = request.args.get('id')
            if body and id:
                Collections.CATEGORIES.update_one(
                    {'_id': id}, {'$set': body}
                )
                return jsonify(Api(True, message="Success").getReturn()), 200
            return jsonify(Api(message='Dados invalidos').getReturn()), 405
        except PyMongoError as err:
            return jsonify(Api(message=err).getReturn()), 500
        except Exception as err:
            return jsonify(Api(message=err).getReturn()), 500
    if request.method == 'DELETE':
        id = request.args.get('id')
        if id:
            try:
                return jsonify(
                    Api(True, 'Success', Collections.CATEGORIES.find_one_and_delete(
                        {'_id': int(id)}
                    )).getDataReturn()
                ), 200
            except PyMongoError as err:
                return jsonify(
                    Api(message=err).getReturn()
                ), 500
            except Exception as err:
                return jsonify(Api(message=err).getReturn()), 500

@app.route(Endpoints.AUTHORIZATION, methods=['POST'])
def api_auth():
    if request.method == 'POST':
        bd: dict = request.get_json()
        if bd and 'email' in bd and 'password' in bd:
            return AuthorizationView.authenticate(bd)
        return jsonify(Api.problem(message='Parametros necessários não foram enviados'))
    return Api.unauthorized()


# @app.route(Endpoints.REPORTS_SALES, methods=['GET'])
# def api_reports_sales():
#     tp = request.args.get('type')
#     if tp == 'saller':
#         d = request.args.get('date')
#         if d:
#             r = SalesReports.getSalesBySaller(d)
#             return jsonify(
#                 Api(
#                     status=r.statusProcess,
#                     message='Success',
#                     data=r.data
#                 ).getDataReturn()
#             ), 200
#         else:
#             return jsonify(Api(message='Necessario passar todos os parametros').getReturn()), 400
#     elif (tp == 'detail'):
#         d = request.args.get('date')
#         if d:
#             r = SalesReports.detailSales(d)
#             return jsonify(
#                 Api(
#                     status=r.statusProcess,
#                     message='Success',
#                     data=r.data
#                 ).getDataReturn()
#             ), 200
#         return jsonify(Api(message='Necessario passar todos os parametros').getReturn()), 400
#     elif (tp == 'period'):
#         fromDate = request.args.get('fromDate')
#         toDate = request.args.get('toDate')
#         return jsonify(
#             Api.fromDB(SalesReports.getSalesByPeriod(fromDate, toDate))
#         )
#     elif (tp == 'byproduct'):
#         fromDate = request.args.get('fromDate')
#         toDate = request.args.get('toDate')
#         p = request.args.get('product')
#         return jsonify(
#             Api.fromDB(SalesReports.getSalesByPeriodAndProduct(
#                 fromDate, toDate, p))
#         )
#     else:
#         return jsonify(Api(message='Necessario passar todos os parametros').getReturn()), 400


@app.route(Endpoints.ESTABLISHMENTS, methods=METHODS)
def api_establishments():
    if request.method == 'GET':
        return EstablishmentsView.get(request.args)
    elif request.method == 'POST' and request.args.get('type') == 'search':
        return EstablishmentsView.get(request.get_json())
    elif request.method == 'POST' and request.args.get('type') == 'post':
        return EstablishmentsView.post(request.get_json())
    elif request.method == 'PUT':
        if request.args.get('option'):
            if request.args.get('option') == 'insert':
                return EstablishmentsView.insertStore(request.args.get('id'), request.get_json())
            elif request.args.get('option') == 'remove':
                return EstablishmentsView.removeStore(request.args.get('id'), request.get_json())
        # else:
        return EstablishmentsView.put(request.args.get('id'), request.get_json())
    elif request.method == 'DELETE':
        return EstablishmentsView.delete(request.args.get('id'))
    else:
        return jsonify(
            Api.problem(message='Requisição inválida')
        ), 405


@app.route(Endpoints.MENUS, methods=METHODS)
def api_menus():
    if request.method == 'GET':
        return MenuViews.get(request.args.get('id'), request.args.get('name'), request.args.get('establishmentsId'))
    if request.method == 'POST':
        return MenuViews.post(MenuData.format(request.get_json()))
    if request.method == 'PUT':
        return MenuViews.put(request.get_json())
    if request.method == 'DELETE':
        return MenuViews.delete(request.get_json())


@app.route(Endpoints.APPS, methods=METHODS)
def api_apps():
    if request.method == 'GET':
        return AppsView.get(request.args.get('id'), request.args.get('appsName'))
    if request.method == 'POST':
        return AppsView.post(Apps.format(request.get_json()))
    if request.method == 'PUT':
        return AppsView.put(Apps.fromJson(request.get_json()))
    if request.method == 'DELETE':
        return AppsView.delete(Apps.fromJson(request.get_json()))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=debug)
    # app.run('192.168.100.115')
