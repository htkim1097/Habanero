import Config
import socket
import threading
import pymysql

class ThreadsServer:
    def __init__(self):
        self.address = Config.comm_config["address"]
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
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))

                # 메인 스레드 종료시 클라이언트 스레드도 종료되도록 데몬 스레드로 함
                client_thread.daemon = True
                client_thread.start()

            except Exception as e:
                print(f"[서버 오류] - {e}")
                break

    def handle_client(self, client_socket, address):
        """
        클라이언트 연결 관련
        """
        print(f"[클라이언트 연결] - {address}")

        try:
            while True:
                data = client_socket.recv(self.baudrate)

                if not data:
                    continue

                print(f"[데이터 송신:{address}] - {data.decode()}")

                client_socket.send(data)
        except:
            print("에러 발생")
        finally:
            client_socket.close()

    def stop_server(self):
        """
        서버 종료에 필요한 절차들을 실행한다.
        """
        pass

    def send_query(self, query):
        try:
            conn = pymysql.connect(
                host = self.db_address,
                port = self.db_port,
                user = self.db_user,
                password = self.db_password,
                charset = self.db_charset,
                database = None
            )

            cur = conn.cursor()
            cur.execute(query)

            db_data = cur.fetchall()

            res = {
                "data" : db_data
            }

            conn.commit()
            conn.close()

            data = ""
            for d in db_data:
                data += f"{d[0]},"

            return str(res).encode()
        except:
            print("send_query() 오류")
            return None


if __name__ == "__main__":
    server = ThreadsServer()

    try:
        server.start_server()
    except Exception as e:
        print(f"[서버 종료] - {e}")
    finally:
        server.stop_server()

