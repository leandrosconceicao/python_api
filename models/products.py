class Products:

    def __init__(self, id, nome, preco, categoria):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.categoria = categoria

    def fromJson(json):
        return Products(
            json['_id'],
            json['produto'],
            json['preco'],
            json['categoria']
        )

    def toJson(self):
        return {
            '_id': int(self.id),
            'produto': self.nome,
            'preco': float(self.preco.replace(',', '.')),
            'categoria': self.categoria
        }