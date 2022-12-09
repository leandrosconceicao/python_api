from controllers.menu_items.menu_items_controller import MenuItemsController
from flask import jsonify
from pymongo.errors import PyMongoError

from models.api_return import Api

class MenuItems:

    @staticmethod
    def get(storeCode: str):
        try:
            if storeCode:
                return jsonify(Api.success(dados=list(MenuItemsController.fetch(storeCode)))), 200
            else:
                return jsonify(Api.problem(message='Parametro obrigatório não foi informado'))
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'Ocorreu ao buscar os dados {err}')), 503
        except Exception as err:
            return jsonify(Api.problem(message=f'Ocorreu um erro desconhecido {err}')), 503