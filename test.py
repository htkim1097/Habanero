from header import Header
from bottom import bottom
from opening import Opening
from arealife_page import AreaLifePage
from arealife import AreaLifeBoard
from User import User
import tkinter as tk
from tkinter import ttk
import datetime
from tkcalendar import Calendar
import socket
import json

CHATTING = {} # 채팅메시지

class CarrotMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("CarrotCarrot")
        self.root.geometry("400x600")

        self.stage = 0  # 앱 실행 초기 화면 판단용 (예: 오프닝 로고)

        # 사용자 및 게시판 생성
        self.user = User(user_id="u001", nick_name="민기", area_name="서울", phone_num="010-1111-2222", temper=36.5, block_list=[], bad_count=0)
        self.board = AreaLifeBoard()

        # 상단 헤더 생성
        self.header = Header(self.root)

        # 바디 프레임 생성
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        # 오프닝 화면 처리
        if self.stage == 0:
            self.logo_view = Opening(self.body_frame)
            self.root.after(0, self.go_to_next_stage)

        # 하단 네비게이션 바 생성
        self.bottom = bottom(self.root, self.show_page)

    def go_to_next_stage(self):
        self.logo_view.destroy()
        self.show_page("홈")

    def show_page(self, name):
        # 기존 body_frame 제거 후 새로 생성
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg=self.get_page_color(name))
        # self.body_frame = tk.Frame(self.root, bg=“white") # get_page_color 함수 지우면 이거 활성화
        self.body_frame.pack(expand=True, fill="both")

        # 헤더 타이틀 변경
        self.header.update_title(name)

        # 페이지 조건별 분기
        if name == "홈":
            tk.Label(self.body_frame, text="홈 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        elif name == "동네생활":
            AreaLifePage(self.body_frame, self.board, self.user)  # 따로 pack 필요 없음 (내부에서 구현됨)

        elif name == "동네지도":
            tk.Label(self.body_frame, text="동네지도 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        elif name == "채팅":

            Chat_list(self.body_frame, self.user, self.chat_content)

        elif name == "나의당근":
            tk.Label(self.body_frame, text="나의 당근 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        else:
            tk.Label(self.body_frame, text="[오류] 페이지를 찾을 수 없습니다.", font=("Arial", 12), bg="#FFCCCC").pack(pady=20)

    def get_page_color(self, name):
        colors = {
            "홈": "#FFFFFF",
            "동네생활": "#FFFACD",
            "동네지도": "#E0FFE0",
            "채팅": "#E0F0FF",
            "나의당근": "#000000"
        }
        return colors.get(name, "#FFFFFF")

    # ☑️ 채팅방 진입 시 액자 변경
    def chat_content(self, room_info):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.header.update_title(room_info["nickname"])
        self.header.back_button(self.back_chat)

        # 채팅 페이지 진입
        Chat_page(self.body_frame, self.user, room_info)

    # ☑️ 뒤로가기 버튼 생성
    def back_chat(self):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.header.update_title("채팅 목록")
        self.header.back_button(None)

        Chat_list(self.body_frame, self.user, self.chat_content)

class Chat_page:
    def __init__(self, parent, user, room_id):
        self.parent = parent
        self.user = user
        self.room_id = room_id
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(expand=True, fill="both")

        self.room_key = str(room_id["room_id"])
        if self.room_key not in CHATTING:
            CHATTING[self.room_key] = []
        self.msgs = CHATTING[self.room_key]

        # 채팅방 진입 시 "게시물이름 채팅방"
        tk.Label(self.frame, text=f"[{room_id['title']}] 채팅방", font=("맑은 고딕", 13)).pack(pady=5)
        tk.Button(self.frame, text="약속 잡기", command = lambda : self.promise(room_id)).pack()

        self.top_frame = tk.Frame(self.frame, bg="white")
        self.top_frame.pack(fill="both", expand=True)
        self.bottom_frame = tk.Frame(self.frame, bg="white")
        self.bottom_frame.pack(fill="x")

        self.canvas = tk.Canvas(self.top_frame, bg="white", highlightthickness=0)
            # highlightthickness = 외곽선 두께

        # ☑️ 마우스 휠 함수
        def mouse_wheel(event):
            self.canvas.yview_scroll((-1 * event.delta), "units")
            # -1 없으면 스크롤이 반대로 작동
            # 현재
        self.canvas.bind_all("<MouseWheel>", mouse_wheel) # 마우스 휠 바인딩
            # bind_all() = 전체 앱에서 마우스 휠 감지할 수 있도록

        # ☑️ 스크롤바, 메시지 프레임
        self.scrollbar = ttk.Scrollbar(self.top_frame, orient="vertical", command=self.canvas.yview)
            # yview() = 세로 스크롤 연결

        self.msg_frame = tk.Frame(self.canvas, bg="white")
        self.msg_frame.bind("<Configure>",
                            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            # 캔버스는 자동으로 스크롤 범위를 계산하지 않음
            # 메시지가 늘어나면 scrollregion(스크롤가능 영역)도 수동으로 해야함
            # bind("이벤트", 함수) ... "<Configure>"은 이벤트 크기or위치 변경 시 발생
            # self.canvas.bbox("all") 의 return = (x1, y1, x2, y2)

        # ☑️ 캔버스_메시지프레임 크기 맞추기 // 보낸사람, 받은사람 좌우 배열을 위함
        def canvas_sizing(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.msg_window, width=canvas_width)

        self.canvas.bind("<Configure>", canvas_sizing)
        self.msg_window = self.canvas.create_window((0, 0), window=self.msg_frame, anchor="nw")
            # creat_window(x, y)
            # 캔버스 안에 메시지 프레임 삽입 (캔버스 스크롤 가능 영역(좌표)을 새로 설정)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
            # yscrollcommand = 스크롤될 때마다 스크롤 위치 알려줌
            # scrollbar.set = 스크롤바의 손잡이 위치와 크기를 설정 매서드

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 하단 입력창
        entry_frame = tk.Frame(self.bottom_frame, bg="white")
        entry_frame.pack(fill="x", pady=5)

        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side="left", padx=10, fill="x", expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(entry_frame, text="전송", command=self.send_message)
        self.send_button.pack(side="right", padx=10)

        # 메시지 띄우기
        self.display_message()

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            now = datetime.datetime.now().strftime("%H:%M")
            formatted_msg = {
                "sender": self.user.nick_name,
                "text": msg,
                "time": now,
            }
            # f"{self.user.nick_name}: {msg}"
            self.msgs.append(formatted_msg) # 메시지 저장🍪🍪🍪🍪
            self.display_single_message(formatted_msg)
            self.entry.delete(0, tk.END)

    def display_message(self):
        for msg in self.msgs:
            self.display_single_message(msg)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    # 약속잡기☀️☀️☀️☀️☀️
    def promise(self, room_info):
        promise_window = tk.Toplevel(self.frame)
        promise_window.title("약속잡기")
        promise_window.geometry("300x500")

        body_frame = tk.Frame(promise_window, bg="white")
        body_frame.pack(expand=True, fill="both")

        top_frame = tk.Frame(body_frame, bg="white")
        top_frame.pack(fill="x")

        # 날짜, 시간, 장소 // 약속 전 나에게 알림(x)
        nick_name = str(room_info["nickname"])
        label = tk.Label(top_frame, text=f"{nick_name}님과 약속", font=("맑은 고딕", 13, "bold"))
        label.pack(anchor="nw",padx=10, pady=10)

        date_frame = tk.Frame(body_frame, bg="white", height=60)
        time_frame = tk.Frame(body_frame, bg="white", height=60)
        location_frame = tk.Frame(body_frame, bg="white", height=60)
        calendar_frame = tk.Frame(body_frame, bg="white", height=170)
        date_frame.pack(fill="x", pady=10)
        time_frame.pack(fill="x", pady=10)
        location_frame.pack(fill="x", pady=10)
        calendar_frame.pack(fill="x",padx=10, pady=10, expand=True)

        date1 = tk.Label(date_frame, bg="white", text="날짜", font=("맑은 고딕", 11, "bold"))
        time1 = tk.Label(time_frame, bg="white", text="시간", font=("맑은 고딕", 11, "bold"))
        location1 = tk.Label(location_frame, bg="white", text="장소", font=("맑은 고딕", 11, "bold"))
        date1.pack(side="left", padx=10, pady=10)
        time1.pack(side="left", padx=10, pady=10)
        location1.pack(side="left", padx=10, pady=10)

        promise_btn = tk.Button(body_frame, bg="#FF6F0F",text="완료",font=("맑은 고딕", 12, "bold"),
                                fg="#FFFFFF", highlightthickness=0, borderwidth=0,height=2)
        promise_btn.pack(side="bottom",fill="x", pady=5)

        # 캘린더 그림 확인 변수
        calendar_view = None