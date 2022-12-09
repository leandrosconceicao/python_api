from typing import Any, Dict


class SalesQuery:

    def __init__(self, product:str, qtd: float) -> Any:
        self.product = product
        self.qtd = qtd

    def toJson(self, product, qtd) -> Dict:
        return {
            'product': product,
            'qtd': qtd
        }