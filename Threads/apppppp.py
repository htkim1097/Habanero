import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image, ImageDraw
from os import path
import socket
from Msg import Message, EnumMessageType
import Config
from copy import deepcopy
from datetime import datetime

# 영문 폰트 SF Pro text, 한글폰트 Apple SD Gothic Neo
# threadsFont = tk.font.Font(family="Apple SD Gothic Neo", size=12, weight="bold", overstrike=False)

# 이미지 경로
#img_path = path.dirname(path.abspath(__file__)) + "\\images\\"
img_path = path.dirname(path.abspath(__file__)) + "\\..\\images\\"


messages = [
    {"id": "user1",
     "feed": "동해물과 백두산이 마르고 닳도록 하나님이 보우하사 우리나라 만세 무궁화 삼천리 화려강산 대한사람 대한으로 길이 보전하세",
     "comment_cnt": "17",
     "like_cnt": "5",
     "elapsed_time": "2025-08-04 15:40:33",
     "img": img_path + "/mudo.jpg"},
    {"id": "user2",
     "feed": "파이썬파이썬파이썬",
     "comment_cnt": "5",
     "like_cnt": "3",
     "elapsed_time": "2025-06-12 12:56:33",
     "img": None},
    {"id": "user1",
     "feed": "동해물과 백두산이 마르고 닳도록 하나님이 보우하사 우리나라 만세 무궁화 삼천리 화려강산 대한사람 대한으로 길이 보전하세",
     "comment_cnt": "17",
     "like_cnt": "5",
     "elapsed_time": "2025-08-04 15:40:33",
     "img": img_path + "/mudo.jpg"},
    {"id": "user1",
     "feed": "동해물과 백두산이 마르고 닳도록 하나님이 보우하사 우리나라 만세 무궁화 삼천리 화려강산 대한사람 대한으로 길이 보전하세",
     "comment_cnt": "17",
     "like_cnt": "5",
     "elapsed_time": "2025-08-04 15:40:33",
     "img": img_path + "/mudo.jpg"},
]


class EnumMenuBar:
    HOME = 0
    MESSAGE = 1
    NEW = 2
    ACTIVITY = 3
    MY_PAGE = 4


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.windows_width = self.winfo_screenwidth()
        self.windows_height = self.winfo_screenheight()
        self.app_width = 471
        self.app_height = 954
        self.bottom_bar_height = 100  # 하단 메뉴바 높이
        self.contents_frame_height = self.app_height - self.bottom_bar_height  # 하단 메뉴 바를 제외한 크기
        self.center_x = int(self.windows_width / 2 - self.app_width / 2)
        self.center_y = int(self.windows_height / 2 - self.app_height / 2) - 25

        self.title("Threads")
        self.geometry(f"{self.app_width}x{self.app_height}+{self.center_x}+{self.center_y}")
        self.resizable(False, False)

        self.socket_family = Config.comm_config["socket_family"]
        self.socket_type = Config.comm_config["socket_type"]
        self.host = Config.comm_config["host"]
        self.port = Config.comm_config["port"]
        self.baudrate = Config.comm_config["baudrate"]

        # 메뉴 버튼의 이미지
        # TODO 활성화 버튼 추가 필요
        self.menu_home_img = ImageTk.PhotoImage(Image.open(img_path + 'home1-1.png'))
        self.w_menu_home_img = ImageTk.PhotoImage(Image.open(img_path + 'home1-2.png'))
        self.menu_msg_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png'))
        self.w_menu_msg_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-2.png'))
        self.menu_new_img = ImageTk.PhotoImage(Image.open(img_path + 'home3-1.png'))
        self.menu_act_img = ImageTk.PhotoImage(Image.open(img_path + 'home4-1.png'))
        self.w_menu_act_img = ImageTk.PhotoImage(Image.open(img_path + 'home4-2.png'))
        self.menu_my_img = ImageTk.PhotoImage(Image.open(img_path + 'home5-1.png'))
        self.w_menu_my_img = ImageTk.PhotoImage(Image.open(img_path + 'home5-2.png'))

        # 임의로 넣은 아이디. 나중에 ""으로
        self.__user_id = "ht"  # 유저 아이디

        self.frames = {}

        # Frame 등록
        self.add_frame(LoginPage, self)
        self.add_frame(JoinPage, self)
        self.add_frame(HomePage, self)
        self.add_frame(PostFeed, self)
        self.add_frame(MessagesPage, self)
        self.add_frame(MsgFriendsPage, self)
        self.add_frame(MyPage, self)
        self.add_frame(firstPage, self)
        self.add_frame(SidebarPage, self)
        self.add_frame(Following_FeedPage, self)

        # 첫 화면
        self.show_frame(LoginPage)

    def add_frame(self, Frame, parent=None):
        """
        Frame 클래스를 추가한다. parent는 frame 흐름 상의 계층적 부모를 넣어준다.
        """
        page_name = Frame.__name__
        if parent is None:
            parent = self
        frame = Frame(parent=parent, controller=self)
        self.frames[page_name] = frame
        frame.place(x=0, y=0, relwidth=1, relheight=1)

    def show_frame(self, Frame):
        """
        등록된 page_name의 frame을 화면에 띄운다.
        """
        frame = self.frames[Frame.__name__]
        frame.show_frame()

    def on_entry_click(self, entry, string):
        """
        entry 컨트롤에 string 문자열과 일치하는 내용이 있을 때 빈칸으로 만든다.
        """
        if entry.get() == string:
            entry.delete(0, tk.END)

    def on_focusout(self, entry, string):
        """
        entry의 포커스가 풀리면 string 문자열을 넣는다.
        """
        if entry.get() == "":
            entry.insert(0, string)

    # def show_error_popup(self, controller):
    #     """
    #     오류 팝업을 띄운다.
    #     """
    #     login_frame = controller.frames["LoginPage"]
    #     login_frame.error_frame.place(x=60, y=300)

    # def show_complete_popup(self, controller):
    #     """
    #     완료 팝업을 띄운다.
    #     """
    #     join_frame = controller.frames["JoinPage"]
    #     join_frame.complete_frame.place(x=60, y=300)

    def show(self):
        """
        테스트용
        """
        print("hello")

    def crop_img_circle(self, image):
        """
        이미지를 원형으로 자른다.
        """
        mask_img = Image.new('L', image.size, color="black")

        x = mask_img.width / 2
        y = mask_img.height / 2
        r = min(mask_img.width, mask_img.height)

        x1 = x - r / 2
        y1 = y - r / 2
        x2 = x + r / 2
        y2 = y + r / 2

        draw = ImageDraw.Draw(mask_img)

        draw.ellipse((x1, y1, x2, y2), fill='white', outline='white')

        image_pix = image.load()
        mask_pix = mask_img.load()
        W, H = mask_img.size

        for y in range(H):
            for x in range(W):
                value = mask_pix[x, y]
                if value == 0:
                    image_pix[x, y] = (0, 0, 0, 0)  # 투명 값 설정
        return image

    def request_db(self, msg):
        """
        DB 정보를 받기 위해 서버에 데이터를 요청한다.
        """
        client_socket = socket.socket(self.socket_family, self.socket_type)
        client_socket.connect((self.host, self.port))

        try:
            while True:
                send_data = str(msg).encode()
                client_socket.send(send_data)
                print(f"[데이터 송신] - {send_data}")

                recv_data = client_socket.recv(self.baudrate)
                print(f"[데이터 수신] - {recv_data}\n")

                return eval(recv_data.decode())
        finally:
            client_socket.close()

    def place_menu_bar(self, place_to, active_menu: int):
        """
        홈 맨 아래 아이콘들을 배치한다.
        """
        home_img = self.menu_home_img
        msg_img = self.menu_msg_img
        new_img = self.menu_new_img
        act_img = self.menu_act_img
        my_img = self.menu_my_img

        if active_menu == EnumMenuBar.HOME:
            home_img = self.w_menu_home_img
        elif active_menu == EnumMenuBar.MESSAGE:
            msg_img = self.w_menu_msg_img
        elif active_menu == EnumMenuBar.ACTIVITY:
            act_img = self.w_menu_act_img
        elif active_menu == EnumMenuBar.MY_PAGE:
            my_img = self.w_menu_my_img

        home1Btn = tk.Button(place_to, image=home_img, bd=0, background="black", activebackground="black",
                             relief="flat", highlightthickness=0, command=lambda: self.on_click_home_btn())
        home1Btn.place(x=5, y=860)

        home2Btn = tk.Button(place_to, image=msg_img, bd=0, background="black", activebackground="black", relief="flat",
                             highlightthickness=0, command=lambda: self.on_click_msg_btn())
        home2Btn.place(x=95, y=860)

        home3Btn = tk.Button(place_to, image=new_img, bd=0, background="black", activebackground="black", relief="flat",
                             highlightthickness=0, command=lambda: self.on_click_new_btn())
        home3Btn.place(x=185, y=860)

        home4Btn = tk.Button(place_to, image=act_img, bd=0, background="black", activebackground="black", relief="flat",
                             highlightthickness=0, command=lambda: self.on_click_act_btn())
        home4Btn.place(x=275, y=860)

        home5Btn = tk.Button(place_to, image=my_img, bd=0, background="black", activebackground="black", relief="flat",
                             highlightthickness=0, command=lambda: self.on_click_my_btn())
        home5Btn.place(x=365, y=860)

    def on_click_home_btn(self):
        self.show_frame(HomePage)

    def on_click_msg_btn(self):
        self.show_frame(MessagesPage)

    def on_click_new_btn(self):
        self.show_frame(PostFeed)

    def on_click_act_btn(self):
        pass

    def on_click_my_btn(self):
        self.show_frame(MyPage)

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_user_id(self):
        return self.__user_id


# 어플 실행 화면 - 시간 남으면..
class firstPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


# 로그인 화면 실행
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.bgImg = ImageTk.PhotoImage(Image.open(img_path + 'Threads.png'))
        self.pwImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.idImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.loginImg = ImageTk.PhotoImage(Image.open(img_path + 'loginBtn.png'))
        self.joinImg = ImageTk.PhotoImage(Image.open(img_path + 'join.png'))

        self.id_default_text = "사용자 아이디"
        self.pw_default_text = "비밀번호"

        # 배경을 Label을 이용하여 처리
        label = tk.Label(self, image=self.bgImg)
        label.place(x=-2, y=-2)

        # 로그인 아이디 입력
        idLabel = tk.Label(self, image=self.idImg)
        idLabel.place(x=30, y=420)

        self.idEntry = tk.Entry(self, bd=0, fg="gray")
        self.idEntry.place(x=60, y=450)
        self.idEntry.insert(0, self.id_default_text)
        self.idEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.idEntry, self.id_default_text))
        self.idEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.idEntry, self.id_default_text))
        self.idEntry.bind("<Return>", lambda e: self.process_login())

        # 로그인 비밀번호 입력
        pwLabel = tk.Label(self, image=self.pwImg)
        pwLabel.place(x=30, y=500)

        self.pwEntry = tk.Entry(self, bd=0, fg="gray")
        self.pwEntry.place(x=60, y=530)
        self.pwEntry.insert(0, self.pw_default_text)
        self.pwEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.pwEntry, self.pw_default_text))
        self.pwEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.pwEntry, self.pw_default_text))
        self.pwEntry.bind("<Return>", lambda e: self.process_login())

        # 로그인 파란색 버튼
        loginBtn = tk.Button(self, image=self.loginImg, bd=0, command=lambda: self.process_login())
        loginBtn.bind("<Return>", lambda e: self.process_login())
        loginBtn.place(x=30, y=595)

        # 회원가입
        joinBtn = tk.Button(self, image=self.joinImg, bd=0, command=lambda: controller.show_frame(JoinPage))
        joinBtn.place(x=160, y=895)

        # 로그인 에러 창
        self.error_frame = tk.Frame(self, width=350, height=180, bg="white")
        self.error_frame.place(x=60, y=400)
        self.error_frame.place_forget()

        errorImg = ImageTk.PhotoImage(Image.open(img_path + "error.png"))
        frame = tk.Label(self.error_frame, image=errorImg, bg="white")
        frame.image = errorImg
        frame.pack()

        closeImg = ImageTk.PhotoImage(Image.open(img_path + "close.png"))
        closeBtn = tk.Button(self.error_frame, image=closeImg, bd=0, command=self.hide_error)
        closeBtn.image = closeImg
        closeBtn.place(x=300, y=15)

        checkImg = ImageTk.PhotoImage(Image.open(img_path + "check.png"))
        checkBtn = tk.Button(self.error_frame, image=checkImg, bd=0, command=self.hide_error)
        checkBtn.image = checkImg
        checkBtn.place(x=280, y=130)

    def show_frame(self):
        self.tkraise()

    def hide_error(self):
        self.error_frame.place_forget()

    def process_login(self):
        """
        서버에 로그인을 요청한다.
        """
        # 로그인 메시지 생성
        user_id = self.idEntry.get()
        user_pw = self.pwEntry.get()
        msg = self.create_login_msg(user_id, user_pw)
        # 로그인 요청
        res = self.controller.request_db(msg)

        # 로그인 성공
        if res["status"]:
            self.controller.set_user_id(user_id)
            self.parent.show_frame(HomePage)
        # 로그인 실패
        else:
            # self.parent.show_error_popup(self)
            print("로그인 실패")

    def create_login_msg(self, id, password):
        """
        Entry 정보를 담은 로그인 메시지를 생성하여 반환한다.
        """
        return Message.create_login_msg(id=id, password=password)


# 회원가입 화면 실행
class JoinPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.nameImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.jidImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.jpwImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.jloginImg = ImageTk.PhotoImage(Image.open(img_path + 'joinBtn.png'))

        self.default_name_text = "사용자 이름"
        self.default_id_text = "사용자 아이디"
        self.default_pw_text = "비밀번호"

        # 배경
        label = tk.Label(self, bg="white")
        label.place(x=-2, y=-2)

        # 배경
        joinFont = tk.font.Font(family="돋움", size=25)
        jlabel = tk.Label(self, text="회원가입", font=joinFont)
        jlabel.place(x=20, y=250)

        # 회원가입 이름 입력
        nameLabel = tk.Label(self, image=self.nameImg)
        nameLabel.place(x=30, y=340)

        nameEntry = tk.Entry(self, bd=0, fg="gray")
        nameEntry.place(x=60, y=370)
        nameEntry.insert(0, self.default_name_text)
        nameEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(nameEntry, self.default_name_text))
        nameEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(nameEntry, self.default_name_text))

        # 회원가입 아이디 입력
        jidLabel = tk.Label(self, image=self.jidImg)
        jidLabel.place(x=30, y=420)
        jidEntry = tk.Entry(self, bd=0, fg="gray")
        jidEntry.place(x=60, y=450)
        jidEntry.insert(0, self.default_id_text)
        jidEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(jidEntry, self.default_id_text))
        jidEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(jidEntry, self.default_id_text))

        # 회원가입 비밀번호 입력
        jpwLabel = tk.Label(self, image=self.jpwImg)
        jpwLabel.place(x=30, y=500)
        jpwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        jpwEntry.place(x=60, y=530)
        jpwEntry.insert(0, self.default_pw_text)
        jpwEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(jpwEntry, self.default_pw_text))
        jpwEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(jpwEntry, self.default_pw_text))

        # 회원가입 파란색 버튼
        jloginBtn = tk.Button(self, image=self.jloginImg, bd=0, activebackground="black", command=self.controller.show)
        jloginBtn.place(x=68, y=850)

    def show_frame(self):
        self.tkraise()

    # 홈 화면


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLeft2.png'))
        self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLogo2.png'))
        self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path + 'homeRight2.png'))

        # 프로필 사진 받는 부분 어떻게 할지 고민,,
        self.profileimg = ImageTk.PhotoImage(Image.open(img_path + 'profileImg.png').resize((40, 40)))

        self.likeimg = ImageTk.PhotoImage(Image.open(img_path + 'like.png').resize((20, 20)))
        self.likedimg = ImageTk.PhotoImage(Image.open(img_path + 'like_red.png').resize((20, 17)))
        self.commentimg = ImageTk.PhotoImage(Image.open(img_path + 'reply.png').resize((20, 20)))
        self.repostimg = ImageTk.PhotoImage(Image.open(img_path + 'repost.png').resize((20, 20)))
        self.msgimg = ImageTk.PhotoImage(Image.open(img_path + 'msg.png').resize((20, 20)))

        # 좋아요 이미지 리스트 [빈하트, 빨간하트]
        self.like_images = [self.likeimg, self.likedimg]  # 0: 빈 하트, 1: 빨간 하트
        self.like_state = 0

        # HomePage 클래스를 배경으로 사용
        # self.home = HomePage(self, controller)
        # self.home.place(x=0, y=0, relwidth=1, relheight=1)

        # 배경
        self.configure(bg="black")

        topFrame = tk.Frame(self, bg="black")
        topFrame.place(x=0, y=0, relwidth=1)

        # 홈 맨 왼쪽 위
        homeLeftBtn = tk.Button(topFrame, image=self.homeLeftImg, bd=0, background="black", activebackground="black",
                                command=lambda: controller.show_frame(SidebarPage))
        # homeLeftBtn.place(x=5, y=0)
        homeLeftBtn.pack(side="left", padx=20, pady=35)

        # 홈 맨 위 가운데 로고
        homeLogoBtn = tk.Button(topFrame, image=self.homeLogoImg, bd=0, background="black", activebackground="black",
                                command=self.controller.show)
        homeLogoBtn.place(x=195, y=18)

        # 홈 맨 위 오른쪽
        homeRightBtn = tk.Button(topFrame, image=self.homeRightImg, bd=0, background="black", activebackground="black",
                                 command=self.controller.show)
        homeRightBtn.place(x=400, y=28)

        # 컨탠츠 프레임
        contentFrame = tk.Frame(self, bg="black")
        contentFrame.place(x=0, y=100, relwidth=1, height=self.controller.contents_frame_height - 100)

        for message in messages:
            feedItem = FeedItemFrame(
                contentFrame,
                self.profileimg,
                message,
                self.like_images,
                self.commentimg,
                self.repostimg,
                self.msgimg
            )
            feedItem.pack(fill="x", pady=(0, 5))

            # 피드 구분 회색 선
            border = tk.Frame(contentFrame, bg="#323232", height=1)
            border.pack(fill="x", pady=10)

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def show_frame(self):
        self.tkraise()

    # 마이 페이지 화면


class MyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_tab = None  # 현재 선택된 탭

        # 배경
        self.configure(bg="black")

        # 테스트용 데이터
        Message = {
            "id": "_oserra",
            "name": "세라",
            "profile_img": img_path + "/명수.png",
            "followers": 41,
            "bio": "집에 가고 싶어요"
        }
        self.name_text = Message['name']  # 이름 저장

        # 홈 화면 기본 설정
        # self.home = HomePage(self, controller)
        # self.home.place(x=0, y=0, relwidth=1, relheight=1)

        self.profile_img = ImageTk.PhotoImage(Image.open(Message['profile_img']).resize((60, 60)))

        # 상단 프로필 프레임
        FrameTop = tk.Frame(self, bg="black", height=240)
        FrameTop.pack(side="top", fill="x")

        name_label = tk.Label(FrameTop, text=f"{Message['name']}", fg="white", bg="black", font=("Arial", 22, 'bold'))
        name_label.place(x=30, y=140)

        self.edit_nameImg = ImageTk.PhotoImage(Image.open(img_path + 'edit_name.png').resize((13, 13)))
        edit_nameBtn = tk.Button(FrameTop, image=self.edit_nameImg, bd=0, background="black", relief="flat",
                                 highlightthickness=0, activebackground="black", command=self.controller.show)
        edit_nameBtn.place(x=95, y=160)

        self.id_label = tk.Label(FrameTop, text=f"{Message['id']}", fg="white", bg="black", font=("Arial", 12))
        self.id_label.place(x=30, y=180)

        follows_cnt_label = tk.Label(FrameTop, text=f"{Message['followers']}" + 'followers', fg="gray", bg="black",
                                     font=("Arial", 11))
        follows_cnt_label.place(x=30, y=215)

        profile_label = tk.Label(FrameTop, image=self.profile_img, fg="white", bg="black")
        profile_label.place(x=380, y=110)  # 데이터 값 가져오기

        self.edit_profileImg = ImageTk.PhotoImage(Image.open(img_path + 'edit_profile.png').resize((20, 20)))
        edit_profileBtn = tk.Button(FrameTop, image=self.edit_profileImg, bd=0, background="black", relief="flat",
                                    highlightthickness=0, activebackground="black", command=self.controller.show)
        edit_profileBtn.place(x=442, y=155)  # 임시 위치 # 파일 선택 창 띄우기

        self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path + 'homeRight2.png'))
        homeRightBtn = tk.Button(FrameTop, image=self.homeRightImg, bd=0, background="black", relief="flat",
                                 highlightthickness=0, activebackground="black", command=self.controller.show)
        homeRightBtn.place(x=400, y=28)

        # 탭 프레임(버튼 배치)
        FrameTabs = tk.Frame(self, bg="black", height=50)
        FrameTabs.pack(side="top", fill="x")

        self.mp1Img = ImageTk.PhotoImage(Image.open(img_path + 'mp1.png'))
        self.mp1Btn = tk.Button(FrameTabs, image=self.mp1Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Threads"))
        self.mp1Btn.place(x=20, y=0)

        self.mp2Img = ImageTk.PhotoImage(Image.open(img_path + 'mp2.png'))
        self.mp2Btn = tk.Button(FrameTabs, image=self.mp2Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Replies"))
        self.mp2Btn.place(x=140, y=0)

        self.mp3Img = ImageTk.PhotoImage(Image.open(img_path + 'mp3.png'))
        self.mp3Btn = tk.Button(FrameTabs, image=self.mp3Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Media"))
        self.mp3Btn.place(x=240, y=0)

        self.mp4Img = ImageTk.PhotoImage(Image.open(img_path + 'mp4.png'))
        self.mp4Btn = tk.Button(FrameTabs, image=self.mp4Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Reposts"))
        self.mp4Btn.place(x=340, y=0)

        lineFrame = tk.Frame(FrameTabs, bg="#666768")
        lineFrame.pack(fill="x", pady=(50, 0))

        # 탭 별 프레임 생성
        self.FrameContent = tk.Frame(self, bg="black", height=450)
        self.FrameContent.pack(side="top", fill="x")

        # def edit_name(self):
        #     self.name_label.place.forget()
        #     self.edit_nameImg.place.forget()
        #
        #     self.name_entry = tk.Entry(self.FrameTop, font=("Arial", 22, 'bold'))
        #     self.name.insert(0, self.name_entry.get())
        #     self.name_entry.place(x=30, y=140)
        #
        #     #이름 변경 확인 버튼
        #     self.confirm_nameBtn = tk.Button(self.FrameTop, text="확인", command=self.save_name)
        #     self.confirm_nameBtn.place(x=200, y=140)
        #
        # def save_name(self):
        #     new_name = self.name_entry.get()
        #     self.name_text = new_name
        #     self.name_label.place(x=30, y=140)
        #     self.edit_nameBtn.place(x=95, y=160)

        # 게시글 없을 시 프레임에 나타나는 메시지
        frame_messages = {
            "Threads": "You haven’t posted any threads yet.",
            "Replies": "You haven’t posted any replies yet.",
            "Media": "You haven’t posted any media yet.",
            "Reposts": "You haven’t reposted any threads yet."
        }

        self.frames = {}

        for name in ["Threads", "Replies", "Media", "Reposts"]:
            frame = tk.Frame(self.FrameContent, bd=0, relief="flat", highlightthickness=0, bg="black")
            frame.place(x=0, y=0, relwidth=1, relheight=1)

            # 메시지 라벨
            label = tk.Label(frame, text=frame_messages[name], fg="gray", bg="black", font=("Arial", 12))
            label.pack(pady=200)

            self.frames[name] = frame

        # 탭 선택 시 변경된 이미지
        self.Cgmp1Img = ImageTk.PhotoImage(Image.open(img_path + 'Cgmp1.png'))
        self.Cgmp2Img = ImageTk.PhotoImage(Image.open(img_path + 'Cgmp2.png'))
        self.Cgmp3Img = ImageTk.PhotoImage(Image.open(img_path + 'Cgmp3.png'))
        self.Cgmp4Img = ImageTk.PhotoImage(Image.open(img_path + 'Cgmp4.png'))

        self.tab_images = {
            "Threads": [self.mp1Img, self.Cgmp1Img],
            "Replies": [self.mp2Img, self.Cgmp2Img],
            "Media": [self.mp3Img, self.Cgmp3Img],
            "Reposts": [self.mp4Img, self.Cgmp4Img]
        }

        self.tab_buttons = {
            "Threads": self.mp1Btn,
            "Replies": self.mp2Btn,
            "Media": self.mp3Btn,
            "Reposts": self.mp4Btn
        }

        self.switch_tabs("Threads")  # 기본 프레임 설정

        controller.place_menu_bar(self, EnumMenuBar.MY_PAGE)

    # 탭 전환 시 버튼 이미지 전환
    def switch_tabs(self, tab_name):
        self.show_sub_frame(tab_name)

        for name, btn in self.tab_buttons.items():
            if name == tab_name:
                btn.config(image=self.tab_images[name][1])  # 현재 선택된 이미지
            else:
                btn.config(image=self.tab_images[name][0])  # 원래 이미지

        self.current_tab = tab_name

    # 프레임 전환
    def show_sub_frame(self, frames_name):
        for name, frame in self.frames.items():
            frame.lower()  # 프레임 숨기기(맨 아래로 이동)
        self.frames[frames_name].lift()  # 프레임 나타내기

    # 프로필 수정 버튼 누르기
    # def click_btn(self):

    def show_frame(self):
        self.tkraise()

    # following 피드 화면


class Following_FeedPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # # HomePage 클래스를 배경으로 사용
        # self.home = HomePage(self, controller)
        # self.home.place(x=0, y=0, relwidth=1, relheight=1)

        topFrame = tk.Frame(self, bg="black")
        topFrame.place(x=0, y=0, relwidth=1)

        self.configure(bg="black")

        # 홈 맨 왼쪽 위 back 버튼
        self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'backBtn.png').resize((70, 25)))
        homeLeftBtn = tk.Button(topFrame, image=self.homeLeftImg, bd=0, background="black", activebackground="black",
                                command=lambda: controller.show_frame(HomePage))
        homeLeftBtn.pack(side="left", padx=10, pady=30)

        # 홈 맨 위 가운데 floowing
        self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'followingBtn.png').resize((140, 35)))
        followingBtn = tk.Button(topFrame, image=self.homeLogoImg, bd=0, background="black", activebackground="black",
                                 command=self.controller.show)
        followingBtn.place(x=167, y=23)

        # 상단 UI 높이 만큼 패딩
        contentFrame = tk.Frame(self, bg="black")
        contentFrame.place(x=0, y=70, relwidth=1, height=self.controller.contents_frame_height - 70)

        lineFrame = tk.Frame(contentFrame, bg="#323232")
        lineFrame.pack(fill="x", pady=10)

        # 프로필 사진 받는 부분 어떻게 할지 고민,,
        self.profileimg = ImageTk.PhotoImage(Image.open(img_path + 'profileImg.png').resize((40, 40)))

        self.commentimg = ImageTk.PhotoImage(Image.open(img_path + 'reply.png').resize((20, 20)))
        self.likeimg = ImageTk.PhotoImage(Image.open(img_path + 'like.png').resize((20, 20)))
        self.likedimg = ImageTk.PhotoImage(Image.open(img_path + 'like_red.png').resize((20, 17)))
        self.repostimg = ImageTk.PhotoImage(Image.open(img_path + 'repost.png').resize((20, 20)))
        self.msgimg = ImageTk.PhotoImage(Image.open(img_path + 'msg.png').resize((20, 20)))

        # 좋아요 버튼(빈 하트, 빨간 하트)
        self.like_images = [self.likeimg, self.likedimg]  # 0: 빈 하트, 1: 빨간 하트
        self.like_state = 0

        for message in messages:
            feedItem = FeedItemFrame(
                contentFrame,
                self.profileimg,
                message,
                self.like_images,
                self.commentimg,
                self.repostimg,
                self.msgimg
            )
            feedItem.pack(fill="x", pady=(0, 5))

            # 피드 구분 회색 선
            border = tk.Frame(contentFrame, bg="#323232", height=1)
            border.pack(fill="x", pady=10)

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def show_frame(self):
        self.tkraise()

    # 각 게시글


class FeedItemFrame(tk.Frame):
    def __init__(self, parent, profile_img, message, like_images, comment_img, repost_img, msg_img):
        super().__init__(parent, bg="black")
        self.controller = parent

        self.like_state = 0
        self.like_images = like_images
        self.commentimg = comment_img
        self.repostimg = repost_img
        self.msgimg = msg_img

        # 왼쪽-오른쪽 구조
        leftFrame = tk.Frame(self, bg="black", width=50)
        leftFrame.pack(side="left", anchor="n", padx=10)

        rightFrame = tk.Frame(self, bg="black")
        rightFrame.pack(side="left", fill="x")

        imgLabel = tk.Label(leftFrame, image=profile_img, bg="black")
        imgLabel.pack(anchor="n")

        contentArea = tk.Frame(rightFrame, bg="black")
        contentArea.pack(fill="x", anchor="w")

        # 아이디 + 시간
        topInfo = tk.Frame(contentArea, bg="black")
        topInfo.pack(anchor="w", pady=(0, 2))

        idLabel = tk.Label(topInfo, text=message["id"], fg="white", bg="black", font=("Arial", 11))
        idLabel.pack(side="left")

        # 시간 계산
        post_time = datetime.strptime(message["elapsed_time"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - post_time
        if diff.days >= 1:
            postTime = f"{diff.days} day ago"
        elif diff.seconds >= 3600:
            postTime = f"{diff.seconds // 3600}h"
        elif diff.seconds >= 60:
            postTime = f"{diff.seconds // 60}m"
        else:
            postTime = f"{diff.seconds}s"

        timeLabel = tk.Label(topInfo, text=postTime, fg="gray", bg="black", font=("Arial", 9))
        timeLabel.pack(side="left", padx=(8, 0))

        # 게시글 내용
        feedLabel = tk.Label(contentArea, text=message["feed"], fg="white", bg="black",
                             wraplength=400, justify="left", font=("맑은고딕", 11))
        feedLabel.pack(anchor="w", pady=(0, 10))

        # 게시글 이미지
        if message["img"]:
            self.post_img = ImageTk.PhotoImage(Image.open(message["img"]).resize((300, 300)))
            imgLabel = tk.Label(contentArea, image=self.post_img, bg="white")
            imgLabel.pack(anchor="w", pady=(0, 10))

        # 버튼 영역(좋아요, 댓글, 리포스트, 공유 버튼)
        btnFrame = tk.Frame(rightFrame, bg="black")
        btnFrame.pack(anchor="w", pady=(0, 5))

        self.likeBtn = tk.Button(btnFrame, image=self.like_images[self.like_state], bd=0, background="black",
                                 activebackground="black", command=self.toggle_like)
        self.likeBtn.pack(side="left")

        likeCnt = tk.Label(btnFrame, text=message["like_cnt"], fg="white", bg="black")
        likeCnt.pack(side="left", padx=(2, 20))

        commentBtn = tk.Button(btnFrame, image=self.commentimg, bd=0, background="black",
                               activebackground="black", command=self.show)
        commentBtn.pack(side="left")
        commentCnt = tk.Label(btnFrame, text=message["comment_cnt"], fg="white", bg="black")
        commentCnt.pack(side="left", padx=(2, 15))

        repostBtn = tk.Button(btnFrame, image=self.repostimg, bd=0, background="black",
                              activebackground="black", command=self.show)
        repostBtn.pack(side="left", padx=(0, 20))

        msgBtn = tk.Button(btnFrame, image=self.msgimg, bd=0, background="black",
                           activebackground="black", command=self.show)
        msgBtn.pack(side="left")

    def toggle_like(self):
        self.like_state = 1 - self.like_state
        self.likeBtn.config(image=self.like_images[self.like_state])

    def show(self):
        print("hi")

    def show_frame(self):
        self.tkraise()

    # Feeds 사이드바


class SidebarPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="black")

        self.feeds1img = ImageTk.PhotoImage(Image.open(img_path + 'forYou.png'))
        self.feeds2img = ImageTk.PhotoImage(Image.open(img_path + 'following.png'))

        sideFrame = tk.Frame(self, bg="black", width=350)
        sideFrame.pack(side="left", fill="y")

        label1 = tk.Label(sideFrame, text="Feeds", fg="white", bg="black", font=("Arial", 23, "bold"))
        label1.place(x="20", y="30")

        foryouBtn = tk.Button(sideFrame, image=self.feeds1img, bd=0, bg="black", activebackground="black",
                              command=lambda: controller.show_frame(HomePage))
        foryouBtn.place(x="20", y="105")

        followingBtn = tk.Button(sideFrame, image=self.feeds2img, bd=0, bg="black", activebackground="black",
                                 command=lambda: controller.show_frame(Following_FeedPage))
        followingBtn.place(x="20", y="180")

    def show_frame(self):
        self.tkraise()

    # 게시물 작성 페이지


# class PostFeed(tk.Frame):
#     def __init__(self, parent, controller, message):
#         super().__init__(parent)
#         self.controller = controller
#
#         self.configure(bg="black")
#
#         topFrame = tk.Frame(self, bg="black")
#         topFrame.pack(side="top", fill="x")
#
#         self.cancelImg = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png').resize((60, 20)))
#         cancelBtnl = tk.Button(topFrame, image=self.cancelImg, bd=0, bg="black", activebackground="black", command=lambda: controller.show_frame("ForYou_FeedPage"))
#         cancelBtnl.pack(anchor="w", padx=20, pady=(30,10))
#
#         self.newPostImg = ImageTk.PhotoImage(Image.open(img_path + 'newPost.png').resize((125, 30)))
#         newPostLabel = tk.Label(topFrame, image=self.newPostImg, bd=0, bg="black")
#         newPostLabel.place(x="175", y="23")
#
#         # 구분 회색 선
#         border = tk.Frame(topFrame, bg="#323232", height=1)
#         border.pack(fill="x", pady=10)
#
#         self.profileimg = ImageTk.PhotoImage(Image.open(img_path + 'profileImg.png').resize((40, 40)))

# # 왼쪽-오른쪽 구조
# leftFrame = tk.Frame(self, bg="black", width=50)
# leftFrame.pack(side="left", anchor="n", padx=10)
#
# rightFrame = tk.Frame(self, bg="black")
# rightFrame.pack(side="left", fill="x")
#
# imgLabel = tk.Label(leftFrame, image=self.profileimg, bg="black")
# imgLabel.pack(anchor="n", padx=10, pady=10)
#
# idLabel = tk.Label(rightFrame, text=message["id"], fg="white", bg="black", font=("Arial", 11))
# idLabel.pack(side="left")
#
# contentArea = tk.Frame(rightFrame, bg="black")
# contentArea.pack(fill="x", anchor="w")

# 메시지 페이지
class MessagesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.messages_text_img = ImageTk.PhotoImage(Image.open(img_path + 'messagesText.png'))
        self.add_chat_room_img = ImageTk.PhotoImage(Image.open(img_path + 'addChatRoom.png'))
        self.search_box_img = ImageTk.PhotoImage(Image.open(img_path + 'searchBox.png').resize((471, 70)))
        self.dotdotdot_logo = ImageTk.PhotoImage(Image.open(img_path + 'dotdotdot.png'))
        self.no_chat_room_message_img = ImageTk.PhotoImage(Image.open(img_path + 'emptyChatRoom.png'))
        self.message_btn_img = ImageTk.PhotoImage(Image.open(img_path + 'newMessages.png'))

        # 배경
        self.configure(bg="black")

        # Messages 문구
        messages_text_btn = tk.Button(self, image=self.messages_text_img, bd=0, background="black",
                                      activebackground="black", highlightthickness=0, command=self.controller.show)
        messages_text_btn.place(x=20, y=30)

        # 채팅 방 추가
        add_chat_room_btn = tk.Button(self, image=self.add_chat_room_img, bd=0, background="black",
                                      activebackground="black", relief="flat", highlightthickness=0,
                                      command=lambda: self.controller.show_frame(MsgFriendsPage))
        add_chat_room_btn.place(x=420, y=30)

        # 검색
        search_box = tk.Label(self, image=self.search_box_img, borderwidth=0)
        search_box.place(x=0, y=80)
        search_box_font = tk.font.Font(size=14)
        search_entry = tk.Entry(self, bd=0, fg="gray", background="#1e1e1e", font=search_box_font)
        search_entry.place(x=55, y=108, width=370)
        search_entry.insert(0, "Search")
        search_entry.bind('<Button-1>', lambda e: self.controller.on_entry_click(search_entry, "Search"))
        search_entry.bind('<FocusOut>', lambda e: self.controller.on_focusout(search_entry, "Search"))

        # ...
        dot3_logo = tk.Label(self, image=self.dotdotdot_logo, bd=0, highlightthickness=0, background="black",
                             borderwidth=0)
        dot3_logo.place(x=185, y=300)
        # 최대 7개의 친구 사진을 가져와서 디자인 배치

        # 채팅 방이 없을 때 문구
        if True:
            no_chat_room_message = tk.Label(self, image=self.no_chat_room_message_img, bd=0, highlightthickness=0,
                                            background="black", borderwidth=0)
            no_chat_room_message.place(x=55, y=500)
        else:
            pass

        # 메시지 추가 버튼
        new_message_btn = tk.Button(self, image=self.message_btn_img, activebackground="black", bd=0,
                                    background="black", relief="flat", highlightthickness=0,
                                    command=lambda: self.controller.show_frame(MsgFriendsPage))
        new_message_btn.place(x=180, y=580)

        controller.place_menu_bar(self, EnumMenuBar.MESSAGE)

    def show_frame(self):
        self.tkraise()

    # 메시지 친구 목록 페이지


class MsgFriendsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.cancel_img = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png'))
        self.new_message_text_img = ImageTk.PhotoImage(Image.open(img_path + 'newMessageText.png'))
        self.to_suggested_text_img = ImageTk.PhotoImage(Image.open(img_path + 'toSuggested.png'))

        # 배경
        self.configure(bg="black")

        # cencel 버튼
        cencel_btn = tk.Button(self, image=self.cancel_img, bd=0, background="black", activebackground="black",
                               highlightthickness=0, command=lambda: self.on_click_cancel())
        cencel_btn.place(x=20, y=50)

        # New message 문구
        new_message_text = tk.Label(self, image=self.new_message_text_img, bd=0, highlightthickness=0,
                                    background="black", borderwidth=0)
        new_message_text.place(x=170, y=50)

        # To: Suggested 문구
        to_suggested_text = tk.Label(self, image=self.to_suggested_text_img, bd=0, highlightthickness=0,
                                     background="black", borderwidth=0)
        to_suggested_text.place(x=0, y=90)

        # 친구 목록
        self.list_frame = tk.Frame(self)
        self.list_frame.place(x=0, y=200, width=self.controller.app_width,
                              height=self.controller.contents_frame_height - 200)

        self.canvas = tk.Canvas(self.list_frame, bg="black", highlightthickness=0)

        self.scrollable_frame = tk.Frame(self.canvas, bg="black")
        self.scrollable_frame.config(height=300)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))

        # 캔버스에 스크롤 가능한 프레임 넣기
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self.on_configure)
        self.canvas.pack(side="left", fill="both", expand=True)

        controller.place_menu_bar(self, EnumMenuBar.MESSAGE)

    def on_configure(self, event):
        """
        스크롤바의 크기를 동적으로 맞추기 위한 설정.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_frame(self):
        self.tkraise()
        self.load_friends()

    def on_click_cancel(self):
        self.controller.show_frame(MessagesPage)

    def load_friends(self):
        msg = Message.create_get_follows_msg(self.controller.get_user_id())
        res = self.controller.request_db(msg)

        for friend in res["data"]:
            msg = Message.create_get_userinfo_msg(friend[0])
            friend_infos = self.controller.request_db(msg)
            data = friend_infos["data"]

            frame = self.create_friend_item(self.scrollable_frame, data["id"], data["name"], data["profile_img"])
            self.bind_mousewheel_recursive(frame)

    def on_click(self, parent, frame):
        for child in parent.winfo_children():
            child.configure(bg="white")
        frame.configure(bg="#e0f0ff")

    def create_friend_item(self, parent, id, name, profile_img):
        frame = tk.Frame(parent, bg="#1e1e1e", bd=0, relief="solid")

        frame.bind("<Button-1>", lambda e: self.on_click(parent, frame))

        try:
            img = Image.open(profile_img).resize((40, 40))
        except:
            img = Image.new("RGB", (40, 40), color="gray")  # 이미지 불러오기 실패 시 회색 대체

        croped_img = self.controller.crop_img_circle(img)
        photo = ImageTk.PhotoImage(croped_img)
        image_label = tk.Label(frame, image=photo, bg="#1e1e1e")
        image_label.image = photo
        image_label.pack(side="left", padx=10, pady=5)

        text_frame = tk.Frame(frame, bg="#1e1e1e")
        name_label = tk.Label(text_frame, text=id, fg="white", font=("Arial", 12, "bold"), anchor="w", bg="#1e1e1e",
                              width=39)
        status_label = tk.Label(text_frame, text=name, font=("Arial", 10), anchor="w", bg="#1e1e1e", fg="gray")

        name_label.pack(anchor="w", expand=True)
        status_label.pack(anchor="w")
        text_frame.pack(side="left", fill="x", expand=True)

        frame.pack(fill="x", pady=2, padx=5)
        return frame

    def bind_mousewheel_recursive(self, widget):
        widget.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        widget.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)

    def on_mousewheel_event(self, event):
        self.canvas.yview_scroll(int((event.delta / 120)), "units")





#게시물 작성 페이지
class PostFeed(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="black")

        topFrame = tk.Frame(self, bg="black")
        topFrame.pack(side="top", fill="x")

        self.cancelImg = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png').resize((60, 20)))
        cancelBtnl = tk.Button(topFrame, image=self.cancelImg, bd=0, bg="black", activebackground="black", command=lambda: controller.show_frame("ForYou_FeedPage"))
        cancelBtnl.pack(anchor="w", padx=20, pady=(30,10))

        self.newPostImg = ImageTk.PhotoImage(Image.open(img_path + 'newPost.png').resize((125, 30)))
        newPostLabel = tk.Label(topFrame, image=self.newPostImg, bd=0, bg="black")
        newPostLabel.place(x="175", y="23")

        # 구분 회색 선
        border = tk.Frame(topFrame, bg="#323232", height=1)
        border.pack(fill="x", pady=10)

        containerFrame = tk.Frame(self, bg="black")
        containerFrame.pack(side="top", anchor="w", padx=10, pady=10)  # 전체 묶는 프레임

        # 왼쪽: 프로필 사진, 오른쪽: 아이디 + 게시글 구조
        leftFrame = tk.Frame(containerFrame, bg="black", width=50)
        leftFrame.pack(side="left", anchor="n", padx=10)

        rightFrame = tk.Frame(containerFrame, bg="black")
        rightFrame.pack(side="left", fill="x")

        self.img = Image.open(messages[0]["img"]).resize((40, 40))
        self.circleImg = self.controller.crop_img_circle(self.img)

        self.profileimg = ImageTk.PhotoImage(self.circleImg)
        imgLabel = tk.Label(leftFrame, image=self.profileimg, bg="black")
        imgLabel.pack(anchor="n", padx=10, pady=10)

        contentArea = tk.Frame(rightFrame, bg="black")
        contentArea.pack(fill="x", anchor="w")

        # 아이디
        topInfo = tk.Frame(contentArea, bg="black")
        topInfo.pack(anchor="w", pady=(0, 2))

        idLabel = tk.Label(topInfo, text=messages[0]["id"], fg="white", bg="black", font=("Arial", 11))
        idLabel.pack(side="left")

        # 게시글 작성
        textEntry = tk.Entry(contentArea,bd=0, bg="black", fg="gray")
        textEntry.pack(side="left")
        textEntry.insert(0, "What's new?")
        textEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(textEntry, "What's new?"))
        textEntry.bind('<FocusOut>', lambda e:  self.controller.on_focusout(textEntry, "What's new?"))

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def show_frame(self):
        self.tkraise()


# ==== 실행 ====
if __name__ == "__main__":
    app = App()
    app.mainloop()