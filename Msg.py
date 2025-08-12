class EnumMessageType:
    """
    메시지 유형 열거형
    """
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
    FOLLOWING = 10
    GET_USER_INFO = 11
    GET_CHAT_DATA = 12
    ADD_CHAT_DATA = 13
    ADD_CHAT_ROOM = 14
    # 서버에서 동작을 구분할 수 있도록 타입을 추가해준다.
    UPDATE_PROFILE = 100
    ADD_LIKE = 16
    GET_COMMENTS = 17

class EnumMsgStatus:
    """
    요청 성공 여부 열거형
    """
    FAILED = 0
    SUCCESS = 1

class Message:
    """
    서버-클라이언트 간 메시지 생성 메서드 집합 클래스
    """

    @classmethod
    def create_response_msg(cls, type, status, message="", data=None):
        """
        서버 -> 클라이언트  
        클라이언트 요청 결과 메시지를 생성한다.   
        """
        return {
            "type" : type,
            "status" : status,
            "message" : message,
            "data" : data,
        }

    @classmethod
    def create_login_msg(cls, id, password):
        """
        클라이언트 -> 서버  
        로그인을 요청하는 메시지를 생성한다.  
        - id: 사용자 아이디  
        - password: 사용자 비밀번호  
        """
        return {
            "type" : EnumMessageType.LOGIN,
            "id" : id,
            "password" : password
        }
    
    @classmethod
    def create_register_msg(cls, id, password, email, name, profile_image=""):
        """
        클라이언트 -> 서버  
        회원가입 요청 메시지를 생성한다.
        """
        return {
            "type" : EnumMessageType.REGISTER,
            "id" : id,
            "password" : password,
            "email" : email,
            "name" : name,
            "profile_image" : profile_image
        }
    
    @classmethod
    def create_post_msg(cls, id, content, post_time, parent_id, image):
        """
        클라이언트 -> 서버  
        게시물 작성 메시지를 생성한다.  
        """
        return {
            "type" : EnumMessageType.POST,
            "id" : id,
            "content" : content,
            "post_time" : post_time,
            "parent_id" : parent_id,
            #"location" : location,
            "image" : image,
        }
    
    @classmethod
    def create_get_feed_msg(cls, id):
        """
        클라이언트 -> 서버  
        피드 데이터 요청 메시지를 생성한다.
         ⚠️ 아이디를 보내면 following 페이지가 보이고, None 보내면 랜덤으로 보임
            (내 게시글은 for toy랑 following 페이지 둘 다 보임)

        """
        return {
            "type" : EnumMessageType.GET_FEED,
            "id" : id,
        }
        
    @classmethod
    def create_get_notif_msg(cls, id):
        """
        클라이언트 -> 서버  
        알림 데이터 요청 메시지를 생성한다.  
        """
        return {
            "type" : EnumMessageType.GET_NOTIFICATIONS,
            "id" : id,
        }
    
    @classmethod
    def create_add_following_msg(cls, id, to_user_id):
        """
        클라이언트 -> 서버  
        친구 추가 메시지 생성  
        """
        return {
            "type" : EnumMessageType.FOLLOWING,
            "id" : id,
            "to_user_id" : to_user_id,
        }
    
    @classmethod
    def create_get_follows_msg(cls, id):
        """
        클라이언트 -> 서버  
        친구 목록 요청 메시지 생성  
        """
        return {
            "type" : EnumMessageType.GET_FOLLOWS,
            "id" : id
        }
    
    @classmethod
    def create_get_userinfo_msg(cls, id):
        """
        클라이언트 -> 서버  
        사용자 정보를 불러온다.
        """
        return {
            "type" : EnumMessageType.GET_USER_INFO,
            "id" : id,
        }
    
    @classmethod
    def create_add_chatroom_msg(cls, user_id, user_id2, chatroom_date):
        """
        클라이언트 -> 서버  
        채팅방을 만든다.  
        """
        return {
            "type" : EnumMessageType.ADD_CHAT_ROOM,
            "user_id" : user_id,
            "user_id2" : user_id2,
            "chatroom_date" : chatroom_date,
        }
    
    @classmethod
    def create_get_chat_data_msg(cls, chatroom_id, last_chat_time):
        """
        클라이언트 -> 서버  
        to_user_id와 채팅한 메시지 데이터들을 받아온다.  
        """
        return {
            "type" : EnumMessageType.GET_CHAT_DATA,
            "chatroom_id" : chatroom_id,
            "last_chat_time" : last_chat_time,
        }
    
    @classmethod
    def create_add_chat_msg(cls, chatroom_id, data):
        """
        클라이언트 -> 서버  
        chatroom_id의 채팅방에서 입력된 data를 저장하도록 요청한다.  
        """
        return {
            "type" : EnumMessageType.ADD_CHAT_DATA,
            "chatroom_id" : chatroom_id,
            "data" : data
        }

    @classmethod
    def create_update_profile(cls, user_id, user_name, profile_image):
        """
        클라이언트 -> 서버

        """
        return {
            "type" : EnumMessageType.UPDATE_PROFILE,
            "user_id" : user_id,
            "user_name" : user_name,
            "profile_image" : profile_image,
        }

    @classmethod
    def create_get_chatroom_list_msg(cls, user_id1, user_id2):
        """
        클라이언트 -> 서버  
        user_id1과 user_id2로 생성된 채팅방이 있는지 확인한다.  
        """
        return {
            "type" : EnumMessageType.GET_CHAT_ROOM,
            "user_id1" : user_id1,
            "user_id2" : user_id2,
        }
    
    @classmethod
    def create_add_like(cls, user_id, post_id):
        """
        클라이언트 -> 서버  
        좋아요를 누른 user_id와 좋아요 대상의 post_id로 좋아요를 추가한다.  
        """
        return {
            "type" : EnumMessageType.ADD_LIKE,
            "user_id" : user_id,
            "post_id" : post_id,
        }
    
    @classmethod
    def create_get_comments(cls, post_id):
        """
        클라이언트 -> 서버  
        post_id에 해당하는 모든 댓글을 가져온다.
        """
        return {
            "type" : EnumMessageType.GET_COMMENTS,
            "post_id" : post_id,
        }
    

class MessageData:
    """
    메시지 데이터를 생성하는 메서드의 집합 클래스
    """
    @classmethod
    def create_userinfo_data(cls, id, name, email, profile_img):
        """
        사용자 정보 데이터
        """
        return {
            "id" : id, 
            "name" : name,
            "email" : email,
            "profile_img" : profile_img,
        }

    @classmethod
    def create_post_data(cls, id, content, like_cnt, comment_cnt, writed_time, image=None, parent_id=None):
        """
        게시글 정보 데이터
        """
        return {
            "id" : id,
            "content" : content,
            "image" : image,
            "like_cnt" : like_cnt,
            "comment_cnt" : comment_cnt,
            "writed_time" : writed_time,
            "parent_id" : parent_id
        }

    @classmethod
    def create_notif_data(cls, notif_type, from_user_id, content):
        """
        알림 정보 데이터
        """
        return {
            "type" : EnumMessageType.GET_NOTIFICATIONS,
            "notif_type" : notif_type,
            "from_user_id" : from_user_id,
            "content" : content,
        } 
    
    @classmethod
    def create_msg_data(cls, user_id, chatroom_id, content, message_time, image=None):
        """
        채팅 메시지 데이터
        """
        return {
            "user_id" : user_id,
            "chatroom_id" : chatroom_id,
            "content" : content,
            "message_time" : message_time,
            "image" : image,
        }
    
    @classmethod
    def create_chatroom_data(cls, chatroom_id, user_id1, user_id2, chatroom_date):
        """
        채팅 방 데이터  
        """
        return {
            "chatroom_id" : chatroom_id,
            "user_id1" : user_id1,
            "user_id2" : user_id2,
            "chatroom_date" : chatroom_date
        }
    
    @classmethod
    def create_comment_data(cls, comment_id, parent_id, user_id, content, writed_time):
        """
        댓글 데이터
        """
        return {
            "comment_id" : comment_id,
            "parent_id" : parent_id,
            "user_id" : user_id,
            "content" : content,
            "writed_time" : writed_time
        }
    
if __name__ == "__main__":
    msg = Message.create_login_msg("ht", "123qwe")
    print(msg)
