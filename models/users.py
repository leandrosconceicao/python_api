import hashlib


class Users:

    def __init__(self, id, email, password, group, username, active, establishments):
        self.id = id
        self.email = email
        self.password = password
        self.group = group
        self.username = username
        self.active = active
        self.establishments = establishments

    @staticmethod
    def format(json):
        return {
            '_id': json['_id'],
            'email': json['email'],
            'pass': hashlib.md5(json['pass'].encode()).hexdigest(),
            'group_user': json['group_user'],
            'username': json['username'],
            'ativo': json['ativo'],
            'establishments': json['establishments']
        }