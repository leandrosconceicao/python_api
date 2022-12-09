class MenuData:

    def __init__(self, id, name, establishmentsId) -> None:
        self.id = id
        self.name = name
        self.establishmentsId = establishmentsId


    def format(json):
        return {
            "_id": json['id'],
            "name": json['name'],
            "establishmentsId": json['establishmentsId']
        }