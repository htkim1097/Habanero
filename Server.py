import Config
import socket
import threading
import pymysql
from Msg import *
import datetime

class ThreadsServer:
    def __init__(self):
        self.address = Config.comm_config["host"]
        self.port = Config.comm_config["port"]
        self.baudrate = Config.comm_config["baudrate"]
        self.db_address = Config.db_config["host"]
        self.db_port = Config.db_config["port"]
        self.db_user = Config.db_config["user"]
        self.db_password = Config.db_config["password"]
        self.db_charset = Config.db_config["charset"]

        self.is_running = False
        
    def start_server(self):
        """
        서버를 실행한다.
        """
        self.socket = socket.socket(Config.comm_config["socket_family"], Config.comm_config["socket_type"])
        self.socket.bind((self.address, self.port))

        # 최대 5개까지 연결 대기
        self.socket.listen(5)

        self.is_running = True

        print(f"[서버 시작] - {self.address}:{self.port}")

        while self.is_running:
            try:
                client_socket, address = self.socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address, self.baudrate))

                # 메인 스레드 종료시 클라이언트 스레드도 종료되도록 데몬 스레드로 함
                client_thread.daemon = True
                client_thread.start()

            except Exception as e:
                print(f"[서버 오류] - {e}")
                break

    def handle_client(self, client_socket, address, baudrate):
        """
        클라이언트 연결 관련
        """
        print(f"\n[클라이언트 연결] - {address}")

        try:
            while True:
                recv_data = b""
                while True:
                    chunk = client_socket.recv(baudrate)
                    if not chunk:
                        break

                    recv_data += chunk

                    if b"<EOF>" in recv_data:
                        recv_data = recv_data.split(b"<EOF>")[0]
                        break

                    print(f"[데이터 수신 {address}] - {recv_data}")

                if recv_data:
                    repr_data = eval(recv_data.decode())
                    res = self.handle_data(repr_data)
                    client_socket.send((str(res) + "<EOF>").encode())
                    print(f"[데이터 송신 {address}] - {res}")

        except Exception as e:
            print(f"[오류:handle_client] - {e}")
        finally:
            client_socket.close()

    def handle_data(self, msg):
        """
        클라이언트로 부터 받은 메시지의 유형에 따라 처리 메서드를 실행한다.
        """
        msg_type = int(msg["type"])

        try:
            if msg_type == EnumMessageType.LOGIN:
                return self.handle_login(msg)
            elif msg_type == EnumMessageType.REGISTER:
                return self.handle_register(msg)
            elif msg_type == EnumMessageType.POST:
                return self.handle_post(msg)
            elif msg_type == EnumMessageType.GET_FEED:
                return self.handle_get_feed(msg)
            elif msg_type == EnumMessageType.GET_NOTIFICATIONS:
                return self.handle_get_notifi(msg)
            elif msg_type == EnumMessageType.GET_FOLLOWS:
                return self.handle_get_follows(msg)
            elif msg_type == EnumMessageType.GET_USER_INFO:
                return self.handle_get_userinfo(msg)
            elif msg_type == EnumMessageType.ADD_CHAT_ROOM:
                return self.handle_add_chatroom(msg)
            # 여기에 Msg.py에서 추가한 타입을 추가해준다.
            elif msg_type == EnumMessageType.UPDATE_PROFILE:
                return self.handle_update_profile(msg)
            elif msg_type == EnumMessageType.GET_CHAT_ROOM:
                return self.handle_get_chatroom(msg)
            else:
                raise Exception("[오류:handle_data] - 클라이언트로부터 받은 데이터의 type 값에 오류가 있습니다.")
            
        except Exception as e:
            print(f"[오류:handle_data] - {e}")

    def handle_login(self, msg):
        """
        로그인 정보를 확인하여 결과를 전달한다.
        """
        m_type = EnumMessageType.LOGIN

        res = self.send_query(f"SELECT * FROM user WHERE user_id = '{msg["id"]}' AND password = '{msg["password"]}';")
         
        if (len(res) > 0):
            return Message.create_response_msg(
                type=m_type, 
                status=EnumMsgStatus.SUCCESS
                )
        else:
            return Message.create_response_msg(
                type=m_type, 
                status=EnumMsgStatus.FAILED, 
                message="로그인 정보 없음"
                )

    def handle_register(self, msg):
        """
        회원가입에서 입력한 값들로 user 테이블에 데이터를 추가한다. 
        """
        m_type = EnumMessageType.REGISTER

        try:
            if (len(self.send_query(f"select * from user where user_id = '{msg["id"]}';")) > 0):
                return Message.create_response_msg(
                    type=m_type, 
                    status=EnumMsgStatus.FAILED, 
                    message="입력한 아이디가 이미 있습니다."
                    )
            else:
                self.send_query(f"INSERT INTO user VALUES ('{msg["id"]}', '{msg["email"]}', '{msg["password"]}', '{msg["name"]}', '{msg["profile_image"]}');")
                res = self.send_query(f"select * from user where user_id = '{msg["id"]}';")

                if (len(res) > 0):
                    return Message.create_response_msg(
                        type=m_type,
                        status=EnumMsgStatus.SUCCESS,
                        )
                else:
                    return Message.create_response_msg(
                        type=m_type,
                        status=EnumMsgStatus.FAILED, 
                        message="조회 실패"
                        )
                
        except Exception as e:
            print(f"[오류:handle_register] - {e}")
            return Message.create_response_msg(
                typ=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )

    def handle_post(self, msg):
        """
        게시글 작성 동작 후 결과를 전달한다.
        """
        m_type = EnumMessageType.POST
        try:
            # parent_id가 없으면 게시글
            if msg['parent_id'] is None:
                res = self.send_query(f"INSERT INTO post VALUES (null, \"{msg["content"]}\", \"{msg["img"]}\", \"{msg["id"]}\", \"{msg["post_time"]}\", null);")            
            # parent_id가 있으면 댓글
            else:
                res = self.send_query(f"INSERT INTO post VALUES (null, \"{msg["content"]}\", \"{msg["img"]}\", \"{msg["id"]}\", \"{msg["post_time"]}\", \"{msg["parent_id"]}\");")

            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS
                )
        
        except Exception as e:
            print(f"[오류:handle_post] - {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )

    def handle_get_feed(self, msg):
        """
        피드 데이터를 전달한다.  
        """
        m_type = EnumMessageType.GET_FEED
        # 임시로 모든 피드를 불러오도록 함. 수정 필용.
        try:
            # id가 None이면 전체 post 중 랜덤으로 보냄(자신 post 포함).
            if msg["id"] is None:
                posts = self.send_query("select * from post")

            # id가 None이 아니면 해당 id의 following 계정과 자신 post를 보냄.
            else:
                # id 사용자가 팔로잉한 대상들의 id를 불러옴.
                f_res = self.send_query(f"select follower_id from follow where following_id = '{msg["id"]}'")
                
                f_list = []
                f_list.append(msg["id"])    # 자신의 id 추가

                # 팔로워 id 추가
                for f in f_res:
                    f_list.append(f[0])

                posts_res = self.send_query("select * from post")
                
                # 팔로잉한 사용자의 포스트로만 필터링
                posts = []
                for post in posts_res:
                    # 포스트 작성자 id가 follwing 리스트에 있을 때
                    if post[3] in f_list:
                        posts.append(post)

            datas = {}

            for post in posts:
                # like_cnt는 user_post_like에서 post_id가 같은 것들만 카운트
                like_res = self.send_query(f"select * from user_post_like where post_id = '{post[0]}'")

                # comment_cnt는 post 중에 parent_id가 post_id인 것들만 카운트
                comment_res = self.send_query(f"select * from post where parent_id = '{post[0]}'")

                data = MessageData.create_post_data(
                    id=post[3],
                    content=post[1],
                    like_cnt= len(like_res),
                    comment_cnt= len(comment_res),
                    writed_time=post[4],
                    image=post[2],
                    )
                datas[post[0]] = data

            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=datas
                )
        except Exception as e:
            print(f"[오류:handle_get_feed]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )
    
    def handle_get_notifi(self, msg):
        """
        
        """
        m_type = EnumMessageType.GET_NOTIFICATIONS
        try:
            res = self.send_query(f"select * from notification where user_id = '{msg["id"]}'")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=res
                )
        except Exception as e:
            print(f"[오류:handel_get_notifi]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )
        
    def handle_get_follows(self, msg):
        """
        친구 목록 요청
        - msg: create_get_follows_msg()로 생성된 메시지
        """
        m_type = EnumMessageType.GET_FOLLOWS
        try:
            res = self.send_query(f"select following_id from follow where follower_id = '{msg["id"]}'")
            
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=res
                )
        except Exception as e:
            print(f"[오류:handle_get_follows]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )
        
    def handle_get_userinfo(self, msg):
        """
        유저 정보 반환  
        - msg: create_get_userinfo_msg()로 생성된 메시지
        """
        m_type = EnumMessageType.GET_USER_INFO
        try:
            res = self.send_query(f"select * from user where user_id = '{msg["id"]}'")
            
            data = MessageData.create_userinfo_data(res[0][0], res[0][3], res[0][1], res[0][4])

            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=data
                )
        
        except Exception as e:
            print(f"[오류:handle_get_userinfo]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )
        
    def handle_add_chatroom(self, msg):
        m_type = EnumMessageType.ADD_CHAT_ROOM
        try:
            res = self.send_query(f"insert into chat_room values (null, '{msg["user_id"]}', '{msg["user_id2"]}', '{msg["chatroom_date"]}');")

            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=""
                )
        
        except Exception as e:
            print(f"[오류:handle_add_chatroom]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )
        
    def handle_get_chatroom(self, msg):
        m_type = EnumMessageType.GET_CHAT_ROOM
        try:
            query = """
            SELECT * FROM chat_room 
            WHERE (user_id = %s AND user_id2 = %s) 
            OR (user_id = %s AND user_id2 = %s);
            """
            params = (
                msg["user_id1"], 
                msg["user_id2"], 
                msg["user_id2"], 
                msg["user_id1"]
            )

            res = self.send_query_safty(query=query, param=params)

            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=""
                )
        
        except Exception as e:
            print(f"[오류:handle_add_chatroom]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )
        
    def handle_add_like(self, msg):
        m_type = EnumMessageType.ADD_LIKE
        try:
            query = """
            SELECT * FROM chat_room 
            WHERE (user_id = %s AND user_id2 = %s) 
            OR (user_id = %s AND user_id2 = %s);
            """
            params = (
                msg["user_id1"], 
                msg["user_id2"], 
                msg["user_id2"], 
                msg["user_id1"]
            )

            res = self.send_query_safty(query=query, param=params)

            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS, 
                data=""
                )
        
        except Exception as e:
            print(f"[오류:handle_add_chatroom]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED, 
                message=e
                )

    def handle_update_profile(self, msg):
        m_type = EnumMessageType.UPDATE_PROFILE

        try:
            res = self.send_query(f"insert into chat_room values (null, '{msg["user_id"]}', '{msg["chatroom_date"]}');")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.SUCCESS,
                data=""
            )

        except Exception as e:
            print(f"[오류:handle_add_chatroom]- {e}")
            return Message.create_response_msg(
                type=m_type,
                status=EnumMsgStatus.FAILED,
                message=e
            )


    @DeprecationWarning
    def send_query(self, query):
        """
        sql 인젝션 위험. param을 추가한 send_query() 사용 권장.  
        DB에 연결하여 쿼리를 전송하고, 결과값을 수신한다.
        """

        conn = pymysql.connect(
            host = self.db_address,
            port = self.db_port,
            user = self.db_user,
            password = self.db_password,
            charset = self.db_charset,
            autocommit=True,
            database = "threads_db"
        )

        cur = conn.cursor()
        print(f"\n[쿼리]: {query}")
        cur.execute(query)

        res = cur.fetchall()

        conn.close()

        print(f"[DB 결과] - {res}")
        return res
    
    def send_query_safty(self, query, param):
        """
        sql 인젝션 안전 버전  
        DB에 연결하여 쿼리를 전송하고, 결과값을 수신한다.
        """

        conn = pymysql.connect(
            host = self.db_address,
            port = self.db_port,
            user = self.db_user,
            password = self.db_password,
            charset = self.db_charset,
            autocommit=True,
            database = "threads_db"
        )

        cur = conn.cursor()
        print(f"\n[쿼리]: {query}")
        cur.execute(query, param)

        res = cur.fetchall()

        conn.close()

        print(f"[DB 결과] - {res}")
        return res
        
    def stop_server(self):
        """
        서버 종료에 필요한 절차들을 실행한다.
        """
        pass


if __name__ == "__main__":
    server = ThreadsServer()

    try:
        server.start_server()
    except Exception as e:
        print(f"[서버 종료] - {e}")
    finally:
        server.stop_server()

