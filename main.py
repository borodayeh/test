import tkinter as tk

from storage import load_data
from ui import AppUI


def main() -> None:
    data = load_data()
    root = tk.Tk()
    AppUI(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()
