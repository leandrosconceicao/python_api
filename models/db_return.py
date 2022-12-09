class DbReturn:

    def __init__(self, statusProcess=False, message='', data=None):
        self.statusProcess = statusProcess
        self.message = message
        self.data = data