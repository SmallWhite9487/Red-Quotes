import tkinter as tk
import os
import sqlite3
import random
import sys
from playsound import playsound
import pygame

def init_windows():
    try:
        global UI, debug
        debug = False
        pygame.mixer.init()
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

def images_b64():
    try:
        global images_b64
        images_b64 = ["iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuOBtp6qgAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAADHcBAOgDAAAMdwEA6AMAAFBhaW50Lk5FVCA1LjEuOAADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAACsv/ozX4hUUAAAAlVJREFUWEe1Vy1PxEAQ3WIwOPgBCEKCRBAU7nIGEhJIIASJB41Cg+M/oAgQDAqJB4lB8APAEAwJXHlvO+X25qbb7bW83Mv0Y2b33XRmu81y5/DrEEtin8XWgQI647Ib5Lewj+AaOCvXI+xWALkAUsBHYQcr7sf0E3YvgFQi8k1kxvIDJxfA9C6Jte5rEXug4ZcuoJyQ5PMNB+dkVgz96BMRkSYg/DcWWXgzoI6j6DDOEFsvoG5yY9CQgz6KMOIfF9Byck+dhTJOaqdaQBeTl9xQWSBZH7hnC6ibnOyBVqzFqiygoKdkQRxiAbwUG8MZWOdT4h08Kg7/wNgd50YFzIIpkxOpQku8iQ0xrwU0RVMRGttaAFOFtLgXfzYEz7fEarQVYRZNWIRhtceKM/SzyBXUiIu3IVc4PeikIhoLIK3llZxERIWAeBF+itVgLVi1QlTVxJxYhXZbslgBhiLZ3veg9rtu24YpmVgDD+Vc41VnYAasSnsMsUxUgaL3wwww+EJsU8QyUYVT9+N3zr5Cw5cFbeKOdoyx7ghJHxl/vAaYgTsQRZP33cAXUCqYAf3SsUAfrrpAIcBagiEku8J9Vi8LiR8cdWJ4v1ccpmK0CBl8UxyaKP9h+GabRpa+IJR9fg6m1BDHOcC8Ty4bCmBgm5dKU1DEXxfoyb+DrPwzpvyzDSensr7L3CrsupxPCsZyDD0Oj/kIfBueqPbQLxK2S/ghkkL67rrvkVbmhyuvkzyW61m+CCXHUILdiVf6AFpgptgp2EZ5XwtY27m8+oxan+djn+7O/QIF9aXJUoZccQAAAABJRU5ErkJggg==",
                        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuOBtp6qgAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAADHcBAOgDAAAMdwEA6AMAAFBhaW50Lk5FVCA1LjEuOAADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAACsv/ozX4hUUAAAAYxJREFUWEfdltFtAyEMhkkGyENm6AQdISt0okzSCSJ1kk7QKfIcidquoWBszhxIkfJJ9O4KZ//89t0lvBzxK8T4HSJfPgcUEO9PFvL6IrzBac0KETmhNqDxeFlDdZ8i4sDHLnTjG19IfiDIez8OJufTZv2RjyazyQlYl4FYpRN95SuSM5ULwOH0d6/pQDc5MJKcKF0AkgtqkK3kxKADiOZCE8CVPDFZhnBzNGEX0VDDfCgCaEeiXrRTbBr5f2RShOpAJaKwWRWHzDphYb3hMBm92eTYEKHdM9TFJZRMa9bCMQkm5NPM7iZcVY6pp2BEhCoKHsMlYHBZWxqcNF6VORg4t7sHJJRM6wkL7pWqBL3v+hZmOQxSo2YBtIMLH3fiFlGsySVoLGSL+GqIVF+L9ClGsgONeuxkbJZBR7Dh+NRFs8Ou+g1X3I1YxKmCuQOsgEXUTZiSP8ZsnIEEVMlR2Tkc6deK9Qn2grG0OLx7PKU/ue7FhGSoPEYcigE0c/Hz/9XogZ4ObUAcXuIkhF8Xi0mRBzMtqAAAAABJRU5ErkJggg==",
                        "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",
                    ]
    except Exception as e:
        print(f"Error loading images: {e}")

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.getcwd(), path)

def DB_load():
    try:
        global QUOTES
        conn = sqlite3.connect(resource_path(os.path.join("data", "quotes.db")))
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
    def DB_insert(lid, quote):
        try:
            conn = sqlite3.connect(resource_path(os.path.join("data", "quotes.db")))
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
    try:
        pass
    except Exception as e:
        print(f"Error in debug mode: {e}")

def main_page():
    def choose_subtitle():
        try:
            text = ["毛泽东思想","邓小平理论","“三个代表”","科学发展观","习近平新时代中国特色社会主义思想"]
            return f"{random.choice(text)}万岁！"
        except Exception as e:
            print(f"Error choosing subtitle: {e}")
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
            "font": ("", 11, "bold"),
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
        tk.Button(of1, text="<红色电台>", **style_common, command=Radio_page).pack(side="left", padx=10)
        of1.pack(side="top", pady=5)

        of2 = tk.Frame(options_frame, bg="red")
        tk.Label(of2, text="由 小白SmallWhite 整理", **style_subtitle).pack(anchor="w", padx=10)
        of2.pack(side="top", pady=2, fill="x")

        of3 = tk.Frame(options_frame, bg="red")
        tk.Label(of3, text=choose_subtitle(), **style_subtitle).pack(padx=10)
        of3.pack(side="bottom", pady=2, fill="x")
        options_frame.pack(side="top", pady=5)
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

def Radio_page():
    def play_current():
        if radio_index < 0 or radio_index >= len(radio_songs):
            radio_status_var.set("未选择歌曲")
            return
        pygame.mixer.music.stop()
        pygame.mixer.music.load(radio_songs[radio_index])
        pygame.mixer.music.play(-1 if radio_loop else 0)
        radio_status_var.set(f"正在播放: {os.path.splitext(os.path.basename(radio_songs[radio_index]))[0]}")
    def pause_play():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            radio_status_var.set("已暂停")
        else:
            pygame.mixer.music.unpause()
            radio_status_var.set("继续播放")
    def stop_play():
        pygame.mixer.music.stop()
        radio_status_var.set("已停止")
    def play_selected():
        if radio_index < 0 and radio_songs:
            set_index(0)
        play_current()
    def next_song():
        if not radio_songs:
            radio_status_var.set("未找到歌曲")
            return
        set_index((radio_index + 1) % len(radio_songs))
        play_current()
    def prev_song():
        if not radio_songs:
            radio_status_var.set("未找到歌曲")
            return
        set_index((radio_index - 1) % len(radio_songs)) 
        play_current()
    def random_song():
        if not radio_songs:
            radio_status_var.set("未找到歌曲")
            return
        set_index(random.randrange(len(radio_songs)))
        play_current()
    def toggle_loop():
        globals()["radio_loop"] = not radio_loop
        loop_text_var.set(f"循环: {'开' if radio_loop else '关'}")
        if radio_index >= 0:
            play_current()
    def set_index(i):
        if not radio_songs:
            radio_status_var.set("未找到歌曲")
            return
        if i < 0 or i >= len(radio_songs):
            return
        nonlocal song_list
        song_list.selection_clear(0, "end")
        song_list.selection_set(i)
        song_list.see(i)
        globals()["radio_index"] = i
    def on_select(event):
        sel = song_list.curselection()
        if sel:
            set_index(sel[0])
    def set_volume(v):
        try:
            v = max(0, min(100, int(v)))
            if radio_muted:
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(v / 100.0)
        except Exception as e:
            print(f"Error set_volume: {e}")
    def on_volume_change(_):
        try:
            val = volume_var.get()
            if val > 0:
                nonlocal prev_volume
                prev_volume = val
            set_volume(val)
        except Exception as e:
            print(f"Error on_volume_change: {e}")
    def toggle_mute():
        try:
            nonlocal radio_muted, prev_volume
            if radio_muted:
                radio_muted = False
                mute_text_var.set("静音: 关")
                set_volume(prev_volume)
            else:
                radio_muted = True
                mute_text_var.set("静音: 开")
                set_volume(0)
        except Exception as e:
            print(f"Error toggle_mute: {e}")
    global radio_songs, radio_index, radio_loop, loop_text_var, radio_status_var
    set_screen(720,360)
    clear_screen()
    style_title = {"bg": "red","fg": "gold","font": ("", 28, "bold")}
    style_subtitle = {"bg": "red","fg": "gold","font": ("", 12, "bold")}
    style_button = {"bg": "gold","font": ("", 14, "bold"),"width": 9,"height": 2}

    radio_index = -1
    radio_loop = False
    loop_text_var = tk.StringVar()
    radio_status_var = tk.StringVar()
    loop_text_var.set("循环: 关")
    radio_status_var.set("未选择歌曲")
    mute_text_var = tk.StringVar()
    volume_var = tk.IntVar()
    mute_text_var.set("静音: 关")
    volume_var.set(40)
    radio_muted = False
    prev_volume = 40

    set_volume(prev_volume)
    songs_dir = resource_path(os.path.join("data", "songs"))
    radio_songs = []
    if os.path.isdir(songs_dir):
        for name in os.listdir(songs_dir):
            if name.lower().endswith(".ogg"):
                full_path = os.path.join(songs_dir, name)
                radio_songs.append(full_path)
    radio_songs.sort()

    tk.Label(UI, text="=红色电台=", **style_title).pack(pady=10)
    main_frame = tk.Frame(UI, bg="red")

    controls_frame = tk.Frame(main_frame, bg="red")
    tk.Label(controls_frame, textvariable=radio_status_var, **style_subtitle).grid(row=0, column=0, columnspan=4, sticky="w", pady=5)
    tk.Button(controls_frame, text="播放", **style_button, command=play_selected).grid(row=1, column=0, padx=3, pady=3)
    tk.Button(controls_frame, text="暂停/继续", **style_button, command=pause_play).grid(row=1, column=1, padx=3, pady=3)
    tk.Button(controls_frame, text="停止", **style_button, command=stop_play).grid(row=1, column=2, padx=3, pady=3)
    tk.Button(controls_frame, text="上一首", **style_button, command=prev_song).grid(row=2, column=0, padx=3, pady=3)
    tk.Button(controls_frame, text="随机", **style_button, command=random_song).grid(row=2, column=1, padx=3, pady=3)
    tk.Button(controls_frame, text="下一首", **style_button, command=next_song).grid(row=2, column=2, padx=3, pady=3)
    tk.Button(controls_frame, text="返回首页", **style_button, command=main_page).grid(row=3, column=0, padx=3, pady=6)
    tk.Button(controls_frame, textvariable=loop_text_var, **style_button, command=toggle_loop).grid(row=3, column=2, padx=3, pady=3)
    controls_frame.pack(side="left", padx=10, pady=5)

    list_frame = tk.Frame(main_frame, bg="red")
    song_list = tk.Listbox(list_frame, width=30, font=("", 12), bg="gold")
    scroll = tk.Scrollbar(list_frame, orient="vertical", command=song_list.yview)
    song_list.configure(yscrollcommand=scroll.set)
    for path in radio_songs:
        song_list.insert("end", os.path.splitext(os.path.basename(path))[0])
    song_list.grid(row=0, column=0, sticky="nsew")
    scroll.grid(row=0, column=1, sticky="ns")
    song_list.bind("<<ListboxSelect>>", on_select)
    list_frame.pack(side="right", padx=10, pady=5, fill="y")

    volume_frame = tk.Frame(list_frame, bg="red")
    tk.Label(volume_frame, text="音量", **style_subtitle).grid(row=4, column=0, sticky="e", padx=3, pady=3)
    tk.Scale(volume_frame, variable=volume_var, from_=0, to=100, orient="horizontal", length=120, command=on_volume_change).grid(row=4, column=1, columnspan=2, padx=3, pady=3)
    tk.Button(volume_frame, textvariable=mute_text_var, **style_button, command=toggle_mute).grid(row=4, column=3, padx=3, pady=3)
    volume_frame.grid(row=1, column=0, columnspan=2, pady=10)

    main_frame.pack(fill="both", expand=True, padx=10)

if __name__ == "__main__":
    images_b64()
    DB_load()
    init_windows()
    main_page()
    if debug:
        debug_mode()
    UI.mainloop()
