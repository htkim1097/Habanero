class MessageType:
    NONE = 0
    REGISTER = 1
    LOGIN = 2
    POST = 3
    GET_FEED =4
    GET_NOTIFICATIONS = 5
    LIKE_POST = 6   

message = {
    "type" : MessageType.NONE,
    "data" : None    
}