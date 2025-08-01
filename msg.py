class MessageType:
    NONE = 0
    REGISTER = 1
    LOGIN = 2
    POST = 3
    GET_FEED =4
    GET_NOTIFICATIONS = 5
    LIKE_POST = 6   

class Message:
    def __init__(self, type, id, password):
        self.type = MessageType.NONE
        self.id = id
        self.password = password
    