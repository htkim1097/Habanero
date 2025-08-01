import tkinter as tk
from PIL import ImageTk, Image

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


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        bgImg = ImageTk.PhotoImage(Image.open('Threads.png'))
        label = tk.Label(self, image=bgImg)
        label.image = bgImg  # 이미지 참조 유지
        label.place(x=-2, y=-2)

        idImg = ImageTk.PhotoImage(Image.open('id.png'))
        idLabel = tk.Label(self, image=idImg)
        idLabel.image = idImg
        idLabel.place(x=30, y=420)

        idEntry = tk.Entry(self, bd=0, fg="gray")
        idEntry.place(x=60, y=450)
        idEntry.insert(0, "사용자 아이디")

        pwImg = ImageTk.PhotoImage(Image.open('id.png'))
        pwLabel = tk.Label(self, image=pwImg)
        pwLabel.image = pwImg
        pwLabel.place(x=30, y=500)

        pwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        pwEntry.place(x=60, y=530)
        pwEntry.insert(0, "비밀번호")

        loginBtnImg = ImageTk.PhotoImage(Image.open('loginBtn.png'))
        loginBtn = tk.Button(self, image=loginBtnImg, bd=0, command=self.login_action)
        loginBtn.image = loginBtnImg
        loginBtn.place(x=30, y=595)

        joinBtnImg = ImageTk.PhotoImage(Image.open('join.png'))
        joinBtn = tk.Button(self, image=joinBtnImg, bd=0,
                            command=lambda: controller.show_frame("JoinPage"))
        joinBtn.image = joinBtnImg
        joinBtn.place(x=160, y=895)

    def login_action(self):
        print("로그인 버튼 클릭됨")


class JoinPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="회원가입 화면입니다", font=("Apple SD Gothic Neo", 24))
        label.pack(pady=200)

        back_btn = tk.Button(self, text="뒤로", command=lambda: controller.show_frame("LoginPage"))
        back_btn.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()