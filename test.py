import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# 친구 항목 생성 함수
def create_friend_item(parent, name, status, image_path):
    frame = tk.Frame(parent, bg="white", bd=1, relief="solid")

    # 친구 클릭 시 하이라이트 처리
    def on_click(event):
        for child in parent.winfo_children():
            child.configure(bg="white")
        frame.configure(bg="#e0f0ff")

    frame.bind("<Button-1>", on_click)

    try:
        img = Image.open(image_path).resize((40, 40))
    except:
        img = Image.new("RGB", (40, 40), color="gray")  # 이미지 불러오기 실패 시 회색 대체

    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(frame, image=photo, bg="white")
    image_label.image = photo
    image_label.pack(side="left", padx=10, pady=5)

    text_frame = tk.Frame(frame, bg="white")
    name_label = tk.Label(text_frame, text=name, font=("Arial", 12, "bold"), anchor="w", bg="white")
    status_label = tk.Label(text_frame, text=status, font=("Arial", 10), anchor="w", bg="white", fg="gray")

    name_label.pack(anchor="w")
    status_label.pack(anchor="w")
    text_frame.pack(side="left", fill="x", expand=True)

    frame.pack(fill="x", pady=2, padx=5)
    return frame

# 마우스휠 이벤트를 자식 위젯까지 전달
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def bind_mousewheel_recursive(widget):
    widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    for child in widget.winfo_children():
        bind_mousewheel_recursive(child)

# 샘플 친구 데이터
friend_data = [
    {"name": "Alice", "status": "Online", "image": "avatar1.png"},
    {"name": "Bob", "status": "Busy", "image": "avatar2.png"},
    {"name": "Charlie", "status": "Away", "image": "avatar3.png"},
    {"name": "Diana", "status": "Offline", "image": "avatar4.png"},
    {"name": "Eve", "status": "Online", "image": "avatar5.png"},
]

# 메인 윈도우 설정
root = tk.Tk()
root.title("SNS 친구 목록")
root.geometry("300x400")
root.configure(bg="white")

# 캔버스 + 스크롤 영역 생성
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg="white")

# 캔버스에 스크롤 가능한 프레임 넣기
scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# 크기 동기화
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_configure)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 친구 항목 생성 및 이벤트 바인딩
for friend in friend_data:
    frame = create_friend_item(scrollable_frame, friend["name"], friend["status"], friend["image"])
    bind_mousewheel_recursive(frame)

root.mainloop()