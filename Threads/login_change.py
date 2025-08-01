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

        for F in (LoginPage, JoinPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


def on_entry_click(entry, string):
    if entry.get() == string:
        entry.delete(0, tk.END)


def on_focusout(entry, string):
    if entry.get() == "":
        entry.insert(0, string)


# 로그인 화면 실행
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        global bgImg, loginImg, joinImg, idImg, pwImg

        #bimg = Image.open('Threads.png')
        bgImg = ImageTk.PhotoImage(Image.open('images/Threads.png'))

        # 배경을 Label을 이용하여 처리
        label = tk.Label(self, image=bgImg)
        label.place(x=-2, y=-2)


        # 로그인 아이디 입력
        #iImg = Image.open('id.png')
        idImg = ImageTk.PhotoImage(Image.open('images/id.png'))
        idLabel = tk.Label(self, image=idImg)
        idLabel.place(x=30, y=420)

        idEntry = tk.Entry(self, bd=0, fg="gray")
        idEntry.place(x=60, y=450)
        idEntry.insert(0, "사용자 아이디")
        idEntry.bind('<Button-1>', lambda e: on_entry_click(idEntry, "사용자 아이디"))
        idEntry.bind('<FocusOut>', lambda e: on_focusout(idEntry, "사용자 아이디"))


        # 로그인 비밀번호 입력
        pImg = Image.open('id.png')
        pwImg = ImageTk.PhotoImage(pImg)
        pwLabel = tk.Label(self, image=pwImg)
        pwLabel.place(x=30, y=500)
        pwEntry = tk.Entry(self, bd=0, fg="gray")
        pwEntry.place(x=60, y=530)
        pwEntry.insert(0, "비밀번호")
        pwEntry.bind('<Button-1>', lambda e: on_entry_click(pwEntry, "비밀번호"))
        pwEntry.bind('<FocusOut>', lambda e: on_focusout(pwEntry, "비밀번호"))


        # 로그인 파란색 버튼
        lImg = Image.open('images/loginBtn.png')
        loginImg = ImageTk.PhotoImage(lImg)
        loginBtn = tk.Button(self, image=loginImg, bd=0, command=show)
        loginBtn.place(x=30, y=595)


        # 회원가입
        jImg = Image.open('images/join.png')
        joinImg = ImageTk.PhotoImage(jImg)
        joinBtn = tk.Button(self, image=joinImg, bd=0, command=lambda: controller.show_frame("JoinPage"))
        joinBtn.place(x=160, y=895)



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
        nImg = Image.open('images/id.png')
        nameImg = ImageTk.PhotoImage(nImg)
        nameLabel = tk.Label(self, image=nameImg)
        nameLabel.place(x=30, y=340)

        nameEntry = tk.Entry(self, bd=0, fg="gray")
        nameEntry.place(x=60, y=370)
        nameEntry.insert(0, "사용자 이름")
        nameEntry.bind('<Button-1>', lambda e: on_entry_click(nameEntry, "사용자 이름"))
        nameEntry.bind('<FocusOut>', lambda e: on_focusout(nameEntry, "사용자 이름"))


        # 회원가입 아이디 입력
        jiImg = Image.open('id.png')
        jidImg = ImageTk.PhotoImage(jiImg)
        jidLabel = tk.Label(self, image=jidImg)
        jidLabel.place(x=30, y=420)

        jidEntry = tk.Entry(self, bd=0, fg="gray")
        jidEntry.place(x=60, y=450)
        jidEntry.insert(0, "사용자 아이디")
        jidEntry.bind('<Button-1>', lambda e: on_entry_click(jidEntry, "사용자 아이디"))
        jidEntry.bind('<FocusOut>', lambda e: on_focusout(jidEntry, "사용자 아이디"))


        # 회원가입 비밀번호 입력
        jpImg = Image.open('id.png')
        jpwImg = ImageTk.PhotoImage(jpImg)
        jpwLabel = tk.Label(self, image=jpwImg)
        jpwLabel.place(x=30, y=500)
        jpwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        jpwEntry.place(x=60, y=530)
        jpwEntry.insert(0, "비밀번호")
        jpwEntry.bind('<Button-1>', lambda e: on_entry_click(jpwEntry, "비밀번호"))
        jpwEntry.bind('<FocusOut>', lambda e: on_focusout(jpwEntry, "비밀번호"))


        # 회원가입 파란색 버튼
        jlImg = Image.open('images/joinBtn.png')
        jloginImg = ImageTk.PhotoImage(jlImg)
        jloginBtn = tk.Button(self, image=jloginImg, bd=0, command=show)
        jloginBtn.place(x=68, y=850)



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