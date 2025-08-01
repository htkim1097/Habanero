import tkinter as tk
import tkinter.font
from tkinter import *
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


def on_entry_click(entry, string):
    if entry.get() == string:
        entry.delete(0, tk.END)


def on_focusout(entry, string):
    if entry.get() == "":
        entry.insert(0, string)


# 로그인 화면 실행 함수
# def login():
#     global bgImg, loginImg, joinImg, idImg, pwImg
#
#     bimg = Image.open('Threads.png')
#     bgImg = ImageTk.PhotoImage(bimg)
#
#     # 배경을 Label을 이용하여 처리
#     label = Label(window, image=bgImg)
#     label.place(x=-2, y=-2)
#
#     # 테스트용
#     # label2 = Label(window, text="안녕하세요", font=("궁서체", 24), bg='#2E2E30', fg='white')
#     # label2.place(x=3, y=5)
#
#
#     # 로그인 아이디 입력
#     iImg = Image.open('id.png')
#     idImg = ImageTk.PhotoImage(iImg)
#     idLabel = Label(window, image=idImg)
#     idLabel.place(x=30, y=420)
#     idEntry = Entry(window, bd=0, fg="gray")
#     idEntry.place(x=60, y=450)
#     idEntry.insert(0, "사용자 아이디")
#     idEntry.bind('<Button-1>', lambda e: on_entry_click(idEntry, "사용자 아이디"))
#     idEntry.bind('<FocusOut>', lambda e: on_focusout(idEntry, "사용자 아이디"))
#
#
#     # 로그인 비밀번호 입력
#     pImg = Image.open('id.png')
#     pwImg = ImageTk.PhotoImage(pImg)
#     pwLabel = Label(window, image=pwImg)
#     pwLabel.place(x=30, y=500)
#     pwEntry = Entry(window, bd=0, fg="gray")
#     pwEntry.place(x=60, y=530)
#     pwEntry.insert(0, "비밀번호")
#     pwEntry.bind('<Button-1>', lambda e: on_entry_click(pwEntry, "비밀번호"))
#     pwEntry.bind('<FocusOut>', lambda e: on_focusout(pwEntry, "비밀번호"))
#
#
#     # 로그인 파란색 버튼
#     lImg = Image.open('loginBtn.png')
#     loginImg = ImageTk.PhotoImage(lImg)
#     loginBtn = Button(window, image=loginImg, bd=0, command=show)
#     loginBtn.place(x=30, y=595)
#
#
#     # 회원가입
#     jImg = Image.open('join.png')
#     joinImg = ImageTk.PhotoImage(jImg)
#     joinBtn = Button(window, image=joinImg, bd=0, command=show)
#     joinBtn.place(x=160, y=895)



# 회원가입 화면 실행 함수
def join():
    global nameImg, jidImg, jpwImg, jloginImg

    # 배경
    label = Label(window, bg="white")
    label.place(x=-2, y=-2)

    # 배경
    joinFont = tk.font.Font(family="돋움", size=25)
    jlabel = tk.Label(window, text="회원가입", font=joinFont)
    jlabel.place(x=20, y=250)

    # 회원가입 이름 입력
    nImg = Image.open('id.png')
    nameImg = ImageTk.PhotoImage(nImg)
    nameLabel = Label(window, image=nameImg)
    nameLabel.place(x=30, y=340)

    nameEntry = Entry(window, bd=0, fg="gray")
    nameEntry.place(x=60, y=370)
    nameEntry.insert(0, "사용자 이름")
    nameEntry.bind('<Button-1>', lambda e: on_entry_click(nameEntry, "사용자 이름"))
    nameEntry.bind('<FocusOut>', lambda e: on_focusout(nameEntry, "사용자 이름"))


    # 회원가입 아이디 입력
    jiImg = Image.open('id.png')
    jidImg = ImageTk.PhotoImage(jiImg)
    jidLabel = Label(window, image=jidImg)
    jidLabel.place(x=30, y=420)

    jidEntry = Entry(window, bd=0, fg="gray")
    jidEntry.place(x=60, y=450)
    jidEntry.insert(0, "사용자 아이디")
    jidEntry.bind('<Button-1>', lambda e: on_entry_click(jidEntry, "사용자 아이디"))
    jidEntry.bind('<FocusOut>', lambda e: on_focusout(jidEntry, "사용자 아이디"))


    # 회원가입 비밀번호 입력
    jpImg = Image.open('id.png')
    jpwImg = ImageTk.PhotoImage(jpImg)
    jpwLabel = Label(window, image=jpwImg)
    jpwLabel.place(x=30, y=500)
    jpwEntry = Entry(window, bd=0, fg="gray")
    jpwEntry.place(x=60, y=530)
    jpwEntry.insert(0, "비밀번호")
    jpwEntry.bind('<Button-1>', lambda e: on_entry_click(jpwEntry, "비밀번호"))
    jpwEntry.bind('<FocusOut>', lambda e: on_focusout(jpwEntry, "비밀번호"))


    # 회원가입 파란색 버튼
    jlImg = Image.open('joinBtn.png')
    jloginImg = ImageTk.PhotoImage(jlImg)
    jloginBtn = Button(window, image=jloginImg, bd=0, command=show)
    jloginBtn.place(x=68, y=850)



# ==== 실행 ====
window = tk.Tk()
window.title("Threads")
window.geometry("471x954")

# 로그인 화면
#login()
join()

window.mainloop()


# 영문 폰트 SF Pro text, 한글폰트 Apple SD Gothic Neo
# threadsFont = tk.font.Font(family="Apple SD Gothic Neo", size=12, weight="bold", overstrike=False)