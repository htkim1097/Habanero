class MessageType:
    NONE = 0
    REGISTER = 1
    LOGIN = 2
    POST = 3
    GET_FEED =4
    GET_NOTIFICATIONS = 5
    GET_FOLLOWS = 6
    GET_CHAT_ROOM = 7
    GET_CHAT = 8
    GET_POST_IMG = 9

class MessageStatusType:
    FAILED = 0
    SUCCESS = 1

class Message:
    @classmethod
    def create_login_msg(cls, id, password):
        return {
            "type" : MessageType.LOGIN,
            "id" : id,
            "password" : password
        }
    
    @classmethod
    def create_login_res_msg(cls, status, message=""):
        return {
            "type" : MessageType.LOGIN,
            "status" : status,
            "message" : message
        }
    
    @classmethod
    def create_register_msg(cls, id, password, email, name, profile_image=""):
        return {
            "type" : MessageType.REGISTER,
            "id" : id,
            "password" : password,
            "email" : email,
            "name" : name,
            "profile_image" : profile_image
        }
    
    @classmethod
    def create_register_res_msg(cls, status, message=""):
        return {
            "type" : MessageType.REGISTER,
            "status" : status,
            "message" : message,
        }
    
    @classmethod
    def create_post_msg(cls, id, content, post_time, parent_id, location=""):
        return {
            "type" : MessageType.POST,
            "id" : id,
            "content" : content,
            "post_time" : post_time,
            "parent_id" : parent_id,
            "location" : location,
        }
    
    @classmethod
    def create_post_res_msg(cls, status, message=""):
        return {
            "type" : MessageType.POST,
            "status" : status,
            "message" : message,
        }
    
    @classmethod
    def create_get_feed_msg(cls, id):
        return {
            "type" : MessageType.GET_FEED,
            "id" : id,
        }
    
    @classmethod
    def create_get_feed_res_msg(cls, status, posts, message=""):
        return {
            "type" : MessageType.GET_FEED,
            "status" : status,
            "message" : message,
            "posts" : posts,
        }
    
    @classmethod
    def create_post_data(cls, id, content, profile_img, like_cnt, comment_cnt, elapsed_time):
        return {
            "id" : id,
            "content" : content,
            "profile_img" : profile_img,
            "like_cnt" : like_cnt,
            "comment_cnt" : comment_cnt,
            "elapsed_time" : elapsed_time,
        }
        
    @classmethod
    def create_get_notif_msg(cls, id):
        return {
            "type" : MessageType.GET_NOTIFICATIONS,
            "id" : id,
        }
    
    @classmethod
    def create_notif_res_msg(cls, status, notifications, message=""):
        return {
            "type" : MessageType.GET_NOTIFICATIONS,
            "status" : status,
            "message" : message,
            "notifications" : notifications,
        }
    
    @classmethod
    def create_notif_data(cls, notif_type, from_user_id, content):
        return {
            "type" : MessageType.GET_NOTIFICATIONS,
            "notif_type" : notif_type,
            "from_user_id" : from_user_id,
            "content" : content,
        }
    
if __name__ == "__main__":
    msg = Message.create_login_msg("ht", "123qwe")
    print(msg)