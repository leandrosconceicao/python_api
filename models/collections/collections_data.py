from config import MongoDB


class Collections:

    USERS = MongoDB.database['usuarios']
    ORDERS = MongoDB.database['pedidos']
    PRODUCTS = MongoDB.database['produtos']
    ADDONES = MongoDB.database['addOnes']
    COMPONENTS = MongoDB.database['components']
    CATEGORIES = MongoDB.database['categorias']
    SESSIONS = MongoDB.database['sessions']
    ESTABLISHMENTS = MongoDB.database['estabelecimentos']
    TABLES = MongoDB.database['mesas']
    MENUS = MongoDB.database['cardapios']
    FINANCIALS = MongoDB.database['recebimentos']
    PAYMENTSFORMS = MongoDB.database['paymentForms']
    APPS = MongoDB.database['apps']
    TOKENS = MongoDB.database['tokens']


class Views:

    menu = MongoDB.database['MENU_ITEMS']