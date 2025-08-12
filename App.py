# App.py
import threading
import time
import tkinter as tk
from tkinter import ttk, font, filedialog
from PIL import ImageTk, Image, ImageDraw
from os import path
import socket
from Msg import *
import Config
from copy import deepcopy
import datetime
from tkinter import filedialog
import io
import base64, io


# 영문 폰트 SF Pro text, 한글폰트 Apple SD Gothic Neo
# threadsFont = tk.font.Font(family="Apple SD Gothic Neo", size=12, weight="bold", overstrike=False)

# 이미지 경로
img_path = path.dirname(path.abspath(__file__)) + "\\images\\"

filename = None


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
        self.add_frame(MessagesPage, self)
        self.add_frame(MsgFriendsPage, self)
        self.add_frame(MyPage, self)
        self.add_frame(firstPage, self)
        self.add_frame(SidebarPage, self)
        self.add_frame(Following_FeedPage, self)
        self.add_frame(PostFeed, self)
        self.add_frame(ActivityPage, self)
        self.add_frame(ChatRoomPage, self)
        self.add_frame(PostDetailPage, self)

        # 첫 화면
        self.show_frame(HomePage)

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

    def show_frame(self, Frame, data=None):
        """
        등록된 page_name의 frame을 화면에 띄운다.
        """
        frame = self.frames[Frame.__name__]
        if data is not None:
            frame.show_frame(data)
        else:
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

    def place_menu_bar(self, place_to, active_menu:int):
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

    def decode_image(self, image_bytes):
        """
        서버에서 받은 이미지 필드 처리 전용.
        입력: image_bytes (예: b"b'iVBORw0KGgo...'" 또는 b'None')
        반환: io.BytesIO (이미지 원본 바이트 스트림) 또는 None

        - b'None' 이면 None 반환
        - b"b'...'" 같이 이중 래핑도 안전하게 처리
        - data:image/...;base64, 프리픽스가 있으면 제거
        """

        print("이미지 변환 1", image_bytes)

        if not image_bytes or image_bytes == b'None':
            return None

        try:
            # 1) bytes → str
            s = bytes(image_bytes).decode('utf-8', 'ignore').strip()

            # 2) 이중 래핑 제거: "b'...'" 또는 'b"..."'
            if (s.startswith("b'") and s.endswith("'")) or (s.startswith('b"') and s.endswith('"')):
                s = s[2:-1]

            # # 3) data URL 프리픽스 대응 (혹시 붙어오는 경우)
            # #예: "data:image/png;base64,iVBORw0KGgo..."
            # if ',' in s and 'base64' in s[:50].lower():
            #     s = s.split(',', 1)[1]

            # 4) base64 → raw bytes
            raw = base64.b64decode(s)

            # 5) BytesIO로 반환 (열고 리사이즈는 호출자가 수행)
            return io.BytesIO(raw)

            # 함수 실행 후 각자 해야 되는 부분
            # image = Image.open(img_io).resize((300, 300))
            # self.img = ImageTk.PhotoImage(image)

        except Exception as e:
            print(f"[decode_image 오류] {e}")
            return None

    # App (controller) 안에 추가
    def open_post_detail(self, post_id, feed_data):
        #page = self.controller.frames["PostDetailPage"]
        #page.set_post(post_id, feed_data)  # 데이터 주입
        #self.show_frame(PostDetailPage)  # 화면 전환
        pass

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

# 홈 화면(for you 피드)
# class HomePage(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLeft2.png'))
#         self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLogo2.png'))
#         self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path + 'homeRight2.png'))
#
#         # 프로필 사진 받는 부분 어떻게 할지 고민,,
#         self.profileimg = ImageTk.PhotoImage(Image.open(img_path + 'profileImg.png').resize((40, 40)))
#
#         self.likeimg = ImageTk.PhotoImage(Image.open(img_path + 'like.png').resize((20, 20)))
#         self.likedimg = ImageTk.PhotoImage(Image.open(img_path + 'like_red.png').resize((20, 17)))
#         self.commentimg = ImageTk.PhotoImage(Image.open(img_path + 'reply.png').resize((20, 20)))
#         self.repostimg = ImageTk.PhotoImage(Image.open(img_path + 'repost.png').resize((20, 20)))
#         self.msgimg = ImageTk.PhotoImage(Image.open(img_path + 'msg.png').resize((20, 20)))
#
#         # 좋아요 이미지 리스트 [빈하트, 빨간하트]
#         self.like_images = [self.likeimg, self.likedimg]  # 0: 빈 하트, 1: 빨간 하트
#         self.like_state = 0
#
#         # 배경
#         self.configure(bg="black")
#
#         topFrame = tk.Frame(self, bg="black")
#         topFrame.place(x=0, y=0, relwidth=1)
#
#         # 홈 맨 왼쪽 위
#         homeLeftBtn = tk.Button(topFrame, image=self.homeLeftImg, bd=0, background="black", activebackground="black",
#                                 command=lambda: controller.show_frame(SidebarPage))
#         # homeLeftBtn.place(x=5, y=0)
#         homeLeftBtn.pack(side="left", padx=20, pady=35)
#
#         # 홈 맨 위 가운데 로고
#         homeLogoBtn = tk.Button(topFrame, image=self.homeLogoImg, bd=0, background="black", activebackground="black",
#                                 command=self.controller.show)
#         homeLogoBtn.place(x=195, y=18)
#
#         # 홈 맨 위 오른쪽
#         homeRightBtn = tk.Button(topFrame, image=self.homeRightImg, bd=0, background="black", activebackground="black",
#                                  command=self.controller.show)
#         homeRightBtn.place(x=400, y=28)
#
#         # 컨탠츠 프레임
#         self.contentFrame = tk.Frame(self, bg="black")
#         self.contentFrame.place(x=0, y=100, relwidth=1, height=self.controller.contents_frame_height - 100)
#
#         controller.place_menu_bar(self, EnumMenuBar.HOME)
#
#     def show_frame(self):
#         self.tkraise()
#         self.load_feed()
#
#
#     # 피드 전체 데이터 가져오는 함수
#     def load_feed(self):
#         msg = Message.create_get_feed_msg(None)
#         res = self.controller.request_db(msg)
#
#         for feed_data in res["data"].values():
#             # 작성자의 프로필 이미지 받아오기
#             msg = Message.create_get_userinfo_msg(feed_data["id"])
#             user_info = self.controller.request_db(msg)
#             profile_img_path = None
#
#             if user_info["status"] == EnumMsgStatus.SUCCESS:
#                 if user_info["data"]["profile_img"] is not None:
#                     print("HomePage 부분 프로필 이미지")
#                     print(user_info["data"]["profile_img"])   # TODO 이미지 불러오기 테스트 후 수정요 -- 아마도 수정완료?!
#                     profile_img_path = Image.open(img_path + "profileimg.png").resize((40,40))
#                 else:
#                     profile_img_path = Image.open(img_path + "noImageMan.png")  # 이미지 불러오기 실패 시
#             else:
#                 pass
#
#             feedItem = FeedItemFrame(
#                 self.contentFrame,
#                 self.controller,
#                 profile_img_path,
#                 feed_data,
#                 self.like_images,
#                 self.commentimg,
#                 self.repostimg,
#                 self.msgimg
#             )
#             feedItem.pack(fill="x", pady=(0, 5))
#
#             # 피드 구분 회색 선
#             border = tk.Frame(self.contentFrame, bg="#323232", height=1)
#             border.pack(fill="x", pady=10)

# 스크롤 구현 완료된 for you 페이지
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

        # ===== 스크롤 가능한 영역 =====
        self.list_frame = tk.Frame(self)
        self.list_frame.place(x=0, y=100, width=self.controller.app_width - 5,
                              height=self.controller.contents_frame_height - 100)

        self.canvas = tk.Canvas(self.list_frame, bg="black", highlightthickness=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg="black")
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 마우스 휠 이벤트 바인딩
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        self.scrollable_frame.bind("<Configure>", self.on_configure)
        self.scrollable_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))

        self.canvas.pack(side="left", fill="both", expand=True)

        controller.place_menu_bar(self, EnumMenuBar.HOME)

        # 피드 리스트 저장용
        self.feed_items = []

    def on_configure(self, event):
        """스크롤 크기 동적 조절"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel_event(self, event):
        if len(self.feed_items) > 1:  # 게시물 많을 때만 스크롤
            self.canvas.yview_scroll(int((-1 * event.delta / 120)), "units")

    def bind_mousewheel_recursive(self, widget):
        widget.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        widget.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)

    def show_frame(self):
        self.tkraise()
        self.load_feed()

    def load_feed(self):
        # 기존 피드 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.feed_items.clear()

        # None을 넣으면 전체 페이지를 불러옴.
        msg = Message.create_get_feed_msg(None)
        res = self.controller.request_db(msg)

        # 데이터 수신 예시
        # { 'type': 4, 'status': 1, 'message': '', 'data':
        # {1: {'id': 'ht', 'content': '', 'image': None, 'like_cnt': '', 'comment_cnt': '', 'writed_time': datetime.datetime(2025, 8, 4, 12, 6, 3)},
        #  2: {'id': 'ht', 'content': '', 'image': None, 'like_cnt': 1, 'comment_cnt': 1, 'writed_time': datetime.datetime(2025, 8, 4, 12, 14, 5)},
        # }

        if not res["data"]:
            return

        for post_id, feed_data in res["data"].items():
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
                profile_img_path = Image.open(img_path + "noImageMan.png")

            feedItem = FeedItemFrame(
                parent=self.scrollable_frame,
                controller=self.controller,
                profile_img_path=profile_img_path,
                feed_data=feed_data,
                like_images=self.like_images,
                comment_img=self.commentimg,
                repost_img=self.repostimg,
                msg_img=self.msgimg,
                post_id=post_id
            )
            feedItem.pack(fill="x", pady=(0, 5))
            self.feed_items.append(feedItem)
            self.bind_mousewheel_recursive(feedItem)

            # 구분선
            border = tk.Frame(self.scrollable_frame, bg="#323232", height=1)
            border.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
            border.pack(fill="x", pady=10)

    # # App (controller) 안에 추가
    # def open_post_detail(self, post_id, feed_data):
    #     page = self.controller.frames["PostDetailPage"]
    #     page.set_post(post_id, feed_data)  # 데이터 주입
    #     self.controller.show_frame(PostDetailPage)  # 화면 전환

# 마이 페이지 화면
class MyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_tab = None  # 현재 선택된 탭

        # 배경
        self.configure(bg="black")

        self.name_text = ""  # 이름 저장

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
        
# 스레드 페이지
class PostDetailPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller
        self.post_id = None
        self.post_data = None
        self.post_img_ref = None

        # 헤더/뒤로 가기
        back = tk.Button(self, text="← Back", command=lambda: self.controller.show_frame(HomePage))
        back.pack(anchor="w", padx=10, pady=10)

        # 본문 영역 (스크롤)
        self.container = tk.Frame(self, bg="black")
        self.container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.container, bg="black", highlightthickness=0)
        self.vbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(self.canvas, bg="black")
        self.win = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))

        # 본문 위젯 자리(동적으로 갈아끼움)
        self.title_lbl = tk.Label(self.body, text="", fg="white", bg="black", font=("Arial", 14, "bold"))
        self.title_lbl.pack(anchor="w", padx=12, pady=(6,2))

        self.content_lbl = tk.Label(self.body, text="", fg="white", bg="black",
                                    wraplength=430, justify="left", font=("맑은고딕", 12))
        self.content_lbl.pack(anchor="w", padx=12, pady=(0,10))

        self.image_lbl = tk.Label(self.body, bg="black")
        self.image_lbl.pack(anchor="w", padx=12, pady=(0,10))

        sep = tk.Frame(self.body, bg="#323232", height=1)
        sep.pack(fill="x", padx=8, pady=10)

        # 댓글 목록 영역
        self.comments_container = tk.Frame(self.body, bg="black")
        self.comments_container.pack(fill="x", padx=8, pady=(0,10))

        # 댓글 입력
        entry_frame = tk.Frame(self, bg="black")
        entry_frame.pack(fill="x", side="bottom")
        self.comment_entry = tk.Entry(entry_frame, bg="#222", fg="white", insertbackground="white")
        self.comment_entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        tk.Button(entry_frame, text="Send", command=self._send_comment).pack(side="right", padx=8, pady=8)


    def set_post(self, post_id, feed_data):
        """Home에서 호출: 상세 표시 데이터 주입"""
        self.post_id = post_id
        self.post_data = feed_data

        # 제목/본문
        self.title_lbl.config(text=feed_data["id"])
        self.content_lbl.config(text=feed_data["content"])

        # 이미지
        self.image_lbl.config(image="")
        self.post_img_ref = None
        img_io = self.controller.decode_image(feed_data.get("image"))
        if img_io:
            img_io.seek(0)
            pil = Image.open(img_io)
            pil.thumbnail((430, 430))
            self.post_img_ref = ImageTk.PhotoImage(pil)
            self.image_lbl.config(image=self.post_img_ref)

        # 댓글 로딩
        self._load_comments()

    def _load_comments(self):
        """서버에서 post_id의 댓글 목록을 받아 렌더링"""
        # TODO: 서버 API가 있으면 사용. 임시로 예시:
        for w in self.comments_container.winfo_children():
            w.destroy()

        # 예시: 서버가 댓글 리스트 반환했다고 가정
        # msg = Message.create_get_comments_msg(self.post_id)
        # res = self.controller.request_db(msg)
        # comments = res["data"]  # [(user, content, time), ...]

        comments = []  # ← 서버 연동 전 임시 리스트
        if not comments:
            tk.Label(self.comments_container, text="No comments yet.", fg="gray", bg="black").pack(anchor="w")
            return

        for c in comments:
            self._add_comment_item(c)

    def _add_comment_item(self, c):
        # c: dict or tuple
        frame = tk.Frame(self.comments_container, bg="black")
        frame.pack(fill="x", pady=6)
        tk.Label(frame, text=c["user"], fg="#ddd", bg="black", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(frame, text=c["content"], fg="white", bg="black", wraplength=430, justify="left").pack(anchor="w")

    def _send_comment(self):
        text = self.comment_entry.get().strip()
        if not text:
            return
        # 서버로 전송(parent_id=self.post_id)
        msg = Message.create_post_msg(
            id=self.controller.get_user_id(),
            content=text,
            post_time=datetime.datetime.now(),
            parent_id=self.post_id,     # ★ 댓글
            image=""
        )
        # 통신은 워커 스레드로
        threading.Thread(target=self._send_comment_worker, args=(msg,), daemon=True).start()

    def _send_comment_worker(self, msg):
        try:
            res = self.controller.request_db(msg)
        except Exception as e:
            res = {"status": 0, "message": str(e)}
        self.after(0, self._after_send_comment, res)

    def _after_send_comment(self, res):
        if res and res.get("status") == 1:
            self.comment_entry.delete(0, "end")
            self._load_comments()  # 재로딩
        else:
            print("댓글 실패:", res)




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

        # 홈 맨 위 가운데 following
        self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'followingBtn.png').resize((140, 35)))
        followingBtn = tk.Button(topFrame, image=self.homeLogoImg, bd=0, background="black", activebackground="black",
                                 command=self.controller.show)
        followingBtn.place(x=167, y=23)

        # 상단 UI 높이 만큼 패딩
        self.contentFrame = tk.Frame(self, bg="black")
        self.contentFrame.place(x=0, y=70, relwidth=1, height=self.controller.contents_frame_height - 70)

        lineFrame = tk.Frame(self.contentFrame, bg="#323232")
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

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def show_frame(self):
        self.tkraise()
        self.load_feed()

    def load_feed(self):
        msg = Message.create_get_feed_msg(self.controller.get_user_id())
        res = self.controller.request_db(msg)

        for post_id, feed_data in res["data"].items():
            # 작성자의 프로필 이미지 받아오기
            msg = Message.create_get_userinfo_msg(feed_data["id"])
            user_info = self.controller.request_db(msg)
            profile_img_path = None

            if user_info["status"] == EnumMsgStatus.SUCCESS:
                if user_info["data"]["profile_img"] is not None:
                    print("HomePage 부분 프로필 이미지")
                    print(user_info["data"]["profile_img"])   # TODO 이미지 불러오기 테스트 후 수정요 -- 아마도 수정완료?!
                    # img = Image.open(profile_img).resize((40, 40))
                    #profile_img_path = Image.open(img_path + "noImageMan.png")  # 임시
                    profile_img_path = Image.open(img_path + "profileimg.png").resize((40,40))  # 임시

                else:
                    profile_img_path = Image.open(img_path + "noImageMan.png")  # 이미지 불러오기 실패 시
            else:
                pass

            feedItem = FeedItemFrame(
                parent = self.contentFrame,
                controller = self.controller,
                profile_img_path = profile_img_path,
                feed_data=feed_data,
                like_images=self.like_images,
                comment_img=self.commentimg,
                repost_img=self.repostimg,
                msg_img=self.msgimg,
                post_id = post_id,
            )
            feedItem.pack(fill="x", pady=(0, 5))

            # 피드 구분 회색 선
            border = tk.Frame(self.contentFrame, bg="#323232", height=1)
            border.pack(fill="x", pady=10)


# 각 게시글
class FeedItemFrame(tk.Frame):
    def __init__(self, parent, post_id, controller, profile_img_path, feed_data, like_images, comment_img, repost_img, msg_img):
        super().__init__(parent, bg="black")
        self.controller = controller
        self.feed_data = feed_data
        self.post_id = post_id

        self.like_state = 0
        self.like_images = like_images
        self.commentimg = comment_img
        self.repostimg = repost_img
        self.msgimg = msg_img

        self.profile_img = ImageTk.PhotoImage(profile_img_path)

        # 왼쪽-오른쪽 구조
        leftFrame = tk.Frame(self, bg="black", width=50)
        leftFrame.pack(side="left", anchor="n", padx=10)

        rightFrame = tk.Frame(self, bg="black")
        rightFrame.pack(side="left", fill="x")

        imgLabel = tk.Label(leftFrame, image=self.profile_img, bg="black")
        # 프로필 이미지 띄우는 중 그러나 안됨 왜지? --- 이제 됨!!
        #imgLabel.image = profile_img
        imgLabel.pack(anchor="n")

        contentArea = tk.Frame(rightFrame, bg="black")
        contentArea.pack(fill="x", anchor="w")

        # 아이디 + 시간
        topInfo = tk.Frame(contentArea, bg="black")
        topInfo.pack(anchor="w", pady=(0, 2))

        idLabel = tk.Label(topInfo, text=feed_data["id"], fg="white", bg="black", font=("Arial", 11))
        idLabel.pack(side="left")

        # 시간 계산
        str_time = str(feed_data["writed_time"])
        post_time = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
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
        feedLabel = tk.Label(contentArea, text=feed_data["content"], fg="white", bg="black",
                             wraplength=400, justify="left", font=("맑은고딕", 11))
        feedLabel.pack(anchor="w", pady=(0, 10))

        # 게시글 이미지(decode_image 함수 사용 버전)
        image_data = feed_data["image"]

        # decode_image 함수가 base64 문자열을 처리할 수 있게 한다고 가정
        pil_img = self.controller.decode_image(image_data)

        # print("디코드 이미지: ", pil_img)

        # # decode_image가 None을 반환했는지 확인
        # if pil_img:
        #     image = Image.open(pil_img).resize((300, 300))
        #     self.img = ImageTk.PhotoImage(image)
        #     imgLabel = tk.Label(contentArea, image=self.img, bg="black")
        #     imgLabel.pack(anchor="w", pady=(0, 10))
        # else:
        #     print("[decode_image 오류] decode_image가 None을 반환했습니다.")

        # 버튼 영역(좋아요, 댓글, 리포스트, 공유 버튼)
        btnFrame = tk.Frame(rightFrame, bg="black")
        btnFrame.pack(anchor="w", pady=(0, 5))

        self.likeBtn = tk.Button(btnFrame, image=self.like_images[self.like_state], bd=0, background="black",
                                 activebackground="black", command=self.toggle_like)
        self.likeBtn.pack(side="left")

        self.likeCnt = tk.Label(btnFrame, text=feed_data["like_cnt"], fg="white", bg="black")
        self.likeCnt.pack(side="left", padx=(2, 20))

        commentBtn = tk.Button(btnFrame, image=self.commentimg, bd=0, background="black",
                               activebackground="black", command=self.show)
        commentBtn.pack(side="left")
        commentCnt = tk.Label(btnFrame, text=feed_data["comment_cnt"], fg="white", bg="black")
        commentCnt.pack(side="left", padx=(2, 15))

        repostBtn = tk.Button(btnFrame, image=self.repostimg, bd=0, background="black",
                              activebackground="black", command=self.show)
        repostBtn.pack(side="left", padx=(0, 20))

        msgBtn = tk.Button(btnFrame, image=self.msgimg, bd=0, background="black",
                           activebackground="black", command=self.show)
        msgBtn.pack(side="left")

        # === 클릭 타겟들 ===
        # 카드 전체
        self.bind("<Button-1>", self.on_open_detail)
        # 주요 영역에도 바인딩(라벨 클릭 시에도 동작하도록)
        imgLabel.bind("<Button-1>", self.on_open_detail)
        contentArea.bind("<Button-1>", self.on_open_detail)
        topInfo.bind("<Button-1>", self.on_open_detail)
        idLabel.bind("<Button-1>", self.on_open_detail)
        timeLabel.bind("<Button-1>", self.on_open_detail)
        feedLabel.bind("<Button-1>", self.on_open_detail)

        # 마우스 올렸을 때 손가락 커서로
        for w in (self, imgLabel, contentArea, topInfo, idLabel, timeLabel, feedLabel):
            w.configure(cursor="hand2")

        # 댓글 버튼은 상세로 들어가도록 해도 됨(선택)
        commentBtn.config(command=self.on_open_detail)

    def on_open_detail(self, event=None):
        # 상세 페이지로 전환 요청
        self.controller.open_post_detail(self.post_id, self.feed_data)
    # ============================

    def toggle_like(self):
        # 상태 토글
        self.like_state = 1 - self.like_state
        self.likeBtn.config(image=self.like_images[self.like_state])

        # 좋아요 수 변경
        current_likes = int(self.likeCnt.cget("text"))
        if self.like_state == 1:
            current_likes += 1
        else:
            current_likes -= 1
        self.likeCnt.config(text=str(current_likes))

    def show_frame(self):
        self.tkraise()

    def show(self):
        print("hi")

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

        foryouBtn = tk.Button(sideFrame, image=self.feeds1img, bd=0, bg="black", activebackground="black", command=lambda: controller.show_frame(HomePage))
        foryouBtn.place(x="20", y="105")

        followingBtn = tk.Button(sideFrame, image=self.feeds2img, bd=0, bg="black", activebackground="black", command=lambda: controller.show_frame(Following_FeedPage))
        followingBtn.place(x="20", y="180")

    def show_frame(self):
        self.tkraise()  

# 게시물 작성 페이지
class PostFeed(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_base64 = None

        self.configure(bg="black")

        topFrame = tk.Frame(self, bg="black")
        topFrame.pack(side="top", fill="x")

        self.cancelImg = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png').resize((60, 20)))
        cancelBtnl = tk.Button(topFrame, image=self.cancelImg, bd=0, bg="black", activebackground="black", command=lambda: self.controller.show_frame(HomePage))
        cancelBtnl.pack(anchor="w", padx=20, pady=(30,10))

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

        self.profileimg = ImageTk.PhotoImage(Image.open(img_path + "noImageMan.png").resize((45, 45)))
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
        self.textEntry = tk.Text(contentArea,bd=0, height="5", bg="black", fg="gray", font=("Arial", 16), insertbackground="gray")
        self.textEntry.pack(side="left")
        self.textEntry.insert(1.0, "What's new?")
        self.click_count = 0
        self.textEntry.bind('<Button-1>', lambda e: self.controller.on_Text_click(self.textEntry, "What's new?"))
        #textEntry.bind('<Button-1>', lambda e: self.controller.on_Text_click(textEntry, self.click_count))

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
        photoBtn = tk.Button(btnFrame, image=self.photoImg, bd=0, bg="black", activebackground="black", command=self.open_Img_File)
        photoBtn.pack(side="left")

        self.postImg = ImageTk.PhotoImage(Image.open(img_path + 'post.png').resize((65, 40)))
        self.postBtn = tk.Button(btnFrame, image=self.postImg, bd=0, background="black", activebackground="black", command=self.update_post_info)
        self.postBtn.pack(padx=(200,0))

        self.controller.place_menu_bar(self, -1)

    def open_Img_File(self):
        file_path = filedialog.askopenfilename(
            title="파일 선택",
            filetypes=(("모든 파일", "*.*"), ("이미지 파일", "*.png;*.jpg;*.jpeg"))
        )
        if file_path:
            print(f"선택된 파일 경로: {file_path}")
            try:
                self.img = Image.open(file_path).resize((300, 300))  # 원하는 크기로 조절
                self.selected_photo = ImageTk.PhotoImage(self.img)  # 인스턴스 변수로 저장
                self.photoLabel.config(image=self.selected_photo)
                self.selected_photo_path = file_path  # 이미지 경로 저장 (나중에 서버 전송용)

                self.file_img = open(file_path, 'rb').read()
                self.image_base64 = base64.b64encode(self.file_img)
                print("오픈 파일=================================")
                print(len(self.file_img))

                #image_base64 = base64.b64encode(file_img).decode('utf-8')
                # self.image_base64 = base64.b64encode(file_img)
                # print("파일 베이스================================")
                # print(len(self.image_base64))

            except Exception as e:
                print(f"이미지 열기 오류: {e}")

    def show_frame(self):
        self.tkraise()

    # def update_post_info(self):
    #
    #     # 이부분을 스레드로 따로 작업하게 해줘
    #     #==========================
    #     # 이미지가 없을 때 b'None'이나 None을 명시적으로 넣어줌
    #     if self.image_base64:
    #         img_data = self.image_base64
    #     else:
    #         img_data = b'None'
    #
    #     msg = Message.create_post_msg(
    #         id=self.controller.get_user_id(),
    #         content=self.textEntry.get("1.0", tk.END),
    #         post_time=datetime.datetime.now(),
    #         parent_id=None,
    #         image=img_data
    #     )
    #     #print(msg)
    #     #res = self.controller.request_db(msg)
    #     #print(res)
    #
    #     self.controller.show_frame(HomePage)
    #     #==========================

    def update_post_info(self):
        # 버튼 중복 클릭 방지(옵션)
        # postBtn을 인스턴스 변수로 들고 있다면 아래처럼:
        self.postBtn.config(state="disabled")

        # 이미지: 없으면 명시적으로 None 표기 (서버에서 처리)
        img_data = self.image_base64 if self.image_base64 else b'None'

        msg = Message.create_post_msg(
            id=self.controller.get_user_id(),
            content=self.textEntry.get("1.0", tk.END),
            post_time=datetime.datetime.now(),
            parent_id=None,
            image=img_data
        )

        # ★ 통신은 워커 스레드에서
        t = threading.Thread(target=self._post_worker, args=(msg,), daemon=True)
        t.start()

    def _post_worker(self, msg):
        try:
            res = self.controller.request_db(msg)
        except Exception as e:
            res = {"type": Message.EnumMessageType.POST if hasattr(Message, "EnumMessageType") else 3,
                   "status": 0, "message": str(e), "data": None}

        # ★ UI 갱신은 메인 스레드에서
        self.after(0, self._on_post_done, res)
        # 여기서는 Tk 호출 금지

    def _on_post_done(self, res):
        # 버튼 복구(옵션)
        self.postBtn.config(state="normal")

        if res and res.get("status") == 1:
            # 성공 → 홈으로
            self.controller.show_frame(HomePage)
        else:
            # 실패 → 에러 표시
            err = res.get("message") if isinstance(res, dict) else "Unknown error"
            print("[POST 실패]", err)
            # 필요하면 팝업/라벨로 사용자에게 알림

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
        messages_text_btn = tk.Button(self, image=self.messages_text_img, bd=0, background="black", activebackground="black", highlightthickness=0, command=self.controller.show)
        messages_text_btn.place(x=20, y=30)

        # 채팅 방 추가
        add_chat_room_btn = tk.Button(self, image=self.add_chat_room_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.controller.show_frame(MsgFriendsPage))
        add_chat_room_btn.place(x=420, y=30)

        # 검색
        # search_box = tk.Label(self, image=self.search_box_img, borderwidth=0)
        # search_box.place(x=0, y=80)
        # search_box_font = tk.font.Font(size=14)
        # search_entry = tk.Entry(self, bd=0, fg="gray", background="#1e1e1e", font=search_box_font)
        # search_entry.place(x=55, y=108, width=370)
        # search_entry.insert(0, "Search")
        # search_entry.bind('<Button-1>', lambda e: self.controller.on_entry_click(search_entry, "Search"))
        # search_entry.bind('<FocusOut>', lambda e: self.controller.on_focusout(search_entry, "Search"))

        # 메시지 리스트
        self.list_frame = tk.Frame(self)
        self.list_frame.place(x=0, y=100, width=self.controller.app_width, height=self.controller.contents_frame_height - 120)

        self.canvas = tk.Canvas(self.list_frame, bg="black", highlightthickness=0)

        self.scrollable_frame = tk.Frame(self.canvas, bg="black")
        self.scrollable_frame.config(height=300)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))

        # 캔버스에 스크롤 가능한 프레임 넣기
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.controller.app_width, height=740)

        self.scrollable_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        self.canvas.pack(side="left", fill="both", expand=True)

        controller.place_menu_bar(self, EnumMenuBar.MESSAGE)

        self.scrollable_frame.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        """
        스크롤바의 크기를 동적으로 맞추기 위한 설정.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_frame(self):
        self.tkraise()
        
        friends = self.controller.request_db(Message.create_get_follows_msg(self.controller.get_user_id()))

        if len(friends["data"]) > 0:
            self.load_chat_rooms(friends)
        else:
            self.load_new_message_controls()

    def load_new_message_controls(self):
        # ...
        dot3_logo = tk.Label(self, image=self.dotdotdot_logo, bd=0, highlightthickness=0, background="black", borderwidth=0)
        dot3_logo.place(x=185, y=300)
        # 최대 7개의 친구 사진을 가져와서 디자인 배치

        # 채팅 방이 없을 때 문구
        no_chat_room_message = tk.Label(self, image=self.no_chat_room_message_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        no_chat_room_message.place(x=55, y=500)

        # 메시지 추가 버튼
        new_message_btn = tk.Button(self, image=self.message_btn_img, activebackground="black", bd=0, background="black" ,relief="flat", highlightthickness=0, command=lambda: self.controller.show_frame(MsgFriendsPage))
        new_message_btn.place(x=180, y=580)

    def load_chat_rooms(self, friends):
        # 목록 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for f in friends["data"]:
            f = f[0]
            msg = self.controller.request_db(Message.create_get_chatroom_list_msg(self.controller.get_user_id(), f))

            if not msg["data"]:
                continue

            chatroom_info = msg["data"][0]

            chatroom_id = chatroom_info["chatroom_id"]
            user_id1 = chatroom_info["user_id1"]
            user_id2 = chatroom_info["user_id2"]
            chatroom_created = chatroom_info["chatroom_date"]

            my_id = self.controller.get_user_id()
            
            if user_id1 == my_id:
                another_id = user_id2
            else:
                another_id = user_id1

            user_info = self.controller.request_db(Message.create_get_userinfo_msg(another_id))
            user_name = user_info["data"]["name"]
            user_profile_img = user_info["data"]["profile_img"]

            chat_data = self.controller.request_db(Message.create_get_chat_data_msg(chatroom_id, ""))
            last_chat = chat_data["data"][-1]["content"]
            last_chat_date = chat_data["data"][-1]["message_time"]

            frame = self.create_chatroom_frame(another_id, user_name, user_profile_img, last_chat, last_chat_date, chatroom_info)
            frame.pack(fill="x", pady=2, padx=5)
            self.bind_mousewheel_recursive(frame)

    def create_chatroom_frame(self, id, name, profile_img, last_msg, last_date, chatroom_info):
        frame = ChatRoomItemFrame(self.scrollable_frame, self.controller, id, name, profile_img, last_msg, last_date, chatroom_info)
        return frame

    def bind_mousewheel_recursive(self, widget):
        widget.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        widget.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)
    
    def on_mousewheel_event(self, event):
        """
        스크롤 이벤트
        """
        self.canvas.yview_scroll(int((event.delta / 120)), "units")

class ChatRoomItemFrame(tk.Frame):
    """
    채팅방 프레임
    """
    def __init__(self, parent, controller, id, name, profile_img, last_msg, last_datetime, chatroom_info):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#1e1e1e", relief="flat", highlightbackground="gray", highlightthickness=0)
        self.frame_id = id
        self.chatroom_info = chatroom_info

        try:
            img = Image.open(profile_img).resize((40, 40))
        except:
            img = Image.open(img_path + "noImageMan.png").resize((40, 40))  # 이미지 불러오기 실패 시

        croped_img = self.controller.crop_img_circle(img)
        photo = ImageTk.PhotoImage(croped_img)
        image_label = tk.Label(self, image=photo, bg="#1e1e1e")
        image_label.image = photo
        image_label.pack(side="left", padx=10, pady=5)
        image_label.bind("<Button-1>", lambda e: self.on_click())

        text_frame = tk.Frame(self, bg="#1e1e1e")
        text_frame.bind("<Button-1>", lambda e: self.on_click())
        name_label = tk.Label(text_frame, text=id, fg="white", font=("Arial", 12, "bold"), anchor="w", bg="#1e1e1e", width=39)
        name_label.bind("<Button-1>", lambda e: self.on_click())
        status_label = tk.Label(text_frame, text=name, font=("Arial", 10), anchor="w", bg="#1e1e1e", fg="gray")
        status_label.bind("<Button-1>", lambda e: self.on_click())
        last_msg_lb = tk.Label(text_frame, text=last_msg[:10], font=("Arial", 10), anchor="e", bg="#1e1e1e", fg="gray")
        last_msg_lb.place(x=340, y=10)
        last_date_lb = tk.Label(text_frame, text=last_datetime, font=("Arial", 8), anchor="e", bg="#1e1e1e", fg="gray")
        last_date_lb.place(x=280, y=30)

        name_label.pack(anchor="w", expand=True)
        status_label.pack(anchor="w")
        text_frame.pack(side="left", fill="x", expand=True)

        self.bind("<Button-1>", lambda e: self.on_click())

    def on_click(self):
        self.controller.show_frame(ChatRoomPage, self.chatroom_info)
            
# 메시지 친구 목록 페이지
class MsgFriendsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.selected_friend = None
        # self.friends_list = []

        self.cancel_img = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png'))
        self.new_message_text_img = ImageTk.PhotoImage(Image.open(img_path + 'newMessageText.png'))
        self.to_suggested_text_img = ImageTk.PhotoImage(Image.open(img_path + 'toSuggested.png'))

        # 배경
        self.configure(bg="black")

        # cencel 버튼
        cencel_btn = tk.Button(self, image=self.cancel_img, bd=0, background="black", activebackground="black", highlightthickness=0, command=lambda: self.on_click_cancel())
        cencel_btn.place(x=20, y=50)

        chat_btn = tk.Button(self, text="chat", command=lambda: self.chat())
        chat_btn.place(x= 400, y=50)

        # New message 문구
        new_message_text = tk.Label(self, image=self.new_message_text_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        new_message_text.place(x=170, y=50)

        # To: Suggested 문구
        to_suggested_text = tk.Label(self, image=self.to_suggested_text_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        to_suggested_text.place(x=0, y=90)

        # 친구 목록
        self.list_frame = tk.Frame(self)
        self.list_frame.place(x=0, y=140, width=self.controller.app_width - 5, height=self.controller.contents_frame_height - 140)

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
        self.selected_friend = None

        msg = Message.create_get_follows_msg(self.controller.get_user_id())
        res = self.controller.request_db(msg)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # self.friends_list.clear()

        for friend in res["data"]:
            msg = Message.create_get_userinfo_msg(friend[0])
            friend_infos = self.controller.request_db(msg)
            data = friend_infos["data"]

            frame = self.create_friend_item(data["id"], data["name"], data["profile_img"])
            frame.pack(fill="x", pady=2, padx=5)
            self.bind_mousewheel_recursive(frame)

        # for f in self.friends_list:
        #     f.pack(fill="x", pady=2, padx=5)

    def create_friend_item(self, id, name, profile_img):
        frame = FriendFrame(self.scrollable_frame, self, id, name, profile_img)
        # self.friends_list.append(frame)
        return frame

    def bind_mousewheel_recursive(self, widget):
        widget.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        widget.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)

    def on_mousewheel_event(self, event):
        if len(self.friends_list) > 13:
            self.canvas.yview_scroll(int((-1 * event.delta / 120)), "units")

    def on_click(self, frame):
        # 선택 안된 아이템을 클릭
        if self.selected_friend != frame.frame_id:
            self.selected_friend = frame.frame_id

            for f in self.friends_list:
                f.configure(highlightthickness=0)

            frame.configure(highlightthickness=1)

        # 선택된 아이템을 클릭
        elif self.selected_friend == frame.frame_id:
            self.selected_friend = None

            frame.configure(highlightthickness=0)

    def chat(self):
        # 기존 채팅방이 존재하는지 확인
        msg = Message.create_get_chatroom_list_msg(self.controller.get_user_id(), self.selected_friend)
        res = self.controller.request_db(msg)

        # 채팅 방이 없다면 채팅 방을 생성한다.
        if not res["data"]:
            now = datetime.datetime.now()
            msg = Message.create_add_chatroom_msg(self.controller.get_user_id(), self.selected_friend, now) 
            chatroom_data = self.controller.request_db(msg)
            chatroom_data = chatroom_data["data"]

        # 채팅 방이 있다면 기존 채팅 방의 정보를 불러온다.
        else:
            chatroom_data = res["data"][0]

        self.controller.show_frame(ChatRoomPage, chatroom_data)

# 친구 목록 아이템
class FriendFrame(tk.Frame):
    def __init__(self, parent, controller, id, name, profile_img):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#1e1e1e", relief="flat", highlightbackground="gray", highlightthickness=0)
        self.frame_id = id

        try:
            img = Image.open(profile_img).resize((40, 40))
        except:
            img = Image.open(img_path + "profileImg.png").resize((40, 40))  # 이미지 불러오기 실패 시

        croped_img = controller.controller.crop_img_circle(img)
        photo = ImageTk.PhotoImage(croped_img)
        image_label = tk.Label(self, image=photo, bg="#1e1e1e")
        image_label.image = photo
        image_label.pack(side="left", padx=10, pady=5)
        image_label.bind("<Button-1>", lambda e: controller.on_click(self))

        text_frame = tk.Frame(self, bg="#1e1e1e")
        text_frame.bind("<Button-1>", lambda e: controller.on_click(self))
        name_label = tk.Label(text_frame, text=id, fg="white", font=("Arial", 12, "bold"), anchor="w", bg="#1e1e1e", width=39)
        name_label.bind("<Button-1>", lambda e: controller.on_click(self))
        status_label = tk.Label(text_frame, text=name, font=("Arial", 10), anchor="w", bg="#1e1e1e", fg="gray")
        status_label.bind("<Button-1>", lambda e: controller.on_click(self))

        name_label.pack(anchor="w", expand=True)
        status_label.pack(anchor="w")
        text_frame.pack(side="left", fill="x", expand=True)

        self.bind("<Button-1>", lambda e: controller.on_click(self))

# 채팅방
class ChatRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.chatroom_id = None
        self.chat_user1 = None
        self.chat_user2 = None
        self.created_date = None
        self.isOnFrame = False
        self.chat_update_interval = 1
        self.message_list = []
        self.last_message_time = ""

        # 메시지를 불러와서 메시지 작성자가 나이면 오른쪽에 아니면 왼쪽에
        # 메시지 작성자의 첫 메시지 옆에 프로필 아이콘 띄우기

        self.friend_profile_img = ImageTk.PhotoImage(Image.open(img_path + 'noImageMan.png').resize((40, 40)))
        self.add_file_img = ImageTk.PhotoImage(Image.open(img_path + 'plus.png'))
        self.message_bar_img = ImageTk.PhotoImage(Image.open(img_path + 'chatbar.png'))
        self.back_img = ImageTk.PhotoImage(Image.open(img_path + 'back_black.png'))

        self.msg_default_text = "Message..."

        # 배경
        self.configure(bg="black")

        self.message_bar = tk.Label(self, image=self.message_bar_img, borderwidth=0)
        self.message_bar.place(x=70, y=850)
        self.message_bar_font = tk.font.Font(size=14)

        # 상대 이름
        self.name_lb = tk.Label(self, text=self.chat_user2, bg="black", fg="white", font=tk.font.Font(size=14))
        self.name_lb.place(x=60, y=40)

        # 채팅 바
        self.message_bar_entry = tk.Entry(self, bd=0, fg="white", background="#1e1e1e", font=self.message_bar_font)
        self.message_bar_entry.place(x=85, y=870, width=350)
        self.message_bar_entry.insert(0, self.msg_default_text)
        self.message_bar_entry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.message_bar_entry, self.msg_default_text))
        self.message_bar_entry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.message_bar_entry, self.msg_default_text))
        self.message_bar_entry.bind('<Return>', lambda e: self.send_text())

        # 파일 추가 버튼
        new_message_btn = tk.Button(self, image=self.add_file_img, activebackground="black", bd=0, background="black" ,relief="flat", highlightthickness=0, command=lambda: self.send_text())
        new_message_btn.place(x=10, y=850)

        # 이전 버튼
        new_message_btn = tk.Button(self, image=self.back_img, activebackground="black", bd=0, background="black" ,relief="flat", highlightthickness=0, command=lambda: self.move_back())
        new_message_btn.place(x=20, y=40)

        # 메시지 리스트
        self.list_frame = tk.Frame(self)
        self.list_frame.place(x=0, y=100, width=self.controller.app_width, height=self.controller.contents_frame_height - 120)

        self.canvas = tk.Canvas(self.list_frame, background="black", highlightthickness=0)

        self.scrollable_frame = tk.Frame(self.canvas, bg="black")
        self.scrollable_frame.config(height=300)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))

        # 캔버스에 스크롤 가능한 프레임 넣기
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.controller.app_width)

        self.scrollable_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        self.canvas.pack(side="left", fill="both", expand=True)

        # 프레임 크기 변경 시 스크롤 범위 갱신
        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)

    def show_frame(self, chatroom_data):
        self.chatroom_id = chatroom_data["chatroom_id"]
        self.chat_user1 = chatroom_data["user_id1"]
        self.chat_user2 = chatroom_data["user_id2"]
        self.created_date = chatroom_data["chatroom_date"]

        self.name_lb.config(text=self.chat_user2)
    
        self.tkraise() 

        self.clear_chat()

        self.isOnFrame = True

        self.chat_thread = threading.Thread(target=self.load_chat_data)
        self.chat_thread.daemon = True
        self.chat_thread.start()

    def move_back(self):
        self.isOnFrame = False
        self.controller.show_frame(MessagesPage)

    def clear_chat(self):
        for ch in self.scrollable_frame.winfo_children():
            ch.destroy()

    def load_chat_data(self):
        self.last_message_time = ""

        while self.isOnFrame:
            # 마지막 업데이트 메시지 시간을 포함하여 get_chat_data 요청 보내기
            messages = self.controller.request_db(Message.create_get_chat_data_msg(self.chatroom_id, self.last_message_time))
            
            if messages["data"]:
                for i, msg in enumerate(messages["data"]):
                    if i != 0:
                        prev_day = datetime.datetime.strptime(str(messages["data"][i - 1]["message_time"]).split(" ")[0], "%Y-%m-%d").day
                    else:
                        prev_day = -1

                    now_day = datetime.datetime.strptime(str(messages["data"][i]["message_time"]).split(" ")[0], "%Y-%m-%d").day

                    # 이전 메시지와 날짜(일)가 다르면
                    # if prev_day == -1 or now_day != prev_day:
                    if now_day != prev_day:
                        # 구분선 추가
                        self.create_sepline(self.scrollable_frame, datetime.datetime.strptime(str(msg["message_time"]).split(" ")[0], "%Y-%m-%d").date())
                        # 메시지 말풍선 gui 생성 후 도시하기
                        self.create_msg_frame(self.scrollable_frame, msg["user_id"], msg["content"], msg["image"], msg["message_time"], True)
                    else:
                        self.create_msg_frame(self.scrollable_frame, msg["user_id"], msg["content"], msg["image"], msg["message_time"], False)

                # 마지막으로 업데이트한 메시지 시간을 저장
                self.last_message_time = messages["data"][-1]["message_time"]

            time.sleep(self.chat_update_interval)

    def create_sepline(self, parent, day_text):
        """
        메시지 날짜 구분선 추가
        """
        border1 = tk.Frame(parent, bg="#323232", height=1)
        border1.pack(padx=10, pady=10, fill="x")

        day_label = tk.Label(parent, text=day_text, bg="black", fg="gray")
        day_label.pack()

    def send_text(self):
        """
        메시지 전송하기
        """
        text = self.message_bar_entry.get()
        my_id = self.controller.get_user_id()

        # 메시지를 작성했다면
        if text != self.msg_default_text and text:
            # 메시지 데이터 정의 후 메시지 전송하기
            data = MessageData.create_msg_data(
                user_id=my_id, 
                chatroom_id=self.chatroom_id, 
                content=text,
                image="",
                message_time=datetime.datetime.now())
            msg = Message.create_add_chat_msg(self.chatroom_id, data)
            res = self.controller.request_db(msg)
            self.message_bar_entry.delete(0, tk.END)

        if self.chat_user1 == my_id:
            to_user_id = self.chat_user2
        else:
            to_user_id = self.chat_user1

        # notif = Message.create_add_notif_msg(
        #     user_id=to_user_id,
        #     from_user_id=self.controller.get_user_id(),
        #     notif_type=EnumNotifType.MESSAGE,
        #     concerned_id=
        # )

    def send_image(self):
        img_path = filedialog.askopenfile()
        img = Image.open(img_path)

        # 채팅 입력 및 전송
        # 서버로 채팅 전송
        
    def update_scrollregion(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel_event(self, event):
        self.canvas.yview_scroll(int((-1 * event.delta / 120)), "units")

    def create_msg_frame(self, parent, user_id, content, image, message_time, is_draw_profile_img):
        is_mine = (self.controller.get_user_id() == user_id)
        bg_color = "#2f2f2f"
        text_color = "white"
        font = ("Arial", 12)
        time_font = ("Arial", 8)

        # 말풍선 프레임
        wrapper_frame = tk.Frame(parent, bg="black")
        wrapper_frame.pack(fill="x", pady=5, padx=10, anchor="e" if is_mine else "w")

        # 프로필 이미지 (상대방만 표시)
        if not is_mine and is_draw_profile_img:
            profile_img = tk.Label(wrapper_frame, image=self.friend_profile_img, bg="black")
            profile_img.pack(side="left", padx=5)

        # 메시지 박스
        msg_bubble = tk.Frame(wrapper_frame, bg=bg_color, padx=10, pady=5)
        msg_bubble.pack(side="right" if is_mine else "left", padx=5)

        if image:
            try:
                img = Image.open(image)
                img.thumbnail((200, 200))
                tk_img = ImageTk.PhotoImage(img)
                img_label = tk.Label(msg_bubble, image=tk_img, bg=bg_color)
                img_label.image = tk_img  # 참조 유지
                img_label.pack()
            except Exception as e:
                print("이미지 로딩 오류:", e)
        else:
            text_label = tk.Label(msg_bubble, text=content, font=font, fg=text_color, bg=bg_color, wraplength=250, justify="left")
            text_label.pack()

        # 시간 표시
        time_label = tk.Label(wrapper_frame, text=str(message_time)[-8:-3], font=time_font, fg="gray", bg="black")
        time_label.pack(anchor="e" if is_mine else "w", padx=5)

        # 스크롤 하단 고정
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def bind_mousewheel_recursive(self, widget):
        widget.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_event))
        widget.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)

# 활동 내역 페이지
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

# ==== 실행 ====
if __name__ == "__main__":
    app = App()
    app.mainloop()