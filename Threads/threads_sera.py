import tkinter as tk
from tkinter import ttk, font, filedialog
from PIL import ImageTk, Image, ImageDraw
from os import path
import socket
from Msg import *
import Config
import datetime

# 영문 폰트 SF Pro text, 한글폰트 Apple SD Gothic Neo
# threadsFont = tk.font.Font(family="Apple SD Gothic Neo", size=12, weight="bold", overstrike=False)

#이미지 경로
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

        # 로그인 후 받은 사용자 임시 데이터 #마이페이지에서 사용중🐧
        self.user_data = {}

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
        self.__user_id = ""  # 유저 아이디

        self.frames = {}

        # Frame 등록
        self.add_frame(LoginPage, self)
        self.add_frame(JoinPage, self)
        self.add_frame(HomePage, self)
        self.add_frame(PostFeed, self)
        self.add_frame(MessagesPage, self)
        self.add_frame(MsgFriendsPage, self)
        self.add_frame(ActivityPage, self)
        self.add_frame(MyPage, self)
        self.add_frame(firstPage, self)
        self.add_frame(SidebarPage, self)
        self.add_frame(Following_FeedPage, self)
        self.add_frame(PostFeed, self)


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

    def show_error_popup(self):
        """
        오류 팝업을 띄운다.
        """
        login_frame = self.frames["LoginPage"]
        login_frame.error_frame.place(x=60, y=300)

        print(self.frames.keys())

    def show_complete_popup(self):
        """
        완료 팝업을 띄운다.
        """
        join_frame = self.frames["JoinPage"]
        join_frame.complete_frame.place(x=60, y=300)




    # 텍스트 클릭 시 글씨 삭제
    def on_Text_click(self, text, string):
        # print(len(text.get("1.0", tk.END)))
        # print(len(string))
        # str1 = text.get("1.0", tk.END).replace(" ", "")
        # str2 = string.replace(" ", "")
        #
        # if str1 == str2:
        #     print("랄라")
        #     text.delete("1.0", tk.END)
        if string in text.get("1.0", tk.END):
            text.delete("1.0", tk.END)

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
                send_data = (str(msg) + "<EOF>").encode()
                client_socket.send(send_data)
                print(f"[데이터 송신] - {send_data}")

                recv_data = b""
                while True:
                    chunk = client_socket.recv(self.baudrate)
                    if not chunk:
                        break

                    recv_data += chunk

                    # 대용량 데이터에 대비하기 위해 파일 끝을 확인하여 수신 받도록 수정 함.
                    if b"<EOF>" in recv_data:
                        recv_data = recv_data.split(b"<EOF>")[0]
                        break

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
        self.show_frame(ActivityPage)

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
        loginBtn = tk.Button(self, image=self.loginImg, bd=0,command=lambda: self.process_login())
        loginBtn.bind("<Return>", lambda e: self.process_login())
        loginBtn.place(x=30, y=595)

        # 회원가입
        joinBtn = tk.Button(self, image=self.joinImg, bd=0, command=lambda: controller.show_frame(JoinPage))
        joinBtn.place(x=160, y=895)


        # 로그인 에러 창
        self.error_frame = tk.Frame(self, width=350, height=180, bg="white")
        self.error_frame.place(x=60, y=400)
        self.error_frame.place_forget()

        self.errorImg = ImageTk.PhotoImage(Image.open(img_path + "error.png"))
        frame = tk.Label(self.error_frame, image=self.errorImg, bg="white")
        frame.image = self.errorImg
        frame.pack()

        self.closeImg = ImageTk.PhotoImage(Image.open(img_path + "close.png"))
        self.closeBtn = tk.Button(self.error_frame, image=self.closeImg, bd=0, command=self.hide_error)
        self.closeBtn.image = self.closeImg
        self.closeBtn.place(x=300, y=15)

        self.checkImg = ImageTk.PhotoImage(Image.open(img_path + "check.png"))
        self.checkBtn = tk.Button(self.error_frame, image=self.checkImg, bd=0, command=self.hide_error)
        self.checkBtn.image = self.checkImg
        self.checkBtn.place(x=280, y=130)


    def show_frame(self):
        self.tkraise()
        self.hide_error()

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
            print(self.controller.get_user_id())
            self.parent.show_frame(HomePage)
        # 로그인 실패
        else:
            self.parent.show_error_popup()
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
        self.parent = parent

        self.nameImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.emailImg = ImageTk.PhotoImage(Image.open(img_path +'id.png'))
        self.numImg = ImageTk.PhotoImage(Image.open(img_path +'id.png'))
        self.jidImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.jpwImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        self.jloginImg = ImageTk.PhotoImage(Image.open(img_path + 'joinBtn.png'))

        self.default_name_text = "사용자 이름"
        self.default_id_text = "사용자 아이디"
        self.default_pw_text = "비밀번호"
        self.default_email_text = "사용자 이메일 주소"

        # 배경
        label = tk.Label(self, bg="white")
        label.place(x=-2, y=-2)

        # 배경
        joinFont = tk.font.Font(family="돋움", size=25)
        jlabel = tk.Label(self, text="회원가입", font=joinFont)
        jlabel.place(x=20, y=250)

        # 회원가입 이름 입력
        self.nameLabel = tk.Label(self, image=self.nameImg)
        self.nameLabel.place(x=30, y=340)

        self.nameEntry = tk.Entry(self, bd=0, fg="gray")
        self.nameEntry.place(x=60, y=370)
        self.nameEntry.insert(0, self.default_name_text)
        self.nameEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.nameEntry, self.default_name_text))
        self.nameEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.nameEntry, self.default_name_text))

        # 회원가입 아이디 입력
        self.jidLabel = tk.Label(self, image=self.jidImg)
        self.jidLabel.place(x=30, y=420)
        self.jidEntry = tk.Entry(self, bd=0, fg="gray")
        self.jidEntry.place(x=60, y=450)
        self.jidEntry.insert(0, self.default_id_text)
        self.jidEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.jidEntry, self.default_id_text))
        self.jidEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.jidEntry, self.default_id_text))

        # 회원가입 이메일 입력
        self.emailLabel = tk.Label(self, image=self.emailImg)
        self.emailLabel.place(x=30, y=500)

        self.emailEntry = tk.Entry(self, bd=0, fg="gray")
        self.emailEntry.place(x=60, y=530)
        self.emailEntry.insert(0, self.default_email_text)
        self.emailEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.emailEntry, self.default_email_text))
        self.emailEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.emailEntry, self.default_email_text))


        # 회원가입 비밀번호 입력
        self.jpwLabel = tk.Label(self, image=self.jpwImg)
        self.jpwLabel.place(x=30, y=580)
        self.jpwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        self.jpwEntry.place(x=60, y=610)
        self.jpwEntry.insert(0, self.default_pw_text)
        self.jpwEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.jpwEntry, self.default_pw_text))
        self.jpwEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.jpwEntry, self.default_pw_text))

        # 회원가입 파란색 버튼
        self.jloginBtn = tk.Button(self, image=self.jloginImg, bd=0, activebackground="white", command=self.process_join)
        self.jloginBtn.place(x=68, y=850)

        # 회원가입 완료 창
        self.complete_frame = tk.Frame(self, width=350, height=180, bg="white")
        self.complete_frame.place(x=60, y=400)
        self.complete_frame.place_forget()

        self.completeImg = ImageTk.PhotoImage(Image.open(img_path + "complete.png"))
        self.completeframe = tk.Label(self.complete_frame, image=self.completeImg, bg="white")
        self.completeframe.image = self.completeImg
        self.completeframe.pack()

        self.checkImg = ImageTk.PhotoImage(Image.open(img_path + "check.png"))
        self.checkBtn = tk.Button(self.complete_frame, image=self.checkImg, bd=0, command=lambda:self.confirm_register_message())
        self.checkBtn.image = self.checkImg
        self.checkBtn.place(x=300, y=15)

        #뒤로 가기 버튼
        self.backImg = ImageTk.PhotoImage(Image.open(img_path + "back.png"))
        self.backBtn = tk.Button(self, image=self.backImg, bd=0, command=lambda:controller.show_frame(LoginPage))
        self.backBtn.place(x=30, y=40)

    def confirm_register_message(self):
        self.jidEntry.delete(0, tk.END)
        self.emailEntry.delete(0, tk.END)
        self.jpwEntry.delete(0, tk.END)
        self.nameEntry.delete(0, tk.END)

        self.jidEntry.insert(0, self.default_id_text)
        self.emailEntry.insert(0, self.default_email_text)
        self.jpwEntry.insert(0, self.default_pw_text)
        self.nameEntry.insert(0, self.default_name_text)
        self.complete_frame.place_forget()
        self.controller.show_frame(LoginPage)


    #회원 가입
    def process_join(self):
        """
        서버에 회원 가입을 요청한다.
        """
        # 회원 가입 메시지 생성
        user_id = self.jidEntry.get()
        user_pw = self.jpwEntry.get()
        user_email = self.emailEntry.get()
        user_name = self.nameEntry.get()

        msg = self.create_register_msg(user_id, user_pw, user_email, user_name)

        # 회원 가입 요청
        res = self.controller.request_db(msg)

        # 회원 가입 성공
        if res["status"]:
            self.controller.set_user_id(user_id)
            self.controller.show_complete_popup()

        # 회원 가입 실패
        else:
            self.parent.show_error_popup()
            print("회원가입 실패")

    def create_register_msg(self, id, password, email, name):
        return Message.create_register_msg(id=id, password=password, email=email, name=name)

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

        self.likeimg = ImageTk.PhotoImage(Image.open(img_path + 'like.png').resize((20, 20)))
        self.likedimg = ImageTk.PhotoImage(Image.open(img_path + 'like_red.png').resize((20, 17)))
        self.commentimg = ImageTk.PhotoImage(Image.open(img_path + 'reply.png').resize((20, 20)))
        self.repostimg = ImageTk.PhotoImage(Image.open(img_path + 'repost.png').resize((20, 20)))
        self.msgimg = ImageTk.PhotoImage(Image.open(img_path + 'msg.png').resize((20, 20)))

        # 좋아요 이미지 리스트 [빈하트, 빨간하트]
        self.like_images = [self.likeimg, self.likedimg]  # 0: 빈 하트, 1: 빨간 하트
        self.like_state = 0


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
        self.contentFrame = tk.Frame(self, bg="black")
        self.contentFrame.place(x=0, y=100, relwidth=1, height=self.controller.contents_frame_height - 100)

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def show_frame(self):
        self.tkraise()
        self.load_feed()

    def load_feed(self):
        msg = Message.create_get_feed_msg(None)
        res = self.controller.request_db(msg)

        # 데이터 수신 예시
        # { 'type': 4, 'status': 1, 'message': '', 'data':
        # {1: {'id': 'ht', 'content': '', 'image': None, 'like_cnt': '', 'comment_cnt': '', 'writed_time': datetime.datetime(2025, 8, 4, 12, 6, 3)},
        #  2: {'id': 'ht', 'content': '', 'image': None, 'like_cnt': 1, 'comment_cnt': 1, 'writed_time': datetime.datetime(2025, 8, 4, 12, 14, 5)},
        # }

        for feed_data in res["data"].values():
            # 작성자의 프로필 이미지 받아오기
            msg = Message.create_get_userinfo_msg(feed_data["id"])
            user_info = self.controller.request_db(msg)
            profile_img_path = None

            if user_info["status"] == EnumMsgStatus.SUCCESS:
                if user_info["data"]["profile_img"] is not None:
                    print(user_info["data"]["profile_img"])   # TODO 이미지 불러오기 테스트 후 수정요
                    # img = Image.open(profile_img).resize((40, 40))
                    profile_img_path = Image.open(img_path + "noImageMan.png")  # 임시
                else:
                    profile_img_path = Image.open(img_path + "noImageMan.png")  # 이미지 불러오기 실패 시
            else:
                pass

            feedItem = FeedItemFrame(
                self.contentFrame,
                profile_img_path,
                feed_data,
                self.like_images,
                self.commentimg,
                self.repostimg,
                self.msgimg
            )
            feedItem.pack(fill="x", pady=(0, 5))

            # 피드 구분 회색 선
            border = tk.Frame(self.contentFrame, bg="#323232", height=1)
            border.pack(fill="x", pady=10)



#활동 페이지 화면
class ActivityPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.activitypageImg = ImageTk.PhotoImage(Image.open(img_path + 'activitypage.png'))

        label = tk.Label(self, image=self.activitypageImg)
        label.pack()


        controller.place_menu_bar(self, EnumMenuBar.ACTIVITY)

    def show_frame(self):
        self.tkraise()




# 마이 페이지 화면
class MyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_tab = None  # 현재 선택된 탭
        self.configure(bg="black") # 배경
        self.name_text = ""  # 이름 저장

        #프로필 수정용 임시 데이터 🐧
        # self.data = {
        #     "user_name": "명수",
        #     "profile_image": img_path + "북극알명수.png"
        #  }



        # 상단 프로필 프레임
        self.FrameTop = tk.Frame(self, bg="black", height=240)
        self.FrameTop.pack(side="top", fill="x")

        self.name_label = tk.Label(self.FrameTop, fg="white", bg="black", font=("Arial", 22, 'bold'))
        self.name_label.place(x=30, y=120)

        self.id_label = tk.Label(self.FrameTop, fg="white", bg="black", font=("Arial", 12))
        self.id_label.place(x=30, y=160)

        self.follows_cnt_label = tk.Label(self.FrameTop, fg="gray", bg="black",
                                     font=("Arial", 11))
        self.follows_cnt_label.place(x=30, y=190)

        #프로필 사진
        self.profile_img = ImageTk.PhotoImage(Image.open(img_path + 'profile.png').resize((65, 65)))
        self.profile_label = tk.Label(self.FrameTop, image=self.profile_img, fg="white", bg="black")
        self.profile_label.place(x=380, y=70)  # 데이터 값 가져오기

        #프로필 수정 버튼
        self.edit_pfImg = ImageTk.PhotoImage(Image.open(img_path +'edit_pf.png').resize((130, 30)))
        self.edit_pfBtn = tk.Button(self, image=self.edit_pfImg, bd=0, relief="flat", highlightthickness=0,
                               activebackground="black", command=self.show_edit_popup)
        self.edit_pfBtn.place(x=320, y=200)


        # 프로필 편집 팝업 창
        #★프레임 설정 변경 해야함☆
        self.editframe = tk.Frame(self, width=400, height=300, bg="blue")
        self.editframe.place_forget()

        self.namenptImg = ImageTk.PhotoImage(Image.open(img_path + 'namenpt.png'))
        self.namenptLabel = tk.Label(self.editframe, image=self.namenptImg, bg="black")
        self.namenptLabel.image = self.namenptImg
        self.namenptLabel.place(x=30, y=90)

        self.cancelImg = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png').resize((50, 20)))
        self.cancelBtn = tk.Button(self.editframe, image=self.cancelImg, bd=0, bg="black", activebackground="black",
                                   command=self.hide_edit_popup)
        self.cancelBtn.place(x=12, y=17)


        self.newnameLabel = tk.Label(self.editframe, fg="white", bg="black",  font=("고딕", 15, 'bold'))
        self.newnameLabel.place(x=30, y=150)

        self.newnameEntry = tk.Entry(self.editframe, width=20, fg="white", bg="black", font=("고딕", 15, 'bold'))
        self.newnameEntry.place(x=50, y=125)
        self.newnameEntry.insert(0, self.name_text)
        self.newnameEntry.bind('<Button-1>',
                               lambda e: self.controller.on_entry_click(self.newnameEntry, self.name_text))
        self.newnameEntry.bind('<FocusOut>',
                               lambda e: self.controller.on_focusout(self.newnameEntry, self.name_text))

        self.doneImg = ImageTk.PhotoImage(Image.open(img_path + 'done.png').resize((70, 15)))
        self.doneBtn = tk.Button(self.editframe, image=self.doneImg, bd=0, bg="black", activebackground="black",
                                 command=self.save_edit_data)
        self.doneBtn.image = self.doneImg
        self.doneBtn.place(x=300, y=15)




        # 탭 프레임(버튼 배치)
        self.FrameTabs = tk.Frame(self, bg="black", height=50)
        self.FrameTabs.pack(side="top", fill="x")

        self.mp1Img = ImageTk.PhotoImage(Image.open(img_path + 'mp1.png'))
        self.mp1Btn = tk.Button(self.FrameTabs, image=self.mp1Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Threads"))
        self.mp1Btn.place(x=20, y=0)

        self.mp2Img = ImageTk.PhotoImage(Image.open(img_path + 'mp2.png'))
        self.mp2Btn = tk.Button(self.FrameTabs, image=self.mp2Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Replies"))
        self.mp2Btn.place(x=140, y=0)

        self.mp3Img = ImageTk.PhotoImage(Image.open(img_path + 'mp3.png'))
        self.mp3Btn = tk.Button(self.FrameTabs, image=self.mp3Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Media"))
        self.mp3Btn.place(x=240, y=0)

        self.mp4Img = ImageTk.PhotoImage(Image.open(img_path + 'mp4.png'))
        self.mp4Btn = tk.Button(self.FrameTabs, image=self.mp4Img, bd=0, relief="flat", highlightthickness=0,
                                activebackground="black", command=lambda: self.switch_tabs("Reposts"))
        self.mp4Btn.place(x=340, y=0)

        self.lineFrame = tk.Frame(self.FrameTabs, bg="#666768")
        self.lineFrame.pack(fill="x", pady=(50, 0))

        # 탭 별 프레임 생성
        self.FrameContent = tk.Frame(self, bg="black", height=450)
        self.FrameContent.pack(side="top", fill="x")


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

    def show_frame(self):
        self.tkraise()
        self.update_user_info()
        self.hide_edit_popup()


    def update_user_info(self):
        msg = Message.create_get_userinfo_msg(self.controller.get_user_id())
        # print(self.controller.get_user_id())
        res = self.controller.request_db(msg)
        # print('res1')
        # print(res)
        # print(res['data']['name'])

        self.name_text = res['data']['name']
        self.name_label.config(text=self.name_text)

        self.id_text = res['data']['id']
        self.id_label.config(text=self.id_text)

        msg2 = Message.create_get_follows_msg(self.controller.get_user_id())
        res2 = self.controller.request_db(msg2)
        self.follows_cnt_label.config(text=str(len(res2['data']))+ ' followers')

        # profile_img_path = msg.get('profile_img',img_path + 'profile_img.png')
        # self.profile_img = ImageTk.PhotoImage(Image.open(profile_img_path).resize((65, 65)))
        # self.profile_label.config(image=self.profile_img)


    def apply_temp_msg(self):
        new_name = self.data.get("user_name","")
        if  new_name:
            self.name_text = new_name
            self.name_label.config(text=self.new_name)



    #이름 변경
    def edit_name(self):
        self.newnameLabel = tk.Label(self.editframe, fg="white", bg="black",  font=("고딕", 15, 'bold'))
        self.newnameLabel.place(x=30, y=220)

        #변경할 이름 입력
        self.newnameEntry = tk.Entry(self.editframe, width=20, fg="white", bg="black", font=("고딕", 15, 'bold'))
        self.newnameEntry.place(x=30, y=250)
        self.newnameEntry.insert(0, self.name_text)
        self.newnameEntry.bind('<Button-1>',
                               lambda e: self.controller.on_entry_click(self.newnameEntry, self.name_text))
        self.newnameEntry.bind('<FocusOut>',
                               lambda e: self.controller.on_focusout(self.newnameEntry, self.name_text))



    #변경된 이름, 이미지 저장
    def save_edit_data(self):
        new_name = self.newnameEntry.get().strip()
        if not new_name:
            print("이름 입력 없음")
            return

        self.hide_edit_popup()
        print(f"이름 수정 완료!: {self.name_text}")

        #res = self.controller.request_db(msg)
        res = self.controller.request_db(
            Message.create_update_profile(self.controller.get_user_id(), new_name,''))

        #이름 변경 성공
        if res["status"]:
            self.update_user_info()

        #이름 변경 실패
        else:
            print("이름 저장 실패:", res)


    def show_edit_popup(self):
        self.newnameEntry.delete(0, tk.END)
        self.newnameEntry.insert(0, self.name_text)
        self.editframe.place(relx=0.5, rely=0.5, anchor="center")
        self.editframe.tkraise()

        # self.newnameEntry.bind('<Button-1>',
        #                        lambda e: self.controller.on_entry_click(self.newnameEntry, self.name_text))
        # self.newnameEntry.bind('<FocusOut>',
        #                        lambda e: self.controller.on_focusout(self.newnameEntry, self.name_text))
        #
        # self.editframe.place(relx=0.5, rely=0.5, anchor="center")
        # self.editframe.lift()

    def hide_edit_popup(self):
        self.editframe.place_forget()



    # following 피드 화면
class Following_FeedPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        topFrame = tk.Frame(self, bg="black")
        topFrame.place(x=0, y=0, relwidth=1)

        self.configure(bg="black")

        # 홈 맨 왼쪽 위 back 버튼
        self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'backBtn.png').resize((70, 25)))
        homeLeftBtn = tk.Button(topFrame, image=self.homeLeftImg, bd=0, background="black", activebackground="black",
                                command=lambda: controller.show_frame(HomePage))
        homeLeftBtn.pack(side="left", padx=10, pady=30)

        # 홈 맨 위 가운데 following
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
        print(profile_img)

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
        post_time = datetime.datetime.strptime(message["elapsed_time"], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
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
class PostFeed(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="black")

        topFrame = tk.Frame(self, bg="black")
        topFrame.pack(side="top", fill="x")

        self.cancelImg = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png').resize((60, 20)))
        cancelBtnl = tk.Button(topFrame, image=self.cancelImg, bd=0, bg="black", activebackground="black",
                               command=lambda: self.controller.show_frame("ForYou_FeedPage"))
        cancelBtnl.pack(anchor="w", padx=20, pady=(30, 10))

        self.newPostImg = ImageTk.PhotoImage(Image.open(img_path + 'newPost.png').resize((125, 30)))
        newPostLabel = tk.Label(topFrame, image=self.newPostImg, bd=0, bg="black")
        newPostLabel.place(x="175", y="23")

        # 구분 회색 선
        border = tk.Frame(topFrame, bg="#323232", height=1)
        border.pack(fill="x", pady=10)

        # 전체 묶는 프레임
        containerFrame = tk.Frame(self, bg="black")
        containerFrame.pack(side="top", anchor="w", padx=10, pady=10)

        # 왼쪽: 프로필 사진, 오른쪽: 아이디 + 게시글 구조
        leftFrame = tk.Frame(containerFrame, bg="black", width=50)
        leftFrame.pack(side="left", anchor="n", padx=10)

        rightFrame = tk.Frame(containerFrame, bg="black")
        rightFrame.pack(side="left", fill="x")

        self.profileimg = ImageTk.PhotoImage(Image.open(messages[0]["img"]).resize((45, 45)))
        imgLabel = tk.Label(leftFrame, image=self.profileimg, bg="pink")
        imgLabel.pack(anchor="n", padx=10, pady=10)

        contentArea = tk.Frame(rightFrame, bg="black")
        contentArea.pack(fill="x", anchor="w")

        # 아이디
        topInfo = tk.Frame(contentArea, bg="black")
        topInfo.pack(anchor="w", pady=(0, 2))

        self.idLabel = tk.Label(topInfo, text="", fg="white", bg="black", font=("Arial", 16))
        self.idLabel.pack(side="left")

        # 게시글 작성
        self.textEntry = tk.Text(contentArea, bd=0, height="5", bg="black", fg="gray", font=("Arial", 16),
                                 insertbackground="gray")
        self.textEntry.pack(side="left")
        self.textEntry.insert(1.0, "What's new?")
        self.click_count = 0
        self.textEntry.bind('<Button-1>', lambda e: self.controller.on_Text_click(self.textEntry, "What's new?"))
        # textEntry.bind('<Button-1>', lambda e: self.controller.on_Text_click(textEntry, self.click_count))

        # 추가한 이미지 들어갈 프레임 --- 위치 수정 필요
        # photoFrame = tk.Frame(contentArea, bg="blue")
        # photoFrame.pack()

        # 추가한 이미지 표시용 라벨
        self.photoLabel = tk.Label(rightFrame, bg="black")
        self.photoLabel.pack(anchor="w", pady=5)

        # 사진 추가 버튼
        btnFrame = tk.Frame(rightFrame, bg="black")
        btnFrame.pack(anchor="w")

        self.photoImg = ImageTk.PhotoImage(Image.open(img_path + 'photo.png').resize((40, 40)))
        photoBtn = tk.Button(btnFrame, image=self.photoImg, bd=0, bg="black", activebackground="black",
                             command=self.open_Img_File)
        photoBtn.pack(side="left")

        self.postImg = ImageTk.PhotoImage(Image.open(img_path + 'post.png').resize((65, 40)))
        postBtn = tk.Button(btnFrame, image=self.postImg, bd=0, background="black", activebackground="black")
        postBtn.pack(padx=(200, 0))

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def open_Img_File(self):
        file_path = filedialog.askopenfilename(
            title="파일 선택",
            filetypes=(("모든 파일", "*.*"), ("이미지 파일", "*.png;*.jpg;*.jpeg"))
        )
        if file_path:
            print(f"선택된 파일 경로: {file_path}")
            try:
                self.img = Image.open(file_path).resize((200, 200))  # 원하는 크기로 조절
                self.selected_photo = ImageTk.PhotoImage(self.img)  # 인스턴스 변수로 저장
                self.photoLabel.config(image=self.selected_photo)

                self.selected_photo_path = file_path  # 이미지 경로 저장 (나중에 서버 전송용)
            except Exception as e:
                print(f"이미지 열기 오류: {e}")

    def show_frame(self):
        self.tkraise()
        self.update_user_info()

    def update_user_info(self):
        msg = Message.create_get_userinfo_msg(self.controller.get_user_id())
        res = self.controller.request_db(msg)
        print(res)
        print(res['data']['name'])

        self.id_text = res['data']['id']
        self.idLabel.config(text=self.id_text)

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



# ==== 실행 ====
if __name__ == "__main__":
    app = App()
    app.mainloop()