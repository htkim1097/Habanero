import Config
import socket
import threading
import pymysql
from Msg import message, MessageType
import copy

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

                client_socket.send(str(res).encode())
        except Exception as e:
            print(f"[오류:handle_client] - {e}")
        finally:
            client_socket.close()

    def handle_data(self, data):
        d_type = int(data["type"])

        try:
            if d_type == MessageType.LOGIN:
                self.handle_login(data)
            elif d_type == MessageType.REGISTER:
                self.handle_register(data)
            else:
                raise Exception("data type 오류: 클라이언트로부터 받은 데이터의 type 값에 오류가 있습니다.")
            
        except Exception as e:
            print(f"[오류:handle_data] - {e}")

    def handle_login(self, data):
        """
        로그인 정보를 확인하여 
        """
        return self.send_query(f"SELECT * FROM user WHERE user_id = '{data["id"]}' AND password = '{data["password"]}';")

    def handle_register(self, data):
        """
        회원가입에서 입력한 값들로 user 테이블에 데이터를 추가한다. 
        """
        return self.send_query(f"INSERT INTO user VALUES ('{data["id"]}', '{data["email"]}', '{data["password"]}', '{data["name"]}', '{data["profile_image"]}');")

    def send_query(self, query):
        """
        DB에 연결하여 쿼리를 전송하고, 결과값을 수신한다.
        """
        try:
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
        except Exception as e:
            print(f"[오류:send_query] - {e}")
            return None
        
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

