from pymongo.errors import *
from pymongo.results import UpdateResult
from models.collections.collections_data import Collections
from models.db_return import DbReturn
from models.queries.queries_model import QueriesModel


class EstablishmentsApi:

    table = Collections.ESTABLISHMENTS

    @staticmethod
    def get(filter=None) -> DbReturn:
        try:
            return DbReturn(statusProcess=True, data=Collections.ESTABLISHMENTS.find(
                {} if filter is None else filter))
        except PyMongoError as err:
            return DbReturn(message=err)
        except Exception as err:
            return DbReturn(message=err)

    @staticmethod
    def post(data: dict) -> DbReturn:
        try:
            Collections.ESTABLISHMENTS.insert_one(
                data                
            )
            return DbReturn(statusProcess=True, message='Success')
        except PyMongoError as err:
            return DbReturn(message=err)
        except Exception as err:
            return DbReturn(message=err)

    @staticmethod
    def put(id: int, data: dict) -> DbReturn:
        try:
            Collections.ESTABLISHMENTS.update_one(
                {"_id": id},
                {'$set': data}
            )
            return DbReturn(statusProcess=True)
        except PyMongoError as err:
            return DbReturn(message=err)
        except Exception as err:
            return DbReturn(message=err)

    @staticmethod
    def insertStore(id: int, data) -> UpdateResult:
        dt = QueriesModel.insertInto(int(id), 'stores', data)
        return Collections.ESTABLISHMENTS.update_one(
            dt[0], dt[1]
        )
    
    @staticmethod
    def removeStore(id: int, data) -> UpdateResult:
        dt = QueriesModel.removeFrom(int(id), 'stores', data)
        return Collections.ESTABLISHMENTS.update_one(
            dt[0], dt[1]
        )


    @staticmethod
    def delete(id: int):
        try:
            Collections.ESTABLISHMENTS.delete_one(
                {"_id": id}
            )
            return DbReturn(
                statusProcess=True,
            )
        except PyMongoError as err:
            return DbReturn(message=err)
        except Exception as err:
            return DbReturn(message=err)