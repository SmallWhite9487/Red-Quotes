import tkinter as tk
from PIL import Image, ImageTk
import os

def init_windows():
    global UI
    UI = tk.Tk()
    UI.title("紅語錄")
    UI.configure(bg="red")
    UI.resizable(False, False)
    
    w, h = 360, 360
    x = (UI.winfo_screenwidth() // 2) - (w // 2)
    y = (UI.winfo_screenheight() // 2) - (h // 2)
    UI.geometry(f"{w}x{h}+{x}+{y}")

def set_screen(w, h):
    UI.update_idletasks()
    x = UI.winfo_x()
    y = UI.winfo_y()
    UI.geometry(f"{w}x{h}+{x}+{y}")

def main_page():
    try:
        set_screen(360,360)
        style_title = {
            "bg": "red",
            "fg": "gold",
            "font": ("", 32, "bold"),
        }
        style_subtitle = {
            "bg": "red",
            "fg": "gold",
            "font": ("", 12, "bold"),
        }
        style_common = {
            "bg": "gold",
            "font": ("", 16, "bold"),
        }
        tk.Label(UI, text="=红语录=", **style_title).pack(pady=10)
        # ICON
        img = Image.open(os.path.join(os.getcwd(), "data", "mainpage_icon.png"))
        img = img.resize((160, 160))
        icon_img = ImageTk.PhotoImage(img)
        tk.Label(UI, image=icon_img, bg="red").pack(pady=5)
        
        # OPTIONS
        options_frame = tk.Frame(UI, bg="red")
        of1 = tk.Frame(options_frame, bg="red")
        tk.Button(of1, text="<每日一语>", **style_common).pack(side="left", padx=10)
        tk.Button(of1, text="<红色电台>", **style_common).pack(side="left", padx=10)
        of1.pack(pady=5)
        
        of2 = tk.Frame(options_frame, bg="red")
        tk.Label(of2, text="由 小白SmallWhite 整理", **style_subtitle).pack(side="left", padx=10)
        of2.pack(side="left", pady=5)
        options_frame.pack(side="top", pady=10)
    except Exception as e:
        print(f"Error in main_page: {e}")

if __name__ == "__main__":
    init_windows()
    main_page()
    UI.mainloop()
