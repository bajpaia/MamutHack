from datetime import datetime

class Client(object):
    def __init__(self, id, risk):
        self.id = id
        self.risk = risk
        self.created = datetime.now()

    def get_priority(self):
        return self.risk + ((datetime.now() - self.created).seconds / 30)


