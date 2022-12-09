from flask import jsonify
from models.api_return import Api
from models.authorization.authorization_data import Authorization
from models.collections.collections_data import Collections
from pymongo.errors import PyMongoError


class AuthorizationView:

    @staticmethod
    def authenticate(request):
        try:
            auth: Authorization = Authorization.fromJson(request)
            r: dict = Collections.USERS.find_one(
                {'email': auth.user, 'pass': auth.password}
            )
            userIsValid: bool = r is not None
            if userIsValid:
                userHasToken: bool = len(auth.token) > 0
                if userHasToken:
                    Collections.USERS.update_one({"_id": auth.user}, {'$set': {
                        "token": auth.token
                    }})
                else:
                    pass
                return jsonify(
                    Api.success(dados=r)
                ), 200
            return jsonify(Api.problem(message='Usuário não encontrado ou dados incorretos, verifique')), 403
        except PyMongoError as err:
            return jsonify(Api.problem(f'{err}')), 500
        except Exception as err:
            return jsonify(Api.problem(f'{err}')), 500
