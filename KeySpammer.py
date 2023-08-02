import tkinter as tk
import pyautogui
import threading
import keyboard

class KeySpammerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Spammer")
        self.root.geometry("250x200")
        self.root.resizable(False, False)

        self.key_to_detect = tk.StringVar()
        self.key_to_detect.set("z")

        self.key_to_spam = tk.StringVar()
        self.key_to_spam.set("a")

        self.interval_seconds = tk.StringVar()
        self.interval_seconds.set("0.1")

        self.is_spamming = False
        self.toggle_button = None

        self.create_widgets()

    def create_widgets(self):
        key_label = tk.Label(self.root, text="検出するキー (一文字のみ)")
        key_label.pack()
        vcmd_key = (root.register(self.validate_key), '%P')
        key_entry = tk.Entry(self.root, textvariable=self.key_to_detect, validate='key', validatecommand=vcmd_key)
        key_entry.pack()

        spam_key_label = tk.Label(self.root, text="連打するキー (一文字のみ)")
        spam_key_label.pack()
        vcmd_spam = (root.register(self.validate_key), '%P')
        spam_key_entry = tk.Entry(self.root, textvariable=self.key_to_spam, validate='key', validatecommand=vcmd_spam)
        spam_key_entry.pack()

        interval_label = tk.Label(self.root, text="連打の間隔 (秒)")
        interval_label.pack()
        vcmd_interval = (root.register(self.validate_interval), '%P')
        interval_entry = tk.Entry(self.root, textvariable=self.interval_seconds, validate='key', validatecommand=vcmd_interval)
        interval_entry.pack()

        self.toggle_button = tk.Button(self.root, text="機能開始", command=self.toggle_spamming)
        self.toggle_button.pack()

    def spam_key(self):
        key_to_detect = self.key_to_detect.get()
        key_to_spam = self.key_to_spam.get()
        interval = float(self.interval_seconds.get())

        print(f"{key_to_detect}キーが押されている間、{key_to_spam}キーを{interval}秒ごとに連打します。")
        while self.is_spamming:
            if keyboard.is_pressed(key_to_detect):
                pyautogui.press(key_to_spam)
                pyautogui.keyUp(key_to_spam)
                pyautogui.PAUSE = interval

        print("連打が終了しました。")

    def toggle_spamming(self):
        if not self.is_spamming:
            try:
                interval = float(self.interval_seconds.get())
                self.is_spamming = True
                self.spam_thread = threading.Thread(target=self.spam_key)
                self.spam_thread.start()
                self.toggle_button.config(text="機能停止")
            except ValueError:
                print("連打の間隔は数字のみを入力してください。")
        else:
            self.is_spamming = False
            self.toggle_button.config(text="機能開始")

    def validate_key(self, value):
        return len(value) <= 1

    def validate_interval(self, value):
        return value == "" or value.replace(".", "").isdigit()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeySpammerApp(root)
    root.mainloop()
