import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image, ImageDraw
from os import path
import socket
from Msg import Message, MessageType
import Config
from copy import deepcopy

# 이미지 경로
img_path = path.dirname(path.abspath(__file__)) + "\\images\\"

# 이미지 객체를 전역 변수로 선언해서 참조 유지
bgImg = None
idImg = None
pwImg = None
loginImg = None
joinImg = None

nameImg = None
jidImg = None
jpwImg = None
jloginImg = None

errorImg = None
closeImg = None
checkImg = None

homeLeftImg = None
homeLogoImg = None
homeRightImg = None
home1Img = None
home2Img = None
home3Img = None
home4Img = None
home5Img = None

# ======================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Threads")
        self.geometry("471x954")
        self.resizable(False, False)

        self.socket_family = Config.comm_config["socket_family"]
        self.socket_type = Config.comm_config["socket_type"]
        self.host = Config.comm_config["host"]
        self.port = Config.comm_config["port"]
        self.baudrate = Config.comm_config["baudrate"]

        self.frames = {}

        # Frame 등록
        for F in (LoginPage, JoinPage, HomePage, MessagesPage, MsgFriendsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # 첫 화면
        # self.show_frame("LoginPage")
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """
        등록된 page_name의 frame을 화면에 띄운다.
        """
        frame = self.frames[page_name]
        frame.tkraise()

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

    def show_error_popup(self, controller):
        """
        오류 팝업을 띄운다.
        """
        login_frame = controller.frames["LoginPage"]
        login_frame.error_frame.place(x=60, y=300)

    def show_complete_popup(self, controller):
        """
        완료 팝업을 띄운다.
        """
        join_frame = controller.frames["JoinPage"]
        join_frame.complete_frame.place(x=60, y=300)
    
    def show(self):
        """
        테스트용
        """
        print("hello")

    def crop_img_circle(image):
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

    def request_db(self, data):
        """
        DB 정보를 받기 위해 서버에 데이터를 요청한다.
        """
        client_socket = socket.socket(self.socket_family, self.socket_type)
        client_socket.connect((self.host, self.port))

        try:
            while True:
                send_data = str(data).encode()
                client_socket.send(send_data)
                print(f"[데이터 송신] - {send_data}")

                recv_data = client_socket.recv(self.baudrate)
                print(f"[데이터 수신] - {recv_data}")

                return recv_data
        finally:
            client_socket.close()

# 로그인 화면 실행
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        global bgImg, loginImg, joinImg, idImg, pwImg

        #bimg = Image.open('Threads.png')
        bgImg = ImageTk.PhotoImage(Image.open(img_path + 'Threads.png'))

        # 배경을 Label을 이용하여 처리
        label = tk.Label(self, image=bgImg)
        label.place(x=-2, y=-2)

        # 로그인 아이디 입력
        #iImg = Image.open('id.png')
        idImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        idLabel = tk.Label(self, image=idImg)
        idLabel.place(x=30, y=420)

        self.idEntry = tk.Entry(self, bd=0, fg="gray")
        self.idEntry.place(x=60, y=450)
        self.idEntry.insert(0, "사용자 아이디")
        self.idEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.idEntry, "사용자 아이디"))
        self.idEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.idEntry, "사용자 아이디"))


        # 로그인 비밀번호 입력
        pImg = Image.open(img_path + 'id.png')
        pwImg = ImageTk.PhotoImage(pImg)
        pwLabel = tk.Label(self, image=pwImg)
        pwLabel.place(x=30, y=500)

        self.pwEntry = tk.Entry(self, bd=0, fg="gray")
        self.pwEntry.place(x=60, y=530)
        self.pwEntry.insert(0, "비밀번호")
        self.pwEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(self.pwEntry, "비밀번호"))
        self.pwEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(self.pwEntry, "비밀번호"))


        # 로그인 파란색 버튼
        lImg = Image.open(img_path + 'loginBtn.png')
        loginImg = ImageTk.PhotoImage(lImg)
        loginBtn = tk.Button(self, image=loginImg, bd=0, command=lambda : self.process_login())
        loginBtn.place(x=30, y=595)


        # 회원가입
        jImg = Image.open(img_path + 'join.png')
        joinImg = ImageTk.PhotoImage(jImg)
        joinBtn = tk.Button(self, image=joinImg, bd=0, command=lambda: controller.show_frame("JoinPage"))
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

    def hide_error(self):
        self.error_frame.place_forget()

    def process_login(self):

        # 로그인 메시지 생성
        msg = self.create_login_msg(self.idEntry.get(), self.pwEntry.get())
        # 로그인 요청
        res = eval(self.controller.request_db(msg).decode())

        if res["status"]:
            self.parent.show_frame("HomePage")
        else:
            self.parent.show_error_popup(self)
        

    def create_login_msg(self, id, password):
        return Message.create_login_msg(id=id, password=password)

# 회원가입 화면 실행
class JoinPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        global nameImg, jidImg, jpwImg, jloginImg

        # 배경
        label = tk.Label(self, bg="white")
        label.place(x=-2, y=-2)

        # 배경
        joinFont = tk.font.Font(family="돋움", size=25)
        jlabel = tk.Label(self, text="회원가입", font=joinFont)
        jlabel.place(x=20, y=250)

        # 회원가입 이름 입력
        nImg = Image.open(img_path + 'id.png')
        nameImg = ImageTk.PhotoImage(nImg)
        nameLabel = tk.Label(self, image=nameImg)
        nameLabel.place(x=30, y=340)

        nameEntry = tk.Entry(self, bd=0, fg="gray")
        nameEntry.place(x=60, y=370)
        nameEntry.insert(0, "사용자 이름")
        nameEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(nameEntry, "사용자 이름"))
        nameEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(nameEntry, "사용자 이름"))


        # 회원가입 아이디 입력
        jiImg = Image.open(img_path + 'id.png')
        jidImg = ImageTk.PhotoImage(jiImg)
        jidLabel = tk.Label(self, image=jidImg)
        jidLabel.place(x=30, y=420)

        jidEntry = tk.Entry(self, bd=0, fg="gray")
        jidEntry.place(x=60, y=450)
        jidEntry.insert(0, "사용자 아이디")
        jidEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(jidEntry, "사용자 아이디"))
        jidEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(jidEntry, "사용자 아이디"))


        # 회원가입 비밀번호 입력
        jpImg = Image.open(img_path + 'id.png')
        jpwImg = ImageTk.PhotoImage(jpImg)
        jpwLabel = tk.Label(self, image=jpwImg)
        jpwLabel.place(x=30, y=500)
        jpwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        jpwEntry.place(x=60, y=530)
        jpwEntry.insert(0, "비밀번호")
        jpwEntry.bind('<Button-1>', lambda e: self.controller.on_entry_click(jpwEntry, "비밀번호"))
        jpwEntry.bind('<FocusOut>', lambda e: self.controller.on_focusout(jpwEntry, "비밀번호"))


        # 회원가입 파란색 버튼
        jlImg = Image.open(img_path + 'joinBtn.png')
        jloginImg = ImageTk.PhotoImage(jlImg)
        jloginBtn = tk.Button(self, image=jloginImg, bd=0, command=self.controller.show)
        jloginBtn.place(x=68, y=850)

    
# 홈 화면
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLeft.png'))
        self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLogo.png'))
        self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path + 'homeRight.png'))
        self.home1Img = ImageTk.PhotoImage(Image.open(img_path + 'home1.png'))
        self.home2Img = ImageTk.PhotoImage(Image.open(img_path + 'home2.png'))
        self.home3Img = ImageTk.PhotoImage(Image.open(img_path + 'home3.png'))
        self.home4Img = ImageTk.PhotoImage(Image.open(img_path + 'home4.png'))
        self.home5Img = ImageTk.PhotoImage(Image.open(img_path + 'home5.png'))

        # 배경
        self.configure(bg="black")

        # 홈 맨 왼쪽 위
        homeLeftBtn = tk.Button(self, image=self.homeLeftImg, bd=0, background="black" ,relief="flat", highlightthickness=0, command=self.controller.show)
        homeLeftBtn.place(x=0, y=0)

        # 홈 맨 위 가운데 로고
        homeLogoBtn = tk.Button(self, image=self.homeLogoImg, bd=0, background="black" ,relief="flat", highlightthickness=0, command=self.controller.show)
        homeLogoBtn.place(x=175, y=0)

        # 홈 맨 위 오른쪽
        homeRightBtn = tk.Button(self, image=self.homeRightImg, bd=0, background="black" ,relief="flat", highlightthickness=0, command=self.controller.show)
        homeRightBtn.place(x=350, y=0)

        # 홈 맨 아래 아이콘들
        home1Btn = tk.Button(self, image=self.home1Img, bd=0, background="black" ,relief="flat", highlightthickness=0, command=self.controller.show)
        home1Btn.place(x=5, y=860)

        home2Btn = tk.Button(self, image=self.home2Img, bd=0, background="black", relief="flat", highlightthickness=0, command=self.controller.show)
        home2Btn.place(x=95, y=860)

        home3Btn = tk.Button(self, image=self.home3Img, bd=0, background="black", relief="flat", highlightthickness=0, command=self.controller.show)
        home3Btn.place(x=185, y=860)

        home4Btn = tk.Button(self, image=self.home4Img, bd=0, background="black", relief="flat", highlightthickness=0, command=self.controller.show)
        home4Btn.place(x=275, y=860)

        home5Btn = tk.Button(self, image=self.home5Img, bd=0, background="black", relief="flat", highlightthickness=0, command=self.controller.show)
        home5Btn.place(x=365, y=860)

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
        self.home1Img = ImageTk.PhotoImage(Image.open(img_path + 'home1.png'))
        self.home2Img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png').resize((77, 77)))
        self.home3Img = ImageTk.PhotoImage(Image.open(img_path + 'home3.png'))
        self.home4Img = ImageTk.PhotoImage(Image.open(img_path + 'home4.png'))
        self.home5Img = ImageTk.PhotoImage(Image.open(img_path + 'home5.png'))

        # 배경
        self.configure(bg="black")

        # Messages 문구
        messages_text_btn = tk.Button(self, image=self.messages_text_img, bd=0, background="black",
                                      activebackground="black", highlightthickness=0, command=self.controller.show)
        messages_text_btn.place(x=20, y=30)

        # 채팅 방 추가
        add_chat_room_btn = tk.Button(self, image=self.add_chat_room_img, bd=0, background="black", activebackground="black", relief="flat", highlightthickness=0, command=self.controller.show)
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
        new_message_btn = tk.Button(self, image=self.message_btn_img, activebackground="black", bd=0, background="black" ,relief="flat", highlightthickness=0, command=self.controller.show)
        new_message_btn.place(x=180, y=580)

        # 홈 맨 아래 아이콘들
        home1Btn = tk.Button(self, image=self.home1Img, bd=0, background="black" ,relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home1Btn.place(x=5, y=860)

        home2Btn = tk.Button(self, image=self.home2Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home2Btn.place(x=95, y=860)

        home3Btn = tk.Button(self, image=self.home3Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home3Btn.place(x=185, y=860)

        home4Btn = tk.Button(self, image=self.home4Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home4Btn.place(x=275, y=860)

        home5Btn = tk.Button(self, image=self.home5Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home5Btn.place(x=365, y=860)

# 메시지 페이지
class MsgFriendsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.cancel_img = ImageTk.PhotoImage(Image.open(img_path + 'cancel.png'))
        self.new_message_text_img = ImageTk.PhotoImage(Image.open(img_path + 'newMessageText.png'))
        self.to_suggested_text_img = ImageTk.PhotoImage(Image.open(img_path + 'toSuggested.png'))

        self.home1Img = ImageTk.PhotoImage(Image.open(img_path + 'home1.png'))
        self.home2Img = ImageTk.PhotoImage(Image.open(img_path + 'home2-1.png').resize((77, 77)))
        self.home3Img = ImageTk.PhotoImage(Image.open(img_path + 'home3.png'))
        self.home4Img = ImageTk.PhotoImage(Image.open(img_path + 'home4.png'))
        self.home5Img = ImageTk.PhotoImage(Image.open(img_path + 'home5.png'))

        # 배경
        self.configure(bg="black")

        # cencel 버튼
        cencel_btn = tk.Button(self, image=self.cancel_img, bd=0, background="black", activebackground="black", highlightthickness=0, command=self.controller.show)
        cencel_btn.place(x=20, y=50)

        # New message 문구
        new_message_text = tk.Label(self, image=self.new_message_text_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        new_message_text.place(x=170, y=50)

        # To: Suggested 문구
        to_suggested_text = tk.Label(self, image=self.to_suggested_text_img, bd=0, highlightthickness=0, background="black", borderwidth=0)
        to_suggested_text.place(x=0, y=90)

        # 홈 맨 아래 아이콘들
        home1Btn = tk.Button(self, image=self.home1Img, bd=0, background="black" ,relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home1Btn.place(x=5, y=860)

        home2Btn = tk.Button(self, image=self.home2Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home2Btn.place(x=95, y=860)

        home3Btn = tk.Button(self, image=self.home3Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home3Btn.place(x=185, y=860)

        home4Btn = tk.Button(self, image=self.home4Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home4Btn.place(x=275, y=860)

        home5Btn = tk.Button(self, image=self.home5Img, bd=0, background="black", relief="flat", activebackground="black", highlightthickness=0, command=self.controller.show)
        home5Btn.place(x=365, y=860)

# ==== 실행 ====
if __name__ == "__main__":
    app = App()
    app.mainloop()