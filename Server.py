import Config
import socket
import threading
import pymysql
from Msg import *
import copy
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
        print(f"[클라이언트 연결] - {address}")

        try:
            while True:
                data = client_socket.recv(baudrate)

                if not data:
                    break

                en_data = data.decode()
                print(f"[데이터 수신 {address}] - {en_data}")

                repr_data = eval(en_data)

                res = self.handle_data(repr_data)
                print(f"[데이터 송신 {address}] - {res}")

                client_socket.send(str(res).encode())
        except Exception as e:
            print(f"[오류:handle_client] - {e}")
        finally:
            client_socket.close()

    def handle_data(self, data):
        d_type = int(data["type"])

        try:
            if d_type == MessageType.LOGIN:
                return self.handle_login(data)
            elif d_type == MessageType.REGISTER:
                return self.handle_register(data)
            elif d_type == MessageType.POST:
                return self.handle_post(data)
            elif d_type == MessageType.GET_FEED:
                return self.handle_get_feed(data)
            elif d_type == MessageType.GET_NOTIFICATIONS:
                return self.handel_get_notifi(data)
            else:
                raise Exception("[오류:handle_data] - 클라이언트로부터 받은 데이터의 type 값에 오류가 있습니다.")
            
        except Exception as e:
            print(f"[오류:handle_data] - {e}")

    def handle_login(self, data):
        """
        로그인 정보를 확인하여 
        """
        res = self.send_query(f"SELECT * FROM user WHERE user_id = '{data["id"]}' AND password = '{data["password"]}';")
         
        if (len(res) > 0):
            return Message.create_login_res_msg(MessageStatusType.SUCCESS)
        else:
            return Message.create_login_res_msg(MessageStatusType.FAILED)

    def handle_register(self, data):
        """
        회원가입에서 입력한 값들로 user 테이블에 데이터를 추가한다. 
        """
        try:
            if (len(self.send_query(f"select * from user where user_id = '{data["id"]}';")) > 0):
                return Message.create_register_res_msg( MessageStatusType.FAILED, "입력한 아이디가 이미 있습니다.")
            else:
                self.send_query(f"INSERT INTO user VALUES ('{data["id"]}', '{data["email"]}', '{data["password"]}', '{data["name"]}', '{data["profile_image"]}');")
                res = self.send_query(f"select * from user where user_id = '{data["id"]}';")

                if (len(res) > 0):
                    return Message.create_register_res_msg(MessageStatusType.SUCCESS)
                else:
                    return Message.create_register_res_msg(MessageStatusType.FAILED, "조회 실패")
                
        except Exception as e:
            print(f"[오류:handle_register] - {e}")
            return Message.create_register_res_msg(MessageStatusType.FAILED, message=e)

    def handle_post(self, data):
        try:
            if data['parent_id'] is None:
                res = self.send_query(f"INSERT INTO post VALUES (null, '{data["content"]}', '{data["location"]}', '{data["id"]}', '{data["post_time"]}', null);")            
            else:
                res = self.send_query(f"INSERT INTO post VALUES (null, '{data["content"]}', '{data["location"]}', '{data["id"]}', '{data["post_time"]}', '{data["parent_id"]}');")
            return Message.create_post_res_msg(status=MessageStatusType.SUCCESS)
        except Exception as e:
            print(f"[오류:handle_post] - {e}")
            return Message.create_post_res_msg(status=MessageStatusType.FAILED, message=e)

    def handle_get_feed(self, data):
        try:
            res = self.send_query(f"select * from post")
            return Message.create_get_feed_res_msg(status=MessageStatusType.SUCCESS, posts=res)
        except Exception as e:
            print(f"[오류:handle_get_feed]- {e}")
            return Message.create_get_feed_res_msg(status=MessageStatusType.FAILED, message=e)
    
    def handel_get_notifi(self, data):
        try:
            res = self.send_query(f"select * from notification where user_id = '{data["id"]}'")
            return Message.create_notif_res_msg(status=MessageStatusType.SUCCESS, notifications=res)
        except Exception as e:
            print(f"[오류:handel_get_notifi]- {e}")
            return Message.create_notif_res_msg(status=MessageStatusType.FAILED, message=e)

    def send_query(self, query):
        """
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
        cur.execute(query)

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

