import tkinter as tk
from PIL import Image, ImageTk
import os

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("紅語錄")
        self.configure(bg="red")
        self.resizable(False, False)
        self.init_screen()
        self.main_page()
        
    def init_screen(self):
        w = 360
        h = 360
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        
    def main_page(self):
        style_title = {
            "bg": "red",
            "fg": "gold",
            "font": ("", 32, "bold"),}
        style_subtitle = {
            "bg": "red",
            "fg": "gold",
            "font": ("", 12, "bold"),}
        style_common = {
            "bg": "gold",
            "font": ("", 16, "bold"),}
        tk.Label(self, text="=红语录=", **style_title).pack(pady=10)
        
        ## ICON
        img = Image.open(os.path.join(os.getcwd(), "data", "mainpage_icon.png"))
        img = img.resize((160, 160))
        self.icon_img = ImageTk.PhotoImage(img)
        tk.Label(self, image=self.icon_img, bg="red").pack(pady=5)
        
        ## OPTIONS
        options_frame = tk.Frame(self, bg="red")
        of1 = tk.Frame(options_frame, bg="red")
        tk.Button(of1, text="<每日一语>", **style_common).pack(side="left", padx=10)
        tk.Button(of1, text="<红色电台>", **style_common).pack(side="left", padx=10)
        of1.pack(pady=5)
        
        of2 = tk.Frame(options_frame, bg="red")
        tk.Label(of2, text="由 小白SmallWhite 整理", **style_subtitle).pack(side="left", padx=10)
        of2.pack(side="left", pady=5)
        options_frame.pack(side="top", pady=10)

if __name__ == "__main__":
    app = UI()
    app.mainloop()
