class QueriesModel:

    def __init__(self, filter, array) -> None:
        self.filter = filter
        self.array = array

    @staticmethod
    def searchByName(field: str):
        return {'$regex': f'{field}', '$options': 'i'}

    @staticmethod
    def insertInto(id, array: str, data) -> tuple:
        return ({"_id": id},
        {'$addToSet': {array: data}})

    @staticmethod
    def removeFrom(id, array: str, data) -> tuple:
        return ({"_id": id},
        {'$pull': {array: data}})