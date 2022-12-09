from typing import Dict
from pymongo.errors import *
from models.collections.collections_data import Collections
from config import MongoDB
from models.db_queries import QueriesFormat
from models.db_return import DbReturn


class SalesReports:

    def salesBySaller(date, saller) -> DbReturn:
        try:
            sm = 0.0
            r = Collections.ORDERS.find(
                {'diaOperacao': date, 'operador': saller}
            )
            for i in r:
                for x in i['pedidos']:
                    sm += float(x['valPedido'])
            return DbReturn(
                statusProcess=True,
                message='Success',
                data=sm
            )
        except PyMongoError as err:
            return DbReturn(message=f'{err}')

    @staticmethod
    def getSalesBySaller(date) -> DbReturn:
        try:
            r = []
            for i in Collections.USERS.find({'ativo': True}):
                d = {}
                d['saller'] = i['username']
                d['qtd'] = SalesReports.salesBySaller(date, i['username']).data
                r.append(d)
            return DbReturn(
                statusProcess=True,
                data=r
            )
        except PyMongoError as err:
            pass

    @staticmethod
    def detailSales(date) -> DbReturn:
        try:
            q = SalesReports.quantSalesByProduct(date).items()
            d = {}
            r = []
            if q:
                for i in q:
                    sub = i[1]['quantidade'] * i[1]['precoUnitario']
                    d['values'] = {
                        'product': i[0],
                        'subtotal': sub,
                        'qtSales': i[1]['quantidade'],
                        'unitPrice': i[1]['precoUnitario'],
                        'category': i[1]['category']
                    }
                    r.append(d)
                    d = {}
                return DbReturn(
                    True, 'Success', r
                )
            else:
                return DbReturn(
                    message='Sem dados'
                )
        except PyMongoError as err:
            return DbReturn(message=f'{err}')

    @staticmethod
    def quantSalesByProduct(data=None) -> Dict:
        dados = {}
        p = Collections.PRODUCTS.find({}).sort(
            [('categoria', 1), ('produto', 1)])
        for i in p:
            query = Collections.ORDERS.find({
                "pedidos": QueriesFormat.filterProduct(i['produto']), 'diaOperacao': data, 'status': {'$ne': 'Cancelado'}
            })
            if query:
                qt = 0
                for y in query:
                    for x in y['pedidos']:
                        if x['opcao'] == i['produto']:
                            qt += int(x['qtProdutos'])
                dados[i['produto']] = {
                    'quantidade': qt, 'precoUnitario': i['preco'], 'category': i['categoria']}
            qt = 0
            # pUnit = 0
        return dados

    @staticmethod
    def getSalesByPeriod(fromDate: str, toDate: str):
        try:
            return DbReturn(
                statusProcess=True,
                message='Success',
                data=list(Collections.ORDERS.find(
                    QueriesFormat.salesByPeriod(fromDate, toDate),
                    {"pedidos": -1, "status": -1, "pago": -1}
                ))
            )
        except PyMongoError as err:
            return DbReturn(
                message=err
            )

    @staticmethod
    def getSalesByPeriodAndProduct(fromDate: str, toDate: str, product: str) -> Dict:
        try:
            return DbReturn(
                statusProcess=True,
                message='Success',
                data=list(Collections.ORDERS.find(
                    QueriesFormat.salesByPeriodAndProduct(
                        fromDate, toDate, product),
                ))
            )
        except PyMongoError as err:
            return DbReturn(message=err)
