class Establishments:

    def __init__(self, id: int, storeName: str, stores: list, ownerId: int) -> None:
        self.id = id
        self.storeName = storeName
        self.stores = stores

    @staticmethod
    def format(json) -> dict:
        return {
            '_id': json['id'],
            'storeName': json['storeName'],
            'stores': Stores.toList(json['stores']),
            'ownerId': json['ownerId'],
        }

    @staticmethod
    def toList(json: list) -> list:
        map = []
        for i in json:
            map.append(Establishments.format(i))
        return map

class Stores:

    def __init__(self, id: str, location: str) -> None:
        self.id = id
        self.location = location

    
    @staticmethod
    def format(json) -> dict:
        return {
            '_id': json['id'],
            'location': json['location']
        }

    @staticmethod
    def toList(json: list) -> list:
        map = []
        for i in json:
            map.append(Stores.format(i))
        return map