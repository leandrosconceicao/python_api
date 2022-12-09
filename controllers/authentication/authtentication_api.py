from models.collections.collections_data import Collections
from pymongo.errors import PyMongoError

class Authentication:

    @staticmethod
    def userPermited(u):
        try:
            if Collections.USERS.find_one({'email': u}):
                return True
            return False
        except PyMongoError:
            return False
        except Exception:
            return False