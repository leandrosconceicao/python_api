class Apps:

    def __init__(self, id: int, appsName: str, version: str, releaseDate: str) -> None:
        self.id = id
        self.appsName = appsName
        self.version = version
        self.releaseDate = releaseDate

    def format(json: dict) -> dict:
        return {
            '_id': json['id'],
            'appsName': json['appsName'],
            'version': json['version'],
            'releaseDate': json['releaseDate']
        }

    def fromJson(json):
        return Apps(
            id = json['id'],
            appsName = json['appsName'],
            version = json['version'],
            releaseDate = json['releaseDate']
        )