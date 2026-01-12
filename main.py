import tkinter as tk

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("紅語錄")
        self.configure(bg="red")
        self.resizable(False, False)
        self.init_screen()
        self.main_page()
        
    def init_screen(self):
        self.update_idletasks()
        w = 360
        h = 360
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        
    def main_page(self):
        style_common = {
            "bg": "gold",
            "activebackground": "orange",
            "relief": "groove",
            "bd": 2,
            "font": ("", 12, "bold"),}
        box = tk.Frame(self, bg="red", bd=1, relief="solid")
        box.pack(expand=True, fill="both")

        btn1 = tk.Button(box, text="<每日一語>", **style_common)
        btn1.grid(row=2, column=0, padx=5, pady=5, ipadx=16, ipady=8)

        btn2 = tk.Button(box, text="<紅色電台>", **style_common)
        btn2.grid(row=0, column=1, padx=5, pady=5, ipadx=16, ipady=8)

if __name__ == "__main__":
    app = UI()
    app.mainloop()
