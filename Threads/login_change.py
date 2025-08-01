import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image


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
img_path = "../images/"


# 테스트용
def show():
    print("hello")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Threads")
        self.geometry("471x954")
        self.resizable(False, False)

        self.frames = {}

        for F in (LoginPage, JoinPage, HomePage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("LoginPage")
        #self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


# 빈칸 클릭 시 글씨 삭제
def on_entry_click(entry, string):
    if entry.get() == string:
        entry.delete(0, tk.END)

def on_focusout(entry, string):
    if entry.get() == "":
        entry.insert(0, string)

# 로그인 에러 창 출력
def show_error_popup(controller):
    login_frame = controller.frames["LoginPage"]
    login_frame.error_frame.place(x=60, y=300)

def show_complete_popup(controller):
    join_frame = controller.frames["JoinPage"]
    join_frame.complete_frame.place(x=60, y=300)


# 로그인 화면 실행
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        global bgImg, loginImg, joinImg, idImg, pwImg, errorImg, closeImg, checkImg

        bgImg = ImageTk.PhotoImage(Image.open(img_path + 'Threads.png'))

        # 배경
        label = tk.Label(self, image=bgImg)
        label.place(x=-2, y=-2)

        # 로그인 아이디 입력
        idImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        idLabel = tk.Label(self, image=idImg)
        idLabel.place(x=30, y=420)

        idEntry = tk.Entry(self, bd=0, fg="gray")
        idEntry.place(x=60, y=450)
        idEntry.insert(0, "사용자 아이디")
        idEntry.bind('<Button-1>', lambda e: on_entry_click(idEntry, "사용자 아이디"))
        idEntry.bind('<FocusOut>', lambda e: on_focusout(idEntry, "사용자 아이디"))

        # 로그인 비밀번호 입력
        pwImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        pwLabel = tk.Label(self, image=pwImg)
        pwLabel.place(x=30, y=500)

        pwEntry = tk.Entry(self, bd=0, fg="gray")
        pwEntry.place(x=60, y=530)
        pwEntry.insert(0, "비밀번호")
        pwEntry.bind('<Button-1>', lambda e: on_entry_click(pwEntry, "비밀번호"))
        pwEntry.bind('<FocusOut>', lambda e: on_focusout(pwEntry, "비밀번호"))

        # 로그인 파란색 버튼
        lImg = Image.open(img_path + 'loginBtn.png')
        loginImg = ImageTk.PhotoImage(lImg)
        # 홈 화면 출력
        loginBtn = tk.Button(self, image=loginImg, bd=0, command=lambda: controller.show_frame("HomePage"))
        # 로그인 실패 창 출력
        #loginBtn = tk.Button(self, image=loginImg, bd=0, command=lambda: show_error_popup(controller))

        loginBtn.place(x=30, y=595)

        # 회원가입
        joinImg = ImageTk.PhotoImage(Image.open(img_path + 'join.png'))
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
        nameImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        nameLabel = tk.Label(self, image=nameImg)
        nameLabel.place(x=30, y=340)

        nameEntry = tk.Entry(self, bd=0, fg="gray")
        nameEntry.place(x=60, y=370)
        nameEntry.insert(0, "사용자 이름")
        nameEntry.bind('<Button-1>', lambda e: on_entry_click(nameEntry, "사용자 이름"))
        nameEntry.bind('<FocusOut>', lambda e: on_focusout(nameEntry, "사용자 이름"))


        # 회원가입 아이디 입력
        jidImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        jidLabel = tk.Label(self, image=jidImg)
        jidLabel.place(x=30, y=420)

        jidEntry = tk.Entry(self, bd=0, fg="gray")
        jidEntry.place(x=60, y=450)
        jidEntry.insert(0, "사용자 아이디")
        jidEntry.bind('<Button-1>', lambda e: on_entry_click(jidEntry, "사용자 아이디"))
        jidEntry.bind('<FocusOut>', lambda e: on_focusout(jidEntry, "사용자 아이디"))

        # 회원가입 비밀번호 입력
        jpwImg = ImageTk.PhotoImage(Image.open(img_path + 'id.png'))
        jpwLabel = tk.Label(self, image=jpwImg)
        jpwLabel.place(x=30, y=500)

        jpwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        jpwEntry.place(x=60, y=530)
        jpwEntry.insert(0, "비밀번호")
        jpwEntry.bind('<Button-1>', lambda e: on_entry_click(jpwEntry, "비밀번호"))
        jpwEntry.bind('<FocusOut>', lambda e: on_focusout(jpwEntry, "비밀번호"))

        # 회원가입 파란색 버튼
        jloginImg = ImageTk.PhotoImage(Image.open(img_path + 'joinBtn.png'))
        jloginBtn = tk.Button(self, image=jloginImg, bd=0, command=show)
        jloginBtn.place(x=68, y=850)



# 홈 화면
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        global homeLeftImg, homeLogoImg, homeRightImg, home1Img, home2Img, home3Img, home4Img, home5Img

        # 배경
        self.configure(bg="black")

        # 홈 맨 왼쪽 위
        homeLeftImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLeft.png'))
        homeLeftBtn = tk.Button(self, image=homeLeftImg, bd=0, background="black" ,relief="flat", highlightthickness=0, command=show)
        homeLeftBtn.place(x=0, y=0)

        # 홈 맨 위 가운데 로고
        homeLogoImg = ImageTk.PhotoImage(Image.open(img_path + 'homeLogo.png'))
        homeLogoBtn = tk.Button(self, image=homeLogoImg, bd=0, background="black" ,relief="flat", highlightthickness=0, command=show)
        homeLogoBtn.place(x=175, y=0)

        # 홈 맨 위 오른쪽
        homeRightImg = ImageTk.PhotoImage(Image.open(img_path + 'homeRight.png'))
        homeRightBtn = tk.Button(self, image=homeRightImg, bd=0, background="black" ,relief="flat", highlightthickness=0, command=show)
        homeRightBtn.place(x=350, y=0)

        # 홈 맨 아래 아이콘들
        home1Img = ImageTk.PhotoImage(Image.open(img_path + 'home1.png'))
        home1Btn = tk.Button(self, image=home1Img, bd=0, background="black" ,relief="flat", highlightthickness=0, command=show)
        home1Btn.place(x=5, y=860)

        home2Img = ImageTk.PhotoImage(Image.open(img_path + 'home2.png'))
        home2Btn = tk.Button(self, image=home2Img, bd=0, background="black", relief="flat", highlightthickness=0, command=show)
        home2Btn.place(x=95, y=860)

        home3Img = ImageTk.PhotoImage(Image.open(img_path + 'home3.png'))
        home3Btn = tk.Button(self, image=home3Img, bd=0, background="black", relief="flat", highlightthickness=0, command=show)
        home3Btn.place(x=185, y=860)

        home4Img = ImageTk.PhotoImage(Image.open(img_path + 'home4.png'))
        home4Btn = tk.Button(self, image=home4Img, bd=0, background="black", relief="flat", highlightthickness=0, command=show)
        home4Btn.place(x=275, y=860)

        home5Img = ImageTk.PhotoImage(Image.open(img_path + 'home5.png'))
        home5Btn = tk.Button(self, image=home5Img, bd=0, background="black", relief="flat", highlightthickness=0, command=show)
        home5Btn.place(x=365, y=860)



# ==== 실행 ====

if __name__ == "__main__":
    app = App()
    app.mainloop()

# window = tk.Tk()
# window.title("Threads")
# window.geometry("471x954")
#
# # 로그인 화면
# #login()
# JoinPage.join()
#
# window.mainloop()


# 영문 폰트 SF Pro text, 한글폰트 Apple SD Gothic Neo
# threadsFont = tk.font.Font(family="Apple SD Gothic Neo", size=12, weight="bold", overstrike=False)