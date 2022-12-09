class OrderItems:

    def __init__(self, qtProducts, selectedOption, description, orderPrice, unitPrice) -> None:
        self.qtProducts = qtProducts
        self.selectedOption = selectedOption
        self.description = description
        self.orderPrice = orderPrice
        self.unitPrice = unitPrice

    def fromJson(json):
        return OrderItems(
            qtProducts=json['qtProdutos'],
            selectedOption=json['opcao'],
            description=json['descPedido'],
            orderPrice=json['valPedido'],
            unitPrice=json['precoUnitario'],
        )


class Orders:

    def __init__(self, id, operationDay, date, orderItens, totalPrice, isPayed, clientName,
    observation, status, saller, table, statusTable, idTable) -> None:
        self.id = id
        self.table = table
        self.idTable = idTable
        self.operationDay = operationDay
        self.date = date
        self.orderItems = orderItens
        self.totalPrice = totalPrice
        self.isPayed = isPayed
        self.clientName = clientName
        self.observation = observation
        self.status = status
        self.statusTable = statusTable
        self.saller = saller

   
    def fromJson(json):
        orders = []
        if json['pedidos'] is not None:   
            for i in json['pedidos']:
                orders.append(OrderItems.fromJson(i))
        return Orders(
            id = json['_id'],
            table = checkValue(json, 'mesa'),
            idTable = checkValue(json, 'idMesa'),
            operationDay = checkValue(json, 'diaOperacao'),
            date = checkValue(json,'data'),
            orderItens = orders,
            totalPrice = checkValue(json,'precoTotal'),
            isPayed = checkValue(json, 'pago'),
            clientName = checkValue(json, 'clientName'),
            observation = checkValue(json,'obs'),
            status = checkValue(json, 'status'),
            statusTable = checkValue(json, 'statusMesa'),
            saller = json['operador'],
        )
    
def checkValue(value, key):
    try:
        return value[key]
    except KeyError:
        return ''


class OrderItems:

    def __init__(self, qtProducts, selectedOption, description, orderPrice, unitPrice):
        self.qtProducts = qtProducts
        self.selectedOption = selectedOption
        self.description = description
        self.orderPrice = orderPrice
        self.unitPrice = unitPrice

    def fromJson(json):
        return OrderItems(
            qtProducts=json['qtProdutos'],
            selectedOption=json['opcao'],
            description=json['descPedido'],
            orderPrice=json['valPedido'],
            unitPrice=json['precoUnitario'],
        )


    