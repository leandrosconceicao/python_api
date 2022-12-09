from flask import jsonify
from itsdangerous import json
from controllers.operations.db_operations import QueriesOperations
from models.api_return import Api


class PaymentsFormsView:

    @staticmethod
    def get():
        r = QueriesOperations.getPaymentsForms()
        return jsonify(
            Api(
                status=r.statusProcess,
                data=list(r.data),
                message=r.message,
            ).getDataReturn()
        ), 200 if r.statusProcess else 405

    @staticmethod
    def post(request):
        r = QueriesOperations.postPaymentsForms(request)
        return jsonify(
            statusProcess=r.statusProcess
        ), 200 if r.statusProcess else 405