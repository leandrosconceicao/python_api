class QueriesFormat:

    def __init__(self, fromDate: str, toDate: str, status: str) -> None:
        self.fromDate = fromDate
        self.toDate = toDate
        self.status = status

    @staticmethod
    def setPeriod(fromDate: str, toDate: str) -> dict:
        return {'$gte': fromDate, '$lte': toDate}

    @staticmethod
    def filterProduct(order: str) -> dict:
        return {
            "$elemMatch": {
                "opcao": order
            }
        }

    @staticmethod
    def salesByPeriod(fromDate: str, toDate: str) -> dict:
        return {
            'data':
                QueriesFormat.setPeriod(fromDate=fromDate, toDate=toDate),
                "status": {'$ne': 'Cancelado'}
        }

    @staticmethod
    def salesByPeriodAndProduct(fromDate: str, toDate: str, product: str) -> dict:
        q = QueriesFormat.salesByPeriod(fromDate, toDate)
        q['pedidos'] = QueriesFormat.filterProduct(
            product)
        return q