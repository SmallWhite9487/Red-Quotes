import tkinter as tk
import os
import sqlite3
import random

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

def clear_screen():
    try:
        for widget in UI.winfo_children():
            widget.destroy()
    except Exception as e:
        print(f"Error clearing screen: {e}")

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
        clear_screen()
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
        tk.Button(of1, text="<每日一语>", **style_common, command=DQ_page).pack(side="left", padx=10)
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

def DQ_page():
    def show_quote(key=None):
        try:
            if key is None:
                available_keys = []
                for leader_key, quotes in QUOTES.items():
                    if quotes:
                        available_keys.append(leader_key)
                if not available_keys:
                    raise Exception("No available quotes.")
                key = random.choice(available_keys)

            quotes = QUOTES.get(key)
            if not quotes:
                raise Exception(f"Quotes of {leaders.get(key, '')} is empty.")

            dq_leader_var.set(f"伟大领袖 {leaders.get(key, '')} 曾经说过：")
            dq_quote_var.set(random.choice(quotes))
        except Exception as e:
            if key is None:
                print(f"Error showing random quote: {e}")
            else:
                print(f"Error showing quote: {e}")
    try:
        global dq_quote_var, dq_leader_var
        set_screen(720,360)
        clear_screen()
        style_title = {
            "bg": "red",
            "fg": "gold",
            "font": ("", 28, "bold"),
        }
        style_subtitle = {
            "bg": "red",
            "fg": "gold",
            "font": ("", 12, "bold"),
        }
        style_button = {
            "bg": "gold",
            "font": ("", 14, "bold"),
            "width": 10,
            "height": 2,
        }
        dq_quote_var = tk.StringVar()
        dq_leader_var = tk.StringVar()
        dq_quote_var.set("请选择一位领导或点击随机抽取每日一语。")
        dq_leader_var.set("未选择领导")

        leaders = {"M": "毛主席",
                    "L": "刘主席",
                    "D": "邓公",
                    "J": "江主席",
                    "H": "胡主席",
                    "X": "习主席",}
        tk.Label(UI, text="=每日一语=", **style_title).pack(pady=10)

        top_frame = tk.Frame(UI, bg="red")
        buttons_frame = tk.Frame(top_frame, bg="red")
        tk.Button(buttons_frame, text="毛主席", **style_button, command=lambda: show_quote("M")).grid(row=0, column=0, padx=3, pady=3)
        tk.Button(buttons_frame, text="刘主席", **style_button, command=lambda: show_quote("L")).grid(row=0, column=1, padx=3, pady=3)
        tk.Button(buttons_frame, text="邓  公", **style_button, command=lambda: show_quote("D")).grid(row=0, column=2, padx=3, pady=3)
        tk.Button(buttons_frame, text="江主席", **style_button, command=lambda: show_quote("J")).grid(row=1, column=0, padx=3, pady=3)
        tk.Button(buttons_frame, text="胡主席", **style_button, command=lambda: show_quote("H")).grid(row=1, column=1, padx=3, pady=3)
        tk.Button(buttons_frame, text="习主席", **style_button, command=lambda: show_quote("X")).grid(row=1, column=2, padx=3, pady=3)
        tk.Button(buttons_frame, text="<随机>", **style_button, command=show_quote).grid(row=2, column=0, columnspan=3, pady=10, sticky="we")
        buttons_frame.pack(side="left", padx=10)

        quote_frame = tk.Frame(top_frame, bg="red")
        tk.Label(quote_frame, textvariable=dq_leader_var, **style_subtitle).pack(anchor="w", pady=5)
        tk.Label(quote_frame, textvariable=dq_quote_var, bg="gold", font=("", 14, "bold"), wraplengt=200).pack(fill="both", expand=True, padx=5, pady=5)
        quote_frame.pack(side="left", fill="both", expand=True)
        top_frame.pack(fill="both", expand=True, padx=10)

        tk.Button(UI, text="<返回>", **style_button, command=main_page).pack(side="bottom",pady=10,padx=10)
    except Exception as e:
        print(f"Error in DQ_page: {e}")

if __name__ == "__main__":
    load_images_b64()
    DB_load()
    init_windows()
    main_page()
    if debug:
        debug_mode()
    UI.mainloop()
