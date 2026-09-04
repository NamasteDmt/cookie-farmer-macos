import tkinter as tk
from tkinter import ttk, scrolledtext
from loguru import logger
import asyncio, threading, sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.env_check import check_environment
from core.dolphin_client import DolphinClient
from utils.logger import setup_logger

class CookieFarmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cookie Farmer (macOS)")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.logger = setup_logger()
        self.dolphin = DolphinClient()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.create_widgets()
        self.refresh_environment()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_async(self, coro, callback=None):
        async def wrapper():
            try:
                result = await coro
                if callback:
                    self.root.after(0, callback, result)
            except Exception as e:
                logger.error(f"Async error: {e}")
                self.root.after(0, self.log, f"Ошибка: {e}", "ERROR")
        asyncio.run_coroutine_threadsafe(wrapper(), self.loop)

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)
        self.btn_refresh = ttk.Button(top_frame, text="Проверить окружение", command=self.refresh_environment)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        self.btn_dolphin = ttk.Button(top_frame, text="Загрузить профили", command=self.load_profiles)
        self.btn_dolphin.pack(side=tk.LEFT, padx=5)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Monaco", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.profiles_list = tk.Listbox(self.root, selectmode=tk.MULTIPLE, font=("Monaco", 10))
        self.profiles_list.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10))

    def log(self, message, level="INFO"):
        self.logger.log(level, message)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def refresh_environment(self):
        self.text_area.delete(1.0, tk.END)
        self.log("Проверка окружения...")
        results = check_environment()
        for mod, status in results.items():
            if status == "OK":
                self.log(f"{mod}: OK", "SUCCESS")
            else:
                self.log(f"{mod}: {status}", "ERROR")

    def load_profiles(self):
        self.log("Загрузка профилей из Dolphin Anty...")
        self.run_async(self.dolphin.get_profiles(), self.display_profiles)

    def display_profiles(self, profiles):
        self.profiles_list.delete(0, tk.END)
        for p in profiles:
            self.profiles_list.insert(tk.END, f"[{p['id']}] {p['name']} (статус: {p['status']})")
        self.log(f"Загружено профилей: {len(profiles)}")

def main():
    root = tk.Tk()
    app = CookieFarmerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
