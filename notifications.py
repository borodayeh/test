import tkinter as tk
from tkinter import ttk
import winsound


BREAK_TEXT = "زمان بلند شدن و استراحت رسیده. بدنت منتظر است."


def play_notification_sound() -> None:
    """Play a gentle notification beep on Windows."""
    try:
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except RuntimeError:
        pass


def show_break_popup(
    root: tk.Tk,
    message: str,
    exercises: list[str],
    on_skip_break,
    on_start_break,
) -> None:
    """Show the break reminder popup with exercises and controls."""
    popup = tk.Toplevel(root)
    popup.title("یادآوری استراحت")
    popup.geometry("420x300")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    container = ttk.Frame(popup, padding=14)
    container.pack(fill="both", expand=True)

    ttk.Label(container, text=BREAK_TEXT, wraplength=380, justify="right").pack(anchor="e", pady=(0, 8))
    ttk.Label(container, text=f"پیام انگیزشی: {message}", wraplength=380, justify="right").pack(anchor="e", pady=(0, 8))

    ttk.Label(container, text="تمرین‌های پیشنهادی:").pack(anchor="e")
    for item in exercises:
        ttk.Label(container, text=f"• {item}", wraplength=380, justify="right").pack(anchor="e", pady=2)

    buttons = ttk.Frame(container)
    buttons.pack(fill="x", pady=(14, 0))

    def start_break() -> None:
        on_start_break()
        popup.destroy()

    def skip_break() -> None:
        on_skip_break()
        popup.destroy()

    ttk.Button(buttons, text="شروع استراحت", command=start_break).pack(side="right", padx=4)
    ttk.Button(buttons, text="رد استراحت", command=skip_break).pack(side="right", padx=4)

    popup.protocol("WM_DELETE_WINDOW", start_break)
