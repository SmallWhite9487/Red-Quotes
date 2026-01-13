import tkinter as tk
import os
import sqlite3

def init_windows():
    try:
        global UI, debug
        debug = True
        UI = tk.Tk()
        UI.title("红语录")
        UI.configure(bg="red")
        UI.resizable(False, False)
        UI.wm_iconphoto(True, tk.PhotoImage(data=images_b64[1]))
        w, h = 360, 360
        x = (UI.winfo_screenwidth() // 2) - (w // 2)
        y = (UI.winfo_screenheight() // 2) - (h // 2)
        UI.geometry(f"{w}x{h}+{x}+{y}")
    except Exception as e:
        print(f"Error initializing window: {e}")

def set_screen(w, h):
    try:
        UI.update_idletasks()
        x = UI.winfo_x()
        y = UI.winfo_y()
        UI.geometry(f"{w}x{h}+{x}+{y}")
    except Exception as e:
        print(f"Error setting screen size: {e}")

def load_images_b64():
    try:
        global images_b64
        images_b64 = []
        with open(os.path.join(os.getcwd(), "data", "image_base64.txt"), "r", encoding="utf-8") as f:
            images_b64 = f.read().split("###==Splitter==###")
    except Exception as e:
        print(f"Error loading images: {e}")

def DB_insert(lid, quote):
    try:
        conn = sqlite3.connect("data/quotes.db")
        DB = conn.cursor()
        DB.execute("SELECT 1 FROM quotes WHERE LID=? AND quote=?", (lid, quote))
        exists = DB.fetchone()
        if not exists:
            DB.execute("INSERT INTO quotes (LID, quote) VALUES (?, ?)", (lid, quote))
            print(f"Successfully inserted: {lid} - {quote}")
        else:
            print(f"Skipped duplicate entry: {lid} - {quote}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error inserting into database: {e}")

def DB_load():
    try:
        global QUOTES
        conn = sqlite3.connect("data/quotes.db")
        DB = conn.cursor()
        DB.execute("SELECT LID, quote FROM quotes")
        records = DB.fetchall()
        conn.close()
        
        #leaders = ["毛泽东", "刘少奇", "邓小平", "江泽民", "胡锦涛", "习近平"]
        QUOTES = {"M": [], "L": [], "D": [], "J": [], "H": [], "X": []}
        ID2Q = {1: QUOTES["M"], 2: QUOTES["L"], 3: QUOTES["D"], 4: QUOTES["J"], 5: QUOTES["H"], 6: QUOTES["X"]}
        for record in records:
            LID, quote = record
            if LID in ID2Q:
                ID2Q[LID].append(quote)
    except Exception as e:
        print(f"Error loading database: {e}")

def debug_mode():
    try:
        pass
    except Exception as e:
        print(f"Error in debug mode: {e}")

def main_page():
    try:
        global main_page_icon
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
        main_page_icon = tk.PhotoImage(data=images_b64[2])
        tk.Label(UI, image=main_page_icon, bg="red").pack(pady=5)
        
        # OPTIONS
        options_frame = tk.Frame(UI, bg="red")
        of1 = tk.Frame(options_frame, bg="red")
        tk.Button(of1, text="<每日一语>", **style_common).pack(side="left", padx=10)
        tk.Button(of1, text="<红色电台>", **style_common).pack(side="left", padx=10)
        of1.pack(side="top", pady=2)

        of2 = tk.Frame(options_frame, bg="red")
        tk.Label(of2, text="由 小白SmallWhite 整理", **style_subtitle).pack(anchor="w", padx=10)
        of2.pack(side="top", pady=2, fill="x")

        of3 = tk.Frame(options_frame, bg="red")
        tk.Label(of3, text="<subtitle>", **style_subtitle).pack(padx=10)
        of3.pack(side="top", pady=2, fill="x")
        options_frame.pack(side="top", pady=10)
    except Exception as e:
        print(f"Error in main_page: {e}")

if __name__ == "__main__":
    load_images_b64()
    DB_load()
    init_windows()
    main_page()
    if debug:
        debug_mode()
    UI.mainloop()
