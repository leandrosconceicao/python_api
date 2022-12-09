from models.collections.collections_data import Collections
from config import MongoDB
from models.db_queries import QueriesFormat
from models.db_return import DbReturn
from models.sales_query import SalesQuery
from pymongo.errors import *
from pymongo.results import DeleteResult, UpdateResult, InsertOneResult

class QueriesOperations:

    @staticmethod
    def getProducts():
        return Collections.PRODUCTS.distinct('produto')

    @staticmethod
    def getCategories():
        return MongoDB.collectionCategorias.distinct('nome')

    @staticmethod
    def getSales(fromDate: str, toDate: str):
        p = QueriesOperations.getProducts()
        d = []
        for i in p:
            q = Collections.ORDERS.find(
                QueriesFormat.salesByPeriodAndProduct(fromDate, toDate, i)
            )
            for x in q:
                d.append(x['pedidos'])
        return d

    @staticmethod
    def getPaymentsByDate(fromDate: str, toDate: str):
        try:
            return DbReturn(
                True, 'Success', list(Collections.FINANCIALS.find(
                    {} if fromDate == None and toDate == None else {
                        'data': QueriesFormat.setPeriod(fromDate, toDate)}
                ))
            )
        except PyMongoError as err:
            return DbReturn(False, f'Ocorreu um erro no banco {err}')
        except Exception as err:
            return DbReturn(False, f'Ocorre um erro na aplicação {err}')

    @staticmethod
    def updateProduct(id: int, dados):
        try:
            Collections.PRODUCTS.update_one(
                        {'_id': int(id)}, {'$set': dados}
                    )
        except PyMongoError as err:
            pass
        except Exception as err:
            pass
        
    @staticmethod
    def updateOrders(id: int, option: str, description: str, preparation: bool):
        try:
            Collections.ORDERS.update_many(
                {"status": {"$ne": "Pago"}}
                ,   { "$set": { 
                    "pedidos.$[elem].opcao": option,
                    "pedidos.$[elem].descPedido": f'{option}{description.replace(option, "")}',
                    "pedidos.$[elem].preparacao": preparation,
                    },
                }, 
                { "arrayFilters": [{ "elem.id": id }] })
            MongoDB.conn.close()
        except PyMongoError as err:
            pass

    
    @staticmethod
    def getPaymentsForms():
        try:
            return DbReturn(
                statusProcess=True,
                data=Collections.PAYMENTSFORMS.find({})
            )
        except PyMongoError as err:
            return DbReturn(
                statusProcess=False,
                data=[],
                message=err,
            )

    @staticmethod
    def postPaymentsForms(request):
        try:
            Collections.PAYMENTSFORMS.insert_one(request)
            return DbReturn(
                statusProcess=True,
            )
        except PyMongoError as err:
            return DbReturn(statusProcess=False, message=f'{err}')

class MenuOperations:

    @staticmethod
    def get(filter: dict):
        return Collections.MENUS.find(filter)
    
    @staticmethod
    def post(document: dict):
        return Collections.MENUS.insert_one(document)
    
    @staticmethod
    def put(filters: dict, document: dict) -> UpdateResult:
        return Collections.MENUS.update_many(
            filters, {'$set': document}
        )
    
    @staticmethod
    def delete(filter) -> DeleteResult:
        return Collections.MENUS.delete_many(
            filter
        )

    
class AppsOperations:

    @staticmethod
    def get(filter: dict):
        return Collections.APPS.find(filter)
    
    @staticmethod
    def post(document: dict):
        return Collections.APPS.insert_one(document)
    
    @staticmethod
    def put(filters: dict, document: dict) -> UpdateResult:
        return Collections.APPS.update_many(
            filters, {'$set': document}
        )
    @staticmethod
    def delete(filter: dict) -> DeleteResult:
        return Collections.APPS.delete_many(filter)

class SessionsOperations:

    @staticmethod
    def get(filter: dict):
        return Collections.SESSIONS.find(filter)
    
    @staticmethod
    def post(document: dict) -> InsertOneResult:
        return Collections.SESSIONS.insert_one(document)
    
    @staticmethod
    def put(filters: dict, document: dict) -> UpdateResult:
        return Collections.SESSIONS.update_many(
            filters, {'$set': document}
        )
    
    @staticmethod
    def delete(filter) -> DeleteResult:
        return Collections.SESSIONS.delete_many(
            filter
        )

    @staticmethod
    def patchIn(id: int, productIds: list) -> UpdateResult:
        products : list = []
        for i in productIds:
            products.append(Collections.CATEGORIES.find_one({'_id': i}))
        return Collections.SESSIONS.update_one(
            {"_id": int(id)},
            {'$addToSet': {"products": {'$each': products}}}
        )
    
    @staticmethod
    def patchOut(id: int, productIds: list) -> UpdateResult:
        print(productIds)
        for i in productIds:
            return Collections.SESSIONS.update_one(
            {"_id": int(id)},
            {'$pull': {"products": {"_id": int(i)}}}
        )


class ImageOperations:

    @staticmethod
    def delete(name : str) -> DeleteResult:
        return Collections.PRODUCTS.update_many({"image.name": name}, {"$unset": {"image": ""}})