import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from exercises import get_random_exercises, get_random_message
from notifications import play_notification_sound, show_break_popup
from storage import save_data
from timer import WorkBreakTimer


class AppUI:
    def __init__(self, root: tk.Tk, app_data: dict):
        self.root = root
        self.data = app_data
        self.root.title("یار ارگونومی")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        self.timer = WorkBreakTimer(
            work_minutes=int(self.data["work_minutes"]),
            break_minutes=int(self.data["break_minutes"]),
            on_tick=self._on_tick,
            on_phase_end=self._on_phase_end,
        )

        self.mode_label = ttk.Label(root, text="حالت فعلی: کار", font=("Segoe UI", 10, "bold"))
        self.mode_label.pack(pady=(18, 8))

        self.countdown_label = ttk.Label(root, text="60:00", font=("Segoe UI", 26, "bold"))
        self.countdown_label.pack()

        self.message_label = ttk.Label(root, text="برای شروع دکمه شروع را بزنید.", wraplength=380, justify="center")
        self.message_label.pack(pady=10)

        actions = ttk.Frame(root)
        actions.pack(pady=10)

        ttk.Button(actions, text="شروع", command=self.start_timer).grid(row=0, column=0, padx=5)
        ttk.Button(actions, text="توقف", command=self.stop_timer).grid(row=0, column=1, padx=5)
        ttk.Button(actions, text="ریست", command=self.reset_timer).grid(row=0, column=2, padx=5)
        ttk.Button(actions, text="تنظیمات", command=self.open_settings).grid(row=0, column=3, padx=5)

        self._on_tick("work", int(self.data["work_minutes"]) * 60)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _format_time(self, seconds: int) -> str:
        minutes, sec = divmod(max(0, seconds), 60)
        return f"{minutes:02d}:{sec:02d}"

    def _safe_ui(self, func, *args):
        self.root.after(0, lambda: func(*args))

    def _on_tick(self, mode: str, remaining: int) -> None:
        self._safe_ui(self._apply_tick, mode, remaining)

    def _apply_tick(self, mode: str, remaining: int) -> None:
        mode_text = "کار" if mode == "work" else "استراحت"
        self.mode_label.configure(text=f"حالت فعلی: {mode_text}")
        self.countdown_label.configure(text=self._format_time(remaining))

    def _on_phase_end(self, mode: str) -> None:
        self._safe_ui(self._handle_phase_end, mode)

    def _handle_phase_end(self, mode: str) -> None:
        if mode == "work":
            play_notification_sound()
            message = get_random_message()
            exercises = get_random_exercises(2)
            self.message_label.configure(text=message)
            show_break_popup(
                root=self.root,
                message=message,
                exercises=exercises,
                on_skip_break=self._skip_break,
                on_start_break=self._start_break,
            )
        else:
            self.data["completed_breaks"] = int(self.data.get("completed_breaks", 0)) + 1
            save_data(self.data)
            self.message_label.configure(text="استراحت تمام شد، آماده یک دور کار مفید!")

    def _skip_break(self) -> None:
        print("[LOG] Break skipped by user")
        self.timer.skip_break()

    def _start_break(self) -> None:
        print("[LOG] Break started by user")

    def start_timer(self) -> None:
        print("[LOG] Start button pressed")
        self.timer.start()

    def stop_timer(self) -> None:
        self.timer.stop()

    def reset_timer(self) -> None:
        self.timer.reset()
        self.message_label.configure(text="تایمر به حالت اولیه برگشت.")

    def open_settings(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("تنظیمات")
        win.geometry("320x220")
        win.resizable(False, False)
        win.transient(self.root)

        ttk.Label(win, text="زمان کار (دقیقه):").pack(anchor="e", padx=16, pady=(12, 4))
        work_var = tk.StringVar(value=str(self.data["work_minutes"]))
        ttk.Entry(win, textvariable=work_var).pack(fill="x", padx=16)

        ttk.Label(win, text="زمان استراحت (دقیقه):").pack(anchor="e", padx=16, pady=(10, 4))
        break_var = tk.StringVar(value=str(self.data["break_minutes"]))
        ttk.Entry(win, textvariable=break_var).pack(fill="x", padx=16)

        autostart_var = tk.BooleanVar(value=bool(self.data.get("autostart_enabled", False)))
        ttk.Checkbutton(win, text="اجرای خودکار با ویندوز", variable=autostart_var).pack(anchor="e", padx=16, pady=(10, 4))

        def save_settings() -> None:
            try:
                work_minutes = max(1, int(work_var.get()))
                break_minutes = max(1, int(break_var.get()))
            except ValueError:
                messagebox.showerror("خطا", "فقط عدد صحیح وارد کنید.")
                return

            self.data["work_minutes"] = work_minutes
            self.data["break_minutes"] = break_minutes
            self.data["autostart_enabled"] = autostart_var.get()
            self.timer.update_durations(work_minutes, break_minutes)
            self._set_autostart(autostart_var.get())
            save_data(self.data)
            win.destroy()

        ttk.Button(win, text="ذخیره", command=save_settings).pack(pady=14)

    def _startup_file_path(self) -> str:
        startup_dir = os.path.join(
            os.getenv("APPDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup",
        )
        return os.path.join(startup_dir, "ErgoHealthReminder.cmd")

    def _set_autostart(self, enabled: bool) -> None:
        path = self._startup_file_path()
        if not path:
            return

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if enabled:
            launcher_target = sys.executable if getattr(sys, "frozen", False) else os.path.abspath("main.py")
            if getattr(sys, "frozen", False):
                command = f'"{launcher_target}"\n'
            else:
                command = f'"{sys.executable}" "{launcher_target}"\n'
            with open(path, "w", encoding="utf-8") as file:
                file.write("@echo off\n")
                file.write(command)
            print("[LOG] Autostart enabled")
        else:
            if os.path.exists(path):
                os.remove(path)
            print("[LOG] Autostart disabled")

    def on_close(self) -> None:
        self.timer.stop()
        save_data(self.data)
        self.root.destroy()
