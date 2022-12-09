from models.db_return import DbReturn
from pymongo.errors import PyMongoError, DuplicateKeyError
from flask import jsonify

class Api:

    def __init__(self, status=False, message = '', data = None):
        self.status = status
        self.message = message
        self.data = data

    def getReturn(self):
        return {
            'statusProcess': self.status,
            'message': self.message
        }

    def getDataReturn(self):
        return {
            'statusProcess': self.status,
            'message': self.message,
            'dados': self.data
        }

    @staticmethod
    def fromDB(dbReturn: DbReturn):
        return Api(
            data=dbReturn.data,
            message=dbReturn.message,
            status=dbReturn.statusProcess
        ).getDataReturn()

    @staticmethod
    def success(dados=[]):
        return Api(
            status=True,
            message='Success',
            data=dados
        ).getDataReturn()
    
    @staticmethod
    def problem( message: str,dados=[]):
        return Api(
            status=False,
            message='Ocorreu um problema' if message is None else f'{message}' ,
            data=dados
        ).getDataReturn()

    @staticmethod
    def unauthorized():
        return jsonify(Api.problem('Metodo não permitido')), 405

    @staticmethod
    def noParams():
        return jsonify(Api.problem('Parametro necessário não foi informado')), 403
    

    @staticmethod
    def request(func):
        try:
            return func()
        except PyMongoError as err:
            return jsonify(Api.problem(message=f'Ocorreu um problema com a requisição {err}')), 500
        except Exception as err:
            return jsonify(Api.problem(message=f'Ocorreu um erro desconhecido {err}'))
