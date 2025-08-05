import socket
import threading
import time
from Config import comm_config, db_config
from copy import deepcopy
from Msg import *
import datetime

def test():
    print("[테스트] - 클라이언트 테스트 시작")

    # 서버 연결 테스트
    try:
        client = socket.socket(comm_config["socket_family"], comm_config["socket_type"])
        client.connect((comm_config["host"], comm_config["port"]))
        print("[테스트] - 서버 연결 성공")
    except Exception as e:
        print(f"[테스트] - 오류: {e}")
        return

    # 회원가입 테스트
    msg = Message.create_register_msg(id="ht", password="123qwe", email="ht@gmail.com", name="kim")
    
    client.send(str(msg).encode())
    #print(f"[데이터 송신] - {send_data}")

    register_res = eval(client.recv(comm_config["baudrate"]).decode())
    #print(f"[데이터 수신] - {recv_data}")

    if register_res is not None and register_res["type"] == EnumMessageType.REGISTER and register_res["status"] == EnumMsgStatus.SUCCESS:
        print("[회원가입 테스트] - 회원가입 성공")
    else:
        print(f"[회원가입 테스트] - 회원가입 실패 : {register_res['message']}")

    # 로그인 테스트
    msg = Message.create_login_msg(id="ht", password="123qwe")

    client.send(str(msg).encode())
    #print(f"[데이터 송신] - {send_data}")

    login_res = eval(client.recv(comm_config["baudrate"]).decode())
    #print(f"[데이터 수신] - {recv_data}")

    if login_res is not None and login_res["type"] == EnumMessageType.LOGIN and login_res["status"] == EnumMsgStatus.SUCCESS:
        print("[로그인 테스트] - 로그인 성공")
    else:
        print(f"[로그인 테스트] - 로그인 실패 : {login_res['message']}")
        client.close()
        return

    # 게시물 작성 테스트
    msg = Message.create_post_msg(id="ht", parent_id=None, post_time=datetime.datetime.now(), content="게시글 작성 테스트!", location=None)

    client.send(str(msg).encode())
    #print(f"[데이터 송신] - {send_data}")

    post_res = eval(client.recv(comm_config["baudrate"]).decode())
    #print(f"[데이터 수신] - {recv_data}")

    if post_res is not None and post_res["type"] == EnumMessageType.POST and post_res["status"] == EnumMsgStatus.SUCCESS:
        print("[Post 테스트] - 게시글 작성 성공")
    else:
        print(f"[Post 테스트] - 게시글 작성 실패 : {post_res['message']}")

    # 피드 조회 테스트
    msg = Message.create_get_feed_msg(id="ht")

    client.send(str(msg).encode())
    #print(f"[데이터 송신] - {send_data}")

    feed_res = eval(client.recv(comm_config["baudrate"]).decode())
    #print(f"[데이터 수신] - {recv_data}")

    if feed_res is not None and feed_res["type"] == EnumMessageType.GET_FEED and feed_res["status"] == EnumMsgStatus.SUCCESS:
        print(f"[Feed 테스트] - 피드 조회 성공: {len(feed_res["posts"])} 개의 게시물 조회 됨.")
        if feed_res["posts"]:
            print(feed_res["posts"][0])
    else:
        print(f"[Feed 테스트] - 피드 조회 실패 : {feed_res['message']}")

    # 알림 조회 테스트
    msg = Message.create_get_notif_msg(id="ht")

    client.send(str(msg).encode())
    #print(f"[데이터 송신] - {send_data}")

    notif_res = eval(client.recv(comm_config["baudrate"]).decode())
    #print(f"[데이터 수신] - {recv_data}")

    if notif_res is not None and notif_res["type"] == EnumMessageType.GET_NOTIFICATIONS and notif_res["status"] == EnumMsgStatus.SUCCESS:
        print(f"[알림 테스트] - 알림 조회 성공: {len(notif_res["notifications"])} 개의 알림.")
    else:
        print(f"[알림 테스트] - 알림 조회 실패 : {notif_res['message']}")

    client.close()
    
    print("\n[테스트] - 기능 테스트 종료")

if __name__ == "__main__":
    test()
