import tkinter as tk
from email.message import Message
from tkinter import font, Frame, Button
from PIL import ImageTk, Image

from App import img_path
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

        for F in (LoginPage, JoinPage, HomePage, MyPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        #self.show_frame("LoginPage")
        #self.show_frame("HomePage")
        self.show_frame("MyPage")


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

# 회원 가입 완료 창 출력
def show_complete_popup(controller):
    join_frame = controller.frames["JoinPage"]
    join_frame.complete_frame.place(x=60, y=300)


# 로그인 화면 실행
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bgImg = ImageTk.PhotoImage(Image.open(img_path+'Threads.png'))

        # 배경
        label = tk.Label(self, image=self.bgImg)
        label.place(x=-2, y=-2)

        # 로그인 아이디 입력
        self.idImg = ImageTk.PhotoImage(Image.open(img_path+'id.png'))
        idLabel = tk.Label(self, image=self.idImg)
        idLabel.place(x=30, y=420)

        idEntry = tk.Entry(self, bd=0, fg="gray")
        idEntry.place(x=60, y=450)
        idEntry.insert(0, "사용자 아이디")
        idEntry.bind('<Button-1>', lambda e: on_entry_click(idEntry, "사용자 아이디"))
        idEntry.bind('<FocusOut>', lambda e: on_focusout(idEntry, "사용자 아이디"))

        # 로그인 비밀번호 입력
        self.pwImg = ImageTk.PhotoImage(Image.open(img_path+'id.png'))
        pwLabel = tk.Label(self, image=self.pwImg)
        pwLabel.place(x=30, y=500)

        pwEntry = tk.Entry(self, bd=0, fg="gray")
        pwEntry.place(x=60, y=530)
        pwEntry.insert(0, "비밀번호")
        pwEntry.bind('<Button-1>', lambda e: on_entry_click(pwEntry, "비밀번호"))
        pwEntry.bind('<FocusOut>', lambda e: on_focusout(pwEntry, "비밀번호"))

        # 로그인 파란색 버튼
        self.lImg = Image.open(img_path+'loginBtn.png')
        self.loginImg = ImageTk.PhotoImage(self.lImg)
        # 홈 화면 출력
        loginBtn = tk.Button(self, image=self.loginImg, bd=0, command=lambda: controller.show_frame("HomePage"))
        # 로그인 실패 창 출력
        #loginBtn = tk.Button(self, image=self.loginImg, bd=0, command=lambda: show_error_popup(controller))

        loginBtn.place(x=30, y=595)

        # 회원가입
        self.joinImg = ImageTk.PhotoImage(Image.open(img_path+'join.png'))
        joinBtn = tk.Button(self, image=self.joinImg, bd=0, command=lambda: controller.show_frame("JoinPage"))
        joinBtn.place(x=160, y=895)

        # 로그인 에러 창
        self.error_frame = tk.Frame(self, width=350, height=180, bg="white")
        self.error_frame.place(x=60, y=400)
        self.error_frame.place_forget()

        self.errorImg = ImageTk.PhotoImage(Image.open(img_path+"error.png"))
        frame = tk.Label(self.error_frame, image=self.errorImg, bg="white")
        frame.image = self.errorImg
        frame.pack()

        self.closeImg = ImageTk.PhotoImage(Image.open(img_path+"close.png"))
        closeBtn = tk.Button(self.error_frame, image=self.closeImg, bd=0, command=self.hide_error)
        closeBtn.image = self.closeImg
        closeBtn.place(x=300, y=15)

        self.checkImg = ImageTk.PhotoImage(Image.open(img_path+"check.png"))
        checkBtn = tk.Button(self.error_frame, image=self.checkImg, bd=0, command=self.hide_error)
        checkBtn.image = self.checkImg
        checkBtn.place(x=280, y=130)

    def hide_error(self):
        self.error_frame.place_forget()



# 회원가입 화면 실행
class JoinPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 배경
        label = tk.Label(self, bg="white")
        label.place(x=-2, y=-2)

        # 배경
        joinFont = tk.font.Font(family="돋움", size=25)
        jlabel = tk.Label(self, text="회원가입", font=joinFont)
        jlabel.place(x=20, y=250)

        # 회원가입 이름 입력
        self.nameImg = ImageTk.PhotoImage(Image.open(img_path+'id.png'))
        nameLabel = tk.Label(self, image=self.nameImg)
        nameLabel.place(x=30, y=340)

        nameEntry = tk.Entry(self, bd=0, fg="gray")
        nameEntry.place(x=60, y=370)
        nameEntry.insert(0, "사용자 이름")
        nameEntry.bind('<Button-1>', lambda e: on_entry_click(nameEntry, "사용자 이름"))
        nameEntry.bind('<FocusOut>', lambda e: on_focusout(nameEntry, "사용자 이름"))


        # 회원가입 아이디 입력
        self.jidImg = ImageTk.PhotoImage(Image.open(img_path+'id.png'))
        jidLabel = tk.Label(self, image=self.jidImg)
        jidLabel.place(x=30, y=420)

        jidEntry = tk.Entry(self, bd=0, fg="gray")
        jidEntry.place(x=60, y=450)
        jidEntry.insert(0, "사용자 아이디")
        jidEntry.bind('<Button-1>', lambda e: on_entry_click(jidEntry, "사용자 아이디"))
        jidEntry.bind('<FocusOut>', lambda e: on_focusout(jidEntry, "사용자 아이디"))

        # 회원가입 비밀번호 입력
        self.jpwImg = ImageTk.PhotoImage(Image.open(img_path+'id.png'))
        jpwLabel = tk.Label(self, image=self.jpwImg)
        jpwLabel.place(x=30, y=500)

        jpwEntry = tk.Entry(self, bd=0, fg="gray", show="*")
        jpwEntry.place(x=60, y=530)
        jpwEntry.insert(0, "비밀번호")
        jpwEntry.bind('<Button-1>', lambda e: on_entry_click(jpwEntry, "비밀번호"))
        jpwEntry.bind('<FocusOut>', lambda e: on_focusout(jpwEntry, "비밀번호"))

        # 회원가입 파란색 버튼
        self.jloginImg = ImageTk.PhotoImage(Image.open(img_path+'joinBtn.png'))
        jloginBtn = tk.Button(self, image=self.jloginImg, bd=0, command=show)
        jloginBtn.place(x=68, y=850)



# 홈 화면
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 배경
        self.configure(bg="black")

        # 홈 맨 왼쪽 위
        self.homeLeftImg = ImageTk.PhotoImage(Image.open(img_path+'homeLeft.png'))
        homeLeftBtn = tk.Button(self, image=self.homeLeftImg, bd=0, background="black" ,relief="flat", highlightthickness=0,activebackground="black", command=show)
        homeLeftBtn.place(x=0, y=0)

        # 홈 맨 위 가운데 로고
        self.homeLogoImg = ImageTk.PhotoImage(Image.open(img_path+'homeLogo.png'))
        homeLogoBtn = tk.Button(self, image=self.homeLogoImg, bd=0, background="black" ,relief="flat", highlightthickness=0,activebackground="black", command=show)
        homeLogoBtn.place(x=175, y=0)

        # 홈 맨 위 오른쪽
        self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path+'homeRight.png'))
        homeRightBtn = tk.Button(self, image=self.homeRightImg, bd=0, background="black" ,relief="flat", highlightthickness=0,activebackground="black", command=show)
        homeRightBtn.place(x=350, y=0)

        # 홈 맨 아래 아이콘들
        self.home1Img = ImageTk.PhotoImage(Image.open(img_path+'home1.png'))
        home1Btn = tk.Button(self, image=self.home1Img, bd=0, background="black" ,relief="flat", highlightthickness=0,activebackground="black", command=show)
        home1Btn.place(x=5, y=860)

        self.home2Img = ImageTk.PhotoImage(Image.open(img_path+'home2.png'))
        home2Btn = tk.Button(self, image=self.home2Img, bd=0, background="black", relief="flat", highlightthickness=0,activebackground="black", command=show)
        home2Btn.place(x=95, y=860)

        self.home3Img = ImageTk.PhotoImage(Image.open(img_path+'home3.png'))
        home3Btn = tk.Button(self, image=self.home3Img, bd=0, background="black", relief="flat", highlightthickness=0,activebackground="black", command=show)
        home3Btn.place(x=185, y=860)

        self.home4Img = ImageTk.PhotoImage(Image.open(img_path+'home4.png'))
        home4Btn = tk.Button(self, image=self.home4Img, bd=0, background="black", relief="flat", highlightthickness=0,activebackground="black", command=show)
        home4Btn.place(x=275, y=860)

        self.home5Img = ImageTk.PhotoImage(Image.open(img_path+'home5.png'))
        home5Btn = tk.Button(self, image=self.home5Img, bd=0, background="black", relief="flat", highlightthickness=0,activebackground="black",  command=lambda: controller.show_frame("MyPage"))
        home5Btn.place(x=365, y=860)



#마이 페이지 화면
class MyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_tab = None #현재 선택된 탭

        #테스트용 데이터
        Message = {
            "id": "_oserra",
            "name": "세라",
            "profile_img":"../images/명수.png",
            "followers": 41,
            "bio": "집에 가고 싶어요"
        }
        self.name_text = Message['name'] #이름 저장

        #홈 화면 기본 설정
        self.home = HomePage(self, controller)
        self.home.place(x=0, y=0, relwidth=1, relheight=1)

        self.profile_img = ImageTk.PhotoImage(Image.open(Message['profile_img']).resize((60, 60)))


        # 상단 프로필 프레임
        FrameTop = tk.Frame(self, bg="black", height=240)
        FrameTop.pack(side="top", fill="x")

        name_label = tk.Label(FrameTop, text=f"{Message['name']}", fg="white", bg="black", font=("Arial", 22, 'bold') )
        name_label.place(x=30, y=140)

        self.edit_nameImg = ImageTk.PhotoImage(Image.open(img_path+'edit_name.png').resize((13, 13)))
        edit_nameBtn = tk.Button(FrameTop, image=self.edit_nameImg, bd=0,background="black", relief="flat", highlightthickness=0, activebackground="black", command=show )
        edit_nameBtn.place(x=95, y=160)

        self.id_label = tk.Label(FrameTop, text=f"{Message['id']}", fg="white", bg="black", font=("Arial", 12) )
        self.id_label.place(x=30, y=180)

        follows_cnt_label = tk.Label(FrameTop, text=f"{Message['followers']}" + 'followers', fg="gray", bg="black", font=("Arial", 11))
        follows_cnt_label.place(x=30, y=215)

        profile_label = tk.Label(FrameTop,image = self.profile_img, fg="white", bg="black")
        profile_label.place(x=380, y=110) #데이터 값 가져오기

        self.edit_profileImg = ImageTk.PhotoImage(Image.open(img_path+'edit_profile.png').resize((20, 20)))
        edit_profileBtn = tk.Button(FrameTop, image=self.edit_profileImg, bd=0,background="black", relief="flat", highlightthickness=0, activebackground="black", command=show )
        edit_profileBtn.place(x=442, y=155) #임시 위치 # 파일 선택 창 띄우기


        self.homeRightImg = ImageTk.PhotoImage(Image.open(img_path+'homeRight.png'))
        homeRightBtn = tk.Button(FrameTop, image=self.homeRightImg, bd=0, background="black", relief="flat", highlightthickness=0, activebackground="black", command=show)
        homeRightBtn.place(x=400, y=10)



        #탭 프레임(버튼 배치)
        FrameTabs = tk.Frame(self, bg="black", height=50)
        FrameTabs.pack(side="top", fill="x")

        self.mp1Img = ImageTk.PhotoImage(Image.open(img_path+'mp1.png'))
        self.mp1Btn = tk.Button(FrameTabs, image=self.mp1Img, bd=0, relief="flat", highlightthickness=0, activebackground="black", command=lambda: self.switch_tabs("Threads"))
        self.mp1Btn.place(x=20, y=0)

        self.mp2Img = ImageTk.PhotoImage(Image.open(img_path+'mp2.png'))
        self.mp2Btn = tk.Button(FrameTabs,image=self.mp2Img, bd=0, relief="flat", highlightthickness=0, activebackground="black", command=lambda: self.switch_tabs("Replies"))
        self.mp2Btn.place(x=140, y=0)

        self.mp3Img = ImageTk.PhotoImage(Image.open(img_path+'mp3.png'))
        self.mp3Btn = tk.Button(FrameTabs, image=self.mp3Img, bd=0, relief="flat", highlightthickness=0, activebackground="black", command=lambda: self.switch_tabs("Media"))
        self.mp3Btn.place(x=240, y=0)

        self.mp4Img = ImageTk.PhotoImage(Image.open(img_path+'mp4.png'))
        self.mp4Btn = tk.Button(FrameTabs, image=self.mp4Img, bd=0,  relief="flat", highlightthickness=0, activebackground="black", command=lambda: self.switch_tabs("Reposts"))
        self.mp4Btn.place(x=340, y=0)

        lineFrame = tk.Frame(FrameTabs, bg="#666768")
        lineFrame.pack(fill="x",pady=(50,0))

        #탭 별 프레임 생성
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

            #메시지 라벨
            label = tk.Label(frame, text=frame_messages[name], fg="gray", bg="black",font=("Arial", 12))
            label.pack(pady=200)

            self.frames[name] = frame


        # 탭 선택 시 변경된 이미지
        self.Cgmp1Img = ImageTk.PhotoImage(Image.open(img_path+'Cgmp1.png'))
        self.Cgmp2Img = ImageTk.PhotoImage(Image.open(img_path+'Cgmp2.png'))
        self.Cgmp3Img = ImageTk.PhotoImage(Image.open(img_path+'Cgmp3.png'))
        self.Cgmp4Img = ImageTk.PhotoImage(Image.open(img_path+'Cgmp4.png'))


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

    #탭 전환 시 버튼 이미지 전환
    def switch_tabs(self, tab_name):
        self.show_frame(tab_name)

        for name, btn in self.tab_buttons.items():
            if name == tab_name:
                btn.config(image = self.tab_images[name][1]) #현재 선택된 이미지
            else:
                btn.config(image = self.tab_images[name][0]) #원래 이미지

        self.current_tab = tab_name


    # 프레임 전환
    def show_frame(self, frames_name):
        for name, frame in self.frames.items():
            frame.lower()  # 프레임 숨기기(맨 아래로 이동)
        self.frames[frames_name].lift() #프레임 나타내기


    #프로필 수정 버튼 누르기
    # def click_btn(self):




# ==== 실행 ====

if __name__ == "__main__":
    app = App()
    app.mainloop()
