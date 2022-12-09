import hashlib


class Authorization:

    def __init__(self, user:str, password: str, token: str) -> None:
        self.user = user
        self.password = password
        self.token = token
    
    @staticmethod
    def fromJson(json):
        return Authorization(
            user = json['email'],
            password = hashlib.md5(json['password'].encode()).hexdigest(),
            token = json['token'] if json['token'] is not None else ''
        )

    def toMap(self):
        return {
            'email': self.user,
            'password': self.password,
            'token': self.token
        }
    
