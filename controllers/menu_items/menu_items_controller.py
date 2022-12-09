from models.collections.collections_data import Collections as col


class MenuItemsController:

    @staticmethod
    def fetch(storeCode: str):
        return col.CATEGORIES.aggregate([
            {
                '$match': {
                    'storeCode': storeCode
                }
            }, {
                '$lookup': {
                    'from': 'produtos',
                    'localField': '_id',
                    'foreignField': 'categoryId',
                    'as': 'products'
                }
            }, {
                '$project': {
                    '_id': 0,
                    'image': 0,
                    'storeCode': 0,
                    'products._id': 0,
                    'products.preparacao': 0,
                    'products.categoria': 0,
                    'products.storeCode': 0,
                    'products.status': 0,
                    'products.dataInsercao': 0,
                    'products.categoryId': 0
                }
            }, {
                '$match': {
                    'products.isActive': True
                }
            }, {
                '$sort': {
                    'ordenacao': 1
                }
            }, {
                '$project': {
                    'products.isActive': 0
                }
            }
        ])
