import tkinter as tk
import Frames

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Threads")
        self.geometry("471x954")
        self.resizable(False, False)

        self.frames = {}

        for F in (Frames.LoginPage, Frames.JoinPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# ==== 실행 ====
if __name__ == "__main__":
    app = App()
    app.mainloop()