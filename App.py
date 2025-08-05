import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image, ImageDraw
from os import path
import socket
from Msg import Message, EnumMessageType
import Config
from copy import deepcopy

# 이미지 경로
img_path = path.dirname(path.abspath(__file__)) + "\\images\\"

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
        self.bottom_bar_height = 100        # 하단 메뉴바 높이
        self.contents_frame_height = self.app_height - self.bottom_bar_height          # 하단 메뉴 바를 제외한 크기
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
        self.menu_home_img = ImageTk.PhotoImage(Image.open(img_path + 'home1.png'))
        self.w_menu_home_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png'))
        self.menu_msg_img = ImageTk.PhotoImage(Image.open(img_path + 'home2.png'))
        self.w_menu_msg_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png'))
        self.menu_new_img = ImageTk.PhotoImage(Image.open(img_path + 'home3.png'))
        self.w_menu_new_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png'))
        self.menu_act_img = ImageTk.PhotoImage(Image.open(img_path + 'home4.png'))
        self.w_menu_act_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png'))
        self.menu_my_img = ImageTk.PhotoImage(Image.open(img_path + 'home5.png'))
        self.w_menu_my_img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png'))

        # 임의로 넣은 아이디. 나중에 ""으로
        self.__user_id = "ht"  # 유저 아이디

        self.frames = {}

        # Frame 등록
        self.add_frame(LoginPage, self)
        self.add_frame(JoinPage, self)
        self.add_frame(HomePage, self)
        self.add_frame(MessagesPage, self)
        self.add_frame(MsgFriendsPage, self)

        # 첫 화면
        self.show_frame(MsgFriendsPage)

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

        x1 = x - r/2
        y1 = y - r/2
        x2 = x + r/2
        y2 = y + r/2

        draw = ImageDraw.Draw(mask_img)

        draw.ellipse((x1,y1, x2, y2), fill = 'white', outline ='white')

        image_pix = image.load()
        mask_pix = mask_img.load()
        W, H = mask_img.size

        for y in range(H):
            for x in range(W):
                value = mask_pix[x, y]
                if value == 0:
                    image_pix[x, y]=(0,0,0,0) #투명 값 설정
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

    def place_menu_bar(self, place_to, active_menu:int):
        """
        홈 맨 아래 아이콘들을 배치한다.
        """
        home_img = self.menu_home_img
        msg_img = self.menu_msg_img
        new_img = self.menu_new_img
        act_img = self.menu_act_img
        my_img = self.menu_act_img

        if active_menu == 0:
            home_img = self.w_menu_home_img
        elif active_menu == 1:
            msg_img = self.w_menu_home_img
        elif active_menu == 2:
            new_img = self.w_menu_home_img
        elif active_menu == 3:
            act_img = self.w_menu_home_img
        elif active_menu == 4:
            my_img = self.w_menu_home_img

        home1Btn = tk.Button(place_to, image=home_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.on_click_home_btn())
        home1Btn.place(x=5, y=860)

        home2Btn = tk.Button(place_to, image=msg_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.on_click_msg_btn())
        home2Btn.place(x=95, y=860)

        home3Btn = tk.Button(place_to, image=new_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.on_click_new_btn())
        home3Btn.place(x=185, y=860)

        home4Btn = tk.Button(place_to, image=act_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.on_click_act_btn())
        home4Btn.place(x=275, y=860)

        home5Btn = tk.Button(place_to, image=my_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.on_click_my_btn())
        home5Btn.place(x=365, y=860)

    def on_click_home_btn(self):
        self.show_frame(HomePage)

    def on_click_msg_btn(self):
        self.show_frame(MessagesPage)

    def on_click_new_btn(self):
        pass

    def on_click_act_btn(self):
        pass

    def on_click_my_btn(self):
        pass

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_user_id(self):
        return self.__user_id

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
        self.pwEntry.insert(0, "비밀번호")
        self.pwEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.pwEntry, "비밀번호"))
        self.pwEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.pwEntry, "비밀번호"))
        self.pwEntry.bind("<Return>", lambda e: self.process_login())

        # 로그인 파란색 버튼
        loginBtn = tk.Button(self, image=self.loginImg, bd=0, command=lambda : self.process_login())
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
        self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLeft.png'))
        self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLogo.png'))
        self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path + 'homeRight.png'))

        # 배경
        self.configure(bg="black")

        # 홈 맨 왼쪽 위
        homeLeftBtn = tk.Button(self, image=self.homeLeftImg, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=self.controller.show)
        homeLeftBtn.place(x=0, y=0)

        # 홈 맨 위 가운데 로고
        homeLogoBtn = tk.Button(self, image=self.homeLogoImg, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=self.controller.show)
        homeLogoBtn.place(x=175, y=0)

        # 홈 맨 위 오른쪽
        homeRightBtn = tk.Button(self, image=self.homeRightImg, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=self.controller.show)
        homeRightBtn.place(x=350, y=0)

        controller.place_menu_bar(self, EnumMenuBar.HOME)

    def show_frame(self):
        self.tkraise()     

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
        add_chat_room_btn = tk.Button(self, image=self.add_chat_room_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=lambda: self.controller.show_frame(MsgFriendsPage))
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
        dot3_logo = tk.Label(self, image=self.dotdotdot_logo, bd=0, highlightthickness=0, background="black", borderwidth=0)
        dot3_logo.place(x=185, y=300)
        # 최대 7개의 친구 사진을 가져와서 디자인 배치

        # 채팅 방이 없을 때 문구
        if True:
            no_chat_room_message = tk.Label(self, image=self.no_chat_room_message_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
            no_chat_room_message.place(x=55, y=500)
        else:
            pass

        # 메시지 추가 버튼
        new_message_btn = tk.Button(self, image=self.message_btn_img, activebackground="black", bd=0, background="black" ,relief="flat", highlightthickness=0, command=lambda: self.controller.show_frame(MsgFriendsPage))
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
        cencel_btn = tk.Button(self, image=self.cancel_img, bd=0, background="black", activebackground="black", highlightthickness=0, command=lambda: self.on_click_cancel())
        cencel_btn.place(x=20, y=50)

        # New message 문구
        new_message_text = tk.Label(self, image=self.new_message_text_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        new_message_text.place(x=170, y=50)

        # To: Suggested 문구
        to_suggested_text = tk.Label(self, image=self.to_suggested_text_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        to_suggested_text.place(x=0, y=90)

        # 친구 목록
        self.list_frame = tk.Frame(self)
        self.list_frame.place(x=0, y=200, width=self.controller.app_width, height=self.controller.contents_frame_height - 200)

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
        name_label = tk.Label(text_frame, text=id, fg="white", font=("Arial", 12, "bold"), anchor="w", bg="#1e1e1e", width=39)
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