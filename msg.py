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
    def create_post_msg(cls, id, content, post_time, parent_id, location=""):
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
            "location" : location,
        }
    
    @classmethod
    def create_get_feed_msg(cls, id):
        """
        클라이언트 -> 서버  
        피드 데이터 요청 메시지를 생성한다.  
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
    def create_post_data(cls, id, content, profile_img, like_cnt, comment_cnt, writed_time):
        """
        게시글 정보 데이터
        """
        return {
            "id" : id,
            "content" : content,
            "profile_img" : profile_img,
            "like_cnt" : like_cnt,
            "comment_cnt" : comment_cnt,
            "writed_time" : writed_time,
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
    
if __name__ == "__main__":
    msg = Message.create_login_msg("ht", "123qwe")
    print(msg)