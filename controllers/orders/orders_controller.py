from pymongo.results import DeleteResult, UpdateResult, InsertOneResult

from models.collections.collections_data import Collections


class OrderController:

    @staticmethod
    def addPayment(filter: dict) -> UpdateResult:
        return Collections.ORDERS.update_one(
            {"_id": filter.get('id')},
            {"$push": {"payment": filter.get('data')}}
        )

    @staticmethod
    def updateOrder(request: dict) -> UpdateResult:
        id: str = request.get('id')
        request.pop("id")
        return Collections.ORDERS.update_one(
            {'_id': id}, {'$set': request}
        )

    @staticmethod
    def pushItems(id: str, data: list) -> UpdateResult:
        return Collections.ORDERS.update_one(
            {"_id": id},
            {'$push': {"pedidos": {"$each": data}}}
        )

    @staticmethod
    def popItems(id: str, data: list) -> UpdateResult:
        return Collections.ORDERS.update_one(
            {"_id": id},
            {'$pull': {"pedidos": {"$each": data}}}
        )

    @staticmethod
    def getPreparationOrders(storeCode: str) -> list:
        return list(Collections.ORDERS.aggregate(
            [
                {
                    '$match': {
                        'storeCode': storeCode,
                        'pedidos': {
                            '$elemMatch': {
                                'preparacao': True
                            }
                        }
                    }
                }
            ])
        )
